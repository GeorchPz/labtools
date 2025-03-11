# -*- coding: utf-8 -*-
"""
Created on Sun May 14 00:36:48 2023

@author: Jorge Pottiez López-Jurado
"""

import os
import numpy as np
import pandas as pd

import cv2 as cv

def image2angle(folderpath, filepath, display, save):
    '''
    Extracts angle from image file.
    Displays image with angle and waits for user to close it.
    Saves image with angle to new folder.

    Parameters
    ----------
    folderpath : str
        Path to folder containing image file.
    filepath : str
        Path to image file.
    display : bool
        If True, displays image with angle.
    save : bool
        If True, saves image with angle to new folder.
    
    Returns
    -------
    ang_rad : float
        Angle in radians between circle center and patch.
    '''
    
    img = cv.imread(filepath, cv.IMREAD_GRAYSCALE)
    
    #detect circle
    circles = cv.HoughCircles(
        img, cv.HOUGH_GRADIENT, 1, 100
        param1=100, param2=30, minRadius=50, maxRadius=500
        )
    # get circle center (raise Exception if circle was not detected)
    try:
        center = (int(circles[0,0,0]), int(circles[0,0,1]))
    except IndexError:
        raise Exception("Unable to identify center.")
    
    duple = [(30,30), (35,35)][0]
    # dilate and threshold image to only see the rectangle as small dot
    kernel = np.ones(duple, np.uint8)
    # kernel = np.ones((35, 35), np.uint8)
    img_dilate = cv.dilate(img, kernel, iterations=1)
    _, img_dilate_thres = cv.threshold(img_dilate,120,255,cv.THRESH_BINARY)
    # get center position of remaining dot
    rect_x = np.argmin(img_dilate_thres.mean(axis=0))
    rect_y = np.argmin(img_dilate_thres.mean(axis=1))
    
    # get angle between circle center and patch
    ang_rad = np.arctan2(center[1] - rect_y, rect_x - center[0])
    if ang_rad<0:
        ang_rad += 2*np.pi
    ang_deg = ang_rad/np.pi*180
    
    if display or save:
        # plot center of circle (axes' origin)
        cv.circle(img, center, 1, (0, 100, 100), 3)
        # display center of cardboard piece   
        cv.circle(img, (rect_x, rect_y), 1, (0, 100, 100), 3)
        # display angle, wait for user to close image
        font = cv.FONT_HERSHEY_SIMPLEX
        cv.putText(img, f'{ang_deg:.1f}', (rect_x, rect_y), font, 2, (0, 255, 0), 2, cv.LINE_AA)
        
        filename = filepath.split('\\')[-1].replace('.jpg','')
        
        if display:
            cv.imshow(f"detected circles: {filename}", img)
            # # Debug displays
            # cv.imshow("detected circles", img_dilate)
            # cv.imshow("detected circles", img_dilate_thres)
            cv.waitKey(0)
    
        if save:
            # Create directory for storing extracted images
            new_folderpath = folderpath.replace('_frames','') + '_angs'
            if not os.path.exists(new_folderpath):
                os.makedirs(new_folderpath)
            
            # Define image file name with time coordinate & angle
            img_path = f"{new_folderpath}\\{filename}.jpg"
            # Save image to file
            cv.imwrite(img_path, img)
        
    return ang_rad


def list_dir(folder):
    '''Lists all files in a directory.'''
    directory = os.listdir(folder)
    return [i for i in directory]


def frames2df(folderpath):
    '''
    Extracts angles from all images in a folder.
    Saves angles to an Excel file.
    
    Parameters
    ----------
    folderpath : str
        Path to folder containing image files.
    
    Returns
    -------
    df : DataFrame
        DataFrame containing time, time in seconds and angle in radians.
    '''
    
    t_labs = []
    t = []
    θ = []
    
    files_dir = list_dir(folderpath)        # all frames
    # files_dir = list_dir(folderpath)[-10:]  # last ten frames
    
    for file in files_dir:
        
        # String of the type 0.01.05
        timelabel = file.replace('frame_','').replace('.jpg','')
        _,mins,secs = timelabel.split('.')
        t_labs.append( timelabel.replace('.',':') )
        t.append( int(mins)*60 + int(secs) )
        
        filepath = folderpath + '\\' + file
        rads = image2angle(folderpath, filepath, display= False, save= True)
        θ.append(rads)
        print(f'{timelabel}  θ= {rads:.2f}')
    
    df = pd.DataFrame({
        'time'   : t_labs,
        't (s)'  : t,
        'θ (rad)': θ
        })

    xlpath = folderpath.replace('_frames','') + '.xlsx'
    df.to_excel(xlpath, index= False)
    
    return df


def main():
    path = r'\Flu_B2_3__videos'

    folder = ['Vel+25%_frames', 'Vel+50%_frames', 'Vel-25%_frames', 'Vel-50%_frames'][0]
    df = frames2df(path + '\\' + folder)

    θ = df.iloc[-10:,2] # : -> all rows, 2º column
    θmean = sum(θ)/len(θ)
    bias  = abs(θ - θmean).mean()
    print('bias: ', bias)
    # bias: 0ºfolder : 0.011086508731490 = 0.01109

    # duple's value1, minimizes θ_f error
    # is value1 solution stable for every θ(t)? its not
    # therefore, we shall use value0

if __name__ == '__main__':
    main()