import os
import shutil
import yaml
from histogpt.helpers.patching import main, PatchingConfigs

# Load configuration from file
def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

# Resolve relative paths to absolute paths based on the config file location
def resolve_path(base_path, relative_path):
    return os.path.abspath(os.path.join(base_path, relative_path))

# Main function for embedding generation
def generate_embeddings(config_path):
    # Load the configuration
    config = load_config(config_path)
    
    # Get the directory of the configuration file
    config_directory = os.path.dirname(os.path.abspath(config_path))
    
    # Resolve the absolute path of the WSI images folder
    wsi_images_folder = resolve_path(config_directory, config['wsi_images_folder'])
    file_extension = config['file_extension']
    save_patches = config['save_patches']
    
    # Get current directory and ensure slide_folder and save_folder exist
    current_directory = os.path.dirname(os.path.abspath(__file__))
    slide_folder = os.path.join(current_directory, 'slide_folder')
    save_folder = os.path.join(current_directory, 'save_folder')
    os.makedirs(slide_folder, exist_ok=True)
    os.makedirs(save_folder, exist_ok=True)
    
    # Move files with specified extension from wsi_images_folder to slide_folder
    if not os.path.exists(wsi_images_folder):
        raise ValueError(f"WSI images folder does not exist: {wsi_images_folder}")
    
    for file_name in os.listdir(wsi_images_folder):
        if file_name.endswith(file_extension):
            source_path = os.path.join(wsi_images_folder, file_name)
            target_path = os.path.join(slide_folder, file_name)
            try:
                shutil.copy(source_path, target_path)
                print(f"Copied: {file_name}")
            except Exception as e:
                print(f"Error copying {file_name}: {e}")
    
    # Configure patching
    configs = PatchingConfigs()
    configs.slide_path = slide_folder               # Path to folder with .svs files
    configs.save_path = save_folder                 # Path to save output files
    configs.model_path = os.path.join(current_directory, 'ctranspath.pth')  # Model path
    configs.file_extension = file_extension
    configs.patch_size = 256                        # Size of each patch
    configs.white_thresh = [170, 185, 175]          # White threshold
    configs.edge_threshold = 2                      # Edge threshold
    configs.resolution_in_mpp = 0.0                 # Microns per pixel
    configs.downscaling_factor = 4.0                # Downscaling factor
    configs.batch_size = 16                         # Batch size
    configs.debug = save_patches                    # Save patches for debugging

    # Run the patching process
    main(configs)

if __name__ == "__main__":
    # Path to the configuration file
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.yaml")
    generate_embeddings(config_path)
