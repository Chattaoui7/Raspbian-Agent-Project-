import cv2
import os

# Define folders
input_folder = r'C:/Users/admin/Desktop/data/input'
output_folder = r'C:/Users/admin/Desktop/data/output'

# Make sure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Valid image extensions
valid_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff']

# Loop through all files in input folder
for filename in os.listdir(input_folder):
    file_ext = os.path.splitext(filename)[1].lower()
    
    if file_ext in valid_extensions:
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        # Read image
        image = cv2.imread(input_path)
        if image is None:
            print(f"⚠️ Could not read image: {filename}")
            continue

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply thermal colormap
        thermal = cv2.applyColorMap(gray, cv2.COLORMAP_JET)

        # Save thermal image
        cv2.imwrite(output_path, thermal)
        print(f"✅ Processed: {filename} → saved to output folder")
