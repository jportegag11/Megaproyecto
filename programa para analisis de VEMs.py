# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 11:17:00 2018

@author: Christian
"""
from matplotlib import pyplot
import numpy as np
vems=[]
archivo = open("flujo.txt", 'r')
for linea in archivo.readlines():
    x=float(linea)
    vems.append(x)
archivo.close() 
################################################# estadisticas
media=np.mean(vems)
desvest=np.std(vems,ddof=1)
#################################################
medial=[]
x=[]
for i in range(len(vems)):
    medial.append(media)
    x.append(i)
error=10
pyplot.errorbar(x,vems,marker='o',linestyle='--')
pyplot.title('Flujo de Muones verticales')
pyplot.xlabel('Tiempo (h)')
pyplot.ylabel('Flujo Vertical de Muones (1/sr m^2 s)')
pyplot.ioff()
pyplot.plot(medial)
pyplot.ion()
pyplot.plot(medial, label="Media = 0.340 y desv.est = 0.004",linestyle='--',color='r')
pyplot.legend()

#pyplot.title("Histogramas de VEMs")
#pyplot.hist(vems, bin=70)
#pyplot.xlabel('Tiempo (h)')
#pyplot.ylabel('VEM(ADCq)')

#label="Media=470, Desviacion estandar=14, kurtosis=-0.44"