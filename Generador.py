# -*- encoding: utf-8 -*-

#!/usr/bin/env python3  

# -------------------------------------------------
#  Universidad Simón Bolívar
#  Inteligencia Artificial II
#  Prof. Ivette Carolina Martinez
#
#  Autores: Jorge Marcano   # Carnet : 11-10566
#           Maria Victoria Jorge  # Carnet : 
#			Fabio Castro # Carnet :
#
# Proyecto 1 - Redes Neurales
# -------------------------------------------------

import sys
import random
import math

global clase1
global clase2

def Circunferencia(x,y) :
	ecuacion = (((x - 10)**2) + ((y - 10)**2))

	if ecuacion >= 49: 
		# No forma parte de la circunferencia
		return 1
	else :
		# Forma parte de la circunferencia
		return -1

if __name__ == '__main__':

	clase1 = 0
	clase2 = 0

	numElems = sys.argv[1]
	f = open('datos'+str(numElems),'w+')
	
	while clase1+clase2 < int(numElems) : 
		x = random.uniform(0,20)
		y = random.uniform(0,20)
		c = Circunferencia(x,y)
		if (c == 1) and (clase1 < (int(numElems)/2)):
			clase1 = clase1+1
			f.write(str(x)+' '+str(y)+' '+str(c)+'\n')

		if (c == -1) and (clase2 <= (int(numElems)/2)):
			clase2 = clase2+1
			f.write(str(x)+' '+str(y)+' '+str(c)+'\n')


	f.close()


