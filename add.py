# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 18:55:45 2018

@author: user
"""
from matplotlib import pyplot
import numpy as np
import collections as cl
import math
ci1=[]
c=[]
ch=[]
cargas=[]
ar=open("atitlan25-08-18_2_nogps_2018_04_28_05h00.dat","r")
for linea in ar.readlines():
    if linea[0]!='#':
        ci1.append(linea)
for i in ci1:
    x=i[6]+i[7]
    if i[8]== '0' or '1' or '2' or '3' or '4' or '5' or '6' or '7' or '8' or '9':
        x=x+i[8]
        c.append(x)
for i in c:
    a=int(i)-50
    ch.append(a)
ci=0
for i in range(len(ch)-12):
    if (i%12)==0:
        ci=int(ch[i])+int(ch[i+1])+int(ch[i+2])+int(ch[i+3])+int(ch[i+4])+int(ch[i+5])+int(ch[i+6])+int(ch[i+7])+int(ch[i+8])+int(ch[i+9])+int(ch[i+10])+int(ch[i+11])
        cargas.append(ci)
datos_counter = cl.Counter(cargas)
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
    if abs(dlogp[i])<0.0009:
        lpc.append(muonica[i+1])
print(lpc)
print(min(abs(dlogp)))  

#Graficas    
pyplot.plot(adcq,frec,'o',muonica,p(muonica))#histo1
pyplot.title('Histograma de Cargas')
pyplot.xlabel('Carga (ADCq)')
pyplot.ylabel('No. Evenetos')
pyplot.show()
pyplot.plot(adcq,logfrec,muonica,logp(muonica))#histo2
pyplot.title('Histograma de Carga Semilogaritmico')
pyplot.xlabel('Carga (ADCq)')
pyplot.ylabel('log(No. Eventos)')
pyplot.show()
#VEM ES DE 448
#for i in range(len(dlogp)):
#    if abs(dlogp[i])<0.0005934:
#        x= i
#        a=[dlogp[i], muonica[i], i]
#        print a
