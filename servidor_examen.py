#El servidor tiene más codigo porque tiene que recibir info de quien se conecta y se desconecta

import os  # Recibes info de los cores, los hilos...
import pickle #Pasar a binario de forma mas rapida
import socket #Para hablar con otra consola
import sys  #Te metes al sistema y sales, para hablar con él, puedes recibir info del sistema operativo
import threading # Instanciar hilos para realizar múltiples tareas simultáneamente


class Servidor(): #Creo una clase en vez de una función, no puedo llamarla más adelante
	#Un ejemplo de funcion sería el de multiplicación de matrices

	#Función para inicializarlo, necesitamos un host y un puerto
	def __init__(self, host=socket.gethostname(), port=int(input("Que puerto quiere usar ? "))):
		self.clientes = [] #Array cualquiera que vamos a depositar los clientes
		#NO EXISTE LÍMITE PARA HILOS, DEPENDE DE LA VERSIÓN DE PYTHON
		print('\nSu IP actual es : ',socket.gethostbyname(host))
		print('\n\tProceso con PID = ',os.getpid(), '\n\tHilo PRINCIPAL con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(), '\n\tTotal Hilos activos en este punto del programa =', threading.active_count())
		self.s = socket.socket() #Creo el socket
		self.s.bind((str(host), int(port))) #"Bindeo" (Enlazo/Conecto) el host y el puerto
		self.s.listen(30) #El servidor está esperando, le decimos que se ponga a la escucha
			#30 --> Veces que va a intentar conectarse hasta parar
		self.s.setblocking(False) #Pongo setblocking en false, el servidor va a recibir hilos de muchos lados
			#cuando tengo muchos hilos intentando conectarse a la vez ocurren deadlocks...
			#Le estamos diciendo que no se bloquee

		threading.Thread(target=self.aceptarC, daemon=True).start()
		threading.Thread(target=self.procesarC, daemon=True).start()

		#Bucle true con opción de apagar sevidor
		while True:
			msg = input('\n << SALIR = 1 >> \n')
			if msg == '1':
				print(" **** Me piro vampiro; cierro socket y mato SERVER con PID = ", os.getpid())
				#Dejo libre el socket
				with open("nicknameList.txt", "w") as f: 					##Creación del archivo donde vamos a guardar las cosas
					f.write(" ")
				self.s.close()
				sys.exit()
			else: pass

	def aceptarC(self):
		print('\nHilo ACEPTAR con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count())
		
		while True:
			try:
				conn, addr = self.s.accept() #Acepto la conexión
				print(f"\nConexion aceptada via {addr}\n ") #Imprimo todas las especificaciones técnicas (Protocolo UTP, UDP, bluetooth)
				#Para poder hacer el broadcast más adelante
				conn.setblocking(False) #Pongo el bloque a false
				self.clientes.append(conn) #Meto el cliente al array de clientes
				self.readNick()
			except: pass #Excepciones del try catch, "pasamos del problema a la siguiente linea" 

	def readNick(self):
		with open("nicknameList.txt", "r") as f: 							##Creación del archivo donde vamos a guardar las cosas
			print("Clientes conectados ahora [\n"+f.read()+"]")


	def procesarC(self): #Función procesar
		#Imrpime información
		print('\nHilo PROCESAR con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count())
		while True: #Tiene que estar todo el tiempo trabajando
			if len(self.clientes) > 0: #Si la longitud de clientes es mayor de 1, hago algo
				for c in self.clientes: #El array de clientes se conforma con la conexión y el ADR
					try:
						data = c.recv(256) #Data va a recibir 32 caracteres
						if data: self.broadcast(data,c)#Si data es verdadero hago broadcast
					except: pass


	def broadcast(self, msg, cliente): #
		aux = 0
		for c in self.clientes: #Recorremos el array clientes
			try:
				if c != cliente: 
					if aux == 0:
						print("\nClientes conectados Right now = ", len(self.clientes))
						self.readNick()
						print(pickle.loads(msg))
						aux = 1
					c.send(msg) #Enviamos el mensaje al cliente
			except: self.clientes.remove(c)

arrancar = Servidor() 