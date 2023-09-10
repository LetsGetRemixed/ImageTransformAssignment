import cv2 as cv
import numpy as np

# Function to get the k-th largest component in a binary image
def get_component(binary, k):
    # Perform connected component analysis
    _, labels, stats, _ = cv.connectedComponentsWithStats(binary.astype(np.uint8), connectivity=8)
    
    # Number of components, subtracting 1 to ignore the background
    number = len(stats) - 1
    
    # If there are fewer than k components, return None
    if number < k:
        return None

    # Remove the entry for the background
    stats = stats[1:]
    
    # Sort components by their area in descending order and get the ids
    ids = np.argsort(-stats[:, cv.CC_STAT_AREA])

    # Get the k-th largest component
    return (labels == ids[k-1] + 1).astype(np.uint8)