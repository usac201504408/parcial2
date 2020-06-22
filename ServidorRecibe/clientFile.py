import socket
import os
import logging

SERVER_ADDR = 'localhost'
SERVER_PORT = 9800

BUFFER_SIZE = 65495

sock = socket.socket()
sock.connect((SERVER_ADDR, SERVER_PORT))
segundos = input("Cuantos segundos deseas grabar? ")
logging.basicConfig(
    level = logging.DEBUG, 
    format = '%(message)s'
    )


logging.info('Comenzando grabacion')
os.system('arecord -d '+segundos+' -f U8 -r 8000 prueba.mp3')

try:
    buff= BUFFER_SIZE
    with open('prueba.mp3', 'rb') as archivo: #Aca se guarda el archivo entrante
        sock.sendfile(archivo,0)

    archivo.close() #Se cierra el archivo

    print("Recepcion de archivo finalizada")

finally:
    print('Conexion al servidor finalizada')
    sock.shutdown(socket.SHUT_WR)
    sock.close() #Se cierra el socket