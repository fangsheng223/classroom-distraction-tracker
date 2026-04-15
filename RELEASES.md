# Releases and Supplemental Archive Notes

## Recommended tagged release structure

When publishing this repository as a public supplemental archive, create a GitHub Release such as `v1.0.0` and keep the release notes synchronized with the files in the repository root.

## Recommended release assets

- source snapshot of the tagged commit
- `derived_release.zip`
- `submission_assets.rar`

## What each archive contains

### `derived_release.zip`

Privacy-aware derived annotations for evaluation-level reproducibility.

### `submission_assets.rar`

Prepared supplementary figures and tables, including:

- `submission_assets/figures/`
- `submission_assets/tables/`

## Suggested versioning practice

- Use semantic or paper-aligned tags such as `v1.0.0`, `camera-ready`, or `paper-submission-2026-04`.
- Keep `README.md`, `DATA_AVAILABILITY.md`, and `MODEL_ACCESS.md` synchronized with each release.
- State clearly whether a release contains code only, code plus derived annotations, or additional supplemental assets.

## Suggested release notes template

```text
Release: v1.0.0
Contents:
- source code
- supplementary figures/tables
- derived annotations (no raw classroom videos)
Notes:
- raw classroom videos are not included
- see DATA_AVAILABILITY.md and MODEL_ACCESS.md for details
```
