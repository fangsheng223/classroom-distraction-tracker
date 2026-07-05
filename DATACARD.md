# Data Card: derived_release (Derived Annotations)

## Summary

This release provides a *derived* (non-visual) annotation package for reproducing the evaluation reported in `paper_manuscript.md` without distributing the original classroom videos.

## Contents

- `derived_status_boxes.csv`
- `manifest.json`

## Record format

Each row in `derived_status_boxes.csv` is one ground-truth box instance:

- `video`: video name (e.g., `class_1`)
- `frame_id`: 1-indexed frame number
- `id`: person identity ID within the video
- `x1,y1,x2,y2`: bounding box in pixel coordinates
- `status`: `Focused` or `Distracted`

Field definitions are also listed in `manifest.json`.

## How it is generated

Run (from repo root):

`python export_derived_dataset.py --annotations_dir annotations --out_dir derived_release`

The exporter reads `annotations/*_status_annotations.json` and writes the derived CSV + manifest.

## Privacy / sensitive data statement

- This package does **not** include any raw videos, frames, face images, or audio.
- `video_path` fields are intentionally omitted.
- Bounding boxes and IDs can still be considered sensitive in some contexts; please follow your institution’s privacy policies.

## Intended use

- Reproducing the paper’s reported metrics under the same evaluation protocol.
- Method comparison / ablation reproduction.

## Out-of-scope use

- Any attempt to re-identify individuals or reconstruct identifiable imagery.
- Any use for surveillance, profiling, or punitive decision-making.

## License / usage restriction

This derived package and its parent dataset (the seven self-collected classroom videos `class_1`…`class_7` and the per-video annotations in `annotations/`) are released under a **research-only, non-commercial license**. The full terms — including permitted uses, prohibited uses (commercial use, re-identification, face recognition, biometric identification, emotion scoring, surveillance, profiling, teacher / student evaluation, punitive decision-making), redistribution rules, consent statement, downstream privacy obligations, and withdrawal procedure — are specified in `DATASET_LICENSE.md` in the repository root. Where this card and `DATASET_LICENSE.md` disagree, the stricter restriction applies.

When publishing this package as a GitHub Release, attach `DATASET_LICENSE.md` and reference it from the release notes so that the same terms apply to the raw videos, the per-video JSON annotations, and the derived annotation package.

## Citation

If you use this derived package, cite the paper and reference the GitHub Release URL (to be filled after publishing), and comply with the research-only non-commercial terms in `DATASET_LICENSE.md`.

See also: `README.md`, `DATA_AVAILABILITY.md`, `DATASET_LICENSE.md`, `RELEASES.md`, and `CONTRIBUTING.md`.
