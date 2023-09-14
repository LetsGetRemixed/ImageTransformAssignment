import cv2
import numpy as np
import matplotlib.pyplot as plt
from get_component import get_component
from remove_holes import remove_holes

def detect_players(image_path):
    original_image = cv2.imread(image_path)
    hsv_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)
    
    #Define what green
    lower_green = np.array([40, 40, 40])  # Lower Green
    upper_green = np.array([80, 255, 255])  # Upper Green
    
    # Create the green mask
    green_mask = cv2.inRange(hsv_image, lower_green, upper_green)
    
    # clean up, clean up, everybody, everywhere
    kernel = np.ones((5, 5), np.uint8)
    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel)
    
    field = cv2.bitwise_not(green_mask)
    
    field = cv2.bitwise_not(field)
    
    # Close them gaps
    field = remove_holes(field)
    
    
    
    #separate red and blue players
    #Red players
    lower_red = np.array([0, 0, 70], dtype=np.uint8)
    upper_red = np.array([80, 80, 255], dtype=np.uint8)
    red_mask = cv2.inRange(original_image, lower_red, upper_red)
    red_mask = cv2.bitwise_and(red_mask, field)     #detecting in mask and field
    
    #Blue Players
    lower_blue = np.array([50, 0, 0], dtype=np.uint8)
    upper_blue = np.array([255, 90, 90], dtype=np.uint8)
    blue_mask = cv2.inRange(original_image, lower_blue, upper_blue)
    blue_mask = cv2.bitwise_and(blue_mask, field)
    
    
    # clean up, clean up, everybody, everywhere
    red_players = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
    blue_players = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, kernel)
    
    
    #red players white
    red_players = cv2.bitwise_not(red_mask)
    red_players = cv2.bitwise_not(red_players)
    #blue players white
    blue_players = cv2.bitwise_not(blue_mask)
    blue_players = cv2.bitwise_not(blue_players)
    
    # Find player centroids
    red_player_centroids = []
    blue_player_centroids = []
    
    # Find red players' centroids
    red_contours, _ = cv2.findContours(red_players, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    for contour in red_contours:
    # pin down an area
        area = cv2.contourArea(contour)
    
    # reds bigger so bigger number babyyyyyyyyyy
        min_contour_area = 10
    
        if area > min_contour_area:
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                red_player_centroids.append((cX, cY))
    
    # Find blue players' centroids
    blue_contours, _ = cv2.findContours(blue_players, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for contour in blue_contours:
    # pin down area
        area = cv2.contourArea(contour)
    
    # blue dudes be tiny so make it smalllllllllll
        min_contour_area = 2.3
    
        if area > min_contour_area:
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                blue_player_centroids.append((cX, cY))
    
    # Sort centroids by their x-coordinate
    red_player_centroids.sort(key=lambda coord: coord[0])
    blue_player_centroids.sort(key=lambda coord: coord[0])
    
    return red_player_centroids, blue_player_centroids, field, red_players, blue_players
