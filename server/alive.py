#JPGM clase con demonio para indicar al server que el cleinte esta activo
import lecturaArchivos

class alives(object):

    def __init__(self):
        pass


    def usuarioAlive(self, carnet):
        #verifica si el usuario esta en la lista de alives
        #se lee todo el archivo para guardarlo en una lista
        #se busca si el usuario ya esta registrado
        #si el usuario no esta entonces lo agrego al archivo
        objetoArchivo = lecturaArchivos.LecturaArchivo("alives.txt")
        listaAlives = objetoArchivo.getArreglo()
        usuarioVive = carnet in listaAlives
        if(usuarioVive == False):
            objetoArchivo.escribirArreglo(str(carnet))
