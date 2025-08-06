"""
    coding: utf-8
    Project: bfa
    File: model.py
    Author: xieyu
    Date: 2025/8/2 14:24
    IDE: PyCharm
"""

import torch
import torch.nn as nn

class Simple3DCNN(nn.Module):
    def __init__(self, in_channels=45, out_channels=21):
        super(Simple3DCNN, self).__init__()
        self.encoder = nn.Sequential(
            nn.Conv3d(in_channels, 64, kernel_size=3, padding=1),
            nn.BatchNorm3d(64),
            nn.ReLU(inplace=True),

            nn.Conv3d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm3d(128),
            nn.ReLU(inplace=True),

            nn.Conv3d(128, 64, kernel_size=3, padding=1),
            nn.BatchNorm3d(64),
            nn.ReLU(inplace=True)
        )

        self.decoder = nn.Sequential(
            nn.Conv3d(64, out_channels, kernel_size=1)  # final output
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x

