#!/bin/bash
# Read dwi from inputs/ and write metric to outputs/
# Metric is read from environment variable METRIC

set -e

echo "Running BeyondFA baseline..."
echo "Listing /input..."
ls /input
echo "Listing /input/*..."
ls /input/*
echo "Listing /output..."
ls /output/

# Define metric
metric="fa"

# Find all dwi.mha files in /input
dwi_mha_files=$(find /input/images/dwi-4d-brain-mri -name "*.mha")

for dwi_mha_file in $dwi_mha_files; do
    # Set up file names
    json_file="/input/dwi-4d-acquisition-metadata.json"

    basename=$(basename $dwi_mha_file .mha)
    bval_path="/tmp/${basename}.bval"
    bvec_path="/tmp/${basename}.bvec"
    nifti_file="/tmp/${basename}.nii.gz"
    output_name="/output/features-128.json"

    # Convert dwi.mha to nii.gz
    echo "Converting $dwi_mha_file to $nifti_file..."
    python convert_mha_to_nifti.py $dwi_mha_file $nifti_file

    # Convert json to bval and bvec
    echo "Converting $json_file to $bval_path and $bvec_path..."
    python convert_json_to_bvalbvec.py $json_file $bval_path $bvec_path

    # Define output directory
    output_dir="/tmp/output"
    mkdir -p $output_dir

    # Create mask, response, FODs, and peaks
    tractseg_dir="${output_dir}/${basename}/tractseg"
    mkdir -p $tractseg_dir

    echo "Creating mask, response, FODs, and peaks..."
    dwi2mask $nifti_file $tractseg_dir/nodif_brain_mask.nii.gz -fslgrad $bvec_path $bval_path
    dwi2response dhollander $nifti_file $tractseg_dir/RF_WM.txt $tractseg_dir/RF_GM.txt $tractseg_dir/RF_CSF.txt -fslgrad $bvec_path $bval_path
    dwi2fod msmt_csd $nifti_file $tractseg_dir/RF_WM.txt $tractseg_dir/WM_FODs.nii.gz $tractseg_dir/RF_GM.txt $tractseg_dir/GM.mif $tractseg_dir/RF_CSF.txt $tractseg_dir/CSF.mif -mask $tractseg_dir/nodif_brain_mask.nii.gz
    sh2peaks $tractseg_dir/WM_FODs.nii.gz $tractseg_dir/peaks.nii.gz -mask $tractseg_dir/nodif_brain_mask.nii.gz

    echo "Running TractSeg..."
    TractSeg -i $tractseg_dir/peaks.nii.gz -o $tractseg_dir

    echo "Predicting 20 types of metrics"
    python ./pre_metrics/inference.py $tractseg_dir/WM_FODs.nii.gz $tractseg_dir/metrics_pred.nii.gz

    echo "Generating featuers_pred.npy"
    python get_pre_metrics.py $tractseg_dir

    echo "transforming featuers_pred to feature-128"
    python ./extract_features/inference.py $tractseg_dir/features_pred.npy $output_name

#    # Run FA calculation
#    fa_dir="${output_dir}/${basename}/metric"
#    mkdir -p $fa_dir
#    echo "Calculating DTI metrics..."
#    scil_dti_metrics.py --not_all --mask $tractseg_dir/nodif_brain_mask.nii.gz \
#        --fa $fa_dir/fa.nii.gz $nifti_file $bval_path $bvec_path -f
#
#    # Get corresponding metrics
#    echo "Calculating average $metric metric in bundles..."
#    bundle_roi_dir="${tractseg_dir}/bundle_segmentations"
#    metric_dir=${fa_dir}
#
#    # Make json with json["fa"]["mean"] = mena of fa in bundle
#    roi_list=$(find $bundle_roi_dir -name "*.nii.gz" | sort)
#    for roi in $roi_list; do
#        bundle_name=$(basename $roi .nii.gz)
#        echo "Calculating $metric in $bundle_name..."
#
#        # Is sum of mask > 0?
#        mask_sum=$(fslstats $roi -V | awk '{print $1}')
#        if [ $mask_sum -eq 0 ]; then
#            echo "$bundle_name,0" >> ${output_dir}/tensor_metrics.json
#        else
#            mean_metric=$(fslstats $fa_dir/$metric.nii.gz -k $roi -m)
#            echo "$bundle_name,$mean_metric" >> ${output_dir}/tensor_metrics.json
#        fi
#    done
#    # scil_volume_stats_in_ROI.py --metrics_dir ${fa_dir} $roi_list > ${output_dir}/tensor_metrics.json
#
#    # Extract specified metric to JSON
#    echo "Extracting $metric metrics to $output_dir..."
#    python extract_metric.py ${output_dir}/tensor_metrics.json $output_dir/fa.json
#
#    # Save the final metric.json to output directory
#    echo "$metric metrics saved to $output_name!"
#    mv $output_dir/fa.json $output_name

done
