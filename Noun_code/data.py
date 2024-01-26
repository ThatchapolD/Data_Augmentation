import os
import cv2
import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split

class_list = ["5gen11front", "5gen11back", "10gen11front", "10gen11back", "20gen11front", "20gen11back", "100gen11front",
              "100gen11back", "500gen11front", "500gen11back", "10gen12front", "10gen12back", "20gen12front", "20gen12back",
              "100gen12front", "100gen12back", "50gen13front", "50gen13back", "500gen13front", "500gen13back", "100gen14front",
              "100gen14back", "500gen14front", "500gen14back", "1000gen14front", "1000gen14back", "20gen15front", "20gen15back",
              "50gen15front", "50gen15back", "100gen15front", "100gen15back", "500gen15front", "500gen15back", "1000gen15front",
              "1000gen15back", "20gen16front", "20gen16back", "50gen16front", "50gen16back", "100gen16front", "100gen16back",
              "500gen16front", "500gen16back", "1000gen16front", "1000gen16back", "20gen17front", "20gen17back", "50gen17front",
              "50gen17back", "100gen17front", "100gen17back", "500gen17front", "500gen17back", "1000gen17front", "1000gen17back",
              "memo_2530front", "memo_2530back", "memo_2535back", "memo_2539_50front", "memo_2539_50back", "memo_2547front",
              "memo_2547back", "memo_2549front", "memo_2549back", "memo_2550front", "memo_2550back", "memo_2553back",
              "memo_2554front", "memo_2554back", "memo_2555_80front", "memo_2555_80back", "memo_2555_100back", "memo_2558back",
              "memo_2559_70front", "memo_2559_70back", "memo_2559_500back", "memo_2562_100front", "memo_2562_100back",
              "memo_2562_1000front", "memo_2562_1000back"]

def rotate_image(image, angle):
    # Convert the OpenCV image (BGR) to PIL (RGB)
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Rotate the PIL image
    rotated_pil_image = pil_image.rotate(angle, resample=Image.BICUBIC, expand=True)

    # Convert the PIL image back to OpenCV format (BGR)
    rotated_image = cv2.cvtColor(np.array(rotated_pil_image), cv2.COLOR_RGB2BGR)

    return rotated_image

def process_image(input_path, rotations, target_width):
    # Read the input image
    image = cv2.imread(input_path)

    # Get image dimensions
    rows, cols = image.shape[:2]

    # Define the bounding box based on image dimensions
    bbox = [0, 0, cols, rows]

    # Crop the region defined by the bounding box
    cropped_image = image[bbox[1]:bbox[3], bbox[0]:bbox[2]]

    # Perform rotations
    rotated_images = []
    for angle in rotations:
        rotated_image = rotate_image(cropped_image, angle)
        rotated_images.append(rotated_image)

    # Calculate the scaling factor based on the target width
    scale_factors = [target_width / max(rotated_image.shape[1], rotated_image.shape[0]) for rotated_image in rotated_images]

    # Perform scaling
    scaled_images = []
    for rotated_image, scale_factor in zip(rotated_images, scale_factors):
        width = int(rotated_image.shape[1] * scale_factor)
        height = int(rotated_image.shape[0] * scale_factor)
        dim = (width, height)
        scaled_image = cv2.resize(rotated_image, dim, interpolation=cv2.INTER_AREA)
        scaled_images.append(scaled_image)

    return scaled_images

def draw_bounding_box(image, bbox_position):
    # Extract bbox coordinates
    top_left_x, top_left_y, bottom_right_x, bottom_right_y = bbox_position

    # Draw bounding box
    cv2.rectangle(image, (int(top_left_x * image.shape[1]), int(top_left_y * image.shape[0])),
                  (int(bottom_right_x * image.shape[1]), int(bottom_right_y * image.shape[0])), (0, 255, 0), 2)

    return image

def split_data(input_folder, output_folder, target_width=300, random_state=None):
    # Create output folder structure
    for folder in ['train', 'valid', 'test']:
        os.makedirs(os.path.join(output_folder, folder), exist_ok=True)

    for class_name in class_list:
        input_class_folder = os.path.join(input_folder, class_name)
        os.makedirs(input_class_folder, exist_ok=True)

        # Process images only if there are files in the class folder
        image_files = [f for f in os.listdir(input_class_folder) if f.endswith('.jpg')]
        if image_files:
            # Process images
            rotations = [90, 180, 270, 360]

            for input_image_file in image_files:
                input_image_path = os.path.join(input_class_folder, input_image_file)

                # Process the image
                processed_images = process_image(input_image_path, rotations, target_width)

                # Shuffle the processed images
                np.random.shuffle(processed_images)

                # Split the processed images into train, valid, and test sets
                train_images, test_valid_images = train_test_split(processed_images, test_size=0.1 + 0.2, random_state=random_state)
                valid_images, test_images = train_test_split(test_valid_images, test_size=0.1 / (0.1 + 0.2), random_state=random_state)

                # Save images to respective folders inside output_folder
                for i, image in enumerate(train_images):
                    output_filename = os.path.join(output_folder, 'train', f"{class_name}_image_{input_image_file}_rotated_{i}.jpg")
                    # Draw bounding box on the image
                    image_with_bbox = draw_bounding_box(image.copy(), [0, 0, 1, 1])  # Replace with actual bounding box coordinates
                    cv2.imwrite(output_filename, image_with_bbox)

                for i, image in enumerate(valid_images):
                    output_filename = os.path.join(output_folder, 'valid', f"{class_name}_image_{input_image_file}_rotated_{i}.jpg")
                    # Draw bounding box on the image
                    image_with_bbox = draw_bounding_box(image.copy(), [0, 0, 1, 1])  # Replace with actual bounding box coordinates
                    cv2.imwrite(output_filename, image_with_bbox)

                for i, image in enumerate(test_images):
                    output_filename = os.path.join(output_folder, 'test', f"{class_name}_image_{input_image_file}_rotated_{i}.jpg")
                    # Draw bounding box on the image
                    image_with_bbox = draw_bounding_box(image.copy(), [0, 0, 1, 1])  # Replace with actual bounding box coordinates
                    cv2.imwrite(output_filename, image_with_bbox)

if __name__ == "__main__":
    output_folder = "Noon_folder/final_output"

    split_data("Noon_folder/input_images", output_folder, target_width=300, random_state=42)