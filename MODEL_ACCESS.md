# Model Access

## Summary

This document lists the model weights referenced by the repository for the manuscript **Interpretable classroom distraction estimation via tracking-to-analysis continuity** and explains whether they are already included, optional, or need to be obtained separately.

## Included in the repository

### Core PyTorch / ONNX models

- `models/lightweight_cnn.pth`
- `models/status_cnn.pth`
- `models/lightweight_cnn.onnx`
- `yolov8n.pt`
- `yolov8s.pt`
- `yolov8n.onnx`
- `model/yolov8n_behavior.pt`

### Legacy / auxiliary weights present in local release tree

- `model/pose_classifier.h5`
- `model/best_pose_model.h5`
- `model/triple_behavior_classifier.h5`
- `runs/behavior_detect/train_gpu/weights/best.pt`

## Configuration references

The default config and scripts may reference files such as:

- `config.yaml`
- `model/pose_classifier.h5`
- `runs/behavior_detect/train_gpu/weights/best.pt`
- `yolov8s.pt`

Before running experiments, confirm that the referenced weight paths exist in your checkout or update the config accordingly.

## If some weights are not shipped in a public mirror

For lightweight public mirrors, large or license-sensitive weights may be removed. In that case:

1. Place the required weights back into the paths expected by the config.
2. Or update `config.yaml` / command line arguments to point to your local copies.
3. For YOLO base weights, Ultralytics may also auto-download compatible public checkpoints if available.

## Minimal inference-ready weight set

For a basic end-to-end demo, the following are sufficient:

- one YOLO person detector checkpoint, such as `yolov8s.pt`
- one classification/state model, such as `models/lightweight_cnn.pth`
- `config.yaml`

## Notes on framework requirements

- `.pt` / `.pth` weights require PyTorch.
- `.onnx` weights require an ONNX-compatible runtime if you use ONNX inference.
- `.h5` weights may require TensorFlow / Keras depending on the script or legacy pipeline you run.
