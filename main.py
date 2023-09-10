import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from remove_holes import remove_holes

# This main function can used to test your remove_holes() function. 
# You may modify this function as needed to test your detect_players() function. 
# The code in this function will not be graded.
def main():
    test_images = ["simple_with_holes.png", "zebra_with_holes.png"]
    data_folder = "data"
    output_folder = "output"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for image_name in test_images:
        input_image_path = os.path.join(data_folder, image_name)
        image = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)

        if image is None:
            print(f"Failed to load {image_name}")
            continue

        binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)[1]

        #### Remove holes ####
        result = remove_holes(binary_image)
        ######################

        # Normalize the image to the range [0, 255] for visualization and saving
        normalized_image = cv2.normalize(result, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

        # Show the result
        plt.figure()
        plt.imshow(normalized_image, cmap='gray')
        plt.show()

        
if __name__ == "__main__":
    main()
