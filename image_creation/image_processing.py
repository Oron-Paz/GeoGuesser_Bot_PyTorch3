import os
from PIL import Image

def delete_small_images(directory, size_threshold_kb):
    standard_image_types = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}  # Add more image extensions as needed

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        if os.path.isfile(filepath):
            try:
                # Check if the file is an SVG or a standard image type
                file_extension = os.path.splitext(filepath)[1].lower()

                if file_extension == '.svg':
                    print(f"Deleting {filename} - SVG file")
                    os.remove(filepath)
                elif file_extension in standard_image_types:
                    # Open the image and get its size
                    img = Image.open(filepath)
                    file_size_kb = os.path.getsize(filepath) / 1024  # Convert bytes to kilobytes

                    # Check if the image size is below the threshold
                    if file_size_kb < size_threshold_kb:
                        print(f"Deleting {filename} - Size: {file_size_kb:.2f} KB")
                        os.remove(filepath)
                    else:
                        print(f"Keeping {filename} - Size: {file_size_kb:.2f} KB")
                else:
                    print(f"Keeping {filename} - Unknown file type")

            except Exception as e:
                print(f"Error processing {filename}: {e}")

# Example usage: Delete images under 10KB in the 'south America' folder, keeping only standard image types
delete_small_images('data/South_America_images', 10)
