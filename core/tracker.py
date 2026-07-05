"""
Enhanced Tracker — Speed-adaptive Dynamic IoU Gating
=====================================================
Core innovation: τ(v) = max(τ_base − k · min(v, v_max), 0.15)

Combined matching score:
    S_ij = w_iou · IoU_ij + w_dist · s_dist(d,b) + w_size · s_size(d,b)
"""

import numpy as np
from collections import deque
from scipy.optimize import linear_sum_assignment


class EnhancedTracker:
    """
    Speed-adaptive multi-object tracker.

    Parameters
    ----------
    base_iou : float
        τ_base — baseline IoU matching threshold (paper: 0.3)
    k : float
        Speed modulation factor (paper: k = 0.1)
    v_max : float
        Speed proxy upper limit  (paper: v_max = 2.0)
    lower_bound : float
        τ(v) floor to prevent over-permissive gating (paper: 0.15)
    max_age : int
        Frames before a lost track is deleted (paper: 150)
    min_hits : int
        Minimum detections before a track is reported (paper: 3)
    use_hungarian : bool
        Hungarian (optimal) vs. greedy assignment (paper default: greedy)
    use_combined_score : bool
        Enable combined S_ij score; False → IoU-only (ablation)
    use_dynamic_threshold : bool
        Enable τ(v); False → fixed τ_base (ablation)
    """

    W_IOU  = 0.5
    W_DIST = 0.3
    W_SIZE = 0.2
    MAX_CENTER_DIST = 100   # pixels

    def __init__(
        self,
        base_iou: float = 0.3,
        k: float = 0.1,
        v_max: float = 2.0,
        lower_bound: float = 0.15,
        max_age: int = 150,
        min_hits: int = 3,
        use_hungarian: bool = False,
        use_combined_score: bool = True,
        use_dynamic_threshold: bool = True,
    ):
        self.base_iou      = base_iou
        self.k             = k
        self.v_max         = v_max
        self.lower_bound   = lower_bound
        self.max_age       = max_age
        self.min_hits      = min_hits
        self.use_hungarian = use_hungarian

        # ablation flags
        self.use_combined_score    = use_combined_score
        self.use_dynamic_threshold = use_dynamic_threshold

        self.tracks     = []
        self.lost_tracks = []
        self.next_id    = 0
        self.frame_count = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def update(self, detections: list) -> list:
        """
        Parameters
        ----------
        detections : list of [x1, y1, x2, y2]

        Returns
        -------
        active_tracks : list of track dicts with 'id', 'box', 'speed', 'hits'
        """
        self.frame_count += 1
        self._predict_tracks()

        matches, unmatched_dets, _ = self._match_detections(detections)

        for det_idx, trk_idx in matches:
            self._update_track(self.tracks[trk_idx], detections[det_idx])

        # attempt trajectory recovery for unmatched detections
        if self.lost_tracks and unmatched_dets:
            recovered = self._recover_tracks(unmatched_dets, detections)
            for det_idx, track in recovered:
                self._update_track(track, detections[det_idx])
                self.tracks.append(track)
                unmatched_dets.remove(det_idx)

        for det_idx in unmatched_dets:
            self._create_track(detections[det_idx])

        self._expire_tracks()

        return [
            {
                "id":    t["id"],
                "box":   list(t["boxes"][-1]),
                "speed": t["speed"],
                "hits":  t["hits"],
            }
            for t in self.tracks
            if t["hits"] >= self.min_hits and t["time_since_update"] < 1
        ]

    # ------------------------------------------------------------------
    # Dynamic threshold  τ(v) = max(τ_base − k · min(v, v_max), 0.15)
    # ------------------------------------------------------------------

    def dynamic_threshold(self, speed: float) -> float:
        """Equation (1) from the paper."""
        return max(
            self.base_iou - self.k * min(speed, self.v_max),
            self.lower_bound,
        )

    # ------------------------------------------------------------------
    # Combined matching score  S_ij
    # ------------------------------------------------------------------

    def matching_score(self, det, pred) -> float:
        """
        S_ij = w_iou · IoU + w_dist · s_dist + w_size · s_size
        """
        iou = self._compute_iou(det, pred)
        if not self.use_combined_score:
            return iou

        det_center  = ((det[0]  + det[2])  / 2, (det[1]  + det[3])  / 2)
        pred_center = ((pred[0] + pred[2]) / 2, (pred[1] + pred[3]) / 2)
        dist = np.hypot(det_center[0] - pred_center[0],
                        det_center[1] - pred_center[1])
        s_dist = max(0.0, 1.0 - dist / self.MAX_CENTER_DIST)

        det_area  = max(1e-6, (det[2]  - det[0])  * (det[3]  - det[1]))
        pred_area = max(1e-6, (pred[2] - pred[0]) * (pred[3] - pred[1]))
        s_size = min(det_area, pred_area) / max(det_area, pred_area)

        return self.W_IOU * iou + self.W_DIST * s_dist + self.W_SIZE * s_size

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _predict_tracks(self):
        for t in self.tracks:
            t["age"]              += 1
            t["time_since_update"] += 1
            if len(t["boxes"]) >= 2:
                dx = t["boxes"][-1][0] - t["boxes"][-2][0]
                dy = t["boxes"][-1][1] - t["boxes"][-2][1]
                t["speed"] = float(np.hypot(dx, dy))
                pred = t["boxes"][-1].copy()
                pred[0] += dx; pred[1] += dy
                pred[2] += dx; pred[3] += dy
                t["predicted"] = pred
            else:
                t["speed"]     = 0.0
                t["predicted"] = t["boxes"][-1] if t["boxes"] else None

    def _match_detections(self, detections):
        matches         = []
        unmatched_dets  = list(range(len(detections)))
        unmatched_trks  = list(range(len(self.tracks)))

        if not detections or not self.tracks:
            return matches, unmatched_dets, unmatched_trks

        score_matrix = np.zeros((len(detections), len(self.tracks)))
        for d, det in enumerate(detections):
            for t, trk in enumerate(self.tracks):
                if trk["predicted"] is None:
                    continue
                score = self.matching_score(det, trk["predicted"])
                tau   = (self.dynamic_threshold(trk["speed"])
                         if self.use_dynamic_threshold
                         else self.base_iou)
                if score >= tau:
                    score_matrix[d, t] = score

        if self.use_hungarian:
            cost = 1.0 - score_matrix
            cost[score_matrix <= 0] = 1e6
            di, ti = linear_sum_assignment(cost)
            for d, t in zip(di, ti):
                if score_matrix[d, t] > 0:
                    matches.append((int(d), int(t)))
        else:
            sm = score_matrix.copy()
            while sm.max() > 0:
                d, t = np.unravel_index(sm.argmax(), sm.shape)
                matches.append((int(d), int(t)))
                sm[d, :] = 0
                sm[:, t] = 0

        matched_d = {m[0] for m in matches}
        matched_t = {m[1] for m in matches}
        unmatched_dets = [i for i in range(len(detections)) if i not in matched_d]
        unmatched_trks = [i for i in range(len(self.tracks))  if i not in matched_t]
        return matches, unmatched_dets, unmatched_trks

    def _recover_tracks(self, unmatched_dets, detections):
        recovered  = []
        used_dets  = set()
        THRESH     = 0.20

        for trk in self.lost_tracks[:]:
            best_score, best_idx = THRESH, None
            for det_idx in unmatched_dets:
                if det_idx in used_dets:
                    continue
                det      = detections[det_idx]
                last_box = trk["boxes"][-1] if trk["boxes"] else None
                if last_box is None:
                    continue
                iou  = self._compute_iou(det, last_box)
                dc   = ((det[0]+det[2])/2, (det[1]+det[3])/2)
                lc   = ((last_box[0]+last_box[2])/2, (last_box[1]+last_box[3])/2)
                dist = np.hypot(dc[0]-lc[0], dc[1]-lc[1])
                max_d = self.MAX_CENTER_DIST * (1 + trk["time_since_update"] * 0.1)
                s_dist = max(0.0, 1.0 - dist / max_d)
                score  = 0.4 * iou + 0.6 * s_dist
                if score > best_score:
                    best_score, best_idx = score, det_idx
            if best_idx is not None:
                recovered.append((best_idx, trk))
                used_dets.add(best_idx)
                self.lost_tracks.remove(trk)
        return recovered

    def _update_track(self, trk, det):
        trk["boxes"].append(list(det))
        trk["hits"]              += 1
        trk["time_since_update"]  = 0
        trk["age"]                = 0

    def _create_track(self, det):
        self.tracks.append({
            "id":               self.next_id,
            "boxes":            deque([list(det)], maxlen=30),
            "age":              0,
            "hits":             1,
            "time_since_update": 0,
            "speed":            0.0,
            "predicted":        None,
        })
        self.next_id += 1

    def _expire_tracks(self):
        remaining = []
        for trk in self.tracks:
            if trk["time_since_update"] > self.max_age:
                if trk["hits"] > self.min_hits:
                    self.lost_tracks.append(trk)
                    if len(self.lost_tracks) > 20:
                        self.lost_tracks.pop(0)
            else:
                remaining.append(trk)
        self.tracks = remaining

    @staticmethod
    def _compute_iou(box1, box2) -> float:
        x1 = max(box1[0], box2[0]);  y1 = max(box1[1], box2[1])
        x2 = min(box1[2], box2[2]);  y2 = min(box1[3], box2[3])
        if x2 <= x1 or y2 <= y1:
            return 0.0
        inter = (x2 - x1) * (y2 - y1)
        a1    = (box1[2]-box1[0]) * (box1[3]-box1[1])
        a2    = (box2[2]-box2[0]) * (box2[3]-box2[1])
        union = a1 + a2 - inter
        return inter / union if union > 0 else 0.0
