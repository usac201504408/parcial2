import socket
import binascii
import os 
import logging

#JPGM Crea un socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP_ADDR = 'localhost' 
IP_ADDR_ALL = ''
IP_PORT = 9800
BUFFER_SIZE = 64 * 1024
serverAddress = (IP_ADDR_ALL, IP_PORT) 
print('Iniciando servidor en {}, puerto {}'.format(*serverAddress))
sock.bind(serverAddress) 
sock.listen(10) 

while True:
 
    print('Esperando conexion remota')
    connection, clientAddress = sock.accept()
    try:
        print('Conexion establecida desde', clientAddress)

       
        while True:
            data = connection.recv(BUFFER_SIZE)
            print('Recibido: {!r}'.format(data))
            if data == binascii.unhexlify("01"): #JPGM recibio peticion de grabar audio
                print('esperando para grabar audio, notificar al cliente que indique tiempo')
                #grabar audio
                # os.system('arecord -d 10 -f U8 -r 8000 prueba.mp3')
                connection.sendall(binascii.unhexlify("CC"))#decirle al cliente que recibi su peticion de grabar audio
                while True:
                    #ESPERAR DEL CLIENTE OTRA INSTRUCCION
                    data2 = connection.recv(BUFFER_SIZE)
                    data2 = data2.decode()
                    print('Recibido: {!r}'.format(data2))
                    if data2:#si se recibio algo
                        connection.sendall(binascii.unhexlify("CC"))#notifico que recibi
                        tiempo = data2
                        comandoGrabacion = "arecord -d " + tiempo + " -f U8 -r 8000 201504408_server.wav"
                        os.system(comandoGrabacion)
                        connection.sendall(binascii.unhexlify("CC"))
                        break
            elif data == binascii.unhexlify("02"): #JPGM recibio peticion de mandar el audio
                pass
               
            elif data == binascii.unhexlify("03"):                
                print('Transmision finalizada desde el cliente ', clientAddress)
                break
    
    except KeyboardInterrupt:
        sock.close()

    finally:
        # Se baja el servidor para dejar libre el puerto para otras aplicaciones o instancias de la aplicacion
        connection.close()