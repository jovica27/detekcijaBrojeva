# -*- coding: utf-8 -*-
"""
Created on Fri Feb 02 02:36:57 2018

@author: JOVICA
"""
import cv2 
import numpy as np

from vector import *
from detekcijaBrojeva import makeRegions
from napraviLinije import makeLines


def najbliziBrojeviIzOkoline(broj,okolniBrojevi):
    minDistance = distance(broj['center'],okolniBrojevi[0]['center'])
    najblizi = okolniBrojevi[0]
    
    for br in okolniBrojevi:
        if (distance(br['center'],broj['center']) < minDistance):
            minDistance = distance(br['center'],broj['center'])
            najblizi = br
    
    najbliziNiz = []
    najbliziNiz.append(najblizi)
    
    return najbliziNiz
            

def brojeviIzOkoline(broj,brojevi):
    okolniBrojevi = []
    for br in brojevi:
        if (distance(br['center'],broj['center'])<20):
            okolniBrojevi.append(br)
            
    if len(okolniBrojevi)>1 :
        return najbliziBrojeviIzOkoline(broj,okolniBrojevi)
    else :
        return okolniBrojevi


def ucitajFrejmPoFrejm(model):
    
#video i prelazak preko linije
    video = "videos/video-5.avi"
    vid = cv2.VideoCapture(video)
    frejm = 0
    brojevi = []
    id=-1

    zelena=0;
    plava=0;
    niz_zelenih=[];
    niz_plavih=[];
    
    while  (1) :  
      
        ret, currentFrame = vid.read()
        #na pocetku jednom postavi linije

            
        if not ret: 
            print ("frejm nije ucitan")
            break
        frejm += 1
        currentFrameCopy=currentFrame.copy();
        if frejm==1:   
            currentFrame=cv2.cvtColor(currentFrame,cv2.COLOR_BGR2RGB)
            linije=makeLines(currentFrame);
            zelena=linije[0];
            plava=linije[1];

        
        currentFrameCopy=cv2.cvtColor(currentFrameCopy,cv2.COLOR_BGR2RGB)
        linije=makeLines(currentFrameCopy);
        
        niz_zelenih.extend([linije[0][1][0],linije[0][1][1],linije[0][2][0],linije[0][2][1]]);
        niz_plavih.extend([linije[1][1][0],linije[1][1][1],linije[1][2][0],linije[1][2][1]]);

    
        #print("trenutni frejm:%d"%frejm);
        kont_brojevi=makeRegions(currentFrame,frejm);
        for br in brojevi:
           if (frejm - br['frame']) <=5 :
               cv2.circle(currentFrame, (br['center'][0], br['center'][1]), 16, (25, 25, 255), 1)
               cv2.putText(currentFrame,  str(br['id']), (br['center'][0],br['center'][1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
           
       #ISCRTAVANJEEEEEEEEEEEEEEEEEEEE 
        cv2.imshow("video",currentFrame)
        cv2.waitKey(15)
       
        for broj in kont_brojevi :
                
                istiBrojUProslomFrejmu = brojeviIzOkoline( broj, brojevi)
                
                brojNadjenih = len(istiBrojUProslomFrejmu)
                if brojNadjenih == 0:
                    id=id+1;
                    broj['id'] = id;
                    broj['prosaoPlavu'] = False
                    broj['prosaoZelenu'] = False

                    brojevi.append(broj)
                elif brojNadjenih == 1:
                    istiBrojUProslomFrejmu[0]['center'] = broj['center']
                    istiBrojUProslomFrejmu[0]['frame'] = frejm
                    istiBrojUProslomFrejmu[0]['putanja'].append(broj['center']);

                
                
                
            #drugi nacin da racuna sumu i ostalo
            #========================= pronadje sliku broja na videu
#        for br in brojevi:
#            starostBroja = frejm - br['frame']
#
#            if (starostBroja < 5):
#
#                distancaBrojaOdLinije1 = pnt2line(br['center'], (plava[1][0], plava[1][1]),(plava[2][0], plava[2][1]))
#                distancaBrojaOdLinije2 = pnt2line(br['center'], (zelena[1][0], zelena[1][1]),(zelena[2][0], zelena[2][1]))
#                
#
#                
#                #cv2.line(img, pnt1, el['center'], (0, 255, 25), 1)
#                
#                if (distancaBrojaOdLinije1 < 10 and not br['prosaoPlavu']):
#                    print ("doslo do kolizije sa prvom, a id broja je: ", br['id'])
#                    
#                    if br['prosaoPlavu'] == False:
#                        br['prosaoPlavu'] = True
#                        pogodak= recDigit(br['img']);
#                        #dodati vrednost na sumu
#                        suma=suma+pogodak;
#                        print("pogadja  :%d"%pogodak);
#                        print("suma je :%d"%suma);
#                        #cv2.imshow(str(br['id']),br['img'])
#                        #cv2.waitKey(0);
#                    
#                        
#                if (distancaBrojaOdLinije2 < 10 and not br['prosaoZelenu']):
#                    #print "doslo do kolizije sa drugom, a id broja je: ", br['id']
#                    #cv2.imshow(str(br['id']),br['img'])
#                    if br['prosaoZelenu'] == False:
#                        br['prosaoZelenu'] = True
#                        pogodak= recDigit(br['img']);
#                        #oduzeti vrednost od sume
#                        suma=suma-pogodak;
#                        print("id broja:%d"%br['id']);
#                        print("pogadja  :%d"%pogodak);
#                        print("suma je :%d"%suma);                       
#                        #cv2.imshow(str(br['id']),br['img'])
#                        #cv2.waitKey(0);
                       

    vid.release()
    cv2.destroyAllWindows()
    
    return brojevi,zelena,plava,niz_zelenih,niz_plavih