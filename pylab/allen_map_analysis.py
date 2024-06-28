import numpy as np
import tifffile
import os
from skimage import filters, measure, exposure
import matplotlib.pyplot as plt
from allensdk.core.reference_space_cache import ReferenceSpaceCache
from allensdk.core.mouse_connectivity_cache import MouseConnectivityCache

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

# Function to download Allen Brain Atlas annotation
def download_allen_brain_atlas_annotation():
    manifest_path = 'manifest.json'
    resolution = 10  # in microns
    reference_space_key = 'annotation/ccf_2022'  # The key for the annotation volume
    rspc = ReferenceSpaceCache(reference_space_key=reference_space_key, resolution=resolution, manifest=manifest_path)
    annotation, _ = rspc.get_annotation_volume()
    return annotation

# Function to segment images using the Allen Brain Atlas annotation
def segment_using_allen_brain_atlas(images, annotation):
    # Resize the annotation to match the image dimensions if needed
    annotation_resized = resize_annotation(annotation, images.shape)

    # Apply the annotation to segment the image
    segmented_images = images * annotation_resized

    return segmented_images

# Function to resize the annotation to match image dimensions
def resize_annotation(annotation, target_shape):
    from skimage.transform import resize
    return resize(annotation, target_shape, preserve_range=True, anti_aliasing=True, order=0)

# Function to analyze images
def analyze_images(images, segmented_images):
    # Apply a Sobel filter for edge detection on the segmented images
    edges = filters.sobel(segmented_images)
    
    # Threshold the image
    threshold_value = filters.threshold_otsu(segmented_images)
    binary_image = segmented_images > threshold_value
    
    # Label the image
    labeled_image = measure.label(binary_image)
    
    # Perform regionprops analysis
    regions = measure.regionprops(labeled_image, intensity_image=segmented_images)
    
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
    filepath = r'D:\Mapping\Animals\sb02\first_test\25-Apr-2024_1\Frames_1_512_512_uint16_0003.tif'
    
    # Load the images
    images = load_tiff_stack(filepath)
    
    # Preprocess the images
    images_preprocessed = preprocess_images(images)
    
    # Download Allen Brain Atlas annotation
    annotation = download_allen_brain_atlas_annotation()
    
    # Segment images using the Allen Brain Atlas annotation
    segmented_images = segment_using_allen_brain_atlas(images_preprocessed, annotation)
    
    # Analyze the images
    edges, labeled_image, regions = analyze_images(images_preprocessed, segmented_images)
    
    # Display the results
    display_results(images_preprocessed, edges, labeled_image, regions)

if __name__ == "__main__":
    main()
