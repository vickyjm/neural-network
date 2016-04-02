import sys

def Circunferencia(x, y):
	ecuacion = (((x - 10)**2) + ((y - 10)**2))

	if ecuacion >= 49: 
		# No forma parte de la circunferencia
		return 1
	else :
		# Forma parte de la circunferencia
		return -1

if __name__ == '__main__':
	archivo = open('datosValidacion', 'w')

	for i in range(100):
		for j in range(100):
			x = i*20/100
			y = j*20/100
			clase = Circunferencia(x,y)
			archivo.write(str(x) + ' ' + str(y) + ' ' + str(clase) + '\n')

	archivo.close()