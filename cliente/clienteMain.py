import clienteClass
import lecturaArchivos
import comandosCliente
from broker import *
from globalconst import *
import os

##JPGM empieza codigo de consumo de la clase
#variables globales:
qos = 2
#inicia loop principal
esperandoRespuesta = False
usuarioCarnet = "" #NUMERO DE CARNET DEL CLIENTE

#extraer el carnet del cliente conectado -> servira para saber a que topic de comandos pertenece
usuariosFile = lecturaArchivos.LecturaArchivo("usuario.txt").getArreglo()

for usuario in usuariosFile:
    usuarioCarnet = str(usuario)

#se instancia la clase
clienteMain = clienteClass.clienteClass(usuarioCarnet)
clienteMain.conectarMQTT()
clienteMain.iniciarLoggin()
#suscribirse a todos los topics del archivo
topics = lecturaArchivos.LecturaArchivo("topics.txt").getArreglo()

for topic in topics:
    clienteMain.suscribirse(topic)

clienteMain.iniciarLoop()





#JGPM El thread de MQTT queda en el fondo, mientras en el main loop hacemos otra cosa
try:
    while True:

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
                usuarioChat = input("Por favor ingresa el carnet del usuario con el que quieres chatear: ")
                topic = "usuarios/14/" + str(usuarioChat)
                #lo suscribo al topic
                clienteMain.suscribirse(topic)
                while True:
                    chat = input("Ingresa un mensaje: ")
                    trama_chat = comandosCliente.comandosCliente().getTrama(COMMAND_CHAT, str(chat))
                    clienteMain.publicar(topic, trama_chat)
            if(menu2 == "2"): #enviar a sala
                print("")    
                #pintar las salas
                opcionesSala = lecturaArchivos.LecturaArchivo("salas.txt").getArreglo()
                print("")
                clienteMain.logginWriteInfo("Salas disponibles")
                # print("Salas disponibles")
                for item_sala in opcionesSala:
                    print(item_sala)

                print("")           
                salaChat = input("Por favor ingresa la sala donde quieres chatear ej:S01 : ")
                topic = "salas/14/" + str(salaChat)
                #lo suscribo al topic
                # client.subscribe((str(topic), qos))
                clienteMain.suscribirse(topic)
                while True:
                    chat = input("Ingresa un mensaje: ")
                    trama_chat = comandosCliente.comandosCliente().getTrama(COMMAND_CHAT, str(chat))
                    # print("trama chat: " + str(trama_chat))
                    # client.publish(topic, trama_chat, qos = 2, retain = False)
                    clienteMain.publicar(topic, trama_chat)

        if(menu1 == "2"): #quiere enviar o recibir archivos
            print("")
            print("    1. Enviar a usuario")
            print("    2. Enviar a sala")
            print("")
            menu2 = input("¿Que opcion deseas? : ")
            if(menu2 == "1"): #enviar a usuario
                print("")
                duracion = input("¿Que duracion tendra el audio en segundos? ej:1 : ")
                usuarioEnvio = input("Por favor ingresa el carnet del usuario al que deseas enviar el audio: ")              
                topic = "comandos/14/" + usuarioCarnet
                #empezar hilo de grabacion, esperar hasta que se termine de grabar para enviar el request
                fileSize = 64 * 1024               
                trama_FTR = comandosCliente.comandosCliente().getTrama(COMMAND_FTR, str(usuarioEnvio), str(fileSize))
                #se publica en mqtt
                # client.publish(topic, trama_FTR, qos = 2, retain = False)
               
                clienteMain.publicar(topic, trama_FTR)
                #se le pide al cliente que espere, levanto bandera
                #CYO INICIO SE COMENTA CODIGO PARA SERVER
                # esperandoRespuesta = True
                # while esperandoRespuesta == True:                    
                #     pass
                # #me conecto al socket y realizo la transferencia -> MESSI
                # print("Enviando archivo...")
                #FIN SE COMENTA CODIGO PARA SERVER
                #CYO empiezo a grabar el audio

                #publico en topic de audios
                topic_audios = "audio/14/" + usuarioEnvio
                #PENDIENTE GRABAR EL AUDIO Y GUARDARLO

                os.system('arecord -d '+duracion+' -f U8 -r 8000 ../cliente/tempFiles/enviar.wav')
                #ESTO SI FUNCIONA, NO FUNCIONA AL DEJARLO EN OTRA CLASE VERIFICAR POR QUE Y VER POR QUE NO PUBLICA EN EL TOPIC BIEN
                in_file = open("../cliente/tempFiles/enviar.wav", "rb") 
                data = in_file.read() 
                in_file.close()
                # print(data)

                # out_file = open("recibido.mp3", "wb") 
                # out_file.write(data)
                # out_file.close()
                # print(data)
                # print("ya leyo")
                # #se manda la data binaria
                # print(type(data))
                #trama_FRR = comandosCliente.comandosCliente().getTrama(COMMAND_FRR, str(usuarioCarnet), str(data))
                #trama_FRR = comandosCliente.comandosCliente().getTrama("", str(data))
                # print(trama_FRR)
                data = bytearray(data)
                clienteMain.publicar(topic_audios, data)



            if(menu2 == "2"): #enviar a sala
                print("")
                duracion = input("¿Que duracion tendra el audio en segundos? ej:1  : ")
                #pintar las salas
                opcionesSala = lecturaArchivos.LecturaArchivo("salas.txt").getArreglo()
                print("")
                clienteMain.logginWriteInfo("Salas disponibles")
                # print("Salas disponibles")
                for item_sala in opcionesSala:
                    print(item_sala)

                print("")
                sala = input("¿A que sala deseas enviar tu audio? ej:S01 :  ")
                topic = "comandos/14/" + usuarioCarnet
                #empezar hilo de grabacion, esperar hasta que se termine de grabar para enviar el request
                fileSize = 64 * 1024
                trama_FTR = comandosCliente.comandosCliente().getTrama(COMMAND_FTR, str(sala), str(fileSize))
                # client.publish(topic, trama_FTR, qos = 2, retain = False)
                clienteMain.publicar(topic, trama_FTR)
                #se le pide al cliente que espere, levanto bandera
                #INICIO SE COMENTA CODIGO PARA SERVER
                # esperandoRespuesta = True
                # while esperandoRespuesta == True:
                #     print("Esperando respuesta del servidor...")
                #     pass
                # #me conecto al socket y realizo la transferencia -> MESSI
                #FIN SE COMENTA CODIGO PARA SERVER

                #publico en topic de audios
                topic_audios = "audio/14/" + sala
                os.system('arecord -d '+duracion+' -f U8 -r 8000 ../cliente/tempFiles/enviar.wav')
                #ESTO SI FUNCIONA, NO FUNCIONA AL DEJARLO EN OTRA CLASE VERIFICAR POR QUE Y VER POR QUE NO PUBLICA EN EL TOPIC BIEN
                in_file = open("../cliente/tempFiles/enviar.wav", "rb") 
                data = in_file.read() 
                in_file.close()
                # print(data)

                #trama_FRR = comandosCliente.comandosCliente().getTrama(COMMAND_FRR, str(usuarioCarnet), str(data))
  
                data = bytearray(data)
                clienteMain.publicar(topic_audios, data)
        
        
        if(menu1 == "3"): #quiere salir
            esperandoRespuesta = False
            clienteMain.pararLoop() #Se mata el hilo que verifica los topics en el fondo
            clienteMain.desconectarBroker() #Se desconecta del broker
            # logging.info("Desconectado del broker. Saliendo...")
            clienteMain.logginWriteInfo("Desconectado del broker. Saliendo...") 
            # print("Desconectado del broker. Saliendo...")
            break
                


except KeyboardInterrupt:
    # logging.warning("Desconectando del broker...")
    clienteMain.logginWriteInfo("Desconectando del broker...")
    # print("Desconectando del broker...")

finally:
    esperandoRespuesta = False
    clienteMain.pararLoop() #Se mata el hilo que verifica los topics en el fondo
    clienteMain.desconectarBroker() #Se desconecta del broker
    # logging.info("Desconectado del broker. Saliendo...")
    clienteMain.logginWriteInfo("Desconectado del broker. Saliendo...")
    # print("Desconectado del broker. Saliendo...")