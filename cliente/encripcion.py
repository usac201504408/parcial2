from Crypto.Cipher import AES


class encripcion(object):

    def __init__(self):
        pass

    def encriptar(self, mensaje):
        obj = AES.new('This is a key123')
        texto_encriptado = obj.encrypt(mensaje)
        return texto_encriptado

    def desencriptar(self, mensaje):
        obj2 = AES.new('This is a key123')
        texto_desencriptado = obj2.decrypt(mensaje)
        return texto_desencriptado
    

texto_encript = encripcion().encriptar("The answer is no")
print("texto encriptado")
print(texto_encript)

texto_decript = encripcion().desencriptar(texto_encript)
print("dexto desencriptado")
print(texto_decript)