#!/usr/bin/python

import operator
import os
from math import *
import sys
from os.path import isfile
from itertools import *
import numpy as np
import matplotlib.mlab as mlab
from matplotlib.pyplot import *
import matplotlib.pyplot as plt

import pylab as plot
params = {'legend.fontsize': 20,
          'legend.linewidth': 4}
plot.rcParams.update(params)

file=sys.argv[1]  #REcibo el nombre del archivo por parametro 

outputPath = "Output/"



cant[]   #cantidad de valores
valores[]    #acumula los valores 

#lleno las listas con 0
for x in range(0,300):
  valores.append(0)
  cant.append(0)
  
  
  
  
fig = plt.figure()
#
inputFile = open(outputPath + file)
for l in inputFile:
  iteracion=int(l.split()[0])
  valorAsociado=int(l.split()[1])
  if valorAsociado > 0:   #NO TENGO EN CUENTA EL ULTIMO  SCORE
    cant[iteracion]++
    valores[iteracion]+=valorAsociado
  

inputFile.close()


iterations = []
value=[]  ##ACA GUARDO LOS VALORES QUE GRAFICO Vs ITERACION (PUEDEN SER SCORE, INTENTOS DE MUTACIONES, ETC)

for x in range(0,300):
  if valores[x] > 0:
      value.append(valores[x] / cant[x])
      iterations.append(x)
  
  

np_time = np.array(iterations)
np_step = np.array(value)
p1 = plt.plot(np_time, np_step, lw=2, label=file)




legend=plt.legend(bbox_to_anchor=(0.38, 0.52), loc=4, borderaxespad=0.,
		    fancybox=True,shadow=True,title='Method')
plt.grid()
plt.show()
fig.savefig(outputPath + "out.png", dpi = 100)