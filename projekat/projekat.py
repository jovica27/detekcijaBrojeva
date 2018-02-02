
#za prikazivanje slika
from __future__ import print_function

#import potrebnih biblioteka
import numpy as np

######MOJI#####
from napraviSlike import makeFrames
from napraviLinije import postaviKrajeveLinije
from napraviModel import makeModelKNNP
from napraviZbirSvihPrekoLinije import intsec  
from ucitajFramePoFrame import ucitajFrejmPoFrejm

#makeFrames(x)
model=makeModelKNNP();
brojevi,zelena,plava,niz_zelenih,niz_plavih=ucitajFrejmPoFrejm(model);

niz_zelenih=np.reshape(niz_zelenih,(-1,4))
niz_plavih=np.reshape(niz_plavih,(-1,4))

postaviKrajeveLinije(niz_zelenih,zelena);
postaviKrajeveLinije(niz_plavih,plava);

plus=intsec(model,plava,brojevi);
print("plus je :%d"%plus);
minus=intsec(model,zelena,brojevi);
print("minus je :%d"%minus); 
suma=plus-minus;   
   
print("suma je :%d"%suma);

#            
#            
#        
#        
#
