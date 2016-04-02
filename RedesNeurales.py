# -*- encoding: utf-8 -*-

#!/usr/bin/env python3  

# -------------------------------------------------
#  Universidad Simón Bolívar
#  Inteligencia Artificial II
#  Prof. Ivette Carolina Martinez
#
#  Autores: Jorge Marcano         # Carnet : 11-10566
#           Maria Victoria Jorge  # Carnet : 11-10495
#           Fabio Castro          # Carnet : 10-10132
#
# Proyecto 1 - Redes Neurales
# -------------------------------------------------

import sys
import random
import math
import numpy as np
import matplotlib.pyplot as plt
from math import e


def filtrarEntrada(x):
	if (x==-1):
		return 0
	else:
		return x

# X es una fila del examples
def calcularO(w,x,w0,capa1,capa2):
	output = []
	for i in range(capa2):
		net = w0[i] # w0*x0 y x0 siempre es 1
		for j in range(capa1):     
			net += w[j][i]*x[j]
		output.append(1.0/(1.0 + np.exp(-net)))
	return output

def backPropagation(examples,rate,nin,nout,nhidden,max_iter):
	np.random.seed(43124)
 
	initW = []  # MATRIZ de pesos entre capa init y hidden
	hidW = []   # MATRIZ de pesos entre capa hidden y out

	# Inicializando pesos entre capa init y capa hidden
	# [[pesosNeurona1],[pesosNeurona2]...] 
	for i in range(0,nin) : 
		initW.append(np.random.randint(low=-500,high=500,size=nhidden)/1000.0)
   # print("Pesos Input-Hidden :",initW)

	# Inicializa el arreglo de umbral entre capa init y hidden
	b0 = np.random.randint(low=-500,high=500,size=nhidden)/1000.0

	#print("Pesos Umbral-Hidden: ",b0)

	# Inicializando pesos entre capa hidden y capa out
	# [[pesosNeurona1],[pesosNeurona2]...]
	for j in range(0,nhidden) :
		hidW.append(np.random.randint(low=-500,high=500,size=nout)/1000.0)
   # print("Pesos Hidden-Output: ",hidW)

	# Inicializa el arreglo de umbral entre capa hidden y out
	b1 = np.random.randint(low=-500,high=500,size=nout)/1000.0
	#print("Pesos Umbral-Output: ",b1)
	aux = 0
	errorArray = []
	iterArray = []
	while (aux < max_iter):
		errorIter = 0
		for ex in examples:

			#Propagate the input forward through the network :
			oHidden = calcularO(initW,ex,b0,nin,nhidden)
			oOut = calcularO(hidW,oHidden,b1,nhidden,nout)
			errorHidden = []
			errorOut = []

			#Propagate the errors backwards :
			#Para cada neurona de salida calcular su error
			for k in range(nout):
				errorOut.append(oOut[k]*(1-oOut[k])*(filtrarEntrada(ex[len(ex)-1][k])-oOut[k]))

			#Para cada neurona intermedia calcular su error
			for j in range(nhidden):
				suma = 0
				for k in range(nout):
					suma += hidW[j][k]*errorOut[k]
				errorHidden.append(oHidden[j]*(1-oHidden[j])*suma)

			# Actualizacion de Pesos : 
			# # Actualizar pesos de las neuronas de input
			for j in range(nhidden):
				for i in range(nin) :
					initW[i][j] += rate*errorHidden[j]*ex[i]
				b0[j] += rate*errorHidden[j]

			# Actualizar pesos de las neuronas entre hidden y out
			for k in range(nout):
				for j in range(nhidden):
					hidW[j][k] += rate*errorOut[k]*oHidden[j]
				b1[k] += rate*errorOut[k]

			err = 0
			for k in range(len(ex[len(ex)-1])):
				err += pow(filtrarEntrada(ex[len(ex)-1][k])-oOut[k],2)
			errorIter += err/2        

		errorArray.append(errorIter)
		iterArray.append(aux)
		aux = aux + 1
	return initW,b0,hidW,b1,errorArray,iterArray

def graficador_circulo(xs,ys,adentro_afuera,tam_cir,tam_cuadr):
	plt.axes()
	i=0
	plt.axis("equal")
	centro = tam_cuadr/2
	while i < len(xs):
		if ( math.sqrt(math.fabs(centro-xs[i])**2+math.fabs(centro-ys[i])**2) < tam_cir):
			if adentro_afuera[i] == 1:
				plt.plot(xs[i],ys[i],'bo')
			else:
				plt.plot(xs[i],ys[i],'r^')
		else:
			if adentro_afuera[i] == 1:
				plt.plot(xs[i],ys[i],'gs')
			else:
				plt.plot(xs[i],ys[i],'m+')	
		i=i+1
	circle = plt.Circle((centro,centro), radius=tam_cir, fc='y')
	plt.gca().add_patch(circle)
	plt.axis([0,tam_cuadr,0,tam_cuadr])
	plt.show()

def readFile(inputLines,inp):
	outputArray = []
	i = 0
	for line in inputLines:
		line = line.split(' ')
		outputArray.append([])
		j = 0
		if inp :
			while j < (len(line)-1):
				outputArray[i].append(float(line[j]))
				j+=1

			outputArray[i].append(list(line[j]))

			z = 0
			while z < len(outputArray[i][j]):
				outputArray[i][j][z] = float(outputArray[i][j][z])
				z+=1
		else :
			while j < len(line):
				outputArray[i].append(float(line[j]))
				j+=1
		i+=1

	return outputArray

def normalizar(matrix,rows,cols) :
	maxAct = 1
	maxArr = []
	# Buscar el maximo de las columnas
	for j in range(cols) :
		for i in range(rows) :
			if matrix[i][j] > maxAct : 
				maxAct = matrix[i][j]
		maxArr.append(maxAct)

	# Usando el maximo de cada columna, dividir cada elemento de dicha columna
	# por ese maximo
	for j in range(cols) :
		for i in range(rows):
			matrix[i][j] = matrix[i][j] / maxArr[j]

	return None



if __name__ == '__main__':
	finput = open(sys.argv[1],'r')
	ftest = open(sys.argv[2],'r')
	foutput = open(sys.argv[3],'w+')

	inputLines = finput.read().splitlines()
	testLines = ftest.read().splitlines()

	trainingSet = []
	testSet = []

	# Lee los archivos y los coloca en arreglos
	trainingSet = readFile(inputLines,True)
	testSet = readFile(testLines,False)

	# # Normaliza el trainingSet y el testSet
	# normalizar(trainingSet,len(trainingSet),len(trainingSet[0])-1)
	# normalizar(testSet,len(testSet),len(testSet[0]))

	initW,b0,hidW,b1,errArr,iterArr = backPropagation(trainingSet,0.1,4,3,4,10000)
	# # plt.plot(errArr,iterArr)
	# # plt.xlabel('Error')
	# # plt.ylabel('Iteraciones')
	# # plt.show()
	# # exit(1)
	for p in range(0,len(testSet)):
		oHidden = calcularO(initW,testSet[p],b0,4,4)
		oOut = calcularO(hidW,oHidden,b1,4,3)
		for elem in oOut :
			if (elem >= 0.5) : 
				foutput.write("1")
			else :
				foutput.write("0")
			foutput.write(" ")
		foutput.write('\n')

	finput.close()
	ftest.close()
	foutput.close()
	# graficador_circulo([10,11,2,3],[10,11,2,3],[1,-1,1,-1],7,20)
