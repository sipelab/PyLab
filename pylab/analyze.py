import numpy as np
import tifffile
import os
from skimage import filters, measure, io, morphology, exposure
import matplotlib.pyplot as plt

# Function to load TIFF stack
def load_tiff_stack(filepath):
    with tifffile.TiffFile(filepath) as tif:
        images = tif.asarray()
    return images

# Function to preprocess images
def preprocess_images(images):
    # Apply histogram equalization
    images_eq = exposure.equalize_hist(images)
    return images_eq

# Function to analyze images
def analyze_images(images):
    # Apply a Sobel filter for edge detection
    edges = filters.sobel(images)
    
    # Threshold the image
    threshold_value = filters.threshold_otsu(images)
    binary_image = images > threshold_value
    
    # Label the image
    labeled_image = measure.label(binary_image)
    
    # Perform regionprops analysis
    regions = measure.regionprops(labeled_image, intensity_image=images)
    
    return edges, labeled_image, regions

# Function to display results
def display_results(images, edges, labeled_image, regions):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    ax = axes.ravel()
    
    ax[0].imshow(images[0], cmap='gray')
    ax[0].set_title('Original Image')
    
    ax[1].imshow(edges[0], cmap='gray')
    ax[1].set_title('Edges')
    
    ax[2].imshow(labeled_image[0], cmap='nipy_spectral')
    ax[2].set_title('Labeled Image')
    
    plt.tight_layout()
    plt.show()
    
    print(f"Number of regions: {len(regions)}")
    for region in regions:
        print(f"Region: {region.label}, Area: {region.area}, Mean Intensity: {region.mean_intensity}")

# Main analysis function
def main():
    # Path to the TIFF stack
    filepath = r'C:\dev\sipefield\devOutput\sub-002\ses-01\anat\sub-002_ses-01_T1w_20240628_000316.tiff'
    
    # Load the images
    images = load_tiff_stack(filepath)
    
    # Preprocess the images
    images_preprocessed = preprocess_images(images)
    
    # Analyze the images
    edges, labeled_image, regions = analyze_images(images_preprocessed)
    
    # Display the results
    display_results(images_preprocessed, edges, labeled_image, regions)

if __name__ == "__main__":
    main()
