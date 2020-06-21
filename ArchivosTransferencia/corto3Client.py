import socket
import binascii

SERVER_IP   = 'localhost' #157.245.82.242
SERVER_PORT = 9800
BUFFER_SIZE = 64 * 1024
#comandos a enviar
grabarAudio = binascii.unhexlify("01")
getAudio = binascii.unhexlify("02")
desconectar = binascii.unhexlify("03")
recibidoServidor = binascii.unhexlify("CC")


# Se crea socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Se conecta al puerto donde el servidor se encuentra a la escucha
server_address = (SERVER_IP, SERVER_PORT)
print('Conectando a {} en el puerto {}'.format(*server_address))
sock.connect(server_address)

try:

    # Se envia un texto codificado EN BINARIO
    # message = "ENviando texto jp prueba 1 prueba 1 ENviando texto jp prueba 1 prueba 1"
    # message = message.encode()
    # print('\n\nEnviando el siguiente texto:  {!s}'.format(message))

    sock.sendall(grabarAudio) #Se envia utilizando "socket.sendall" 

    print("\n\n")

    # Esperamos la respuesta del ping servidor
    # bytesRecibidos = 0
    # bytesEsperados = len(grabarAudio)

    # #TCP envia por bloques de BUFFER_SIZE bytes
    # while bytesRecibidos < bytesEsperados:
    data = sock.recv(BUFFER_SIZE)
    if data == recibidoServidor: #recibi del servidor confirmacion, le envio un valor
        tiempo = input("¿Que duracion en segundos deseas para el archivo de audio?")
        tiempo = tiempo.encode()
        sock.sendall(tiempo)
        while True:
            data1 = sock.recv(BUFFER_SIZE)
            if data1 == recibidoServidor:
                #confirmado que se esta grabando el audio. espero a que me confirme de nuevo que ya esta
                while True:
                    data2 = sock.recv(BUFFER_SIZE)
                    if data2 ==recibidoServidor: # ya termino
                        break
                
        
    

    #bytesRecibidos += len(data)
    print('Recibido: {!s}'.format(data))

finally:
    print('\n\nConexion finalizada con el servidor')
    sock.close()