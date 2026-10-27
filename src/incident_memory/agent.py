from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timedelta, timezone

import cv2
import numpy as np

from .memory import FrameRecord, IncidentMemory
from .vision import ImageQuality, VisionComparison, assess_quality, align_and_compare


class InvestigationLimitError(RuntimeError):
    pass


class InvestigationAgent:
    """Bounded, deterministic perception-decision-action controller."""

    def __init__(self, fixture: dict, *, max_iterations: int = 10, omit_baseline: bool = False) -> None:
        self.fixture = fixture
        self.max_iterations = max_iterations
        self.omit_baseline = omit_baseline
        self.trace: list[dict] = []
        self.memory = IncidentMemory()
        self.iteration = 0
        self.run_id = fixture.get("event_id", "event")
        self.current_quality: ImageQuality | None = None
        self.comparison: VisionComparison | None = None
        self.selected_baseline: FrameRecord | None = None
        self.finding = "unverified"
        self.outcome = "incomplete"
        self.review_request: dict | None = None
        self.sensor_result: dict | None = None

    def _record(self, action: str, observation: dict, result: dict, *, error: str | None = None,
                stopping: str | None = None, thresholds: dict | None = None) -> None:
        if self.iteration >= self.max_iterations:
            raise InvestigationLimitError("maximum investigation tool-call budget reached")
        self.iteration += 1
        self.trace.append({
            "iteration": self.iteration,
            "observation_inputs": observation,
            "thresholds": thresholds or {},
            "selected_action": action,
            "evidence_references": result.get("evidence_references", []),
            "result": result,
            "error": error,
            "stopping_condition": stopping,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def retrieve_event_frames(self) -> dict:
        data = self.fixture
        frame_id = f"{self.run_id}-baseline"
        if not self.omit_baseline:
            base_quality = assess_quality(data["baseline"])
            self.memory.add_frame(FrameRecord(frame_id, data["camera_id"], data["baseline_time"], data["baseline"],
                                              quality_score=base_quality.quality_score))
        if data.get("older") is not None:
            older_quality = assess_quality(data["older"])
            self.memory.add_frame(FrameRecord(f"{self.run_id}-older", data["camera_id"], data["older_time"],
                                              data["older"], quality_score=older_quality.quality_score))
        result = {"camera_id": data["camera_id"], "event_id": self.run_id,
                  "available_historical_frames": int(not self.omit_baseline) + int(data.get("older") is not None),
                  "event_frame_ref": f"{self.run_id}-event"}
        self._record("retrieve_event_frames", {"event_id": self.run_id, "camera_id": data["camera_id"]}, result,
                     thresholds={"history_context": "mechanical_room"})
        return result

    def evaluate_image_quality(self) -> ImageQuality:
        self.current_quality = assess_quality(self.fixture["current"])
        result = {**self.current_quality.__dict__, "evidence_references": [f"{self.run_id}-event"]}
        self._record("evaluate_image_quality", {"frame": f"{self.run_id}-event"}, result,
                     thresholds={"minimum_blur_variance": 24, "minimum_resolution_px": 96})
        return self.current_quality

    def select_historical_baseline(self) -> FrameRecord | None:
        self.selected_baseline = self.memory.select_historical_baseline(
            self.fixture["camera_id"], self.fixture["event_time"])
        result = {"selected_frame_id": self.selected_baseline.frame_id if self.selected_baseline else None,
                  "selected_timestamp": self.selected_baseline.timestamp.isoformat() if self.selected_baseline else None,
                  "reason": "nearest usable pre-event frame for the same camera and context",
                  "evidence_references": [self.selected_baseline.frame_id] if self.selected_baseline else []}
        self._record("select_historical_baseline", {"camera_id": self.fixture["camera_id"],
                     "event_time": self.fixture["event_time"].isoformat()}, result,
                     thresholds={"exclude_incident_frames": True, "minimum_quality_score": 0.4})
        return self.selected_baseline

    def align_and_compare(self, reference: np.ndarray | None = None, current: np.ndarray | None = None,
                          *, reference_id: str | None = None, current_id: str | None = None) -> VisionComparison:
        reference = reference if reference is not None else self.selected_baseline.image
        current = current if current is not None else self.fixture["current"]
        self.comparison = align_and_compare(reference, current)
        result = self.comparison.public()
        result["evidence_references"] = [reference_id or self.selected_baseline.frame_id,
                                         current_id or f"{self.run_id}-event"]
        self._record("align_and_compare", {"reference": result["evidence_references"][0],
                     "current": result["evidence_references"][1]}, result,
                     thresholds={"mask_delta_saturation": 42, "minimum_region_area_fraction": 0.0025,
                                 "minimum_registration_reliability": 0.45})
        return self.comparison

    def inspect_region(self, region: dict) -> dict:
        x, y, w, h = region["bbox"]
        patch = self.fixture["current"][y:y + h, x:x + w]
        hsv = cv2.cvtColor(patch, cv2.COLOR_BGR2HSV)
        sat = hsv[:, :, 1]
        value = hsv[:, :, 2]
        result = {"region_id": region["region_id"], "visual_cue": region["visual_cue"],
                  "cool_tone_fraction": region["cool_tone_fraction"],
                  "median_saturation": round(float(np.median(sat)), 2),
                  "median_luminance": round(float(np.median(value)), 2),
                  "interpretation": "visible color/texture change only; material and cause are unverified",
                  "evidence_references": [f"{self.run_id}-event:{region['region_id']}"]}
        self._record("inspect_region", {"region_id": region["region_id"], "bbox": region["bbox"]}, result,
                     thresholds={"cool_tone_descriptor_only": True})
        return result

    def retrieve_additional_frame(self, *, reason: str) -> FrameRecord | None:
        frames = self.memory.older_frames(self.fixture["camera_id"], self.fixture["baseline_time"])
        frame = frames[0] if frames else None
        result = {"reason": reason, "frame_id": frame.frame_id if frame else None,
                  "available": frame is not None,
                  "evidence_references": [frame.frame_id] if frame else []}
        self._record("retrieve_additional_frame", {"reason": reason, "camera_id": self.fixture["camera_id"]}, result,
                     error=None if frame else "no additional usable historical frame was available")
        return frame

    def correlate_sensor_event(self) -> dict:
        sensor = self.fixture.get("sensor") or {}
        try:
            sensor_time = datetime.fromisoformat(sensor.get("timestamp", "").replace("Z", "+00:00"))
            delta = abs((sensor_time - self.fixture["event_time"]).total_seconds())
            valid_time = sensor_time.tzinfo is not None and delta <= 300
        except (ValueError, TypeError):
            delta, valid_time = None, False
        active = bool(sensor.get("active")) and valid_time
        self.sensor_result = {"sensor_type": sensor.get("type", "unknown"), "active": bool(sensor.get("active")),
                              "time_aligned": valid_time, "offset_seconds": delta,
                              "classification": "SENSOR_CORRELATED" if active else "UNVERIFIED",
                              "evidence_references": [sensor.get("source", "sensor-event")]}
        self._record("correlate_sensor_event", {"sensor_type": sensor.get("type", "unknown"),
                     "timestamp": sensor.get("timestamp")}, self.sensor_result,
                     thresholds={"maximum_time_offset_seconds": 300})
        return self.sensor_result

    def generate_review_request(self, request_type: str, reason: str) -> dict:
        self.review_request = {"type": request_type, "mandatory": request_type == "operator_review",
                               "reason": reason, "available_actions": ["approve", "reject", "request_more_evidence"]}
        self._record("generate_review_request", {"finding": self.finding}, self.review_request,
                     stopping="waiting_for_human_review" if self.review_request["mandatory"] else "retake_requested")
        return self.review_request

    def create_evidence_report(self) -> dict:
        hashes = {}
        for name in ("baseline", "current"):
            ok, encoded = cv2.imencode(".png", self.fixture[name])
            if ok:
                hashes[name] = hashlib.sha256(encoded.tobytes()).hexdigest()
        if self.comparison is not None:
            for name, image in (("change_mask", self.comparison.mask), ("overlay", self.comparison.overlay)):
                ok, encoded = cv2.imencode(".png", image)
                if ok:
                    hashes[name] = hashlib.sha256(encoded.tobytes()).hexdigest()
        report = {
            "schema_version": "1.0", "run_id": self.run_id, "event_id": self.run_id,
            "camera_id": self.fixture["camera_id"], "scenario": self.fixture["scenario"],
            "synthetic_demo": bool(self.fixture.get("synthetic", False)),
            "created_at": datetime.now(timezone.utc).isoformat(), "outcome": self.outcome,
            "finding": self.finding, "evidence_classes": self._evidence_classes(),
            "sensor_correlation": self.sensor_result, "quality": self.current_quality.__dict__ if self.current_quality else None,
            "comparison": self.comparison.public() if self.comparison else None,
            "regions": self.comparison.candidate_regions if self.comparison else [],
            "review_request": self.review_request,
            "privacy_redaction": self.fixture.get("privacy_redaction"),
            "limitations": ["RGB appearance does not prove water or root cause", "human review is required for safety or maintenance action"],
            "sha256": hashes, "trace": self.trace,
        }
        self._record("create_evidence_report", {"finding": self.finding, "outcome": self.outcome},
                     {"report_schema": "1.0", "sha256_count": len(hashes), "evidence_references": list(hashes)},
                     stopping="bounded investigation complete")
        report["trace"] = self.trace
        return report

    def _evidence_classes(self) -> list[str]:
        classes = ["OBSERVED"] if self.comparison and self.comparison.candidate_regions else []
        if self.sensor_result and self.sensor_result.get("classification") == "SENSOR_CORRELATED":
            classes.append("SENSOR_CORRELATED")
        if self.finding in {"possible_visible_water_change", "possible_water_presence"}:
            classes.append("HYPOTHESIS")
        if self.finding in {"unverified", "insufficient_evidence"}:
            classes.append("UNVERIFIED")
        return classes or ["UNVERIFIED"]

    def run(self) -> dict:
        started = time.perf_counter()
        try:
            if self.fixture.get("privacy_redaction"):
                self._record("redact_detected_faces", {"input_frames": [f"{self.run_id}-baseline", f"{self.run_id}-event"]},
                             {**self.fixture["privacy_redaction"], "evidence_references": []})
            self.retrieve_event_frames()
            quality = self.evaluate_image_quality()
            if not quality.usable:
                extra = self.retrieve_additional_frame(reason="alarm frame quality is below comparison threshold; seek corroborating view")
                self.finding, self.outcome = "insufficient_evidence", "retake_requested"
                self.generate_review_request("retake", "Alarm frame quality is inadequate; no incident claim is made.")
                report = self.create_evidence_report()
                report["retake_frame_available"] = extra is not None
                report["elapsed_ms"] = round((time.perf_counter() - started) * 1000, 3)
                return report

            baseline = self.select_historical_baseline()
            if baseline is None:
                self.finding, self.outcome = "insufficient_evidence", "baseline_missing"
                self.generate_review_request("retake", "No quality-screened pre-event baseline is available.")
                return self.create_evidence_report()

            comparison = self.align_and_compare()
            if not comparison.comparable:
                self.finding, self.outcome = "insufficient_evidence", "comparison_rejected"
                self.generate_review_request("retake", "Frame alignment or comparability is insufficient.")
                return self.create_evidence_report()

            if comparison.candidate_regions:
                region = comparison.candidate_regions[0]
                self.inspect_region(region)
                older = self.retrieve_additional_frame(reason="check whether candidate region was present before the nearest baseline")
                if older is not None:
                    primary_comparison = comparison
                    historical = self.align_and_compare(older.image, self.fixture["current"],
                                                        reference_id=older.frame_id, current_id=f"{self.run_id}-event")
                    # Similarity is computed only inside the candidate crop; it is evidence of prior appearance,
                    # not evidence of material identity or physical cause.
                    x, y, w, h = region["bbox"]
                    old_patch = older.image[y:y + h, x:x + w]
                    now_patch = self.fixture["current"][y:y + h, x:x + w]
                    if old_patch.shape == now_patch.shape:
                        visual_similarity = 1.0 - float(np.mean(cv2.absdiff(old_patch, now_patch))) / 255.0
                    else:
                        visual_similarity = 0.0
                    history_result = {"region_id": region["region_id"], "similarity": round(visual_similarity, 4),
                                      "prior_candidate_regions": len(historical.candidate_regions),
                                      "interpretation": "similar appearance exists in an older pre-event image" if visual_similarity >= 0.92 else "older image does not closely match this region",
                                      "evidence_references": [older.frame_id, f"{self.run_id}-event:{region['region_id']}"]}
                    self._record("compare_historical_region", {"older_frame": older.frame_id,
                                 "event_frame": f"{self.run_id}-event", "region_id": region["region_id"]},
                                 history_result, thresholds={"preexisting_similarity": 0.92})
                    self.comparison = primary_comparison
                    if visual_similarity >= 0.92:
                        self.finding, self.outcome = "visually_similar_change_previously_observed", "no_new_change_supported"
                        self.correlate_sensor_event()
                        return self.create_evidence_report()

                sensor = self.correlate_sensor_event()
                if sensor["classification"] == "SENSOR_CORRELATED" and region["cool_tone_fraction"] >= 0.25:
                    self.finding, self.outcome = "possible_visible_water_change", "human_review_required"
                    self.generate_review_request("operator_review", "New localized cool-toned change and a time-aligned water sensor warrant operator review; cause remains unverified.")
                else:
                    self.finding, self.outcome = "observed_change_cause_unverified", "additional_evidence_recommended"
                    self.generate_review_request("retake", "A localized visual change lacks sufficient independent evidence for a leak hypothesis.")
            else:
                sensor = self.correlate_sensor_event()
                if sensor["classification"] == "SENSOR_CORRELATED":
                    self.finding, self.outcome = "sensor_alert_without_credible_visual_change", "additional_evidence_recommended"
                    self.generate_review_request("retake", "Sensor alert has no credible localized visual support; obtain another view or follow site procedure.")
                else:
                    self.finding, self.outcome = "no_credible_visual_water_evidence", "no_visual_change_supported"
            return self.create_evidence_report()
        except Exception as exc:
            self.finding, self.outcome = "insufficient_evidence", "safe_stop_error"
            self._record("safe_stop", {"error_type": type(exc).__name__}, {"message": "investigation stopped without an incident conclusion"},
                         error=str(exc), stopping="fail_closed")
            return self.create_evidence_report()

