from __future__ import annotations

from enum import Enum

class FailureType(str, Enum):
    DOWN = "down"
    DEGRADED = "degraded"
    LATENCY_UP = "latency_up"
    