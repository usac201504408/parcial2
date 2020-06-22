#socket.sendfile() disponible desde Python 3.3

import socket

class servidor(): #creamos una clase para el servidor
    def __init__(self,a,p,b,p1): #definimos las variables iniciales a utilizar
        self.addr = a
        self.port = p
        self.port1 = p1
        self.buff = b #8 KB para buffer de transferencia de archivos

    def mandarservidor(self): #metodo para mandar un archivo de audio servidor
        server_socket = socket.socket()
        server_socket.bind((self.addr, self.port))
        server_socket.listen(10) #1 conexion activa y 9 en cola
        try:
            #while True:
                print("\nEsperando conexion remota...\n")
                conn, addr = server_socket.accept()
                print('Conexion establecida desde ', addr)
                print('Enviando archivo de audio')
                with open('prueba.mp3', 'rb') as f: #Se abre el archivo a enviar en BINARIO
                    conn.sendfile(f, 0)
                    f.close()
                conn.close()
                print("\n\nArchivo enviado a: ", addr)
        finally:
            print("Cerrando el servidor...")
            #server_socket.shutdown(socket.SHUT_RDWR)
            server_socket.close()

    def recibirservidor(self): #se crea un metodo para recibir un audio en el servidor
        server_socket = socket.socket()
        server_socket.bind((self.addr, self.port1))
        server_socket.listen(10) #1 conexion activa y 9 en cola
        try:
            #while True:
                print("\nEsperando conexion remota...\n")
                conn, addr = server_socket.accept()
                print('Conexion establecida desde ', addr)
                print('Enviando archivo de prueba de 5MB...')
                buff=self.buff
                with open('recibido.mp3', 'wb') as f: #Se abre el archivo a enviar en BINARIO
                    while buff:
                        buff = conn.recv(self.buff)
                        f.write(buff)
                    f.close()
                conn.close()
                print("\n\nArchivo enviado a: ", addr)
        finally:
            print("Cerrando el servidor...")
            #server_socket.shutdown()
            server_socket.close()

Datos= servidor('localhost' , 9800, 65495,9801) #Definimos los valores iniciales
Datos.mandarservidor()
#Datos.recibirservidor()