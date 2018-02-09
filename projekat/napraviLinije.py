# -*- coding: utf-8 -*-
"""
Created on Fri Feb 02 02:09:17 2018

@author: JOVICA
"""
from __future__ import print_function

#import potrebnih biblioteka
import numpy as np
#import imutils
import cv2

import matplotlib.pylab as plt

brojac2=0;
def postaviKrajeveLinije(niz_linija,linija_za_menjanje):
    #[xmin,ymin,xmax,ymax]
    #MAX
    xmax_vred=niz_linija[:,2]
    ymax_vred=niz_linija[:,3]
    s_vred_max=np.mean(xmax_vred)   
    bool_izbaci_pik=xmax_vred<s_vred_max+50
    index=np.argmax(xmax_vred[bool_izbaci_pik]);
    linija_za_menjanje[2][0]=xmax_vred[index];
    linija_za_menjanje[2][1]=ymax_vred[index];
    print("srednja vrednost za max je: %d"%s_vred_max)
    print("max vrednost max:%d"%linija_za_menjanje[2][0]);
    
    #MIN
    xmin_vred=niz_linija[:,0]
    ymin_vred=niz_linija[:,1]
    s_vred_min=np.mean(xmin_vred);
    bool_izbaci_pik=xmin_vred>s_vred_min-50
    index=np.argmin(xmin_vred[bool_izbaci_pik]);
    linija_za_menjanje[1][0]=xmin_vred[index];
    linija_za_menjanje[1][1]=ymin_vred[index];
    print("srednja vrednost za min je: %d"%s_vred_min)
    print("max vrednost min:%d"%linija_za_menjanje[1][0]);
    return;
    
def makeLines(img):
      #detekcija linije
     
     img_plava=img.copy();
     img_zelena=img.copy();
     
   
     #zelena boja  
     lower_range = np.array([0, 100, 0])
     upper_range = np.array([50, 255, 50])
     img_zelena=cv2.inRange(img_zelena,lower_range,upper_range)
     
     #plava boja
     lower_range = np.array([0, 0, 100])
     upper_range = np.array([50, 50, 255])
     img_plava=cv2.inRange(img_plava,lower_range,upper_range)
     
     zelena=makeLine(img,img_zelena);
     plava=makeLine(img,img_plava)
     return zelena,plava;
def makeLine(img,img_boja):

   
     kernel=np.ones((3,3));
     img_boja=cv2.dilate(img_boja,kernel,iterations=1);

     edges = cv2.Canny(img_boja,50,150,apertureSize =3)

     minLineLength = 100
     maxLineGap =2
     lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
     
     xmin=lines[0][0][0]
     xmax=lines[-1][0][0]
     ymin=lines[0][0][1]
     ymax=lines[-1][0][1]
     for x in range(0, len(lines)):
         for x1,y1,x2,y2 in lines[x]:
             if x1<xmin:
                 xmin=x1;
                 ymin=y1;
        
             if x2<xmin:
                xmin=x2;
                ymin=y2;  
             if x1>xmax:
                xmax=x1;
                ymax=y1;
        
             if x2>xmax:
                xmax=x2;
                ymax=y2; 
                
#     cv2.circle(img,(xmin,ymin), 10, (255,0,0), 3)
#     cv2.circle(img,(xmax,ymax), 10, (255,0,0), 3)
     #iscrtavanje krajeva linije
#     global brojac2;
#     brojac2=brojac2+1;
#     if(brojac2<15):
#         plt.figure();
#         plt.imshow(img,'gray');
     
        
     #dobijem formulu za pravu
     z=np.polyfit([xmin,xmax],[ymin,ymax],1);

     return z,[xmin,ymin],[xmax,ymax];