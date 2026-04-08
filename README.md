# Classroom Distraction Frequency Tracker

An edge-optimized, dual-mode computer vision framework for tracking and quantifying student distraction frequency in real classroom settings.

> **Paper:** *Edge-Optimized Dual-Mode Tracking-to-Analysis Pipeline for Robust Classroom Distraction Frequency Quantification* (Under Review)

---

## System Demo

| Real-Time NRT Mode | Offline Batch Mode |
|---|---|
| MJPEG stream overlay | Per-student distraction report |
| P99 head latency: 322 ms | Throughput: **21.15 FPS** |

![System Architecture](assets/system_architecture.png)

---

## Key Results

### Table 1 — Main Quantitative Comparison

| Method | MOTA@0.3 | IDF1@0.3 | IDSW@0.3 | MOTA@0.5 | IDF1@0.5 | F1 | FPS |
|---|---|---|---|---|---|---|---|
| **Ours_Full** | **0.8928±0.075** | **0.9460±0.038** | **5.6±5.7** | **0.5995±0.198** | **0.7976±0.100** | **0.5427±0.054** | **21.15±3.49** |
| YOLOv8_ByteTrack | 0.8686±0.093 | 0.9315±0.052 | 13.7±5.6 | 0.6238±0.198 | 0.8031±0.108 | N/A | 83.19±9.33 |
| Fixed_IoU_0.5_E2E | 0.8888±0.074 | 0.9445±0.037 | 16.1±8.6 | 0.5981±0.197 | 0.7967±0.100 | 0.5386±0.055 | 27.17±5.42 |
| Fixed_IoU_0.3_E2E | 0.8904±0.074 | 0.9449±0.037 | 9.3±7.1 | 0.5987±0.197 | 0.7968±0.100 | 0.5399±0.054 | 25.92±4.19 |

### Table 2 — Scene-Level Breakdown

| Scene | #Videos | MOTA@Main | IDF1@Main | MOTA@Strict | IDF1@Strict | F1 | FPS |
|---|---|---|---|---|---|---|---|
| Scene A (class 1–5) | 5 | 0.9264±0.027 | 0.9630±0.013 | 0.7015±0.082 | 0.8497±0.039 | 0.5449±0.057 | 22.89±2.23 |
| Scene B (class 6–7) | 2 | 0.8086±0.072 | 0.9035±0.037 | 0.3447±0.100 | 0.6671±0.051 | 0.5372±0.026 | 16.80±0.44 |

### Table 3 — Ablation Study

| Setting | Combined Score | Dyn. Threshold | Context | F1 | FPS |
|---|---|---|---|---|---|
| Full_Model | ✓ | ✓ | ✓ | 0.5427±0.054 | 21.88±3.31 |
| No_Combined_Score | ✗ | ✓ | ✓ | 0.5426±0.054 | 24.15±2.83 |
| No_Dynamic_Threshold | ✓ | ✗ | ✓ | 0.5427±0.054 | 22.47±3.43 |
| No_Context | ✓ | ✓ | ✗ | 0.5416±0.054 | 24.25±4.58 |
| Basic_IoU_Only | ✗ | ✗ | ✗ | 0.5416±0.054 | 27.70±5.19 |

---

## Architecture

```
Video Stream
    │
    ▼
┌─────────────────┐
│  YOLOv8 Detector │  (person class only, det_interval=3)
└────────┬────────┘
         │ bounding boxes
         ▼
┌─────────────────────────────────┐
│       Enhanced Tracker           │
│  · Speed-adaptive dynamic IoU   │  τ(v) = max(τ_base − k·min(v,v_max), 0.15)
│  · Combined matching score Sij  │  Sij = 0.5·IoU + 0.3·dist + 0.2·size
│  · Two-stage trajectory recovery│
└────────┬────────────────────────┘
         │ tracked ROIs (with ID)
         ▼
┌─────────────────────────────┐
│  Lightweight CNN (21,475 params) │
│  Input: 224×224 ROI crop        │
│  Output: [nose_offset,          │
│           head_down_angle,      │
│           shoulder_diff]        │
└────────┬────────────────────┘
         │ hard parameters
         ▼
┌──────────────────────────────┐
│  Context Correction Module    │
│  Temporal majority voting     │
│  Boundary-aware smoothing     │
└────────┬─────────────────────┘
         │ per-frame state {Focused, Distracted}
         ▼
┌───────────────────────────┐
│  Temporal Statistics       │
│  WDR_t = (1/|V_t|)·Σ z_k  │
│  STR_i = (1/(T-1))·Σ 𝟙()  │
└────────┬──────────────────┘
         │
         ▼
   Per-student Report
   (distraction rate, transition freq, timeline)
```

---

## Dual-Mode Execution

| Mode | Throughput | P99 Latency | Use Case |
|---|---|---|---|
| Near Real-Time (NRT) | 9.64 FPS | 322 ms [298–392 ms] | Live classroom monitoring |
| Offline Batch | **21.15 FPS** | N/A | Post-class analysis |

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the backend server

```bash
cd backend
python manage.py runserver 0.0.0.0:8000
```

### 3. Open the frontend

Navigate to `http://localhost:8000/` in your browser.

### 4. (Optional) Run core algorithm standalone

```python
from core.tracker import EnhancedTracker
from core.classifier import LightweightCNNModel
from core.temporal_stats import compute_wdr, compute_str

tracker = EnhancedTracker(base_iou=0.3)
# ... see core/tracker.py for full usage
```

---

## Repository Structure

```
classroom-distraction-tracker/
├── core/
│   ├── tracker.py          # Speed-adaptive dynamic IoU tracker
│   ├── classifier.py       # Lightweight CNN (21,475 params)
│   ├── temporal_stats.py   # WDR / STR temporal statistics
│   └── context.py          # Context correction module
├── backend/                # Django REST API + MJPEG streaming
│   ├── manage.py
│   ├── web_demo_backend/   # Django settings
│   └── api/
│       ├── urls.py         # API endpoints
│       └── views.py        # Request handlers
├── frontend/
│   └── index.html          # Vue.js single-page app
├── config.yaml             # Hyperparameters
└── requirements.txt
```

> **Note:** Pre-trained model weights are not included in this repository.
> The system requires `models/lightweight_cnn.pth` (PyTorch) and
> `yolov8s.pt` (Ultralytics) to run inference.

---

## Citation

```bibtex
@article{distraction2025,
  title   = {Edge-Optimized Dual-Mode Tracking-to-Analysis Pipeline for
             Robust Classroom Distraction Frequency Quantification},
  year    = {2025},
  note    = {Under Review}
}
```
