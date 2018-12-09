# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 16:48:32 2018

@author: user
"""
import random
from matplotlib import pyplot
import numpy as np
import collections as cl
import math
import warnings
warnings.simplefilter('ignore', np.RankWarning)
########################################################
x=(np.random.normal(500,30,1000000000))
c=[]
for i in x:
    i=int(i)
    c.append(i)
######################################################
#######Incertidumbre##################################
###########histograma de cargas#################################
datos_counter = cl.Counter(c)
tablaFreqAbs = datos_counter.most_common()
tablaFreqAbs.sort()

adcq=[]
frec=[]
for i in tablaFreqAbs:
    adcq.append(i[0])
    frec.append(i[1])
#listas logaritmicas
logfrec=[]
for i in frec:
    logfrec.append(math.log10(i))
#region de interes de muones
adcqm=[]
for i in tablaFreqAbs:
    if i[0]<600 and i[0]>300:
        adcqm.append(i)
    
muonica=[]
cont=[]
for i in adcqm:
    muonica.append(i[0])
    cont.append(i[1])

z=np.polyfit(muonica,cont,deg=4)#full true
p=np.poly1d(z)
#derivada
dp=np.diff(p(muonica))/np.diff(muonica)
pc=[]
for i in range(len(dp)):
    if abs(dp[i])<0.1:
        pc.append(muonica[i+1])
print(pc)        
########################################################
logcont=np.log10(cont)    
logz=np.polyfit(muonica,logcont,deg=4)
logp=np.poly1d(logz)
dlogp=np.diff(logp(muonica))/np.diff(muonica)
lpc=[]
for i in range(len(dlogp)):
    if abs(dlogp[i])<0.001:
        lpc.append(muonica[i+1])
print(lpc)  
#Graficas    
pyplot.plot(adcq,frec,'o',muonica,p(muonica))#histo1
pyplot.title('Histograma de Cargas')
pyplot.xlabel('Carga (ADCq)')
pyplot.ylabel('Conteo')
pyplot.show()
pyplot.plot(adcq,logfrec,muonica,logp(muonica))#histo2
pyplot.title('Histograma de Carga con logaritmo')
pyplot.xlabel('Carga (ADCq)')
pyplot.ylabel('log(Conteo)')
pyplot.show()