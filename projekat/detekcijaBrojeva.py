# -*- coding: utf-8 -*-
"""
Created on Fri Feb 02 01:41:04 2018

@author: JOVICA
"""
#za prikazivanje slika
from __future__ import print_function

#import potrebnih biblioteka
import numpy as np
#import imutils
import cv2

import matplotlib.pylab as plt

brojac=0;
def makeRegions(img_col,frejm):
    
     img_gs = cv2.cvtColor(img_col, cv2.COLOR_RGB2GRAY) # konvert u grayscale

     ret,image_bin=cv2.threshold(img_gs,200, 255, cv2.THRESH_BINARY);

     #za kropovanje ce se koristiti     
     image_bin_za_crop=image_bin.copy();
     #oslobadanje tackica i podebljavanje kontura da bi se spojile ako negde ima ne spojeno
     kernel=np.ones((3,3));
     image_bin=cv2.dilate(image_bin,kernel,iterations=1);
     kernel=np.ones((1,1));
     image_bin=cv2.erode(image_bin,kernel,iterations=2);

     #pronalazi brojeve
     #external zbog nule, osmice i ostalo 
     img,contours,hierarchy =cv2.findContours(image_bin,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE);
             
     img=img_col.copy();
     
     kont_brojevi=[];

     for cnt in contours:
         x,y,w,h = cv2.boundingRect(cnt); 
         if not (w<7 and h<15 or w>40 and h>40):

             img_cropped=image_bin_za_crop[y:y+h,x: x+w];
             broj = {'id':-1,'center': (x+(w/2),y+(h/2)),'img' : img_cropped,'frame' : frejm,'putanja':[]}
             broj['putanja'].append(broj['center']);
            
             kont_brojevi.append(broj);
             img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

    
     global brojac;
     brojac=brojac+1;
     if(brojac<2):
         plt.figure();
         plt.imshow(img,'gray');
     

     return kont_brojevi;