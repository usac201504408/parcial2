#JPGM clase para comandos del server
import binascii

class comandosServer(object):

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
        elif(comando == binascii.unhexlify("08")): #comando para chat
            trama = comando + bytes(separador) + bytes(variable1)
        elif(comando == binascii.unhexlify("05")): #comando para ACKNOWLEDGE alive
            trama = comando + bytes(separador) + bytes(variable1)
            
            
        return trama

    def splitTramaCliente(self, trama, separador = "$"):
        #verifico si le muestro o no al usuario este mensaje
        #las tramas ALIVE emitidas por el cliente no se las muestro a el
        trama = bytes(trama)
        trama = trama.decode()
        arregloTrama = trama.split(separador)
        
        return arregloTrama
        
            
#codigo de test clase
# objetoComandos = comandosCliente()
# # # # # trama_recibida = objetoComandos.getTrama(binascii.unhexlify("05"), "201504408")
# # # trama_chat = objetoComandos.getTrama(b'\x80', str("hola"))
# # # print("trama chat: " + str(trama_chat))
# tramaCLiente = objetoComandos.splitTramaCliente(b'\x08$hola', "$")
# # print(tramaCLiente)
# print(type(tramaCLiente[0].encode()))
# print(type(binascii.unhexlify("08")))
# print(type(binascii.unhexlify("04")))

# if(tramaCLiente[0].encode() != binascii.unhexlify("04")):
#     print("mensaje de texto")
#     print(tramaCLiente[0].encode())
# else:
#     print(tramaCLiente[0].encode())