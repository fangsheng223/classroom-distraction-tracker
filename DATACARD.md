# Data Card: derived_release (Derived Annotations)

## Summary

This public release provides a derived, non-visual annotation package in `derived_release/` for evaluation-level reproducibility without distributing raw classroom videos.

## Contents

- `derived_status_boxes.csv`
- `manifest.json`

## Record format

Each row in `derived_status_boxes.csv` corresponds to one box-level annotation instance.

Fields include:

- `video`: video identifier
- `frame_id`: 1-indexed frame number
- `id`: person identity ID within the video
- `x1,y1,x2,y2`: bounding box coordinates in pixels
- `status`: `Focused` or `Distracted`

Additional field descriptions are listed in `manifest.json`.

## Release note on generation

This lightweight public repository ships the derived package directly. The internal export utility used to produce this package is not required in order to inspect or use this release.

## Privacy / sensitive data statement

- This package does **not** include raw videos, frames, face crops, or audio.
- Direct source paths are omitted from the public release.
- Bounding boxes and IDs can still be sensitive in some contexts; follow your institution's privacy and data-governance requirements.

## Intended use

- reproducing evaluation-level results
- comparing methods under the same derived annotation protocol
- supporting paper artifact review and supplementary material inspection

## Out-of-scope use

- any attempt to re-identify individuals
- any attempt to reconstruct identifiable imagery
- surveillance, profiling, or punitive decision-making

## Usage note

If you use this derived package, cite the corresponding paper/project release and reference the repository or release URL.
