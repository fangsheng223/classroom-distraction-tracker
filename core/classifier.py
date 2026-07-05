"""
Lightweight CNN — Hard-Parameter Regression
============================================
Trainable parameters: 21,475  (<<< 500 K)
Input : 224 × 224 × 3  RGB ROI crop
Output: [nose_offset, head_down_angle, shoulder_diff]
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class LightweightCNNModel(nn.Module):
    """
    Depthwise-separable CNN for biomechanical hard-parameter regression.

    Architecture
    ------------
    Conv(3→16, 3×3) + BN + ReLU + MaxPool
    DSConv(16→32) + BN + ReLU + MaxPool
    DSConv(32→64) + BN + ReLU + MaxPool
    DSConv(64→128) + BN + ReLU + MaxPool
    GlobalAvgPool
    FC(128→64) + Dropout(0.2)
    FC(64→3)   + per-output range constraint
    """

    def __init__(self):
        super().__init__()

        # Stage 1 — standard conv
        self.conv1 = nn.Conv2d(3, 16, 3, padding=1)   # 432 params
        self.bn1   = nn.BatchNorm2d(16)

        # Stage 2 — depthwise-separable
        self.dw2 = nn.Conv2d(16, 16, 3, padding=1, groups=16)   # 144
        self.pw2 = nn.Conv2d(16, 32, 1)                          # 512
        self.bn2 = nn.BatchNorm2d(32)

        # Stage 3
        self.dw3 = nn.Conv2d(32, 32, 3, padding=1, groups=32)   # 288
        self.pw3 = nn.Conv2d(32, 64, 1)                          # 2048
        self.bn3 = nn.BatchNorm2d(64)

        # Stage 4
        self.dw4 = nn.Conv2d(64, 64, 3, padding=1, groups=64)   # 576
        self.pw4 = nn.Conv2d(64, 128, 1)                         # 8192
        self.bn4 = nn.BatchNorm2d(128)

        self.pool = nn.AdaptiveAvgPool2d(1)

        self.fc1     = nn.Linear(128, 64)    # 8192
        self.dropout = nn.Dropout(0.2)
        self.fc2     = nn.Linear(64, 3)      # 192

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Parameters
        ----------
        x : (B, 3, 224, 224)

        Returns
        -------
        params : (B, 3)
            [nose_offset ∈ [0,50],
             head_down_angle ∈ [-30,60],
             shoulder_diff ∈ [0,40]]
        """
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.max_pool2d(x, 2)                          # → 112

        x = F.relu(self.dw2(x))
        x = F.relu(self.bn2(self.pw2(x)))
        x = F.max_pool2d(x, 2)                          # → 56

        x = F.relu(self.dw3(x))
        x = F.relu(self.bn3(self.pw3(x)))
        x = F.max_pool2d(x, 2)                          # → 28

        x = F.relu(self.dw4(x))
        x = F.relu(self.bn4(self.pw4(x)))
        x = F.max_pool2d(x, 2)                          # → 14

        x = self.pool(x).flatten(1)                      # → (B,128)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)

        return torch.stack([
            torch.sigmoid(x[:, 0]) * 50,           # nose_offset  [0, 50]
            torch.tanh(x[:, 1]) * 45 + 15,         # head_angle   [-30, 60]
            torch.sigmoid(x[:, 2]) * 40,           # shoulder_diff[0, 40]
        ], dim=1)

    def count_parameters(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


def load_model(weights_path: str, device: str = "cpu") -> LightweightCNNModel:
    """Load a trained model checkpoint."""
    model = LightweightCNNModel().to(device)
    ckpt  = torch.load(weights_path, map_location=device)
    model.load_state_dict(ckpt["model_state_dict"])
    model.eval()
    return model


def classify_hard_params(
    params: torch.Tensor,
    nose_threshold: float = 20.0,
    head_threshold: float = 30.0,
    shoulder_threshold: float = 25.0,
) -> list:
    """
    Rule-based state classification from hard parameters.

    Returns list of str: 'Focused' | 'Distracted'
    """
    results = []
    for p in params:
        nose, head, shoulder = p[0].item(), p[1].item(), p[2].item()
        if nose > nose_threshold or head > head_threshold or shoulder > shoulder_threshold:
            results.append("Distracted")
        else:
            results.append("Focused")
    return results
