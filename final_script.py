import os
import h5py
import torch
from transformers import BioGptTokenizer, BioGptConfig
from histogpt.models import HistoGPTForCausalLM, PerceiverResamplerConfig
from histogpt.helpers.inference import generate
from openslide import OpenSlide
from PIL import Image
import textwrap
import matplotlib.pyplot as plt

# Define device: Use GPU if available, otherwise fallback to CPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 1. Configure HistoGPT and load weights
print("Initializing HistoGPT model...")
histogpt = HistoGPTForCausalLM(BioGptConfig(), PerceiverResamplerConfig()).to(device)
weights_path = './histogpt-1b-6k-pruned.pth'
state_dict = torch.load(weights_path, map_location=device)
histogpt.load_state_dict(state_dict, strict=True)
print("HistoGPT model loaded successfully.")

# 2. Initialize tokenizer
tokenizer = BioGptTokenizer.from_pretrained("microsoft/biogpt")

# Define text prompt
prompt_text = 'Final diagnosis:'
prompt = torch.tensor(tokenizer.encode(prompt_text)).unsqueeze(0).to(device)

# 3. Process HDF5 files
h5_folder = './save_folder/h5_files/256px_ctranspath_0.0mpp_4.0xdown_normal'
features_list = []

print(f"Processing HDF5 files from: {h5_folder}...")
h5_files = [f for f in os.listdir(h5_folder) if f.endswith('.h5')]
for file_name in h5_files:
    file_path = os.path.join(h5_folder, file_name)
    with h5py.File(file_path, 'r') as f:
        features = f['feats'][:]  # Read the 'feats' dataset
        features_tensor = torch.tensor(features).unsqueeze(0).to(device)
        features_list.append((file_name, features_tensor))
        print(f"Processed features from: {file_name}")

# 4. Process SVS files and generate unique decoded text for each
slide_folder = './slide_folder'
output_folder = './output'
os.makedirs(output_folder, exist_ok=True)

print(f"Processing SVS files from: {slide_folder}...")
svs_files = [f for f in os.listdir(slide_folder) if f.endswith('.svs')]

for i, svs_file in enumerate(svs_files):
    base_name = os.path.splitext(svs_file)[0]
    output_file_path = os.path.join(output_folder, f"{base_name}.txt")
    thumbnail_file_path = os.path.join(output_folder, f"{base_name}_thumbnail.png")

    # Skip processing if both the text and thumbnail already exist
    if os.path.exists(output_file_path) and os.path.exists(thumbnail_file_path):
        print(f"Output already exists for {svs_file}. Skipping.")
        continue

    # Process the SVS file and display thumbnail
    slide_path = os.path.join(slide_folder, svs_file)
    print(f"Processing slide: {svs_file}")

    slide = OpenSlide(slide_path)
    level = slide.get_best_level_for_downsample(32)
    downsampled_dimensions = slide.level_dimensions[level]

    thumbnail = slide.read_region((0, 0), level, downsampled_dimensions).convert("RGB")

    # Select features dynamically (e.g., based on a mapping or index)
    if i < len(features_list):  # Ensure we don't exceed the features list
        _, corresponding_features = features_list[i]
    else:
        print(f"Warning: Not enough features for {svs_file}. Skipping.")
        continue

    # Generate text for the specific `.svs` file
    output = generate(
        model=histogpt,
        prompt=prompt,
        image=corresponding_features,
        length=64,
        top_k=10,
        top_p=0.8,
        temp=0.7,
        device=device
    )
    decoded_text = tokenizer.decode(output[0, 1:], skip_special_tokens=True)

    # Save the decoded text to a .txt file
    with open(output_file_path, 'w') as f:
        f.write(decoded_text)
    print(f"Decoded text saved to: {output_file_path}")

    # Save the thumbnail image to the folder
    thumbnail.save(thumbnail_file_path)
    print(f"Thumbnail image saved to: {thumbnail_file_path}")

    print("Decoded Text:", decoded_text)
    print(textwrap.fill(decoded_text, width=64))
