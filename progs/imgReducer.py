from PIL import Image
import os

def reduce_image_size(input_image_path, output_image_path, target_size_mb):
    # Open the image
    image = Image.open(input_image_path)
    image.
    # Get original image size
    original_size_bytes = os.path.getsize(input_image_path)
    original_size_mb = original_size_bytes / (1024 * 1024)

    # Check if image size is already smaller than target size
    if original_size_mb <= target_size_mb:
        print("Image size is already smaller than target size.")
        return

    # Calculate the compression quality factor needed to achieve target size
    target_size_bytes = target_size_mb * 1024 * 1024
    compression_quality = int(100 - (target_size_bytes / original_size_bytes * 100))

    # Compress the image with adjusted quality
    image.save("C:/User/DELL/Documents/Projects/ThunderDocs/files/resized_image/",format='JPEG', quality=compression_quality)

    # Get new image size
    new_size_bytes = os.path.getsize(output_image_path)
    new_size_mb = new_size_bytes / (1024 * 1024)

    print(f"Image successfully resized. Original size: {original_size_mb:.2f} MB, New size: {new_size_mb:.2f} MB.")

# Example usage
input_image_path = "C:/Users/DELL/Documents/Projects/ThunderDocs/files/0c6fef42-fb3c-11ee-96c4-1065305bec91WhatsApp Image 2024-03-31 at 15.31.39_40575c40.jpg"
output_image_path = "C:/Users/DELL/Documents/Projects/ThunderDocs/files/resized_image/"
target_size_mb = 0.5  # Target size in megabytes

reduce_image_size(input_image_path, output_image_path, target_size_mb)
