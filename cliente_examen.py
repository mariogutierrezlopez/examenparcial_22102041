import threading #Librería para instanciar hilos
import sys #Funciones del sistema
import socket #Para hablar con otra consola
import pickle #Pasar a binario de forma mas rapida
import os #Sistema operativo
import random
import multiprocessing as mp # Para trabajar en paralelo
import math
import time

class Cliente(): #Clase cliente
    #Funcion init: Arranca el sistema con la IP y el puerto mediante el método __init__() que es el constructor
    def __init__(self,nickname = "", host=input("Intoduzca la IP del servidor ?  "), port=int(input("Intoduzca el PUERTO del servidor ?  "))):
        #Pregunta al sistema la IP y el puerto
        self.s = socket.socket() #Creo el objeto socket como atributo de cliente
        #Bucle while para obtener un string cliente válido
        while (nickname == ""):
            nickname = input("Introduce el nickname correctamente: ")
        self.nickname = nickname #Creo un atributo nickname en el objeto cliente y le doy el valor recibido por teclado

        with open("nicknameList.txt", "a") as f: 					
            f.write(self.nickname+"\n")		#Registro el nickname en este archivo txt
        self.s.connect((host, int(port))) #Me conecto al host y el puerto mediante el método socket.connect() el cual necesita una tupla con la IP y el puerto
        #Imprime el estado del programa

        #LE ENVIO LOS DATOS AL SERVIDOR

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
    def par_core(A, B, MC, i_MC, f_MC): # La tarea que hacen todos los cores
        for i in range(i_MC, f_MC): # Size representado en colores en el excel que itera sobre las filas en A
            for j in range(len(B[0])): # Size representado en colores en el excel que itera sobre las columnas en B
                for k in range(len(A[0])): # n_fil_B o lo que es l mismo el n_col_A
                    MC[i*len(B[0]) + j] += A[i][k] * B[k][j]# Guarda resultado en MC[] de cada core

    def par_mult(A, B, self): # f() que prepara el reparto de trabajo para la mult. en paralelo
        n_fil_A = len(A) # Obtengo num de filas de A 
        n_col_A = len(A[0]) # Obtengo num de colunmas de A 
        n_fil_B = len(B) # Obtengo num de filas de B
        n_col_B = len(B[0]) # # Obtengo num de filas de B
        n_cores = mp.cpu_count() # Obtengo los cores de mi pc
        size_col = math.ceil(n_col_B/n_cores) # Columnas  a procesar x c/cpre, ver Excel adjunto
        size_fil = math.ceil(n_fil_A/n_cores) # Filas a procesar x c/cpre, ver Excel adjunto
        MC = mp.RawArray('i', n_fil_A * n_col_B) # Array MC de memoria compartida donde se almacenaran los resultados, ver excel adjunto
        cores = [] # Array para guardar los cores y su trabajo
        for core in range(n_cores):# Asigno a cada core el trabajo que le toca, ver excel adjunto
            i_MC = min(core * size_fil, n_fil_A) # Calculo i para marcar inicio del trabajo del core en relacion a las filas
            f_MC = min((core + 1) * size_fil, n_fil_A) # Calculo f para marcar fin del trabajo del core, ver excel
            cores.append(mp.Process(target=self.par_core, args=(A, B, MC, i_MC, f_MC)))# Añado al Array los cores y su trabajo
        for core in cores:
            core.start()# Arranco y ejecuto el trabajo para c/ uno de los cores que tenga mi equipo, ver excel
        for core in cores:
            core.join()# Bloqueo cualquier llamada hasta que terminen su trabajo todos los cores
        C_2D = [[0] * n_col_B for i in range(n_fil_A)] # Convierto el array unidimensional MC en una matrix 2D (C_2D) 
        for i in range(n_fil_A):# i para iterar sobre las filas de A
            for j in range(n_col_B):# j para iterar sobre las columnas de B
                C_2D[i][j] = MC[i*n_col_B + j] # Guardo el C_2D los datos del array MC
        return C_2D



    def recibir(self):
        #Te imprime quien es el que está manejando recibir
        print('\nHilo RECIBIR con ID =',threading.currentThread().getName(), '\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count())
        #Bucle while que va a estar siempre escuchando
        while True:
            try:
                data = self.s.recv(256) #Creo una variable data que recibe el dato de alguien que ha escrito en el chat
                    #El método es el método receive dentro del socket
                    #256 --> Es la longitud del mensaje, cuanto más rapido mejor
                if data:
                    print(pickle.loads(data)) #Imprimo lo que viene del otro lado de recibir
                    dimensiones = pickle.loads(data).split(';')

                    n_fil_A = dimensiones[0] # Obtengo num de filas de A 
                    n_col_A = dimensiones[1] # Obtengo num de colunmas de A 
                    n_fil_B = dimensiones[2] # Obtengo num de filas de B
                    n_col_B = dimensiones[3] # # Obtengo num de filas de B

                    A = [[random.randint(0,215) for i in range(n_col_A)] for j in range(n_fil_A)] # Genero A[22102041][6]con num. aleatorios del 0 al 215, ver excel 
                    B = [[random.randint(0,215) for i in range(n_col_B)] for j in range(n_fil_B)] # Genero B[6][22102041]con num. aleatorios del 0 al 215, ver excel
                    if n_col_A != n_fil_B: raise Exception('Dimensiones no validas') # Compruebo que se puedan multiplicar A y B
                    finS = time.time()
                    inicioP = time.time()
                    C = self.par_mult(A, B) # Ejecuto multiplicacion paralela
                    finP = time.time()
                    print('\n\nMatriz  A y B se han multiplicado con exito en SECUENCIAL ha tardado ', finS-inicioS, ' y en PARALELO ', finP-inicioP)
                    #El método pickle es para convertir de binario a lenguaje natural
                    fichero = open("examenparcial_22102041.txt","a")
                    with open("examenparcial_22102041.txt","a") as fichero:
                        fichero.write("Tiempo en SECUENCIAL " + str(finP - inicioP))
            except: pass #Si ocurre un error, que siga dando vueltas

    #Función enviar
    #Método send que tiene socket
    #El método pickle.dumps() convierte de lenguaje natural a binario
    def enviar(self, msg):
        self.s.send(pickle.dumps(self.nickname + ": " + msg)) #Enviamos un string de la forma "Usuario: Este es mi mensaje"

        with open("u22102041AI1.txt", "a") as f: #Abrimos el archivo de texto para guardar también el mensaje de forma que haya un log de arhcivos
            f.write(self.nickname + ": " + msg + "\n") #Escribimos en el fichero el mensaje


arrancar = Cliente() #Inicializamos el cliente