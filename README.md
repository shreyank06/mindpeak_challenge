# mindpeak_challenge

conda activate histogpt_env

To do
```
check whether different texts are generated for different svs files
```
```
change the code for multiple svs files
```
packages needed
```
pip3.10 install openslide-python
```
```
pip3.10 install opencv-python
```
```
sudo pip3.10 install transformers==4.38.2
```
install dagster
```
pip install dagster dagit
```
run pipeline
```
dagit -f dagster_pipeline.py
```
start the enviornment
```
conda env create -f environment.yml
```

after installing the model weights change the model_names from 
```
histogpt-1b-6k-pruned.pth?download=true
```
to 
```
histogpt-1b-6k-pruned.pth
```
and 
```
ctranspath.pth?download=true
```
to 
```
ctranspath.pth?
```
