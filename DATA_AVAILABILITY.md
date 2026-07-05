# Data Availability

## Summary

This repository is intended to support code-level and evaluation-level reproducibility for the manuscript **Interpretable classroom distraction estimation via tracking-to-analysis continuity** while respecting privacy constraints for classroom videos.

## Publicly included in this repository

- Source code for inference, evaluation, visualization, and web demo components.
- Configuration files such as `config.yaml` and `requirements.txt`.
- Derived annotations in `derived_release/`.
- Annotation files in `annotations/` used for evaluation and reproducibility.
- Submission figures and tables in `submission_assets/`.

## Auxiliary training data from public Roboflow exports

The lightweight CNN training pipeline uses an auxiliary behavior dataset that is independent of the seven classroom evaluation videos. The local merged copy is stored as `data/merged_behavior_dataset/` and follows the YOLO format with six categories: `writing`, `reading`, `listening`, `phone`, `sleeping`, and `looking_around`.

The auxiliary dataset was assembled from public Roboflow exports. The local source folders and Roboflow metadata are:

- `Student Behavior Date/Class Monitoring.v1i.yolov8/`: Roboflow project `class-monitoring-yln3r`, version 1, license CC BY 4.0, URL: <https://app.roboflow.com/fangsheng-z3tuv/class-monitoring-yln3r/1>.
- `Student Behavior Date/Student Behaviour Detection.v1i.yolov8/`: Roboflow project `student-behaviour-detection-neazg-kaavr`, version 1, license CC BY 4.0, URL: <https://app.roboflow.com/fangsheng-z3tuv/student-behaviour-detection-neazg-kaavr/1>.
- `Student Behavior Date/Multi_all.v1i.yolov8/`: Roboflow project `multi_all-5awsd`, version 1, license CC BY 4.0, URL: <https://app.roboflow.com/fangsheng-z3tuv/multi_all-5awsd/1>.
- `Student Behavior Date/S.B.C.v1i.yolov8/`: Roboflow project `s.b.c-a6fxy`, version 1, license CC BY 4.0, URL: <https://app.roboflow.com/fangsheng-z3tuv/s.b.c-a6fxy/1>.
- `Student Behavior Date/per.v1i.yolov8/`: Roboflow project `per-tawzy-xedyk`, version 1, license CC BY 4.0, URL: <https://app.roboflow.com/fangsheng-z3tuv/per-tawzy-xedyk/1>.

The manuscript reports the merged auxiliary dataset scale as 9,856 images and 170,389 bounding-box annotations. Users should download the original public datasets from Roboflow and comply with the corresponding licenses and platform terms.

## Derived hard-parameter regression data

The script `create_regression_dataset.py` converts `data/merged_behavior_dataset/` into `data/hard_params_dataset/`. The conversion maps behavior categories to three proxy regression targets: `nose_offset`, `head_down`, and `shoulder_diff`, using behavior-to-hard-parameter priors and random perturbations. This derived training dataset is used to train the lightweight CNN and does not use the seven classroom evaluation videos.

## Classroom evaluation videos (research-only release)

Following reviewer requests for an openly auditable evaluation set, the seven self-collected classroom videos `class_1.mp4` … `class_7.mp4` used to evaluate the manuscript are **publicly released for research and non-commercial use only**. The release is published together with the per-video annotations in `annotations/class_{1..7}_status_annotations.json` and the privacy-aware derived package in `derived_release/`, so that the full evaluation pipeline described in Section 4.3 of the manuscript can be reproduced end-to-end.

The full license, scope, consent statement and downstream privacy obligations are specified in `DATASET_LICENSE.md`. Key terms (summary):

- Use is permitted only for academic research, method development and reproduction of the reported experiments. Any form of commercial use is prohibited.
- Re-identification of individuals, biometric / face-recognition / emotion-scoring uses, surveillance, profiling and any punitive decision-making about specific individuals or classes are explicitly prohibited.
- Redistribution of the raw videos outside the official release channel requires written permission from the dataset maintainers; the stricter of this license and any other applicable terms always applies.
- Downstream users must store the videos on access-controlled systems, comply with applicable data-protection regulations, and use cropped / blurred views in publications whenever full-frame imagery is not strictly necessary.
- Withdrawal requests and reports of misuse should be sent to the corresponding author; affected footage will be removed from the public release within a reasonable period.

The release URL is fixed and listed below. The seven self-collected classroom evaluation videos (`class_1.mp4` … `class_7.mp4`) are now archived to **Zenodo** (record: <https://zenodo.org/records/21206959>) under the research-only, non-commercial license described in `DATASET_LICENSE.md`; see the **"Permanent identifier (Zenodo DOI — version of record)"** section below for the persistent identifier. The Zenodo deposit also mirrors `derived_release.zip` and `submission_assets.zip` (the two assets that are also attached as GitHub Release assets at <https://github.com/fangsheng223/classroom-distraction-tracker/releases/tag/v1.1.0-dataset>). Requests for additional access can be sent to the corresponding author of the manuscript under `DATASET_LICENSE.md`.

## Permanent identifier (Zenodo DOI — version of record)

To satisfy PeerJ Computer Science’s data-availability requirements, the **seven self-collected classroom evaluation videos (`class_1.mp4` … `class_7.mp4`)** are now archived to **Zenodo** under the research-only, non-commercial license described in `DATASET_LICENSE.md`. Zenodo assigns a permanent DOI to each archived version, which serves as the version-of-record identifier cited from the manuscript and from this repository. A direct download of the seven raw videos plus the derived package is available from the latest Zenodo record (v2): <https://zenodo.org/records/21207208>.

| Identifier | Value |
|------------|-------|
| **Zenodo Concept DOI (always latest)** | **10.5281/zenodo.21206958** ([https://doi.org/10.5281/zenodo.21206958](https://doi.org/10.5281/zenodo.21206958)) |
| **Zenodo record URL (Concept, always latest)** | <https://zenodo.org/records/21206958> |
| **Zenodo DOI (latest version, v2)** | **10.5281/zenodo.21207208** ([https://doi.org/10.5281/zenodo.21207208](https://doi.org/10.5281/zenodo.21207208)) |
| **Zenodo record URL (latest version, v2)** | <https://zenodo.org/records/21207208> (129.8 MB, includes the seven raw videos) |
| **Zenodo DOI (historical v1, no videos)** | 10.5281/zenodo.21206959 ([https://doi.org/10.5281/zenodo.21206959](https://doi.org/10.5281/zenodo.21206959)) |
| **Zenodo record URL (historical v1)** | <https://zenodo.org/records/21206959> (3.9 MB, no raw videos) |
| **Tagged GitHub Release (code + annotations + derived package)** | https://github.com/fangsheng223/classroom-distraction-tracker/releases/tag/v1.1.0-dataset |
| **Repository URL** | https://github.com/fangsheng223/classroom-distraction-tracker |

> This table is the canonical persistent-identifier table for the self-curated dataset. The Zenodo Concept DOI **10.5281/zenodo.21206958** always resolves to the latest published version of the dataset; the current latest version DOI is **10.5281/zenodo.21207208** (<https://zenodo.org/records/21207208>, 129.8 MB, archives the seven `class_*.mp4` files together with `derived_release.zip` and `submission_assets.zip`). The same Concept DOI is cited from the badge and tables in `README.md` and from the manuscript Data Availability statement. Earlier versions of the same Concept DOI (e.g. v1 10.5281/zenodo.21206959, 3.9 MB, without the raw videos) remain individually citable for reproducibility audits. The tagged GitHub Release above remains a valid, citable, versioned reference for the source code, per-video annotations, and the derived package.

### How to mint the Zenodo DOI (recommended procedure)

The recommended, no-cost workflow is to enable Zenodo's GitHub integration so that every tagged release of this repository automatically receives a Zenodo record and DOI:

1. Sign in to **Zenodo** (<https://zenodo.org/>) with the GitHub account that owns `fangsheng223/classroom-distraction-tracker`.
2. Go to **Account settings → Applications → GitHub**, click **Connect**, and authorize Zenodo.
3. Still under the **GitHub** tab, flip the switch next to `fangsheng223/classroom-distraction-tracker` to enable the integration.
4. Optional but recommended: keep the `.zenodo.json` file shipped at the repository root; Zenodo reads this file and uses it to pre-fill the record metadata (creator names, affiliations, license, keywords).
5. Optional but recommended: keep the `CITATION.cff` file shipped at the repository root so that GitHub's "Cite this repository" button and Zenodo's metadata extractor share the same author list.
6. The next time a GitHub release is created or republished (e.g. an updated `v1.2.0`), Zenodo will automatically archive the repository, mint a DOI, and display it in the Zenodo dashboard.
7. Copy the resulting DOI and record URL into:
   - the Zenodo DOI badge and the "Self-Curated Dataset at a Glance" table at the top of `README.md`;
   - the "Permanent identifier (Zenodo DOI)" table above;
   - the manuscript Data Availability statement.

> **Note on scope.** Per PeerJ's policy, the DOI/URL requirement applies to the **self-curated dataset**, not to third-party Roboflow exports (which are already individually citable at their Roboflow project pages). Therefore the Zenodo DOI references the seven `class_*.mp4` files together with the per-video annotations and the privacy-aware derived package — i.e. exactly the artefacts described in `DATASET_LICENSE.md` as the "self-curated evaluation dataset".

## Derived public package

The folder `derived_release/` provides a privacy-aware reproducibility package:

- `derived_status_boxes.csv`
- `manifest.json`

This package omits original frames, audio, and direct source paths, and only keeps the fields needed for evaluation-level reproduction.

## Photographs in the Manuscript

**Figures 1, 2, and 14** in the manuscript are visual outputs derived from the seven self-collected classroom evaluation videos (`class_1.mp4` … `class_7.mp4`). These are **not** downloaded from any third-party dataset or external source.

Permission for the use of these photographs in the manuscript has been obtained under the consent framework described in `DATASET_LICENSE.md` (Section 4: Consent and Ethical Statement). The same research-only, non-commercial terms that govern the evaluation videos apply to these derived visual outputs.

If you reproduce these figures or similar visual outputs in your own work, you must:
1. Comply with the `DATASET_LICENSE.md` terms (research-only, non-commercial use).
2. Prefer cropped, blurred, or anonymized views in publications as described in Section 5 of `DATASET_LICENSE.md`.
3. Acknowledge the source dataset and include a link to the repository license terms.

## External / Third-Party Datasets

Some experiments in this project reference third-party or separately collected datasets placed under `Student Behavior Date/`. Their redistribution may be subject to separate licenses or platform terms. Users should obtain those datasets from the original providers or use their own legally obtained copies. For the auxiliary behavior dataset used by the lightweight CNN, the Roboflow sources are listed above.

## Manuscript data availability statement

Recommended wording for the manuscript:

```text
The auxiliary behavior dataset used to train the lightweight CNN was assembled from public Roboflow exports under CC BY 4.0 licenses; the source URLs are listed in the public repository documentation. The seven self-collected classroom evaluation videos used in this study are publicly released for research and non-commercial use only, together with their per-video annotations and the privacy-aware derived annotation package, so that the full evaluation pipeline can be reproduced end-to-end. The release license, scope, consent statement, and downstream privacy obligations (including prohibitions on commercial use, re-identification, biometric / face-recognition uses, surveillance, profiling, and punitive decision-making about specific individuals or classes) are specified in the DATASET_LICENSE document distributed with the repository. Withdrawal requests can be sent to the corresponding author and affected footage will be removed from the public release within a reasonable period.
```

## How to regenerate the derived package

```bash
python export_derived_dataset.py --annotations_dir annotations --out_dir derived_release
```

## Recommended citation / usage note

If you use the derived annotations or code in this repository, cite the manuscript **Interpretable classroom distraction estimation via tracking-to-analysis continuity** and the corresponding project release, and describe whether your experiments used:

- the public derived package only,
- the full internal annotation set,
- or a separate locally obtained raw-video dataset.
