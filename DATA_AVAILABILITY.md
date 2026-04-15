# Data Availability

## Summary

This public repository provides release-facing code, configuration, a privacy-aware derived annotation package, and supplementary figures/tables for the classroom distraction tracker project.

## Included in this public repository

- Source code under `backend/`, `core/`, and `frontend/`
- Configuration files such as `config.yaml` and `requirements.txt`
- Derived annotations in `derived_release/`
- Supplementary figures and tables in `submission_assets/`
- Documentation describing model access, release packaging, and data constraints

## Not included in the public repository

- Raw classroom videos
- Audio, original frames, or other directly identifying classroom media
- Controlled internal data collections that are not approved for public redistribution

If you have local copies of classroom videos, treat them as controlled research materials and verify that you have permission before sharing them.

## Derived public package

The folder `derived_release/` is the public, privacy-aware data package included with this release.

It contains:

- `derived_status_boxes.csv`
- `manifest.json`

This package omits raw frames, audio, and direct source paths, and keeps only the fields needed for evaluation-level reproducibility.

## Third-party or separately obtained data

Some development or internal evaluation may rely on separately obtained datasets or institutional data sources. Those materials are not redistributed here and remain subject to their original licenses, terms, or privacy restrictions.

## Reproducibility scope

This lightweight public mirror is intended to support:

- artifact inspection
- code review
- evaluation-level reproducibility using the derived package
- access to supplementary figures and tables

Exact end-to-end reruns on raw classroom videos require controlled local access to the original data and any private/internal assets used during development.
