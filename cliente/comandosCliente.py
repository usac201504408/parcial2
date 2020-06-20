#JPGM clase para comandos de cliente
import binascii

class comandosCliente(object):

    def __init__(self):
        pass

    def getTrama(self, comando, variable1, variable2 = "", separador = "$"):
       
        trama = bytes
        
        #se codifica la variable para poderla sumar
        variable1 = variable1.encode()
        separador = separador.encode()
        #puede venir 1, 2 o mas, yo voy a empezar a partir para armar la trama
        if(comando == binascii.unhexlify("03")): #transferencia archivos, usa dos variables y una constante
            pass
        elif(comando == binascii.unhexlify("04")): #alive usa 1 variable y una constante
            trama = comando + bytes(separador) + bytes(variable1)
        elif(comando == binascii.unhexlify("80")): #comando para chat
            trama = comando + bytes(separador) + bytes(variable1)
            print("entro")
        return trama

    def splitTramaCliente(self, trama, separador = "$"):
        # print("trama que vino: " + str(trama))
        # print(type(trama))
        # if(type(trama) == bytes): #si la trama son bytes osea no es parte del chat
        #verifico si le muestro o no al usuario este mensaje
        #las tramas ALIVE emitidas por el cliente no se las muestro a el
        print("trama para split" + str(trama))
        mensajeSplit = ""
        trama = trama.decode()
        print("trama decode" + str(trama))
        arregloTrama = trama.split(separador)
        print(arregloTrama)
        # print('Recibido: {!r}'.format(trama))
        
        #el primer item es el comando, aqui valido si el comando es para mostrarle al cliente
        #se codifica nuevamente ahora que ya esta aislado para compararla
        if(arregloTrama[0].encode() == binascii.unhexlify("04")):
            # print("es trama alive")
            return arregloTrama[1]
        elif(arregloTrama[0].encode() == binascii.unhexlify("04")):
            # print("es trama alive")
            return arregloTrama[1]
        return mensajeSplit
        
            
#codigo de test clase
# objetoComandos = comandosCliente()
# # # trama_recibida = objetoComandos.getTrama(binascii.unhexlify("05"), "201504408")
# trama_chat = objetoComandos.getTrama(b'\x80', str("hola"))
# print("trama chat: " + str(trama_chat))
# tramaCLiente = objetoComandos.boolTramaCliente(b'\x04$201504408', "$")
# print(tramaCLiente)