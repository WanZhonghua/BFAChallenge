"""
    coding: utf-8
    Project: bfa
    File: get_pred_metrics.py
    Author: xieyu
    Date: 2025/8/3 15:40
    IDE: PyCharm
"""
import os
import sys

import numpy as np

from utils import get_bundle_names
import nibabel as nib


def main(base_dir):

    bundle_names = get_bundle_names()

    metrics_path = os.path.join(base_dir, 'metrics_pred.nii.gz')

    seg_base_path = os.path.join(base_dir, "bundle_segmentations")

    out_path = os.path.join(base_dir, "features_pred.npy")

    segs = []
    segs_num = []
    for bundle_name in bundle_names:
        cur_seg_path = os.path.join(seg_base_path, f"{bundle_name}.nii.gz")
        cur_seg = nib.load(cur_seg_path).get_fdata().astype(int)
        segs.append(cur_seg)
        segs_num.append(np.count_nonzero(cur_seg))
        if segs_num[-1] == 0:
            segs_num[-1] = 1

    result = np.zeros((20, len(bundle_names)))

    cur_metrics = nib.load(metrics_path).get_fdata()

    for i in range(20):
        cur_metric = cur_metrics[..., i]
        for j in range(len(bundle_names)):
            cur_item = np.sum(cur_metric * segs[j]) / segs_num[j]
            result[i, j] = cur_item

    np.save(out_path, result)


if __name__ == '__main__':

    base_dir = sys.argv[1]

    main(base_dir)
