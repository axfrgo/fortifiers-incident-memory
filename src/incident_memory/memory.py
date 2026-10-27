from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from threading import Lock

import numpy as np


class TimestampValidationError(ValueError):
    pass


@dataclass
class FrameRecord:
    frame_id: str
    camera_id: str
    timestamp: datetime
    image: np.ndarray
    context: str = "mechanical_room"
    quality_score: float = 1.0
    incident: bool = False


def require_aware(timestamp: datetime) -> datetime:
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise TimestampValidationError("timestamps must include a timezone")
    return timestamp.astimezone(timezone.utc)


class IncidentMemory:
    """Small frame index; incident images are never promoted to baseline implicitly."""

    def __init__(self) -> None:
        self._frames: list[FrameRecord] = []
        self._event_ids: dict[str, str] = {}
        self._lock = Lock()

    def add_frame(self, frame: FrameRecord) -> None:
        require_aware(frame.timestamp)
        with self._lock:
            if any(existing.frame_id == frame.frame_id for existing in self._frames):
                raise ValueError(f"duplicate frame id: {frame.frame_id}")
            self._frames.append(frame)

    def select_historical_baseline(self, camera_id: str, event_time: datetime, context: str = "mechanical_room") -> FrameRecord | None:
        event_time = require_aware(event_time)
        with self._lock:
            candidates = [f for f in self._frames if f.camera_id == camera_id and f.context == context
                          and not f.incident and require_aware(f.timestamp) < event_time and f.quality_score >= 0.4]
        if not candidates:
            return None
        return max(candidates, key=lambda f: require_aware(f.timestamp))

    def older_frames(self, camera_id: str, before: datetime, context: str = "mechanical_room") -> list[FrameRecord]:
        before = require_aware(before)
        with self._lock:
            frames = [f for f in self._frames if f.camera_id == camera_id and f.context == context
                      and require_aware(f.timestamp) < before]
        return sorted(frames, key=lambda f: require_aware(f.timestamp), reverse=True)

    def register_event(self, event_id: str, payload_fingerprint: str) -> bool:
        """Return True for an already-seen event id; differing payload remains a conflict."""
        with self._lock:
            previous = self._event_ids.get(event_id)
            if previous is not None and previous != payload_fingerprint:
                raise ValueError("event id was already used with a different payload")
            self._event_ids[event_id] = payload_fingerprint
            return previous is not None

