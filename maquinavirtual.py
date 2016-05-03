import sys

class maquinaVirtual:

	dirProcs = None	#Contiene el directorio de procedimientos

	cuadruploActual = 0	#Contador con el cuadruplo en ejecucion

	cuadruplos = None	#Lista que contienelos cuadruplos

	memoria = [[[],[],[]],[[],[],[]]] #[[[Global Entero], [Global Decimal], [Global Texto]], [[Local Entero], [Local Decimal], [Local Texto]]]

	cantidadEspacioActual = []  #Cantidad de espacio de la funcion actual [localEnteras, localDecimales, localTexto]

	referenciaFuncion = [] #Guarda los parametros que se mandan por referencia

	guardarDireccionFuncionActual = [] #Guarda la direccion de la funcion actual para cuando termine la llamada a funcion pueda regresar al cuadruplo que se encontraba

	listaAtributos = [] #Los atributos de las clases del metodo que fue llamado

	direccionResultadoFuncion = [] #Guarda la direccion de memoria que va a tener el resultado del retorno de una funcion

	contLocalInt = 0

	contLocalDecimal = 0

	contLocalTexto = 0

	def __init__(self, dirProcs, cuadruplos, contGlobalInt, contGlobalDecimal, contGlobalTexto, contInicioInt, contInicioDecimal, contInicioTexto):
		self.dirProcs = dirProcs
		self.cuadruplos = cuadruplos
		self.memoria[0][0] = [0] * contGlobalInt
		self.memoria[0][1] = [0.0] * contGlobalDecimal
		self.memoria[0][2] = [""] * contGlobalTexto
		self.memoria[1][0] = [0] * contInicioInt
		self.memoria[1][1] = [0.0] * contInicioDecimal
		self.memoria[1][2] = [""] * contInicioTexto
		self.contLocalInt = contInicioInt
		self.contLocalDecimal = contInicioDecimal
		self.contLocalTexto = contInicioTexto
		self.cantidadEspacioActual.append([contInicioInt,contInicioDecimal, contInicioTexto])

		while (self.cuadruplos[self.cuadruploActual][0] != "end"):
			if self.cuadruplos[self.cuadruploActual][0] in ["+", "-", "*", "/", "==", ">", "&&", "||", "<", "!=", ">=", "<="]:
				self.operacion(self.cuadruplos[self.cuadruploActual][0])

			elif self.cuadruplos[self.cuadruploActual][0] == "goto":
				self.cuadruploActual = self.cuadruplos[self.cuadruploActual][3] - 1

			elif self.cuadruplos[self.cuadruploActual][0] == "=":
				self.asignar()

			elif self.cuadruplos[self.cuadruploActual][0] == "endproc":
				self.endproc()

			elif self.cuadruplos[self.cuadruploActual][0] == "era":
				self.era()

			elif self.cuadruplos[self.cuadruploActual][0] == "param":
				self.param()

			elif self.cuadruplos[self.cuadruploActual][0] == "gotof":
				self.gotof()

			elif self.cuadruplos[self.cuadruploActual][0] == "gosub":
				self.gosub()

			elif self.cuadruplos[self.cuadruploActual][0] == "imprimir":
				self.imprimir()

			elif self.cuadruplos[self.cuadruploActual][0] == "leer":
				self.leer()

			elif self.cuadruplos[self.cuadruploActual][0] == "retornar":
				self.retornar()

			elif self.cuadruplos[self.cuadruploActual][0] == "resultado":
				self.guardarDireccionRetorno()

			elif self.cuadruplos[self.cuadruploActual][0] == "ver":
				self.validarRango()

			elif self.cuadruplos[self.cuadruploActual][0] == "atributo":
				self.atributo()

			self.cuadruploActual = self.cuadruploActual + 1

	# Imprime el valor del cuadruplo en la consola
	def imprimir(self):
		aux1 = None
		if type(self.cuadruplos[self.cuadruploActual][3]) is int:
			posEnMemoria = self.obtenerPosEnMemoria(self.cuadruplos[self.cuadruploActual][3])
			aux1 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]

		elif type(self.cuadruplos[self.cuadruploActual][3]) is list:
			aux1 = self.cuadruplos[self.cuadruploActual][3][0]
			if type(aux1) is list:
				posEnMemoria = self.obtenerPosEnMemoria(aux1[0])
				aux1 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]
				posEnMemoria = self.obtenerPosEnMemoria(aux1)
				aux1 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]
		else:
			i = 0
			while i < len(self.listaAtributos):
				if self.listaAtributos[i][0] == self.cuadruplos[self.cuadruploActual][3]:
					posEnMemoria = self.obtenerPosEnMemoria(self.listaAtributos[i][1])
					aux1 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]
				i = i + 1

		print(aux1)



	#Regresa el id de la clase padre que se encuentra dentro del directorio de procedimientos.
	def obtenerIdClasePadre(self,clase):
		return self.dirProcs[clase,0][0]

	#Calcula el tamano que va a requerir una funcion para generar espacio en la memoria.
	#Retorna en formato [cantenteros,cantdecimales,canttexto]
	def obtenerTamanioFuncion(self):
		if type(self.cuadruplos[self.cuadruploActual][3]) is list:
			return
		clase = None
		clase = self.cuadruplos[self.cuadruploActual][2]
		funcion = self.cuadruplos[self.cuadruploActual][3]
		if clase != None:
			idClasePadre = self.obtenerIdClasePadre(clase)
			idFuncion = None
			for i in self.dirProcs[clase,0][3]:
				if i[0] == funcion:
					idFuncion = i[1]
			return self.dirProcs[funcion,idFuncion][3]
		else:
			return self.dirProcs[funcion,0][3]

	# Guarda las direcciones de los atributos de un objeto para procesar con los metodos
	def atributo(self):
		atributo = self.cuadruplos[self.cuadruploActual][2]
		direccion = self.cuadruplos[self.cuadruploActual][3]
		self.listaAtributos.append([atributo,direccion])

	# Realiza las operaciones basicas entre dos operadores y lo guarda en una direccion temporal
	def operacion(self, op):
		aux1 = 0
		aux2 = 0
		if type(self.cuadruplos[self.cuadruploActual][1]) is int:
			posEnMemoria = self.obtenerPosEnMemoria(self.cuadruplos[self.cuadruploActual][1])
			aux1 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]

		elif type(self.cuadruplos[self.cuadruploActual][1]) is list:
			aux1 = self.cuadruplos[self.cuadruploActual][1][0]
			if type(aux1) is list:
				posEnMemoria = self.obtenerPosEnMemoria(aux1[0])
				aux1 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]
				posEnMemoria = self.obtenerPosEnMemoria(aux1)
				aux1 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]

		else:
			i = 0
			while i < len(self.listaAtributos):
				if self.listaAtributos[i][0] == self.cuadruplos[self.cuadruploActual][1]:
					posEnMemoria = self.obtenerPosEnMemoria(self.listaAtributos[i][1])
					aux1 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]
				i = i + 1


		if type(self.cuadruplos[self.cuadruploActual][2]) is int:
			posEnMemoria = self.obtenerPosEnMemoria(self.cuadruplos[self.cuadruploActual][2])
			aux2 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]

		elif type(self.cuadruplos[self.cuadruploActual][2]) is list:
			aux2 = self.cuadruplos[self.cuadruploActual][2][0]
			if type(aux2) is list:
				posEnMemoria = self.obtenerPosEnMemoria(aux2[0])
				aux2 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]
				posEnMemoria = self.obtenerPosEnMemoria(aux2)
				aux2 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]
		else:
			i = 0
			while i < len(self.listaAtributos):
				if self.listaAtributos[i][0] == self.cuadruplos[self.cuadruploActual][2]:
					posEnMemoria = self.obtenerPosEnMemoria(self.listaAtributos[i][1])
					aux2 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]
				i = i + 1

		posEnMemoria = self.obtenerPosEnMemoria(self.cuadruplos[self.cuadruploActual][3])

		if op == "+":
			self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = aux1 + aux2
		elif op == "*":
			self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = aux1 * aux2
		elif op == "/":
			self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = aux1 / aux2
		elif op == "-":
			self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = aux1 - aux2
		elif op == "==":
			if aux1 == aux2:
				self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = 1
			else:
				self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = 0
		elif op == ">":
			if aux1 > aux2:
				self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = 1
			else:
				self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = 0
		elif op == "&&":
			if aux1 and aux2:
				self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = 1
			else:
				self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = 0
		elif op == "||":
			if aux1 or aux2:
				self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = 1
			else:
				self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = 0
		elif op == "<":
			if aux1 < aux2:
				self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = 1
			else:
				self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = 0
		elif op == "!=":
			if aux1 != aux2:
				self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = 1
			else:
				self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = 0
		elif op == ">=":
			if aux1 >= aux2:
				self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = 1
			else:
				self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = 0
		elif op == "<=":
			if aux1 <= aux2:
				self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = 1
			else:
				self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = 0

	# Recibe una direccion virtual de memoria y la transforma a una real
	# Retorna en formato [globalOLocal,Entero/Decimal/Texto,posicionDentroDeLaLista]
	# Ej. [0,1,10]

	def obtenerPosEnMemoria(self, direccion):
		posEnMemoria = [0, 0, 0]
		if direccion >= 15000:
			posEnMemoria[0] = 1
			if direccion >= 15000 and direccion < 25000:
				posEnMemoria[1] = 0
				posEnMemoria[2] = direccion - 15000 - self.cantidadEspacioActual[len(self.cantidadEspacioActual) - 1][0] + self.contLocalInt
				return posEnMemoria
			elif direccion >= 25000 and direccion < 35000:
				posEnMemoria[1] = 1
				posEnMemoria[2] = direccion - 25000 - self.cantidadEspacioActual[len(self.cantidadEspacioActual) - 1][1] + self.contLocalDecimal
				return posEnMemoria
			elif direccion >= 35000 and direccion < 45000:
				posEnMemoria[1] = 2
				posEnMemoria[2] = direccion - 35000 - self.cantidadEspacioActual[len(self.cantidadEspacioActual) - 1][2] + self.contLocalTexto
				return posEnMemoria
		else:
			if direccion < 5000:
				posEnMemoria[1] = 0
				posEnMemoria[2] = direccion
				return posEnMemoria
			elif direccion >= 5000 and direccion < 10000:
				posEnMemoria[1] = 1
				posEnMemoria[2] = direccion - 5000
				return posEnMemoria
			elif direccion >= 10000 and direccion < 15000:
				posEnMemoria[1] = 2
				posEnMemoria[2] = direccion - 10000
				return posEnMemoria

	# Lee un valor de la consola
	def leer(self):
		if type(self.cuadruplos[self.cuadruploActual][3]) is int:
			posEnMemoria = self.obtenerPosEnMemoria(self.cuadruplos[self.cuadruploActual][3])

		elif type(self.cuadruplos[self.cuadruploActual][3]) is list:
			aux1 = self.cuadruplos[self.cuadruploActual][3][0]
			if type(aux1) is list:
				posEnMemoria = self.obtenerPosEnMemoria(aux1[0])
				aux1 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]
				posEnMemoria = self.obtenerPosEnMemoria(aux1)
		else:
			i = 0
			while i < len(self.listaAtributos):
				if self.listaAtributos[i][0] == self.cuadruplos[self.cuadruploActual][3]:
					posEnMemoria = self.obtenerPosEnMemoria(self.listaAtributos[i][1])
				i = i + 1


		if posEnMemoria[1] == 0:
			while True:
				try:
					self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = int(input('>> '))
					break
				except ValueError:
					print("Numero Invalido, Intente nuevamente")
		elif posEnMemoria[1] == 1:
			while True:
				try:
					self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = float(input('>> '))
					break
				except ValueError:
					print("Numero invalido, Intente nuevamente")
		elif posEnMemoria[1] == 2:
			self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = input('>> ')

	# El valor que se especifica en el cuadruplo es insertado a la direccion de memoria ya sea una variable, atributo o elemento de un arreglo
	def asignar(self):
		aux1 = None
		if type(self.cuadruplos[self.cuadruploActual][1]) is int:
			posEnMemoria = self.obtenerPosEnMemoria(self.cuadruplos[self.cuadruploActual][1])
			aux1 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]

		elif type(self.cuadruplos[self.cuadruploActual][1]) is list:
			aux1 = self.cuadruplos[self.cuadruploActual][1][0]
			if type(aux1) is list:
				posEnMemoria = self.obtenerPosEnMemoria(aux1[0])
				aux1 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]
				posEnMemoria = self.obtenerPosEnMemoria(aux1)
				aux1 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]

		else:
			i = 0
			while i < len(self.listaAtributos):
				if self.listaAtributos[i][0] == self.cuadruplos[self.cuadruploActual][1]:
					posEnMemoria = self.obtenerPosEnMemoria(self.listaAtributos[i][1])
					aux2 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]
				i = i + 1

		if type(self.cuadruplos[self.cuadruploActual][3]) is int:
			posEnMemoria = self.obtenerPosEnMemoria(self.cuadruplos[self.cuadruploActual][3])

		elif type(self.cuadruplos[self.cuadruploActual][3]) is list:
			posEnMemoria = self.obtenerPosEnMemoria(self.cuadruplos[self.cuadruploActual][3][0][0])
			aux = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]
			posEnMemoria = self.obtenerPosEnMemoria(aux)
		else:
			i = 0
			while i < len(self.listaAtributos):
				if self.listaAtributos[i][0] == self.cuadruplos[self.cuadruploActual][3]:
					posEnMemoria = self.obtenerPosEnMemoria(self.listaAtributos[i][1])
					aux2 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]
				i = i + 1


		if posEnMemoria[1] == 0:
			self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = int(aux1)
		elif posEnMemoria[1] == 1:
			self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = float(aux1)
		else:
			self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = str(aux1)

	# Revisa cuantas variables locales requiere de cada tipo y aumenta la memoria y cambia de contexto para entrar a una funcion nueva
	def era(self):
		self.referenciaFuncion.append([])
		aux = self.obtenerTamanioFuncion()
		self.cantidadEspacioActual.append(aux)
		self.memoria[1][0] = self.memoria[1][0] + ([0] * aux[0])
		self.contLocalInt = self.contLocalInt + aux[0]

		self.memoria[1][1] = self.memoria[1][1] + ([0.0] * aux[1])
		self.contLocalDecimal = self.contLocalDecimal + aux[1]

		self.memoria[1][2] = self.memoria[1][2] + ([""] * aux[2])
		self.contLocalTexto = self.contLocalTexto + aux[2]

	# Va al numero de cuadruplo especificado por el cuadruplo y se guarda el actual para volver una vez que termine la funcion
	def gosub(self):
		self.guardarDireccionFuncionActual.append(self.cuadruploActual)
		self.cuadruploActual = int(self.cuadruplos[self.cuadruploActual][3]) - 1

	# Si la condicion resulta en falso entonces el cuadruplo actual se mueve al cuadruplo que especifica el gotof
	def gotof(self):
		aux1 = None
		if type(self.cuadruplos[self.cuadruploActual][1]) is int:
			posEnMemoria = self.obtenerPosEnMemoria(self.cuadruplos[self.cuadruploActual][1])
			aux1 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]

		elif type(self.cuadruplos[self.cuadruploActual][1]) is list:
			aux1 = self.cuadruplos[self.cuadruploActual][1][0]
			if type(aux1) is list:
				posEnMemoria = self.obtenerPosEnMemoria(aux1[0])
				aux1 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]
				posEnMemoria = self.obtenerPosEnMemoria(aux1)
				aux1 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]
		if aux1 == 0:
			self.cuadruploActual = self.cuadruplos[self.cuadruploActual][3] - 1

	# Se asignan valores a los parametros de una funcion y se revisa si son por referencia para insertar a la pila e parametros por refrencia
	def param(self):
		aux = self.cuadruplos[self.cuadruploActual]
		valor = None
		if type(aux[3]) is int:
			posEnMemoria = self.obtenerPosEnMemoria(aux[3])

			if posEnMemoria[0] == 0:
				valor = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]
			else:
				valor = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2] - self.cantidadEspacioActual[len(self.cantidadEspacioActual) - 2][posEnMemoria[1]]]

		elif type(aux[3]) is list:
			valor = aux[3][0]
			if type(valor) is list:
				posEnMemoria = self.obtenerPosEnMemoria(valor)
				valor = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]
				posEnMemoria = self.obtenerPosEnMemoria(valor)
				valor = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]
		else:
			i = 0
			while i < len(self.listaAtributos):
				if self.listaAtributos[i][0] == aux[3]:
					posEnMemoria = self.obtenerPosEnMemoria(self.listaAtributos[i][1])
					valor = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]
				i = i + 1


		posEnMemoria = self.obtenerPosEnMemoria(aux[2])
		self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = valor
		if aux[1]:
			self.referenciaFuncion[len(self.referenciaFuncion) - 1].append([aux[2], aux[3]])

	# Borra la memoria local de la funcion que termino, se borra la lista de atributos para reiniciar los metodo y regresa los valores por referencia
	def endproc(self):
		self.cuadruploActual = self.guardarDireccionFuncionActual.pop()
		referencias = self.referenciaFuncion.pop()
		self.regresaValoresPorReferencia(referencias)
		aux = self.cantidadEspacioActual.pop()
		if aux[0] > 0:
			del self.memoria[1][0][-aux[0]:]
			self.contLocalInt = self.contLocalInt - aux[0]
		if aux[1] > 0:
			del self.memoria[1][1][-aux[1]:]
			self.contLocalDecimal = self.contLocalDecimal - aux[1]
		if aux[2] > 0:
			del self.memoria[1][2][-aux[2]:]
			self.contLocalTexto = self.contLocalTexto - aux[2]

		del self.listaAtributos[:]

	# Se inserta el valor local a las variables que fueron referenciadas cambiando el valor en el contexto viejo
	def regresaValoresPorReferencia(self, referencias):
		for par in referencias:
			posEnMemoria1 = self.obtenerPosEnMemoria(par[0])
			if par[1] is list:
				posEnMemoria2 = self.obtenerPosEnMemoria(par[1][0][0])
				aux = self.memoria[posEnMemoria2[0]][posEnMemoria2[1]][posEnMemoria2[2]]
				posEnMemoria2 = self.obtenerPosEnMemoria(aux)
			else:
				posEnMemoria2 = self.obtenerPosEnMemoria(par[1])
			self.memoria[posEnMemoria2[0]][posEnMemoria2[1]][posEnMemoria2[2]- self.cantidadEspacioActual[len(self.cantidadEspacioActual) - 2][posEnMemoria2[1]]] = self.memoria[posEnMemoria1[0]][posEnMemoria1[1]][posEnMemoria1[2]]

	# Le asigna un valor a una direccion en especifico
	def retornar(self):
		aux1 = None

		if type(self.cuadruplos[self.cuadruploActual][3]) is int:
			posEnMemoria = self.obtenerPosEnMemoria(self.cuadruplos[self.cuadruploActual][3])
			aux1 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]

		elif type(self.cuadruplos[self.cuadruploActual][3]) is list:
			aux1 = self.cuadruplos[self.cuadruploActual][3][0]
			if type(aux1) is list:
				posEnMemoria = self.obtenerPosEnMemoria(aux1)
				aux1 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]

		else:
			i = 0
			while i < len(self.listaAtributos):
				if self.listaAtributos[i][0] == self.cuadruplos[self.cuadruploActual][3]:
					posEnMemoria = self.obtenerPosEnMemoria(self.listaAtributos[i][1])
					aux2 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]
				i = i + 1

		if len(self.direccionResultadoFuncion) > 0:
			posEnMemoria2 = self.obtenerPosEnMemoria(self.direccionResultadoFuncion.pop())
			self.memoria[posEnMemoria2[0]][posEnMemoria2[1]][posEnMemoria2[2]- self.cantidadEspacioActual[len(self.cantidadEspacioActual) - 2][posEnMemoria2[1]]] = aux1

	# Guarda la direccion en la que se va a hacer el retorno de una funcion
	def guardarDireccionRetorno(self):
		self.direccionResultadoFuncion.append(self.cuadruplos[self.cuadruploActual][3])

	# Revisa que el valor entero que llego se encuentre dentro del rango de los arreglos
	def validarRango(self):
		longLista = self.cuadruplos[self.cuadruploActual][3]
		aux1 = None
		if type(self.cuadruplos[self.cuadruploActual][1]) is int:
			posEnMemoria = self.obtenerPosEnMemoria(self.cuadruplos[self.cuadruploActual][1])
			aux1 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]

		elif type(self.cuadruplos[self.cuadruploActual][1]) is list:
			aux1 = self.cuadruplos[self.cuadruploActual][1][0]
			if type(aux1) is list:
				posEnMemoria = self.obtenerPosEnMemoria(aux1[0])
				aux1 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]
				posEnMemoria = self.obtenerPosEnMemoria(aux1)
				aux1 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]
		if aux1 < 0 or aux1 > longLista:
			print ("Error en tiempo de ejecucion: Indice fuera de rango" )
			sys.exit()
