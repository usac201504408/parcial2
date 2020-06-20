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


#Configuracion inicial de logging
logging.basicConfig(
    level = logging.INFO, 
    format = '[%(levelname)s] (%(threadName)-10s) %(message)s'
    )


def postAlive():
    while True:
        #hago un publish para decir que estoy vivo
        trama = comandosCliente.comandosCliente().getTrama(COMMAND_ALIVE, "201504408")
        
        client.publish("comandos/14", trama, qos = 2, retain = False)
        time.sleep(20)


#Handler en caso suceda la conexion con el broker MQTT
def on_connect(client, userdata, flags, rc): 
    connectionText = "CONNACK recibido del broker con codigo: " + str(rc)
    logging.debug(connectionText)
    #AQUI COLOCAR HILO ALIVE

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
 
    if(arregloTrama_split[0].encode() != binascii.unhexlify("04")): #alive no muestro
        print("")
        print("Nuevo cliente del topic " + str(msg.topic) + " dice: " + str(arregloTrama_split[1]))
        logging.debug("El contenido del mensaje es: " + str(mensajedecode))
        
    
   

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
        logging.info("Esperando comando")
        print("Hola, bienvenido al chat del grupo 14, and i'll tell you all about it when i see you again")
        print("Menu")
        print("1. Enviar texto")
        print("2. Enviar mensaje de voz")
        print("3.  Salir")
        print("")
        menu1 = input("¿Que opcion deseas? : ")  
        if(menu1 == "1"): #quiere enviar texto
            print("")
            print("    1. Enviar a usuario")
            print("    2. Enviar a sala")
            print("")
            menu2 = input("¿Que opcion deseas? : ")
            if(menu2 == "1"): #enviar a usuario
                print("")
                usuario = input("Por favor ingresa el carnet del usuario con el que quieres chatear: ")
                topic = "usuarios/14/" + str(usuario)
                #lo suscribo al topic
                client.subscribe((str(topic), qos))
                while True:
                    chat = input("Ingresa un mensaje: ")
                    trama_chat = comandosCliente.comandosCliente().getTrama(COMMAND_CHAT, str(chat))
                    print("trama chat: " + str(trama_chat))
                    client.publish(topic, trama_chat, qos = 2, retain = False)
            if(menu2 == "2"): #enviar a sala
                print("")               
                sala = input("Por favor ingresa la sala donde quieres chatear (S01): ")
                topic = "salas/14/S01" + str(sala)
                #lo suscribo al topic
                client.subscribe((str(topic), qos))
                while True:
                    chat = input("Ingresa un mensaje: ")
                    trama_chat = comandosCliente.comandosCliente().getTrama(COMMAND_CHAT, str(chat))
                    print("trama chat: " + str(trama_chat))
                    client.publish(topic, trama_chat, qos = 2, retain = False)




        


except KeyboardInterrupt:
    logging.warning("Desconectando del broker...")

finally:
    client.loop_stop() #Se mata el hilo que verifica los topics en el fondo
    client.disconnect() #Se desconecta del broker
    logging.info("Desconectado del broker. Saliendo...")