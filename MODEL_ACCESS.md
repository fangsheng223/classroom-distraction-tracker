# Model Access

## Summary

This public repository does not ship large model weight files. To run local inference, place the required checkpoints in the expected paths or update the config to point to your local copies.

## Paths referenced by this repository

The default `config.yaml` references:

- `yolov8s.pt`
- `models/lightweight_cnn.pth`

Depending on how you run the code, the backend/API may also expect local runtime components and weights to be available alongside the repository checkout.

## What you need for local inference

For a minimal local setup, provide at least:

- one YOLO detector checkpoint such as `yolov8s.pt`
- one classifier/state checkpoint such as `models/lightweight_cnn.pth`
- the repository `config.yaml`

## How to use your own local copies

You can either:

1. place the weight files at the paths expected by `config.yaml`, or
2. edit `config.yaml` to point to your local checkpoint locations.

For supported public YOLO base checkpoints, Ultralytics may also download them automatically if your environment allows it.

## If you only need the supplementary materials

You do not need any model weights to inspect:

- `derived_release/`
- `submission_assets/`
- the documentation files in the repository root

## Framework notes

- `.pt` and `.pth` weights require PyTorch.
- Additional local runtime integration may be needed for full inference workflows, depending on your checkout.
