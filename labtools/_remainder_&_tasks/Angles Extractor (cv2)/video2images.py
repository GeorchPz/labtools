# -*- coding: utf-8 -*-
"""
Created on Fri May  5 18:36:08 2023

@author: Jorge Pottiez López-Jurado
"""

import os
from datetime import timedelta

import cv2 as cv
from cropper import cropper

def video2image(video_path, save= True):
    '''
    Extract images from video file at a given time interval.

    Parameters
    ----------
    video_path : str
        Path to video file.
    save : bool, optional
        Save extracted images to file. The default is True.
    
    Returns
    -------
    None.
    '''
    # Define time interval for extracting images
    interval = 5  # in seconds
    
    # Open video file
    cap = cv.VideoCapture(video_path)
    
    # Get total number of frames in video
    num_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    # Get frame rate of video
    fps = int(cap.get(cv.CAP_PROP_FPS))
    
    # Initialize variable to keep track of time
    time_elapsed = 0
    
    # Iterate over video frames and extract images every interval seconds
    for i in range(num_frames):
        # Read frame
        ret, frame = cap.read()
        
        # Rotate the frame by 180 degrees
        rotated_frame = cv.rotate(frame, cv.ROTATE_180)
        # Crop image, to just keep the plot
        final_frame = cropper(rotated_frame)
        
        # Check if end of video has been reached
        if not ret:
            break
        
        # Calculate time elapsed in video
        time_elapsed = timedelta(seconds=i/fps)
        
        # Check if it's time to extract an image
        if time_elapsed.total_seconds() % interval == 0:
            
            print(time_elapsed)
            
            if save:
                # Create directory for storing extracted images
                dir_name = os.path.splitext(video_path)[0] + '_frames'
                if not os.path.exists(dir_name):
                    os.makedirs(dir_name)
                
                # Define image file name with time coordinate
                img_name = 'frame_' + str(time_elapsed).replace(':','.')
                img_path = f"{dir_name}\\{img_name}.jpg"
                # Save image to file
                cv.imwrite(img_path, final_frame)
        
    # Release video file
    cap.release()
    return None

def main():
    # Define video file path
    path = 'C:\\Users\\jorge\\OneDrive - Universitat de les Illes Balears\\Flu_B2_3__videos'

    file = ['Vel+25%.mp4', 'Vel+50%.mp4', 'Vel-25%.mp4', 'Vel-50%.mp4'][0]
    video_path = path + '\\' + file

    video2image(video_path, save= True)

if __name__ == '__main__':
    main()