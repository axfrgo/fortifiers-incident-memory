from __future__ import annotations

from datetime import datetime, timedelta, timezone

import numpy as np
import pytest

from incident_memory.agent import InvestigationAgent
from incident_memory.memory import FrameRecord, IncidentMemory, TimestampValidationError
from incident_memory.scenarios import fixture


def run(scenario):
    return InvestigationAgent(fixture(scenario)).run()


def actions(result):
    return [step["selected_action"] for step in result["trace"]]


def test_sensor_correlated_new_visual_change_requests_operator_review():
    result = run("clear_change")
    assert result["outcome"] == "human_review_required"
    assert "OBSERVED" in result["evidence_classes"]
    assert "SENSOR_CORRELATED" in result["evidence_classes"]
    assert "HYPOTHESIS" in result["evidence_classes"]
    assert "inspect_region" in actions(result)
    assert "correlate_sensor_event" in actions(result)
    assert result["review_request"]["mandatory"] is True


def test_low_quality_frame_requests_retake_and_never_claims_detection():
    result = run("poor_image")
    assert result["outcome"] == "retake_requested"
    assert result["finding"] == "insufficient_evidence"
    assert "align_and_compare" not in actions(result)
    assert "retrieve_additional_frame" in actions(result)


def test_lighting_only_change_is_downgraded_without_water_claim():
    result = run("lighting_shift")
    assert result["outcome"] == "no_visual_change_supported"
    assert result["finding"] == "no_credible_visual_water_evidence"
    assert result["evidence_classes"] == ["UNVERIFIED"]


def test_older_history_changes_next_action_and_outcome():
    result = run("historical_match")
    names = actions(result)
    assert "retrieve_additional_frame" in names
    assert "compare_historical_region" in names
    assert result["outcome"] == "no_new_change_supported"
    assert result["finding"] == "visually_similar_change_previously_observed"


def test_demo_outcomes_produce_distinct_agent_paths():
    traces = {name: tuple(actions(run(name))) for name in ("clear_change", "poor_image", "lighting_shift", "historical_match")}
    assert len(set(traces.values())) == 4


def test_baseline_retrieval_filters_camera_time_and_incident_frames():
    mem = IncidentMemory()
    now = datetime.now(timezone.utc)
    image = np.zeros((10, 10, 3), dtype=np.uint8)
    mem.add_frame(FrameRecord("old", "cam-a", now - timedelta(days=1), image))
    mem.add_frame(FrameRecord("wrong-camera", "cam-b", now - timedelta(minutes=1), image))
    mem.add_frame(FrameRecord("incident", "cam-a", now - timedelta(seconds=10), image, incident=True))
    mem.add_frame(FrameRecord("future", "cam-a", now + timedelta(minutes=1), image))
    selected = mem.select_historical_baseline("cam-a", now)
    assert selected is not None and selected.frame_id == "old"


def test_naive_timestamp_rejected():
    mem = IncidentMemory()
    with pytest.raises(TimestampValidationError):
        mem.add_frame(FrameRecord("naive", "cam", datetime.now(), np.zeros((2, 2, 3), dtype=np.uint8)))


def test_duplicate_event_id_is_idempotent_and_payload_conflict_rejected():
    mem = IncidentMemory()
    assert mem.register_event("alarm-1", "abc") is False
    assert mem.register_event("alarm-1", "abc") is True
    with pytest.raises(ValueError, match="different payload"):
        mem.register_event("alarm-1", "different")


def test_missing_baseline_requests_retake_and_stops_safely():
    result = InvestigationAgent(fixture("dry_normal"), omit_baseline=True).run()
    assert result["outcome"] == "baseline_missing"
    assert result["review_request"]["type"] == "retake"
    assert "align_and_compare" not in actions(result)


def test_missing_sensor_downgrades_visual_finding():
    item = fixture("clear_change")
    item["sensor"] = None
    result = InvestigationAgent(item).run()
    assert result["outcome"] == "additional_evidence_recommended"
    assert result["finding"] == "observed_change_cause_unverified"


def test_agent_never_emits_unsafe_actuator_action():
    result = run("clear_change")
    actions_used = set(actions(result))
    assert not actions_used.intersection({"shut_down_machinery", "disable_alarm", "open_door", "dispatch_responder"})


def test_incident_event_is_not_baseline_automatically():
    mem = IncidentMemory()
    now = datetime.now(timezone.utc)
    image = np.zeros((8, 8, 3), dtype=np.uint8)
    mem.add_frame(FrameRecord("incident", "cam", now - timedelta(seconds=5), image, incident=True))
    assert mem.select_historical_baseline("cam", now) is None
