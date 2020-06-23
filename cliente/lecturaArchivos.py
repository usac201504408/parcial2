#clase para lectura de archivos


class LecturaArchivo(object):

    def __init__(self, nombreArchivo):
        self.nombreArchivo = nombreArchivo

    def getArreglo(self):
        datos = list()
        archivo = open(self.nombreArchivo, 'r')
        for linea in archivo:
            datos.append(linea.replace('\n', '').strip())
        archivo.close()
        return datos
    
    def escribirArreglo(self, valor):
        archivo = open(self.nombreArchivo, 'a')
        textoAppend = str(valor) + "\n"
        archivo.write(textoAppend)
        archivo.close()

    def getBytes(self):       
        in_file = open("prueba.mp3", "rb") # opening for [r]eading as [b]inary
        data = in_file.read() # if you only wanted to read 512 bytes, do .read(512)
        in_file.close()
        return data


#Ejemplo de consumo de la clase
# nuevoarreglo = LecturaArchivo("prueba.mp3").getBytes()
# print(nuevoarreglo)
     

