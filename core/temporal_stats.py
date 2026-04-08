"""
Temporal Statistics — WDR & STR
================================
WDR_t = (1 / |V_t|) · Σ_{k ∈ V_t} z_k          (Window Distraction Rate)
STR_i = (1 / (T-1)) · Σ_{t=2}^{T} 𝟙(y_t^i ≠ y_{t-1}^i)   (State Transition Rate)
"""

from __future__ import annotations
from collections import deque
from typing import Dict, Optional


def compute_wdr(state_window: list[int]) -> float:
    """
    Window Distraction Rate.

    Parameters
    ----------
    state_window : list of int
        Binary sequence within the sliding window W.
        1 = Distracted, 0 = Focused.
        Only frames where the student was successfully tracked (V_t) are included.

    Returns
    -------
    float  WDR_t ∈ [0, 1]
    """
    n = len(state_window)
    if n == 0:
        return 0.0
    return sum(state_window) / n


def compute_str(state_sequence: list[int]) -> float:
    """
    State Transition Rate.

    Parameters
    ----------
    state_sequence : list of int
        Full temporal state sequence for student i over T frames.

    Returns
    -------
    float  STR_i ∈ [0, 1]
    """
    T = len(state_sequence)
    if T < 2:
        return 0.0
    transitions = sum(
        1 for t in range(1, T)
        if state_sequence[t] != state_sequence[t - 1]
    )
    return transitions / (T - 1)


class TemporalStatsTracker:
    """
    Per-student online temporal statistics over a sliding window of W frames.

    Usage
    -----
    tracker = TemporalStatsTracker(window_size=30)
    for frame_states in video_frames:
        for student_id, state in frame_states.items():
            tracker.update(student_id, state)
        stats = tracker.get_stats()
    """

    def __init__(self, window_size: int = 30):
        self.W = window_size
        self._windows:     Dict[str, deque] = {}
        self._full_seq:    Dict[str, list]  = {}
        self._transitions: Dict[str, int]   = {}
        self._last_state:  Dict[str, Optional[str]] = {}

    def update(self, student_id: str, state: str) -> None:
        """
        Register one frame observation for a student.

        Parameters
        ----------
        student_id : str
        state      : 'Focused' | 'Distracted'
        """
        z = 1 if state == "Distracted" else 0

        if student_id not in self._windows:
            self._windows[student_id]     = deque(maxlen=self.W)
            self._full_seq[student_id]    = []
            self._transitions[student_id] = 0
            self._last_state[student_id]  = None

        self._windows[student_id].append(z)
        self._full_seq[student_id].append(z)

        prev = self._last_state[student_id]
        if prev is not None and prev != state:
            self._transitions[student_id] += 1
        self._last_state[student_id] = state

    def get_stats(self, student_id: str) -> dict:
        """Return current WDR and STR for one student."""
        if student_id not in self._windows:
            return {"wdr": 0.0, "str": 0.0, "transitions": 0, "frames": 0}

        wdr = compute_wdr(list(self._windows[student_id]))
        T   = len(self._full_seq[student_id])
        str_val = (self._transitions[student_id] / (T - 1)) if T > 1 else 0.0

        return {
            "wdr":         wdr,
            "str":         str_val,
            "transitions": self._transitions[student_id],
            "frames":      T,
        }

    def get_all_stats(self) -> dict:
        """Return stats for all tracked students."""
        return {sid: self.get_stats(sid) for sid in self._windows}

    def reset(self, student_id: Optional[str] = None) -> None:
        """Reset one student (or all if student_id is None)."""
        if student_id is None:
            self._windows.clear()
            self._full_seq.clear()
            self._transitions.clear()
            self._last_state.clear()
        elif student_id in self._windows:
            del self._windows[student_id]
            del self._full_seq[student_id]
            del self._transitions[student_id]
            del self._last_state[student_id]
