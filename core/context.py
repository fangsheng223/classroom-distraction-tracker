"""
Context Correction Module
==========================
Temporal majority-voting over a causal (NRT) or bidirectional (Offline)
neighbourhood window to suppress high-frequency boundary flips.

Decision logic:
    - If confidence ∈ (τ_low, τ_high)  →  apply weighted history average
    - Otherwise                         →  accept raw CNN output directly
"""

from __future__ import annotations
import numpy as np
from collections import defaultdict, deque
from typing import Dict, Optional, Tuple


class ClassroomContextAnalyzer:
    """Collective attention analysis (simplified)."""

    def __init__(self):
        self._behavior_history: deque = deque(maxlen=60)

    def analyze(self, student_states: list) -> dict:
        if not student_states:
            return {"attention_level": 0.5, "pattern": "unknown"}

        focused = sum(1 for s in student_states if s.get("status") == "Focused")
        level   = focused / len(student_states)
        self._behavior_history.append(level)

        pattern = "mixed_attention"
        if len(self._behavior_history) >= 10:
            recent  = list(self._behavior_history)[-10:]
            avg     = np.mean(recent)
            trend   = np.polyfit(range(10), recent, 1)[0]
            if avg > 0.7:
                pattern = "collective_focus"
            elif avg < 0.3:
                pattern = "collective_distraction"
            elif trend > 0.05:
                pattern = "attention_increasing"
            elif trend < -0.05:
                pattern = "attention_decreasing"

        return {"attention_level": float(level), "pattern": pattern}


class EnhancedDistractionDetector:
    """
    Per-student context-aware state smoother.

    Parameters
    ----------
    tau_low  : float  Lower decision boundary  (paper: 0.25)
    tau_high : float  Upper decision boundary  (paper: 0.55)
    window   : int    Causal history window for NRT mode
    enabled  : bool   Toggle; when False behaves as pass-through
    """

    def __init__(
        self,
        context_analyzer: Optional[ClassroomContextAnalyzer] = None,
        tau_low:  float = 0.25,
        tau_high: float = 0.55,
        window:   int   = 5,
        enabled:  bool  = True,
    ):
        self.analyzer  = context_analyzer or ClassroomContextAnalyzer()
        self.tau_low   = tau_low
        self.tau_high  = tau_high
        self.window    = window
        self.enabled   = enabled

        self._conf_history: Dict[str, deque] = defaultdict(
            lambda: deque(maxlen=window)
        )

    def set_enabled(self, flag: bool) -> None:
        self.enabled = flag

    def correct(
        self,
        student_id: str,
        raw_state:  str,
        confidence: float,
    ) -> Tuple[str, float]:
        """
        Apply boundary-aware context correction to a single observation.

        Parameters
        ----------
        student_id : str
        raw_state  : 'Focused' | 'Distracted'
        confidence : float  ∈ [0, 1]

        Returns
        -------
        (corrected_state, corrected_confidence)
        """
        self._conf_history[student_id].append(confidence)

        if not self.enabled or len(self._conf_history[student_id]) < 2:
            return raw_state, confidence

        # Boundary zone: apply weighted sliding average
        if self.tau_low < confidence < self.tau_high:
            history = list(self._conf_history[student_id])
            weights = np.exp(np.linspace(-1, 0, len(history)))
            weights /= weights.sum()
            smoothed = float(np.dot(weights, history))
            state    = "Distracted" if smoothed > (self.tau_low + self.tau_high) / 2 else "Focused"
            return state, smoothed

        return raw_state, confidence

    def reset(self, student_id: Optional[str] = None) -> None:
        if student_id is None:
            self._conf_history.clear()
        elif student_id in self._conf_history:
            del self._conf_history[student_id]
