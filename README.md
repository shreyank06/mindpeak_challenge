# MindPeak Challenge

This repository contains the code and pipeline for the MindPeak challenge. Follow the steps below to set up the environment, install dependencies, and run the pipeline.

## Setup Instructions

1. **Activate the Conda Environment**  
```
   conda activate histogpt_env
```

2. **Create the Environment (if not already created)**
```
conda env create -f environment.yml
```
3. **Install Required Packages**
```
pip3.10 install openslide-python opencv-python transformers==4.38.2
pip install dagster dagit
```

4. **Run the Pipeline**
```
dagit -f dagster_pipeline.py
```

5. **Model Configuration**
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
```
```
ctranspath.pth
```
