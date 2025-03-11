# -*- coding: utf-8 -*-
"""
Created on Sun May 14 01:37:06 2023

@author: Jorge Pottiez López-Jurado
"""

import cv2

def cropper(image):
    '''
    Crops the corners of the image
    
    Parameters:
    image : numpy.ndarray
        The image to be cropped
    
    Returns:
    cropped_image : numpy.ndarray
        The cropped image
    '''
    
    # Get the dimensions of the image
    height, width = image.shape[:2]
    
    # Define the desired border widths to be cropped
    L_width  = 200
    R_width  = 420
    B_height = 120 # bottom
    
    # Calculate the coordinates of the ROI
    x = L_width
    y = 0
    roi_width = width - L_width - R_width
    roi_height = height - B_height
    
    # Crop the image
    cropped_image = image[y:y+roi_height, x:x+roi_width]
    
    return cropped_image


def main():
    # folder = r"\Flu_B2_3__videos\Vel+25%"
    folder = r"\Flu_B2_3__videos\Vel+50%"
    file = 'frame_0.00.50.jpg'

    # Load the image
    image = cv2.imread(folder + '\\' + file)
    cropped_image = cropper(image)

    # Display the original and cropped images
    # cv2.imshow('Original Image', image)
    cv2.imshow('Cropped Image', cropped_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()