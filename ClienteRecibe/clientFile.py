import socket

SERVER_ADDR = 'localhost'
SERVER_PORT = 9800

BUFFER_SIZE = 65495

sock = socket.socket()
sock.connect((SERVER_ADDR, SERVER_PORT))


try:
    buff= BUFFER_SIZE
    archivo = open('recibido.mp3', 'wb') #Aca se guarda el archivo entrante
    while buff:
        buff = sock.recv(BUFFER_SIZE) #Los bloques se van agregando al archivo
        archivo.write(buff)

    archivo.close() #Se cierra el archivo

    print("Recepcion de archivo finalizada")

finally:
    print('Conexion al servidor finalizada')
    sock.shutdown(socket.SHUT_WR)
    sock.close() #Se cierra el socket