import os
import numpy as np
from PIL import Image

def normalize_and_save(slice, filename, target_dir, slice_index, category):
    """
    Normalize the slice data to 0-255 for image conversion and save as PNG.
    Filename reflects original and new format with '.npy.png' extension.
    """
    slice_normalized = ((slice - slice.min()) / (slice.max() - slice.min()) * 255).astype(np.uint8)
    img = Image.fromarray(slice_normalized)
    # Append '.npy.png' to each filename to indicate original and converted formats
    output_filename = f"{filename[:-4]}_slice{slice_index}_{category}.png.png"
    img.save(os.path.join(target_dir, output_filename))

def convert_npy_to_png(source_dir, target_dir, categories):
    """
    Convert .npy files in the source directory to .png images in the target directory,
    appending '.npy.png' to filenames to include original and converted formats.
    """
    for filename in os.listdir(source_dir):
        if filename.endswith('.npy'):
            file_path = os.path.join(source_dir, filename)
            volume = np.load(file_path)
            num_slices = volume.shape[2]
            num_categories = volume.shape[3]

            for i in range(num_slices):
                for j in range(num_categories):
                    slice = volume[:, :, i, j]
                    category_name = categories[j]  # Use predefined category names
                    normalize_and_save(slice, filename, target_dir, i, category_name)


# Define the source and target directories
images_dir = 'C:/Users/ADHI/Desktop/MAJOR PROJECT/BraTS2020_TrainingData/input_data_128/val/images'
predictions_dir = 'C:/Users/ADHI/Desktop/MAJOR PROJECT/BraTS2020_TrainingData/input_data_128/val/predictions'
target_images_dir = 'C:/Users/ADHI/Desktop/MAJOR PROJECT/BraTS2020_TrainingData/converted npy to png/images_png'
target_predictions_dir = 'C:/Users/ADHI/Desktop/MAJOR PROJECT/BraTS2020_TrainingData/converted npy to png/predictions_png'

# Category names for tumor types (masks) and modalities (images)
mask_categories = ['Background', 'Swelling', 'Non-Enhanced Tumor', 'Enhanced Tumor']
image_modalities = ['T2', 'T1ce', 'Flair']

# Convert both images and masks with meaningful category names and ensure file naming consistency
convert_npy_to_png(images_dir, target_images_dir, image_modalities)
convert_npy_to_png(predictions_dir, target_predictions_dir, mask_categories)
