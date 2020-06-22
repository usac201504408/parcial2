#socket.sendfile() disponible desde Python 3.3

import socket

SERVER_ADDR = 'localhost'
SERVER_PORT = 9800


BUFFER_SIZE = 64 * 1024 #8 KB para buffer de transferencia de archivos

server_socket = socket.socket()
server_socket.bind((SERVER_ADDR, SERVER_PORT))
server_socket.listen(10) #1 conexion activa y 9 en cola
try:
    while True:
        print("\nEsperando conexion remota...\n")
        conn, addr = server_socket.accept()
        print('Conexion establecida desde ', addr)
        print('Enviando archivo de prueba de 5MB...')
        buff=BUFFER_SIZE
        with open('recibido.mp3', 'wb') as f: #Se abre el archivo a enviar en BINARIO
            while buff:
                buff = conn.recv(65495)
                f.write(buff)
            f.close()
        conn.close()
        print("\n\nArchivo enviado a: ", addr)
finally:
    print("Cerrando el servidor...")
    #server_socket.shutdown(socket.SHUT_WR)
    server_socket.close()