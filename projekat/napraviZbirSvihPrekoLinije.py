# -*- coding: utf-8 -*-
"""
Created on Fri Feb 02 02:27:13 2018

@author: JOVICA
"""
from napraviModel import recDigit

from scipy import stats

def intsec(model,linija,brojevi):  
    zbir=0;
    for broj in brojevi:
         print("id broja:%d"%broj['id']);
         if len(broj['putanja'])>1:
             # Train the model using the training sets
             trainX=[];
             trainY=[];
             for cord in broj['putanja']:
                 trainX.append(cord[0])
                 trainY.append(cord[1])
            
             slope,intercept, t_value, p_values, sst_err=stats.linregress(trainX,trainY) #regr.fit((array(trainX)).reshape(1,-1),(array(trainY).reshape(1,-1)))
         
       
             #proveravam gde se seku(n1-n2)/k2-k1
             k21=slope-linija[0][0]
             n12=linija[0][1]-intercept
            
             #seku se negde
             if(k21!=0):
                 #print("nisu paralelni")
                 #presecen broj treba proveriti gde je prvi put uocen, ako je ispod linije ne treba ga gledati 
                 vrdYodLinije=linija[0][0]*broj['putanja'][0][0]+linija[0][1]
                 #provera da li se seku u okviru()plave ili zelene linije da li se seku u okviru putanje prave(7. na kraju prvog vid), i da li je prvi put uocen iznad linije
                 xcross=n12/(k21*1.0);
                 if(xcross>=broj['putanja'][0][0]-10 and xcross<=broj['putanja'][-1][0]+10 and xcross>=linija[1][0] and xcross<=linija[2][0] and vrdYodLinije>broj['putanja'][0][1]):
                      #ako se seku dodaj taj broj na sumu
                      #print("racuna sumu")
                      zbir=zbir+recDigit(model,broj['img']);
                      #print("zbir je:%d"%zbir);
             
    return zbir;
    