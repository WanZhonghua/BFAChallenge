"""
    coding: utf-8
    Project: bfa
    File: inference.py
    Author: xieyu
    Date: 2025/8/2 15:26
    IDE: PyCharm
"""

import os
import sys

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import numpy as np
import nibabel as nib

from model import Simple3DCNN
from tqdm import tqdm


def inference(model_path, FOD_path, out_path, save_nii=False):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    FOD = nib.load(FOD_path).get_fdata()

    input_tensor = torch.tensor(FOD, dtype=torch.float32)

    input_tensor = input_tensor.permute(3, 0, 1, 2).unsqueeze(0)

    model = Simple3DCNN()
    model.load_state_dict(torch.load(model_path, map_location=device))
    model = model.to(device)

    model.eval()

    with torch.no_grad():

        x = input_tensor.to(device)

        output = model(x)

        if save_nii:
            pred_np = output.squeeze().cpu().numpy()  # shape: (21, D, H, W)

            pred_nii = nib.Nifti1Image(pred_np.transpose(1, 2, 3, 0), affine=np.eye(4))  # (D,H,W,C)

            nib.save(pred_nii, out_path)


if __name__ == "__main__":
    model_path = "../models/fit_metrics/best_model.pth"

    FOD_path = sys.argv[1]
    out_path = sys.argv[2]

    inference(model_path, FOD_path, out_path, save_nii=True)
