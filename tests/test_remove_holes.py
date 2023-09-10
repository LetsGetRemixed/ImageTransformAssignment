import os
import sys

# Get the absolute path of the script's directory
current_directory = os.path.abspath(os.path.dirname(__file__))

# Get the parent directory
parent_directory = os.path.dirname(current_directory)

# Add the parent directory to sys.path
sys.path.append(parent_directory)

import pytest
import cv2
import numpy as np
import matplotlib.pyplot as plt
from remove_holes import remove_holes  # Import your remove_holes function; replace 'your_module' with the actual module name

# Test with given images
@pytest.mark.parametrize("input_filename, output_filename", [
    ("simple_with_holes.png", "simple_without_holes.png"),
    ("zebra_with_holes.png", "zebra_without_holes.png")
])
def test_remove_holes(input_filename, output_filename):
    # Read the test image
    input_image_path = os.path.join("data", input_filename)  # Assuming the test images are in a folder named 'test_images'
    image = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        pytest.fail(f"Failed to load {input_filename}")

    # Binarize the image
    binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)[1]

    # Call the function to be tested
    result = remove_holes(binary_image)

    # Normalize the image to the range [0, 255] for saving
    normalized_image = cv2.normalize(result, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    # Save the output image
    output_image_path = os.path.join("output", output_filename)
    cv2.imwrite(output_image_path, normalized_image)

    # Optionally: Add assertions to validate that 'result' is as expected

# Test with random images
def test_remove_holes2():
    # Test case 1: A simple image with a hole in the middle
    img1 = np.zeros((5, 5), dtype=np.uint8)
    img1[1:4, 1:4] = 1
    img1[2, 2] = 0
    expected1 = np.copy(img1)
    expected1[2, 2] = 1
    result1 = remove_holes(img1)
    assert np.array_equal(result1, expected1)

    # Test case 2: A more complex image with multiple holes
    img2 = np.zeros((10, 10), dtype=np.uint8)
    img2[1:4, 1:4] = 1
    img2[2, 2] = 0
    img2[6:9, 6:9] = 1
    img2[7, 7] = 0
    expected2 = np.copy(img2)
    expected2[2, 2] = 1
    expected2[7, 7] = 1
    assert np.array_equal(remove_holes(img2), expected2)

    # Test case 3: An image with no holes
    img3 = np.ones((5, 5), dtype=np.uint8)
    expected3 = np.ones((5, 5), dtype=np.uint8)
    assert np.array_equal(remove_holes(img3), expected3)

    # Test case 4: An image with all holes
    img4 = np.zeros((5, 5), dtype=np.uint8)
    expected4 = np.zeros((5, 5), dtype=np.uint8)
    assert np.array_equal(remove_holes(img4), expected4)