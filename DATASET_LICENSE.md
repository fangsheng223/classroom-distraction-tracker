# Classroom Evaluation Video Dataset — License and Usage Terms

This document specifies the public release terms for the seven self-collected classroom videos used to evaluate the manuscript **Interpretable classroom distraction estimation via tracking-to-analysis continuity**. It applies to the videos `class_1.mp4` … `class_7.mp4` and to any frames, ROI crops, or visual derivatives produced from them.

## 1. Background and motivation for release

In the original submission the seven classroom evaluation videos were treated as restricted research material. In response to reviewer requests for an openly auditable evaluation set, we now release the seven videos as a **research-only, non-commercial dataset** so that other researchers can reproduce the reported tracking and distraction-state results on the exact data described in Section 4.3 of the manuscript.

We release the videos as-is, together with the existing derived annotation package (`derived_release/`) and the per-video annotation files in `annotations/`, so that the full evaluation pipeline can be re-run end-to-end.

## 2. Scope of the release

The released dataset consists of:

- Seven classroom video files: `class_1.mp4` … `class_7.mp4`.
- Per-video frame and ID-level annotations: `annotations/class_{1..7}_status_annotations.json`.
- Privacy-aware derived annotation package: `derived_release/`.

Release channel: GitHub Release / institutional repository / on-request academic distribution. The exact distribution URL will be added to the README and to the manuscript data availability statement once the release is published.

## 3. License: research and non-commercial use only

The seven classroom videos and all visual derivatives (frames, ROI crops, annotated overlays) are released under a **research-only, non-commercial license**. By downloading or using the dataset, users agree to the following terms.

Permitted uses:

- Academic research, including reproducing the experiments reported in the manuscript.
- Method development, ablation studies, and benchmarking against the reported metrics.
- Inclusion of small, well-justified visual examples in academic papers, theses, or technical reports, subject to the privacy rules in Section 5.
- **Use of manuscript Figures 1, 2, and 14**: these figures are derived visual outputs from the seven self-collected evaluation videos released under this license. Any reproduction must comply with the privacy obligations in Section 5 and acknowledge the source as specified below.

Prohibited uses:

- Any form of commercial use, including but not limited to product development, paid services, advertising, sale or sublicensing of the videos or their derivatives.
- Redistribution of the raw videos outside the official release channel without written permission from the dataset maintainers.
- Any use that attempts to **re-identify** individual students, teachers or other persons appearing in the videos.
- Surveillance, profiling, scoring, ranking, evaluation of teaching quality, or any punitive decision-making about specific individuals or classes.
- Training or evaluating face-recognition, biometric-identification, emotion-scoring, or similar identity- or affect-inference systems.
- Use as input to large-scale generative-model training or distribution as part of unrestricted public datasets.

This license is intended to be compatible with, but more restrictive than, common research licenses such as CC BY-NC 4.0. Where this document and any other license file disagree, the stricter restriction applies.

## 4. Consent and ethical statement

The seven videos were recorded in real classroom sessions for the purpose of educational research on classroom attention analysis. Recording was carried out with the knowledge of the participating instructors and with consent obtained under the local institutional norms applicable at the time of recording. Videos were collected with no audio analysis, no biometric enrollment, and no individual scoring of students.

The release described in this document is limited to the original research purpose. Anyone wishing to use the dataset for purposes not foreseen by the original consent must independently assess the legal and ethical basis of that use under their own jurisdiction and institutional policies.

If at any point a participant or institution requests withdrawal of specific footage, the maintainers will remove the affected files from the public release within a reasonable period and will not redistribute them further.

## 5. Privacy obligations for downstream users

When using the released videos, users must:

- Treat the videos as **sensitive research data**: store them on access-controlled systems, do not upload them to public web folders, and do not embed them in publicly indexable web pages.
- Not perform face recognition, identity matching, lip reading, or any attempt to link individuals across videos or to external identity databases.
- Not publish full-frame images that allow casual viewers to identify specific students. When figures are required in publications, prefer cropped, blurred, mosaicked, or otherwise anonymised views, or use the privacy-aware visual examples already provided in the manuscript and supplementary material.
- Comply with all applicable local data-protection regulations (for example, but not limited to, GDPR, PIPL, or local equivalents) as well as their own institutional review board / ethics committee requirements.

## 6. No warranty

The dataset is provided **as is**, without warranty of any kind, express or implied, including but not limited to warranties of fitness for a particular purpose, accuracy of annotations, or non-infringement. The maintainers accept no liability for damages arising from the use of the dataset.

## 7. How to cite

If you use the released videos, the per-video annotations, the derived annotation package, or the manuscript figures (Figures 1, 2, and 14) derived from the videos, please cite the manuscript and the dataset release. Recommended citation:

```text
[Authors]. Interpretable classroom distraction estimation via tracking-to-analysis continuity. [Journal/Preprint information]. [Year].
Classroom Evaluation Video Dataset (class_1..class_7). Released for research and non-commercial use only. [Release URL]. [Year].
```

When reproducing manuscript Figures 1, 2, or 14, please also state in your paper:
> "Figures 1, 2, and/or 14 were reproduced from Jia et al. (Year), under the research-only non-commercial license specified in the DATASET_LICENSE.md of https://github.com/fangsheng223/classroom-distraction-tracker."

Please also indicate, in your paper or report, which of the following you actually used:

- the seven raw videos;
- only the per-video JSON annotations in `annotations/`;
- only the privacy-aware `derived_release/` package.

## 8. Contact and access

Access requests, withdrawal requests, license clarifications, or reports of misuse should be directed to the corresponding author of the manuscript using the contact information given in the paper. The public release is **finalised** at the Zenodo Concept DOI **10.5281/zenodo.21206958** (<https://zenodo.org/records/21206958>) under the terms in §1. The latest version is **v2** (DOI **10.5281/zenodo.21207208**, <https://zenodo.org/records/21207208>, 129.8 MB) and mirrors the seven `class_*.mp4` raw evaluation videos together with `derived_release.zip` and `submission_assets.zip`. The earlier v1 record (10.5281/zenodo.21206959, 3.9 MB, no raw videos) is preserved as a historical snapshot. A short written access form (institution, proposed use, agreement to §1 terms) is sufficient for access requests — see the Zenodo record's "Access conditions" panel for the request email.
