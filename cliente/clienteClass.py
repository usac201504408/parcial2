import paho.mqtt.client as mqtt
from broker import *
from globalconst import *
import comandosCliente
import binascii
import logging
import threading
import time
import lecturaArchivos

class clienteClass(object):

    def __init__(self, usuarioCliente):
        self.usuarioCliente = usuarioCliente
        pass

    def postAlive(self):
        while True:
            #hago un publish para decir que estoy vivo
            trama = comandosCliente.comandosCliente().getTrama(COMMAND_ALIVE, self.usuarioCliente)       
            self.client.publish("comandos/14/" + str(self.usuarioCliente), trama, qos = 2, retain = False)
            time.sleep(20)


    #Handler en caso suceda la conexion con el broker MQTT
    def on_connect(self, client, userdata, flags, rc): 
        connectionText = "CONNACK recibido del broker con codigo: " + str(rc)
        logging.debug(connectionText)
        #Lanza el primer hilo con los parámetros:
        #name: Nombre "humano" para identificar fácil al hilo
        #target: La función a ejecutar (o método de un objeto)
        #args: argumentos, deben ser enviados como tupla
        #daemon: servicio corriendo de fondo -> permite detener el hilo con "Thread._stop()"
        self.t1 = threading.Thread(name = 'Contador de 1 segundo',
                                target = self.postAlive,
                                args = (()),
                                daemon = True
                            )
        self.t1.start()

    #Callback que se ejecuta cuando llega un mensaje al topic suscrito
    def on_message(self, client, userdata, msg):
        #Se muestra en pantalla informacion que ha llegado
        arregloTrama_split = comandosCliente.comandosCliente().splitTramaCliente(msg.payload)
        
        if(arregloTrama_split[0].encode() == binascii.unhexlify("04")): #alive no muestro al cliente
            pass
        elif(arregloTrama_split[0].encode() == binascii.unhexlify("05")): #acknowledge del server
            # print("")
            # print("El cliente del topic " + str(msg.topic) + " da el comando ACK y dice: " + str(arregloTrama_split[1]))
            # logging.debug("El contenido del mensaje es: " + str(mensajedecode))
            pass
        elif(arregloTrama_split[0].encode() == binascii.unhexlify("03")): #trama FTR del ciente      
            pass
        elif(arregloTrama_split[0].encode() == binascii.unhexlify("06")): #trama OK del server
            #bajo bandera de espera
            global esperandoRespuesta
            esperandoRespuesta = False    
            pass
        elif (arregloTrama_split[0].encode() == binascii.unhexlify("08")):
            print("El cliente del topic " + str(msg.topic) + " da el comando CHAT y dice: " + str(arregloTrama_split[1]))
        elif (arregloTrama_split[0].encode() == binascii.unhexlify("02")): #trama FRR file receive request
            #conectarme al socket para recibir archivo MESSI
            # print("Cliente conectandose a SOCKET para recibir archivo ")

            #PARCIAL 2, RECIBIR DE MQTT EL ARCHIVO, se extrae de la trama 2 el valor
            print("Estas recibiendo del topic " + str(msg.topic) + " binarios del audio: "  + str(arregloTrama_split[2]))
            pass 

    #Handler en caso se publique satisfactoriamente en el broker MQTT
    def on_publish(self, client, userdata, mid): 
        publishText = "Publicacion satisfactoria"
        logging.debug(publishText)    


    def conectarMQTT(self):
        self.client = mqtt.Client(clean_session=True) #Nueva instancia de cliente
        self.client.on_connect = self.on_connect #Se configura la funcion "Handler" cuando suceda la conexion
        self.client.on_message = self.on_message #Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
        self.client.on_publish = self.on_publish #Se configura la funcion "Handler" que se activa al publicar algo
        self.client.username_pw_set(MQTT_USER, MQTT_PASS) #Credenciales requeridas por el broker
        self.client.connect(host=MQTT_HOST, port = MQTT_PORT) #Conectar al servidor remoto
        


    def iniciarLoggin(self):
        logging.basicConfig(
        level = logging.INFO, 
        format = '[%(levelname)s] (%(threadName)-10s) %(message)s'
        )   

    def publicar(self, topic, trama):
        self.client.publish(topic, trama, qos = 2, retain = False)

    def suscribirse(self, topic,):
        self.client.subscribe((str(topic),  2))

    def iniciarLoop(self):
        #Iniciamos el thread (implementado en paho-mqtt) para estar atentos a mensajes en los topics subscritos
        self.client.loop_start()

    def pararLoop(self):
        self.client.loop_stop()

    def desconectarBroker(self):
        self.client.disconnect()



# ###empieza codigo de consumo de la clase
# #variables globales:
# qos = 2
# #extraer el carnet del cliente conectado -> servira para saber a que topic de comandos pertenece
# usuariosFile = lecturaArchivos.LecturaArchivo("usuario.txt").getArreglo()
# #se instancia la clase
# clienteprueba = clienteClass("201504408")
# clienteprueba.conectarMQTT()
# clienteprueba.iniciarLoggin()
# #suscribirse a todos los topics del archivo
# topics = lecturaArchivos.LecturaArchivo("topics.txt").getArreglo()
# for topic in topics:
#     clienteprueba.suscribirse(topic)

# clienteprueba.iniciarLoop()

# #inicia loop principal
# esperandoRespuesta = False
# usuarioCarnet = "201504408" #NUMERO DE CARNET DEL CLIENTE



# #El thread de MQTT queda en el fondo, mientras en el main loop hacemos otra cosa
# try:
#     while True:
#         # logging.info("Esperando comando")
#         print("Hola, bienvenido al chat del grupo 14, and i'll tell you all about it when i see you again")
#         print("Menu")
#         print("1. Enviar texto")
#         print("2. Enviar mensaje de voz")
#         print("3.  Salir")
#         print("")
#         menu1 = input("¿Que opcion deseas? : ")  
#         if(menu1 == "1"): #quiere enviar texto
#             print("")
#             print("    1. Enviar a usuario")
#             print("    2. Enviar a sala")
#             print("")
#             menu2 = input("¿Que opcion deseas? : ")
#             if(menu2 == "1"): #enviar a usuario
#                 print("")
#                 usuarioChat = input("Por favor ingresa el carnet del usuario con el que quieres chatear: ")
#                 topic = "usuarios/14/" + str(usuarioChat)
#                 #lo suscribo al topic
#                 clienteprueba.suscribirse(topic)
#                 while True:
#                     chat = input("Ingresa un mensaje: ")
#                     trama_chat = comandosCliente.comandosCliente().getTrama(COMMAND_CHAT, str(chat))
#                     # print("trama chat: " + str(trama_chat))
#                     # client.publish(topic, trama_chat, qos = 2, retain = False)
#                     clienteprueba.publicar(topic, trama_chat)
#             if(menu2 == "2"): #enviar a sala
#                 print("")               
#                 salaChat = input("Por favor ingresa la sala donde quieres chatear (S01): ")
#                 topic = "salas/14/" + str(salaChat)
#                 #lo suscribo al topic
#                 # client.subscribe((str(topic), qos))
#                 clienteprueba.suscribirse(topic)
#                 while True:
#                     chat = input("Ingresa un mensaje: ")
#                     trama_chat = comandosCliente.comandosCliente().getTrama(COMMAND_CHAT, str(chat))
#                     # print("trama chat: " + str(trama_chat))
#                     # client.publish(topic, trama_chat, qos = 2, retain = False)
#                     clienteprueba.publicar(topic, trama_chat)

#         if(menu1 == "2"): #quiere enviar o recibir archivos
#             print("")
#             print("    1. Enviar a usuario")
#             print("    2. Enviar a sala")
#             print("")
#             menu2 = input("¿Que opcion deseas? : ")
#             if(menu2 == "1"): #enviar a usuario
#                 print("")
#                 duracion = input("¿Que duracion tendra el audio? : ")
#                 usuarioEnvio = input("Por favor ingresa el carnet del usuario al que deseas enviar el audio: ")
#                 topic = "comandos/14/" + usuarioCarnet
#                 #empezar hilo de grabacion, esperar hasta que se termine de grabar para enviar el request
#                 fileSize = 64 * 1024
#                 trama_FTR = comandosCliente.comandosCliente().getTrama(COMMAND_FTR, str(usuarioEnvio), str(fileSize))
#                 #se publica en mqtt
#                 # client.publish(topic, trama_FTR, qos = 2, retain = False)
#                 clienteprueba.publicar(topic, trama_FTR)
#                 #se le pide al cliente que espere, levanto bandera
#                 esperandoRespuesta = True
#                 while esperandoRespuesta == True:                    
#                     pass
#                 #me conecto al socket y realizo la transferencia -> MESSI
#                 print("Enviando archivo...")



#             if(menu2 == "2"): #enviar a sala
#                 print("")
#                 duracion = input("¿Que duracion tendra el audio? : ")
#                 sala = input("Por favor ingresa el nombre de la sala a la que deseas enviar el audio: ")
#                 topic = "comandos/14/" + usuarioCarnet
#                 #empezar hilo de grabacion, esperar hasta que se termine de grabar para enviar el request
#                 fileSize = 64 * 1024
#                 trama_FTR = comandosCliente.comandosCliente().getTrama(COMMAND_FTR, str(sala), str(fileSize))
#                 # client.publish(topic, trama_FTR, qos = 2, retain = False)
#                 clienteprueba.publicar(topic, trama_FTR)
#                 #se le pide al cliente que espere, levanto bandera
#                 esperandoRespuesta = True
#                 while esperandoRespuesta == True:
#                     print("Esperando respuesta del servidor...")
#                     pass
#                 #me conecto al socket y realizo la transferencia -> MESSI
                


# except KeyboardInterrupt:
#     # logging.warning("Desconectando del broker...")
#     print("Desconectando del broker...")

# finally:
#     esperandoRespuesta = False
#     clienteprueba.pararLoop() #Se mata el hilo que verifica los topics en el fondo
#     clienteprueba.desconectarBroker() #Se desconecta del broker
#     # logging.info("Desconectado del broker. Saliendo...")
#     print("Desconectado del broker. Saliendo...")