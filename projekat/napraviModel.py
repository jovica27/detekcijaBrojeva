# -*- coding: utf-8 -*-
"""
Created on Fri Feb 02 02:13:01 2018

@author: JOVICA
"""
from sklearn.neighbors import KNeighborsClassifier

from skimage import exposure

#profesor mnist
from sklearn.datasets import fetch_mldata
import numpy as np
import cv2

import matplotlib.pylab as plt

#isecenu sliku transformise u oblik pogodan da bi se vrsila predikcija() i vrsi predikciju

def recDigit(model,cropped_img):
    
    dim = (28, 28)
    pom = cv2.resize(cropped_img, dim, interpolation = cv2.INTER_CUBIC)

    pom=pom.flatten();
    pom = np.reshape(pom, (1,-1))
    prediction=model.predict(pom)[0];
    print("predvidja broj:")
    print (prediction)
    return prediction;
   

#formira model
brojac3 = 0
def makeModelKNNP():
    mnist = fetch_mldata('MNIST original')
    data=mnist.data;
    labels = mnist.target.astype('int')
    train_rank = 5000;
    test_rank = 100;
    #trainData=data;
    #trainLabels=labels;
    train_subset = np.random.choice(data.shape[0], train_rank)
    test_subset = np.random.choice(data.shape[0], test_rank)
    #train dataset
    trainData = data[train_subset]
    trainLabels = labels[train_subset]
    #test dataset
    valData = data[test_subset]
    valLabels = labels[test_subset]
    # initialize the values of k for our k-Nearest Neighbor classifier along with the
# list of accuracies for each value of k

    kVals = range(1, 30, 2)
    accuracies = []
# loop over various values of `k` for the k-Nearest Neighbor classifier
    
    for k in xrange(1, 30, 2):
	# train the k-Nearest Neighbor classifier with the current value of `k`
    
    	model = KNeighborsClassifier(n_neighbors=k)
    	model.fit(trainData, trainLabels)  
 
	# evaluate the model and update the accuracies list
    	score = model.score(valData, valLabels)
    	print("k=%d, accuracy=%.2f%%" % (k, score * 100))
    	accuracies.append(score)
       

 
# find the value of k that has the largest accuracy
    i = np.argmax(accuracies)
    print("k=%d achieved highest accuracy of %.2f%% on validation data" % (kVals[i],accuracies[i] * 100))
#    i=1;
# re-train our classifier using the best k value and predict the labels of the
# test data
    print("=-------------------------------------------------");
    mojaLista=[];
    print("velicina data seta: %d"%len(trainData));
    for it in range(0,len(trainData)):
        pom=trainData[it];
        #prebacujem iz vektora u matricu
        pom = pom.reshape((28, 28)).astype("uint8")
        pom = exposure.rescale_intensity(pom, out_range=(0, 255))

        
        ret,pom=cv2.threshold(pom,127, 255, cv2.THRESH_BINARY);
        
#        global brojac3;
#        brojac3=brojac3+1;
#        if(brojac3<15):
#            plt.figure();
#            plt.imshow(pom,'gray');
         
        pom_bin=pom.copy();
        kernel=np.ones((3,3));
        pom=cv2.dilate(pom,kernel,iterations=1);
        kernel=np.ones((1,1));
        pom=cv2.erode(pom,kernel,iterations=2);

        img2,contours,hierarchy =cv2.findContours(pom,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE);
        ##print("broj kontura je:%d"%len(contours));
 
        #for cnt in contour:
            
        for cnt in contours:
            x,y,w,h = cv2.boundingRect(cnt); 
            if(h<6 and w<6):
                print("nije broj");

            else:
                    
                   ##print("jeste broj")
                   pom_cropped=pom_bin[y:y+h,x: x+w];
                   
#                   if(brojac3<15):
#                       plt.figure();
#                       plt.imshow(pom_cropped,'gray');
                   ##print("sirina:%d,i visina:%d"%(w, h));
                   dim = (28, 28)
                   pom_cropped = cv2.resize(pom_cropped, dim, interpolation = cv2.INTER_CUBIC )
                   
#                   
#                   if(brojac3<15):
#                       plt.figure();
#                       plt.imshow(pom_cropped,'gray');
                       
                   pom_cropped=pom_cropped.flatten();
                   pom_cropped = np.reshape(pom_cropped, (1,-1))
                   
                   cv2.rectangle(pom_bin,(x,y),(x+w,y+h),(0,255,0),2)
                   trainData[it]=pom_cropped;
                   mojaLista.append(pom_cropped);
                   
        #cv2.imshow('iscrtani reg',pom_cropped_copy);
        #cv2.waitKey()
    print("------------------------------------");
    print("broj mojih:%d"%len(mojaLista));
    model = KNeighborsClassifier(n_neighbors=kVals[i])
    model.fit(trainData, trainLabels)

    return model;