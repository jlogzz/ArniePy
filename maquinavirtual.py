import sys

class maquinaVirtual:
	#variable type counters
	countLocInt = 0 #counter of local Int variables #countLocInt

	countLocFloat = 0 #counter of Float variables #countLocFloat

	countLocText = 0 #counter of Local Text variables #countLocText

	#rest of variable declaration
	dirProcedures = None #Actual directory for procedures #dirProcs

	currentQuadruple = 0	#Container with current quadruple in exec #cuadruploActual

	quadruples = None	#List of quadruples  #cuadruplos

	memoria = [[[],[],[]],[[],[],[]]] #[[[Global Int], [Global Float], [global Text]], [[Local Int], [Local Float], [Local Text]]]

	currentSpace = []  #Amount of current space of the function in use [LocalInt, LocalFloat, LocalText] #cantidadEspacioActual

	functionReference = [] #Guarda los parametros que se mandan por referencia #referenciaFuncion

	saveCurrentDirectionFunc = [] #Guarda la direccion de la funcion actual para cuando termine la llamada a funcion pueda regresar al cuadruplo que se encontraba #guardarDireccionFuncionActual

	listaAtributos = [] #Los atributos de las clases del metodo que fue llamado

	directionFunctionResult = [] #Saves the direction in memory whith the return value of a function  Guarda la direccion de memoria que va a tener el resultado del retorno de una funcion


	def __init__(self, dirProcedures, quadruples, countGlobalInt, countGlobalFloat, countGlobalText, countInitInt, countInitFloat, countInitText):
		self.dirProcedures = dirProcedures
		self.quadruples = quadruples
		self.memoria[0][0] = [0] * countGlobalInt
		self.memoria[0][1] = [0.0] * countGlobalFloat
		self.memoria[0][2] = [""] * countGlobalText
		self.memoria[1][0] = [0] * countInitInt
		self.memoria[1][1] = [0.0] * countInitFloat
		self.memoria[1][2] = [""] * countInitText
		self.countLocInt = countInitInt
		self.contLocalFloat = countInitFloat
		self.countLocText = countInitText
		self.currentSpace.append([countInitInt,countInitFloat, countInitText])

		while (self.quadruples[self.currentQuadruple][0] != "end"):
			if self.quadruples[self.currentQuadruple][0] in ["+", "-", "*", "/", "==", ">", "&&", "||", "<", "!=", ">=", "<="]:
				self.operacion(self.quadruples[self.currentQuadruple][0])

			elif self.quadruples[self.currentQuadruple][0] == "goto":
				self.currentQuadruple = self.quadruples[self.currentQuadruple][3] - 1 #minus one beacause it starts with 0 index

			elif self.quadruples[self.currentQuadruple][0] == "=": # prob int listas
				self.assign()

			elif self.quadruples[self.currentQuadruple][0] == "endproc": # ya
				self.endproc()

			elif self.quadruples[self.currentQuadruple][0] == "era": # ya
				self.era()

			elif self.quadruples[self.currentQuadruple][0] == "param": # ya prob int listas att
				self.param()

			elif self.quadruples[self.currentQuadruple][0] == "gotof": # ya prob int listas
				self.gotof()

			elif self.quadruples[self.currentQuadruple][0] == "gosub": # ya
				self.gosub()

			elif self.quadruples[self.currentQuadruple][0] == "print": # ya
				self.printf()

			elif self.quadruples[self.currentQuadruple][0] == "read": # ya
				self.read()

			elif self.quadruples[self.currentQuadruple][0] == "returnDir": #ya
				self.returnDir()

			elif self.quadruples[self.currentQuadruple][0] == "result": # ya
				self.saveReturnDir()

			elif self.quadruples[self.currentQuadruple][0] == "ver":
				self.validarRango()

			elif self.quadruples[self.currentQuadruple][0] == "atributo":
				self.atributo()

			self.currentQuadruple = self.currentQuadruple + 1 #next quadruple

	# Prints the value of the quadruple in the console
	def printf(self):
		aux1 = None
		if type(self.quadruples[self.currentQuadruple][3]) is int:
			memoPos = self.getMemPos(self.quadruples[self.currentQuadruple][3]) #saves int in memPos
			aux1 = self.memoria[memoPos[0]][memoPos[1]][memoPos[2]]

		elif type(self.quadruples[self.currentQuadruple][3]) is list:
			aux1 = self.quadruples[self.currentQuadruple][3][0]	#saves list in aux1 you want to print
			if type(aux1) is list:
				memoPos = self.getMemPos(aux1[0])
				aux1 = self.memoria[memoPos[0]][memoPos[1]][memoPos[2]]
				memoPos = self.getMemPos(aux1)
				aux1 = self.memoria[memoPos[0]][memoPos[1]][memoPos[2]]
		else:
			i = 0
			while i < len(self.listaAtributos):
				if self.listaAtributos[i][0] == self.quadruples[self.currentQuadruple][3]:
					memoPos = self.getMemPos(self.listaAtributos[i][1])
					aux1 = self.memoria[memoPos[0]][memoPos[1]][memoPos[2]]
				i = i + 1

		print(aux1)


	#Regresa el id de la clase padre que se encuentra dentro del directorio de procedimientos.
	#def obtenerIdClasePadre(self,clase):
	#	return self.dirProcedures[clase,0][0]

	#Calcula el tamano que va a requerir una funcion para generar espacio en la memoria.
	#Retorna en formato [cantenteros,cantdecimales,canttexto]
	def getFuncSize(self):
		if type(self.quadruples[self.currentQuadruple][3]) is list:	# if it's a list return nothing
			return
		#clase = None
		#clase = self.quadruples[self.currentQuadruple][2]
		function = self.quadruples[self.currentQuadruple][3]
		#if clase != None:
		#	idClasePadre = self.obtenerIdClasePadre(clase)
		#	idfunction = None
		#	for i in self.dirProcedures[clase,0][3]:
		#		if i[0] == function:
		#			idfunction = i[1]
		#	return self.dirProcedures[function,idfunction][3]
		#else:
		return self.dirProcedures[function,0][3]

	# Guarda las direcciones de los atributos de un objeto para procesar con los metodos
	def atributo(self):
		atributo = self.quadruples[self.currentQuadruple][2]
		direccion = self.quadruples[self.currentQuadruple][3]
		self.listaAtributos.append([atributo,direccion])

	# Realiza las operaciones basicas entre dos operadores y lo guarda en una direccion temporal
	def operacion(self, op):
		aux1 = 0
		aux2 = 0
		if type(self.quadruples[self.currentQuadruple][1]) is int:
			posEnMemoria = self.getMemPos(self.quadruples[self.currentQuadruple][1])
			aux1 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]

		elif type(self.quadruples[self.currentQuadruple][1]) is list:
			aux1 = self.quadruples[self.currentQuadruple][1][0]
			if type(aux1) is list:
				posEnMemoria = self.getMemPos(aux1[0])
				aux1 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]
				posEnMemoria = self.getMemPos(aux1)
				aux1 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]

		else:
			i = 0
			while i < len(self.listaAtributos):
				if self.listaAtributos[i][0] == self.quadruples[self.currentQuadruple][1]:
					posEnMemoria = self.getMemPos(self.listaAtributos[i][1])
					aux1 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]
				i = i + 1


		if type(self.quadruples[self.currentQuadruple][2]) is int:
			posEnMemoria = self.getMemPos(self.quadruples[self.currentQuadruple][2])
			aux2 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]

		elif type(self.quadruples[self.currentQuadruple][2]) is list:
			aux2 = self.quadruples[self.currentQuadruple][2][0]
			if type(aux2) is list:
				posEnMemoria = self.getMemPos(aux2[0])
				aux2 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]
				posEnMemoria = self.getMemPos(aux2)
				aux2 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]
		else:
			i = 0
			while i < len(self.listaAtributos):
				if self.listaAtributos[i][0] == self.quadruples[self.currentQuadruple][2]:
					posEnMemoria = self.getMemPos(self.listaAtributos[i][1])
					aux2 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]
				i = i + 1

		posEnMemoria = self.getMemPos(self.quadruples[self.currentQuadruple][3])

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
				self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = True
			else:
				self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = False
		elif op == ">":
			if aux1 > aux2:
				self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = True
			else:
				self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = False
		elif op == "&&":
			if aux1 and aux2:
				self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = True
			else:
				self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = False
		elif op == "||":
			if aux1 or aux2:
				self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = True
			else:
				self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = False
		elif op == "<":
			if aux1 < aux2:
				self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = True
			else:
				self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = False
		elif op == "!=":
			if aux1 != aux2:
				self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = True
			else:
				self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = False
		elif op == ">=":
			if aux1 >= aux2:
				self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = True
			else:
				self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = False
		elif op == "<=":
			if aux1 <= aux2:
				self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = True
			else:
				self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = False

	# Recibe una direccion virtual de memoria y la transforma a una real
	# Retorna en formato [globalOLocal,Entero/Decimal/Texto,posicionDentroDeLaLista]
	# Ej. [0,1,10]

	def getMemPos(self, direccion): #obtenerPosEnMemoria
		posEnMemoria = [0, 0, 0]
		if direccion >= 15000:
			posEnMemoria[0] = 1 #Local Variable
			if direccion >= 15000 and direccion < 25000:
				posEnMemoria[1] = 0
				posEnMemoria[2] = direccion - 15000 - self.cantidadEspacioActual[len(self.cantidadEspacioActual) - 1][0] + self.countLocInt
				return posEnMemoria
			elif direccion >= 25000 and direccion < 35000:
				posEnMemoria[1] = 1
				posEnMemoria[2] = direccion - 25000 - self.cantidadEspacioActual[len(self.cantidadEspacioActual) - 1][1] + self.countLocalFloat
				return posEnMemoria
			elif direccion >= 35000 and direccion < 45000:
				posEnMemoria[1] = 2
				posEnMemoria[2] = direccion - 35000 - self.cantidadEspacioActual[len(self.cantidadEspacioActual) - 1][2] + self.countLocText
				return posEnMemoria
		else:
			if direccion < 5000:
				posEnMemoria[1] = 0 #Global Variable
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
	def read(self):
		if type(self.quadruples[self.currentQuadruple][3]) is int:
			memoPos = self.getMemPos(self.quadruples[self.currentQuadruple][3])

		elif type(self.quadruples[self.currentQuadruple][3]) is list:
			aux1 = self.quadruples[self.currentQuadruple][3][0]
			if type(aux1) is list:
				memoPos = self.getMemPos(aux1[0])
				aux1 = self.memoria[memoPos[0]][memoPos[1]][memoPos[2]]
				memoPos = self.getMemPos(aux1)
		else:
			i = 0
			while i < len(self.listaAtributos):
				if self.listaAtributos[i][0] == self.quadruples[self.currentQuadruple][3]:
					memoPos = self.getMemPos(self.listaAtributos[i][1])
				i = i + 1


		if memoPos[1] == 0:
			while True:
				try:
					self.memoria[memoPos[0]][memoPos[1]][memoPos[2]] = int(input('>> '))
					break
				except ValueError:
					print("Numero Invalido, Intente nuevamente")
		elif memoPos[1] == 1:
			while True:
				try:
					self.memoria[memoPos[0]][memoPos[1]][memoPos[2]] = float(input('>> '))
					break
				except ValueError:
					print("Numero invalido, Intente nuevamente")
		elif memoPos[1] == 2:
			self.memoria[memoPos[0]][memoPos[1]][memoPos[2]] = input('>> ')

	# El valor que se especifica en el cuadruplo es insertado a la direccion de memoria ya sea una variable, atributo o elemento de un arreglo
	def assign(self):
		aux1 = None
		print(self.quadruples[self.currentQuadruple][1])
		if type(self.quadruples[self.currentQuadruple][1]) is int:
			posEnMemoria = self.getMemPos(self.quadruples[self.currentQuadruple][1])
			print(posEnMemoria)
			aux1 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]


		elif type(self.quadruples[self.currentQuadruple][1]) is list:
			aux1 = self.quadruples[self.currentQuadruple][1][0]
			if type(aux1) is list:
				posEnMemoria = self.getMemPos(aux1[0])
				aux1 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]
				posEnMemoria = self.getMemPos(aux1)
				aux1 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]

		else:
			i = 0
			while i < len(self.listaAtributos):
				if self.listaAtributos[i][0] == self.quadruples[self.currentQuadruple][1]:
					posEnMemoria = self.getMemPos(self.listaAtributos[i][1])
					aux2 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]
				i = i + 1

		if type(self.quadruples[self.currentQuadruple][3]) is int:
			posEnMemoria = self.getMemPos(self.quadruples[self.currentQuadruple][3])

		elif type(self.quadruples[self.currentQuadruple][3]) is list:
			posEnMemoria = self.getMemPos(self.quadruples[self.currentQuadruple][3][0][0])
			aux = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]
			posEnMemoria = self.getMemPos(aux)
		else:
			i = 0
			while i < len(self.listaAtributos):
				if self.listaAtributos[i][0] == self.quadruples[self.currentQuadruple][3]:
					posEnMemoria = self.getMemPos(self.listaAtributos[i][1])
					aux2 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]
				i = i + 1


		if posEnMemoria[1] == 0:
			self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = int(aux1)
		elif posEnMemoria[1] == 1:
			self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = float(aux1)
		else:
			self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]] = str(aux1)

	# Checks how many local variables are needed from each type and increments memory space y cambia de contexto para entrar a una funcion nueva
	def era(self):
		self.functionReference.append([])
		aux = self.getFuncSize()
		self.currentSpace.append(aux)
		self.memoria[1][0] = self.memoria[1][0] + ([0] * aux[0])
		self.countLocInt = self.countLocInt + aux[0]

		self.memoria[1][1] = self.memoria[1][1] + ([0.0] * aux[1])
		self.countLocalFloat = self.countLocalFloat + aux[1]

		self.memoria[1][2] = self.memoria[1][2] + ([""] * aux[2])
		self.countLocText = self.countLocText + aux[2]

	# First it saves the direction of current function and then goes to the specified quadruple actualizing currentQuadruple
	def gosub(self):
		self.saveCurrentDirectionFunc.append(self.currentQuadruple)
		self.currentQuadruple = int(self.quadruples[self.currentQuadruple][3]) - 1

	# Si la condicion resulta en falso entonces el cuadruplo actual se mueve al cuadruplo que especifica el gotof
	def gotof(self):
		aux1 = None
		if type(self.quadruples[self.currentQuadruple][1]) is int:
			memoPos = self.getMemPos(self.quadruples[self.currentQuadruple][1])
			aux1 = self.memoria[memoPos[0]][memoPos[1]][memoPos[2]]

		elif type(self.quadruples[self.currentQuadruple][1]) is list:
			aux1 = self.quadruples[self.currentQuadruple][1][0]
			if type(aux1) is list:
				memoPos = self.getMemPos(aux1[0])
				aux1 = self.memoria[memoPos[0]][memoPos[1]][memoPos[2]]
				memoPos = self.getMemPos(aux1)
				aux1 = self.memoria[memoPos[0]][memoPos[1]][memoPos[2]]
		if aux1 == 0:
			self.currentQuadruple = self.quadruples[self.currentQuadruple][3] - 1

	# Se asignan valores a los parametros de una funcion y se revisa si son por referencia para insertar a la pila e parametros por refrencia
	def param(self):
		aux = self.quadruples[self.currentQuadruple]
		value = None
		if type(aux[3]) is int:
			memoPos = self.getMemPos(aux[3])

			if memoPos[0] == 0:
				value = self.memoria[memoPos[0]][memoPos[1]][memoPos[2]]
			else:
				value = self.memoria[memoPos[0]][memoPos[1]][memoPos[2] - self.currentSpace[len(self.currentSpace) - 2][memoPos[1]]]

		elif type(aux[3]) is list:
			value = aux[3][0]
			if type(value) is list:
				memoPos = self.getMemPos(value)
				value = self.memoria[memoPos[0]][memoPos[1]][memoPos[2]]
				memoPos = self.getMemPos(value)
				value = self.memoria[memoPos[0]][memoPos[1]][memoPos[2]]
		else:
			i = 0
			while i < len(self.listaAtributos):
				if self.listaAtributos[i][0] == aux[3]:
					memoPos = self.getMemPos(self.listaAtributos[i][1])
					value = self.memoria[memoPos[0]][memoPos[1]][memoPos[2]]
				i = i + 1


		memoPos = self.getMemPos(aux[2])
		self.memoria[memoPos[0]][memoPos[1]][memoPos[2]] = value
		if aux[1]:
			self.functionReference[len(self.functionReference) - 1].append([aux[2], aux[3]])

	# Borra la memoria local de la funcion que termino, se borra la lista de atributos para reiniciar los metodo y regresa los valores por referencia
	def endproc(self):
		self.currentQuadruple = self.saveCurrentDirectionFunc.pop()
		references = self.functionReference.pop()
		self.returnValuesByReference(references)
		aux = self.currentSpace.pop()
		if aux[0] > 0:
			del self.memoria[1][0][-aux[0]:]
			self.countLocInt = self.countLocInt - aux[0]
		if aux[1] > 0:
			del self.memoria[1][1][-aux[1]:]
			self.countLocalFloat = self.countLocalFloat - aux[1]
		if aux[2] > 0:
			del self.memoria[1][2][-aux[2]:]
			self.countLocText = self.countLocText - aux[2]

		del self.listaAtributos[:] # inecesario?

	# Se inserta el valor local a las variables que fueron referenciadas cambiando el valor en el contexto viejo
	def returnValuesByReference(self, references):
		for par in references:
			memoPos1 = self.getMemPos(par[0])
			if par[1] is list:
				memoPos2 = self.getMemPos(par[1][0][0])
				aux = self.memoria[memoPos2[0]][memoPos2[1]][memoPos2[2]]
				memoPos2 = self.getMemPos(aux)
			else:
				memoPos2 = self.getMemPos(par[1])
			self.memoria[memoPos2[0]][memoPos2[1]][memoPos2[2]- self.currentSpace[len(self.currentSpace) - 2][memoPos2[1]]] = self.memoria[posEnMemoria1[0]][posEnMemoria1[1]][posEnMemoria1[2]]

	# Le asigna un valor a una direccion en especifico
	def returnDir(self):
		aux1 = None

		if type(self.quadruples[self.currentQuadruple][3]) is int:
			memoPos = self.getMemPos(self.quadruples[self.currentQuadruple][3])
			aux1 = self.memoria[memoPos[0]][memoPos[1]][memoPos[2]]

		elif type(self.quadruples[self.currentQuadruple][3]) is list:
			aux1 = self.quadruples[self.currentQuadruple][3][0]
			if type(aux1) is list:
				memoPos = self.getMemPos(aux1)
				aux1 = self.memoria[memoPos[0]][memoPos[1]][memoPos[2]]

		else:
			i = 0
			while i < len(self.listaAtributos):
				if self.listaAtributos[i][0] == self.quadruples[self.currentQuadruple][3]:
					memoPos = self.getMemPos(self.listaAtributos[i][1])
					aux2 = self.memoria[memoPos[0]][memoPos[1]][memoPos[2]]
				i = i + 1

		if len(self.directionFunctionResult) > 0:
			memoPos2 = self.getMemPos(self.directionFunctionResult.pop())
			self.memoria[memoPos2[0]][memoPos2[1]][memoPos2[2]- self.currentSpace[len(self.currentSpace) - 2][memoPos2[1]]] = aux1

	# Guarda la direccion en la que se va a hacer el retorno de una funcion
	def saveReturnDir(self):
		self.directionFunctionResult.append(self.quadruples[self.currentQuadruple][3])

	# Revisa que el valor entero que llego se encuentre dentro del rango de los arreglos
	def validarRango(self):
		longLista = self.quadruples[self.currentQuadruple][3]
		aux1 = None
		if type(self.quadruples[self.currentQuadruple][1]) is int:
			posEnMemoria = self.getMemPos(self.quadruples[self.currentQuadruple][1])
			aux1 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]

		elif type(self.quadruples[self.currentQuadruple][1]) is list:
			aux1 = self.quadruples[self.currentQuadruple][1][0]
			if type(aux1) is list:
				posEnMemoria = self.getMemPos(aux1[0])
				aux1 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]
				posEnMemoria = self.getMemPos(aux1)
				aux1 = self.memoria[posEnMemoria[0]][posEnMemoria[1]][posEnMemoria[2]]
		if aux1 < 0 or aux1 > longLista:
			print ("Error en tiempo de ejecucion: Indice fuera de rango" )
			sys.exit()

m = maquinaVirtual(0,((),('=',2, '','a'),('=',3, '','b'),('+', 'a', 'b', 'a'),),2,0,0,0,0,0,0,0)
m.execute()
print m.a
