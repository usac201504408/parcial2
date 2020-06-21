#JPGM clase para manejo de cliente
#imports
import paho.mqtt.client as mqtt
from broker import *
from globalconst import *
import logging
import time
import lecturaArchivos
import comandosCliente
import threading
import binascii
import alive


#Configuracion inicial de logging
logging.basicConfig(
    level = logging.INFO, 
    format = '[%(levelname)s] (%(threadName)-10s) %(message)s'
    )


def postAlive():
    while True:
        #hago un publish para decir que estoy vivo
        trama = comandosCliente.comandosCliente().getTrama(COMMAND_ALIVE, "201504408")       
        # client.publish("comandos/14/201504408", trama, qos = 2, retain = False)
        time.sleep(20)

def negociacionRedireccion(destinatario, fileSize, nombreFile):
    
    if(str(destinatario).isdigit() == True): #es un carnet
        trama_redireccion = comandosCliente.comandosCliente().getTrama(COMMAND_FRR,destinatario,fileSize)
        client.publish("comandos/14/" + str(destinatario), trama_redireccion, qos = 2, retain = False)
        print("Enviando comando FRR al cliente destino " + str(destinatario) + " nombre archivo: " + str(nombreFile) + " de tamanio " + str(fileSize))
        #se empieza la transferencia
        pass
    else: #es una sala, tengo que enciclar hasta mandar a todos, revisando quienes estan en esa sala
        #con el archivo de listado de personas asignadas a salas
        usuariosRegistrados = lecturaArchivos.LecturaArchivo("usuarios.txt").getArreglo()
        for usuarioDestino in usuariosRegistrados:
            #recorro cada item del arreglo para ver si le toca recibir el archivo o no
            #verifico en todas las salas que tenga asignadas
            objetoUsuario = usuarioDestino.split(",") 
            carnetDestino = objetoUsuario[0]
            longitud = len(objetoUsuario)
            #si la longitud es mayor a dos, la persona esta asignada a alguna sala, si no no.
            if(longitud >= 2):
                for index in range(2,longitud - 1):
                    #voy verificando si la sala que tiene asignada es la destino
                    salaAsignada = objetoUsuario[index]
                    print("sala asignada de " + str(carnetDestino) + " es : " + str(salaAsignada))
                    if(salaAsignada == destinatario):
                        #si tiene asignada la sala, entonces le envio la trama        
                        trama_redireccion = comandosCliente.comandosCliente().getTrama(COMMAND_FRR,str(carnetDestino),fileSize)
                        client.publish("comandos/14/" + str(carnetDestino), trama_redireccion, qos = 2, retain = False)
                        print("Enviando comando FRR al cliente destino " + str(carnetDestino) + " nombre archivo: " + str(nombreFile) + " de tamanio " + str(fileSize))
        print("termino de enviar a todos los usuarios en la sala")
        


#Handler en caso suceda la conexion con el broker MQTT
def on_connect(client, userdata, flags, rc): 
    connectionText = "CONNACK recibido del broker con codigo: " + str(rc)
    logging.debug(connectionText)
    #Lanza el primer hilo con los parámetros:
    #name: Nombre "humano" para identificar fácil al hilo
    #target: La función a ejecutar (o método de un objeto)
    #args: argumentos, deben ser enviados como tupla
    #daemon: servicio corriendo de fondo -> permite detener el hilo con "Thread._stop()"
    t1 = threading.Thread(name = 'Contador de 1 segundo',
                            target = postAlive,
                            args = (()),
                            daemon = True
                        )
    t1.start()

#Handler en caso se publique satisfactoriamente en el broker MQTT
def on_publish(client, userdata, mid): 
    publishText = "Publicacion satisfactoria"
    logging.debug(publishText)
    


#Callback que se ejecuta cuando llega un mensaje al topic suscrito
def on_message(client, userdata, msg):
    #Se muestra en pantalla informacion que ha llegado
    logging.debug("Ha llegado el mensaje al topic: " + str(msg.topic))
    mensajedecode =  msg.payload.decode()
    arregloTrama_split = comandosCliente.comandosCliente().splitTramaCliente(msg.payload)
 

    if(arregloTrama_split[0].encode() == binascii.unhexlify("04")): #alive no muestro al cliente
        print("")
        print("El cliente del topic " + str(msg.topic) + " da el comando ALIVE y dice soy: " + str(arregloTrama_split[1]))
        logging.debug("El contenido del mensaje es: " + str(mensajedecode))
        trama_ack = comandosCliente.comandosCliente().getTrama(COMMAND_ACK, str(arregloTrama_split[1])) 
        client.publish("comandos/14/" + str(arregloTrama_split[1]), trama_ack, qos = 2, retain = False)
        #procedo a guardar a la lista de vivos al cliente
        remitente = str(msg.topic).split("/")[2]
        alive.alives().usuarioAlive(remitente)


    elif(arregloTrama_split[0].encode() == binascii.unhexlify("05")): #acknowledge del server
        # print("")
        # print("El cliente del topic " + str(msg.topic) + "da el comando ACK y dice: " + str(arregloTrama_split[1]))
        # logging.debug("El contenido del mensaje es: " + str(mensajedecode))
        pass
    elif(arregloTrama_split[0].encode() == binascii.unhexlify("03")): #trama FTR de cliente
        print("")
        print("El cliente del topic " + str(msg.topic) + " da el comando FTR para enviar a: " + str(arregloTrama_split[1]) + " el tamanio es de: " + str(arregloTrama_split[2]))
        logging.debug("El contenido del mensaje es: " + str(mensajedecode))
        #se procede a evaluar si le damos respuesta de NO o de OK
        #se extrae el remitente del topic    
        remitente = str(msg.topic).split("/")[2]
        trama_ok = comandosCliente.comandosCliente().getTrama(COMMAND_OK, str(remitente)) 
        client.publish("comandos/14/" + str(remitente), trama_ok, qos = 2, retain = False)
        print("Se envio un comando OK al cliente " + str(remitente))
        #se procede a recibir el archivo del cliente MESSI
        #luego de recibirlo procedo a hacer la negociacion con el destinatario, inicio un hilo
        nombreFile = "archivo.wav"
        destinatario = arregloTrama_split[1]
        tamanioFile =  arregloTrama_split[2]
        t2 = threading.Thread(name = 'Contador de 1 segundo',
                            target = negociacionRedireccion,
                            args = ((str(destinatario), str(tamanioFile), str(nombreFile))),
                            daemon = True
                        )
        t2.start()


  
   

#conexion a mqtt
#configurar al cliente como publisher y subscriber
client = mqtt.Client(clean_session=True) #Nueva instancia de cliente
client.on_connect = on_connect #Se configura la funcion "Handler" cuando suceda la conexion
client.on_message = on_message #Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
client.on_publish = on_publish #Se configura la funcion "Handler" que se activa al publicar algo
client.username_pw_set(MQTT_USER, MQTT_PASS) #Credenciales requeridas por el broker
client.connect(host=MQTT_HOST, port = MQTT_PORT) #Conectar al servidor remoto


#Nos conectaremos a distintos topics:
qos = 2
#suscribirse a todos los topics del archivo
topics = lecturaArchivos.LecturaArchivo("topics.txt").getArreglo()
for topic in topics:
    client.subscribe((str(topic), qos))



#Iniciamos el thread (implementado en paho-mqtt) para estar atentos a mensajes en los topics subscritos
client.loop_start()

#El thread de MQTT queda en el fondo, mientras en el main loop hacemos otra cosa
try:
    while True:
        pass


except KeyboardInterrupt:
    logging.warning("Desconectando del broker...")

finally:
    client.loop_stop() #Se mata el hilo que verifica los topics en el fondo
    client.disconnect() #Se desconecta del broker
    logging.info("Desconectado del broker. Saliendo...")