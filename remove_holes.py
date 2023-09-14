import cv2
import numpy as np
import matplotlib.pyplot as plt

def remove_holes(my_image):
    
    my_image = cv2.threshold(my_image, 128, 255, cv2.THRESH_BINARY)[1]
    
    C = np.logical_not(my_image).astype(np.uint8)
    
    # Find connected components
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(C, connectivity=4)
    
    # Find the label of the background (largest connected component)
    background_label = np.argmax(stats[1:, cv2.CC_STAT_AREA]) + 1
    
     #If there are no holes, return original
    if num_labels == 1:
        result = my_image
        return result
    
    # Set all labels except the background label to 0
    labels[labels != background_label] = 0
    
    # Convert C back to binary
    C = (labels > 0).astype(np.uint8) * 255
    
    # Invert C to get the result
    result = cv2.bitwise_not(C)
    
    # Display the original and modified images for testing
   # plt.subplot(121), plt.imshow(my_image, cmap='gray'), plt.title('Original Image')
   # plt.subplot(122), plt.imshow(result, cmap='gray'), plt.title('Image with Holes Preserved')
   # plt.show()
    
    return result
