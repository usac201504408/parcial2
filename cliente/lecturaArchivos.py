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


#Ejemplo de consumo de la clase
# nuevoarreglo = LecturaArchivo("usuario.txt").getArreglo()
# print(nuevoarreglo)
     

