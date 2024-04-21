from PIL import Image
import os
class ImageSizeReducer:
    def __init__(self):
        print("hello")
    def compress_image(input_image_path, output_image_path, target_size_kb, quality=85):
        # Open the image
        img = Image.open(input_image_path)
        
        while True:
            # Save the image with the given quality
            img.save(output_image_path, optimize=True, quality=quality)
            
            if os.path.getsize(output_image_path) <= target_size_kb * 1024:
                break

            quality -= 5
            if quality < 10:
                raise Exception("Cannot compress the image enough to reach the target size.")
        
        return output_image_path

    input_path = "C:/Users/DELL/Downloads/wp3210970-wallpaper-240x320-spiderman.jpg"
    output_path = "C:/Users/DELL/Pictures/saved Pictures/compressed_img.jpg"
    target_size = 700  # Target size in KB

    compressed_image_path = compress_image(input_path, output_path, target_size)
    print(f"Compressed image saved at: {compressed_image_path}")
