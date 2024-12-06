# MindPeak Challenge

This repository contains the code and pipeline for the MindPeak challenge. Follow the steps below to set up the environment, install dependencies, and run the pipeline.

## Setup Instructions

<<<<<<< HEAD
Before proceeding, you will have to manually download the wsi_images and place it **wsi_images** folder which is inside **python_code** folder.

The model weights are not in this repo because it could not be transferred to git because of its large size.
=======
Before proceeding, you will have to manually download the wsi_images and place it **wsi_images** folder which is inside **python_code** folder
The **model weights** are not in this repo because it could not be transferred to git because of its large size.
>>>>>>> 52625821e2a26722e460a5ed85a8a5055ab8f89a


1. **Install Required Packages**
```
pip3.10 install openslide-python opencv-python transformers==4.38.2
pip install dagster dagit
```

2. **Run the Pipeline**
```
cd python_code
```
```
download model weights
```
```
dagit -f dagster_pipeline.py
```

3. **Model Configuration**
After downloading model weights, update the file names in the code:
Change
```
histogpt-1b-6k-pruned.pth?download=true
to
histogpt-1b-6k-pruned.pth
```
and 
```
ctranspath.pth?download=true
to
ctranspath.pth
```
