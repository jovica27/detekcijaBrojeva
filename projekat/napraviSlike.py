# -*- coding: utf-8 -*-
"""
Created on Fri Feb 02 02:07:02 2018

@author: JOVICA
"""
from __future__ import print_function

#import potrebnih biblioteka

#import imutils
import cv2

def makeFrames(dest):
    vidcap = cv2.VideoCapture(dest)
    count = 0; 
    success=True;
    while success:
        #print "pozvao funkciju"
        success,image = vidcap.read()
        cv2.imwrite("./images/frame%d.jpg" % count, image)     # save frame as JPEG file
        if cv2.waitKey(10) == 27:                     # exit if Escape is hit
                break
        count += 1
    return;
