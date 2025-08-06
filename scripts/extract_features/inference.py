"""
    coding: utf-8
    Project: bfa
    File: inference.py
    Author: xieyu
    Date: 2025/8/3 15:30
    IDE: PyCharm
"""
import sys

import torch
import numpy as np
from torch import nn
import json


class MLP(nn.Module):
    def __init__(self, input_dim=1440, hidden_dim=128):
        super().__init__()
        self.backbone = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU()
        )
        self.sex_head = nn.Linear(hidden_dim, 2)
        self.group_head = nn.Linear(hidden_dim, 2)
        self.age_head = nn.Linear(hidden_dim, 1)

    def forward(self, x):
        x = self.backbone(x)
        sex = self.sex_head(x)
        group = self.group_head(x)
        age = self.age_head(x).squeeze(1)
        return sex, group, age

    def inference(self, x):
        x = self.backbone(x)
        return x


def write_features_2_json(feature_pred, out_path):
    feature_pred = list(feature_pred)

    with open(out_path, 'w') as f:
        json.dump(feature_pred, f, indent=4)
    pass


def predict(feature_path, model_path='../models/extract_features/best_model.pth', device='cpu'):
    # 加载数据
    feature = np.load(feature_path).astype(np.float32)

    mean = feature.mean(axis=1, keepdims=True)
    std = feature.std(axis=1, keepdims=True)
    std[std == 0] = 1
    feature = (feature - mean) / std

    feature = feature.reshape(-1)

    x = torch.tensor(feature).unsqueeze(0).to(device)  # shape: (1, 1440)

    # 加载模型
    model = MLP()
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()

    with torch.no_grad():
        feature_pred = model.inference(x).squeeze().numpy()

    return feature_pred

if __name__ == '__main__':
    feature_file = sys.argv[1]
    output_file = sys.argv[2]
    feature_pred = predict(feature_file)
    write_features_2_json(feature_pred, output_file)
