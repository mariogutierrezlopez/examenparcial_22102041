import threading #Librería para instanciar hilos
import sys #Funciones del sistema
import socket #Para hablar con otra consola
import pickle #Pasar a binario de forma mas rapida
import os #Sistema operativo

class Cliente(): #Clase cliente
	#Funcion init: Arranca el sistema con la IP y el puerto mediante el método __init__() que es el constructor
	def __init__(self,nickname = "", host=input("Intoduzca la IP del servidor ?  "), port=int(input("Intoduzca el PUERTO del servidor ?  "))):
		#Pregunta al sistema la IP y el puerto
		self.s = socket.socket() #Creo el objeto socket como atributo de cliente
		
		#Bucle while para obtener un string cliente válido
		while (nickname == ""):
			nickname = input("Introduce el nickname correctamente: ")
		self.nickname = nickname #Creo un atributo nickname en el objeto cliente y le doy el valor recibido por teclado

		#Abro un archivo nicknameList.txt en modo appends donde vamos a guardar el usuario
		with open("nicknameList.txt", "a") as f: 					
			f.write(self.nickname+"\n")		#Registro el nickname en este archivo txt
		self.s.connect((host, int(port))) #Me conecto al host y el puerto mediante el método socket.connect() el cual necesita una tupla con la IP y el puerto
		#Imprime el estado del programa
		print('\n\tProceso con PID = ',os.getpid(), '\n\tHilo PRINCIPAL con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tTotal Hilos activos en este punto del programa =', threading.active_count())
		
		#instanciamos un hilo demonio para que reciba la llamada, llama a la función recibir
		threading.Thread(target=self.recibir, daemon=True).start()
		
		#Un while que está todo el tiempo escuchando
		while True:
			msg = input('\nEscriba texto ?   ** Enviar = ENTER   ** Salir Chat = 1 \n') #Recibe el texto
			if msg != '1' : self.enviar(msg) #Si el mensaje no es 1 envia el mensaje
			else: #Si el mensaje es 1 se cierra el socket
				print(" **** Me piro vampiro; cierro socket y mato al CLIENTE con PID = ", os.getpid()) #Imprimimos mensaje de despedida
				self.deleteNick(nickname) #Eliminamos el nickname del archivo nicknameList.txt
				self.s.close() #Cerramos el socket con el método socket.close()
				sys.exit() #Cerramos el sistema
				#Si dejo abierto el socket, eso se queda ahí, "como cuando reservas una habitación de hotel y no la cancelas"
				#por lo tanto es necesario cerrar el cliente con esos métodos

	#Función para eliminar el nickname del archivo txt dejando los demás archivos guardados
	def deleteNick(self, nick):
		lineas = [] #Lineas es un array con los nicknames
		with open("nicknameList.txt", 'r') as f:	 #Abrimos el fichero nicknameLists en modo lectura				
					nicknames = f.readlines()		#Array nicknames
					for n in nicknames:				#Recorremos el array de nicknames buscando el nick que le entregamos a la función por parámetro
						if (nick not in n):			#Si no coincide, lo incluimos en el array lineas
							lineas.append(n)
		with open("nicknameList.txt", 'w') as f:	#Abro el archivo nicknameLists.txt en modo escritura
			for n in lineas:						#Creo un bucle for que va a escribir todos los usuarios restantes en el fichero
				f.write(n)

	#Función recibir
	def recibir(self):
		#Te imprime quien es el que está manejando recibir
		print('\nHilo RECIBIR con ID =',threading.currentThread().getName(), '\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count())
		#Bucle while que va a estar siempre escuchando
		while True:
			try:
				data = self.s.recv(256) #Creo una variable data que recibe el dato de alguien que ha escrito en el chat
					#El método es el método receive dentro del socket
					#256 --> Es la longitud del mensaje, cuanto más rapido mejor
				if data: print(pickle.loads(data)) #Imprimo lo que viene del otro lado de recibir
					#El método pickle es para convertir de binario a lenguaje natural
			except: pass #Si ocurre un error, que siga dando vueltas

	#Función enviar
	#Método send que tiene socket
	#El método pickle.dumps() convierte de lenguaje natural a binario
	def enviar(self, msg):
		self.s.send(pickle.dumps(self.nickname + ": " + msg)) #Enviamos un string de la forma "Usuario: Este es mi mensaje"

		with open("u22102041AI1.txt", "a") as f: #Abrimos el archivo de texto para guardar también el mensaje de forma que haya un log de arhcivos
			f.write(self.nickname + ": " + msg + "\n") #Escribimos en el fichero el mensaje


arrancar = Cliente() #Inicializamos el cliente

		