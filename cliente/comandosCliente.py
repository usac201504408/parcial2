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
        return trama
        
            
#codigo de test clase
# trama_recibida = comandosCliente().getTrama(binascii.unhexlify("04"), "201504408")
# print("trama: " + str(trama_recibida))