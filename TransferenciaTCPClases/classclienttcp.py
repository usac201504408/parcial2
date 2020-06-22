import socket
import os
import logging

class cliente():
    def __init__(self,a,p,b,p1):
        self.addr = a
        self.port = p
        self.buff = b
        self.port1 = p1

    def recibircliente(self): #creando metodo para recepcion de audio
        sock = socket.socket()
        sock.connect((self.addr, self.port))


        try:
            buff= self.buff
            archivo = open('recibido.mp3', 'wb') #Aca se guarda el archivo entrante
            while buff:
                buff = sock.recv(self.buff) 
                archivo.write(buff)

            archivo.close() #Se cierra el archivo

            print("Recepcion de archivo finalizada")

        finally:
            print('Conexion al servidor finalizada')
            sock.shutdown(socket.SHUT_WR)
            sock.close() #Se cierra el socket

    def enviarcliente(self): #creando metodo para envio de audio

        sock = socket.socket()
        sock.connect((self.addr, self.port1))
        segundos = input("Cuantos segundos deseas grabar? ")
        logging.basicConfig(
            level = logging.DEBUG, 
            format = '%(message)s'
            )


        logging.info('Comenzando grabacion')
        os.system('arecord -d '+segundos+' -f U8 -r 8000 prueba.mp3')

        try:
            buff= self.buff
            with open('prueba.mp3', 'rb') as archivo: #Aca se guarda el archivo entrante
                sock.sendfile(archivo,0)

            archivo.close() #Se cierra el archivo

            print("Recepcion de archivo finalizada")

        finally:
            print('Conexion al servidor finalizada')
            sock.shutdown(socket.SHUT_WR)
            sock.close() #Se cierra el socket

Datos= cliente('localhost' , 9800, 65495,9801)
Datos.recibircliente()
#Datos.enviarcliente()
#tengo 2 puertos porque tcp no me deja cerrar la conexion y reabrirla antes de 1 min