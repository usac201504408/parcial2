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


#Ejemplo de consumo de la clase
# nuevoarreglo = LecturaArchivo("usuario.txt").getArreglo()
# print(nuevoarreglo)
     

