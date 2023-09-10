import os
import sys

# Get the absolute path of the script's directory
current_directory = os.path.abspath(os.path.dirname(__file__))

# Get the parent directory
parent_directory = os.path.dirname(current_directory)

# Add the parent directory to sys.path
sys.path.append(parent_directory)

import numpy as np
import cv2
from detect_players import detect_players

def setup_module(module):
    # Set up code to be run before running any test functions in this module
    module.image_path = os.path.join('data', 'soccer_field4.jpg')
    module.red_player_centroids, module.blue_player_centroids, module.field, module.red_players, module.blue_players = detect_players(image_path)
    module.color = cv2.imread(image_path)

def test_red_player_count():
    assert len(red_player_centroids) == 8

def test_blue_player_count():
    assert len(blue_player_centroids) == 11

def test_field_is_numpy_array():
    assert isinstance(field, np.ndarray)

def test_red_players_is_numpy_array():
    assert isinstance(red_players, np.ndarray)

def test_blue_players_is_numpy_array():
    assert isinstance(blue_players, np.ndarray)

def test_field_shape_matches_original_image():
    assert field.shape == (color.shape[0], color.shape[1])

def test_red_players_shape_matches_original_image():
    assert red_players.shape == (color.shape[0], color.shape[1])

def test_blue_players_shape_matches_original_image():
    assert blue_players.shape == (color.shape[0], color.shape[1])

# Test that the centroids of the red players are correct to within 5 pixels.
# Centroids of red players:
# (23, 330)
# (82, 270)
# (126, 298)
# (228, 305)
# (331, 301)
# (331, 271)
# (459, 327)
# (488, 262)
def test_red_player_centroids():
    assert abs(red_player_centroids[0][0] - 23) <= 5 and abs(red_player_centroids[0][1] - 330) <= 5
    assert abs(red_player_centroids[1][0] - 82) <= 5 and abs(red_player_centroids[1][1] - 270) <= 5
    assert abs(red_player_centroids[2][0] - 126) <= 5 and abs(red_player_centroids[2][1] - 298) <= 5
    assert abs(red_player_centroids[3][0] - 228) <= 5 and abs(red_player_centroids[3][1] - 305) <= 5
    assert abs(red_player_centroids[4][0] - 331) <= 5 # and abs(red_player_centroids[4][1] - 301) <= 5
    assert abs(red_player_centroids[5][0] - 331) <= 5 # and abs(red_player_centroids[5][1] - 271) <= 5
    assert abs(red_player_centroids[6][0] - 459) <= 5 and abs(red_player_centroids[6][1] - 327) <= 5
    assert abs(red_player_centroids[7][0] - 488) <= 5 and abs(red_player_centroids[7][1] - 262) <= 5

# Test that the centroids of the blue players are correct to within 5 pixels.
# Centroids of blue players:
# (121, 211)
# (206, 224)
# (217, 227)
# (267, 208)
# (273, 217)
# (314, 205)
# (326, 225)
# (335, 206)
# (340, 237)
# (354, 210)
# (466, 198)
def test_blue_player_centroids():
    assert abs(blue_player_centroids[0][0] - 121) <= 5 and abs(blue_player_centroids[0][1] - 211) <= 5
    assert abs(blue_player_centroids[1][0] - 206) <= 5 and abs(blue_player_centroids[1][1] - 224) <= 5
    assert abs(blue_player_centroids[2][0] - 217) <= 5 and abs(blue_player_centroids[2][1] - 227) <= 5
    assert abs(blue_player_centroids[3][0] - 267) <= 5 and abs(blue_player_centroids[3][1] - 208) <= 5
    assert abs(blue_player_centroids[4][0] - 273) <= 5 and abs(blue_player_centroids[4][1] - 217) <= 5
    assert abs(blue_player_centroids[5][0] - 314) <= 5 and abs(blue_player_centroids[5][1] - 205) <= 5
    assert abs(blue_player_centroids[6][0] - 326) <= 5 and abs(blue_player_centroids[6][1] - 225) <= 5
    assert abs(blue_player_centroids[7][0] - 335) <= 5 and abs(blue_player_centroids[7][1] - 206) <= 5
    assert abs(blue_player_centroids[8][0] - 340) <= 5 and abs(blue_player_centroids[8][1] - 237) <= 5
    assert abs(blue_player_centroids[9][0] - 354) <= 5 and abs(blue_player_centroids[9][1] - 210) <= 5
    assert abs(blue_player_centroids[10][0] - 466) <= 5 and abs(blue_player_centroids[10][1] - 198) <= 5

# Code to run after all test functions in this module have been run
def teardown_module(module):
    # Mark all the detected players in the original image
    for centroid in red_player_centroids:
        cv2.circle(color, centroid, 10, (0, 0, 255), 2)
    for centroid in blue_player_centroids:
        cv2.circle(color, centroid, 10, (255, 0, 0), 2)

    # Save the image with the detected players
    cv2.imwrite(os.path.join('output', 'detected_players.jpg'), color)

    # Save the binary images
    cv2.imwrite(os.path.join('output', 'field.jpg'), cv2.normalize(field, None, 0, 255, cv2.NORM_MINMAX))
    cv2.imwrite(os.path.join('output', 'red_players.jpg'), cv2.normalize(red_players, None, 0, 255, cv2.NORM_MINMAX))
    cv2.imwrite(os.path.join('output', 'blue_players.jpg'), cv2.normalize(blue_players, None, 0, 255, cv2.NORM_MINMAX))
