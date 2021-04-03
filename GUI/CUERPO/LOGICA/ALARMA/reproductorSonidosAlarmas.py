from CUERPO.LOGICA.recursos import Recursos_IoT_Domotica
import os 
from PyQt5 import QtMultimedia
from PyQt5 import QtCore
from pygame import mixer
from PyQt5.QtWidgets import  QFileDialog
from os import getcwd
from PyQt5.QtCore import pyqtSignal
import os
from PyQt5.QtWidgets import QMessageBox

import shutil  #para copiar archivos
from mutagen.wave import WAVE  #para ver la duracion de las canciones
from mutagen.mp3 import MP3 

from CUERPO.LOGICA.recursos import Recursos_IoT_Domotica

class ReproductorSonidosAlarmas(QtCore.QObject):
    MAX_DURACION=6*60 #6 minutos
    senal_cancionAgregada=pyqtSignal(str)


    def __init__(self,context,direccionCarpetas,carpetaMusicaDefault,carpetaMusicaMia,cancionDefault):
        QtCore.QObject.__init__(self)

        self.direccionCarpetas=direccionCarpetas
        self.carpetaMusicaMia=carpetaMusicaMia
        self.carpetaMusicaDefault=carpetaMusicaDefault
        self.cargarNombresCanciones()
    
        self.context=context
        self.cancionDefault=cancionDefault

        self.nombreCancionSeleccionada=""
        self.carpetaCancionSeleccionada="" #puede ser el nombre de la carpeta
        #que almacena las 'canciones default' o las 'canciones que descargo el usuario'

        mixer.init()
    #dame el nombre completo de la cancion seleccionada



    def agregarUnaCancion(self):
        print("Agregando una cancion")                                                        
        cancion,_= QFileDialog.getOpenFileName(self.context, "Sonido de mi elección","c://", "Formatos validos (*.mp3  *.wav )")
        if cancion:
            cancion = os.path.normpath(cancion) #normalizando la ruta
            soloNombreCancion = cancion.split(os.sep)[-1]
            
            if len(soloNombreCancion)>30:
                #.wav==4 caracteres
                #.mp3==4 caracteres
                #de esta manera reducimos el nombre de izquierda a derecha y no quitamos
                #la extension del archivo 
                soloNombreCancion= (soloNombreCancion[:26])+ (soloNombreCancion[-4:])


            origenArchivoCopiar=cancion
            destinoArchivoCopiar=self.direccionCarpetas+self.carpetaMusicaMia+soloNombreCancion

            if soloNombreCancion.endswith(".wav"):
                infoCancion=WAVE(cancion)
            else:
                infoCancion=MP3(cancion)
            
            tamano=infoCancion.info.length #tiempo en segundos de la cancion
            print("Tamano cancion:",tamano)
            if tamano<self.MAX_DURACION:
                #Copiando cancion...
                shutil.copyfile(origenArchivoCopiar,destinoArchivoCopiar)
                self.senal_cancionAgregada.emit(soloNombreCancion)
            else:
                print("La duracion del archivo no puede ser mayor a los 6 minutos")
                ventanaDialogo = QMessageBox()
                ventanaDialogo.setIcon(QMessageBox.Critical)
                ventanaDialogo.setWindowTitle('Error')
                ventanaDialogo.setText("Lo sentimos pero no puede cargar\narchivos mayores a los 6 minutos")
                ventanaDialogo.setStandardButtons(QMessageBox.Ok)
                btn_ok = ventanaDialogo.button(QMessageBox.Ok)
                btn_ok.setText('Entendido')
                ventanaDialogo.exec_()


    def cargarNombresCanciones(self):
        self.listaCancionesDefault=[]
        archivosCarpetaDefault=os.listdir( str(self.direccionCarpetas+self.carpetaMusicaDefault) )
        self.listaCancionesDefault=[archivo for archivo in archivosCarpetaDefault if archivo.endswith(".mp3") or  archivo.endswith(".wav")]        

        self.listaCancionesMias=[]
        archivosCarpetaMia=os.listdir( str(self.direccionCarpetas+self.carpetaMusicaMia) )
        self.listaCancionesMias=[archivo for archivo in archivosCarpetaMia if archivo.endswith(".mp3") or  archivo.endswith(".wav")]

    def refrescarListaMisAlarmas(self):
        self.cargarNombresCanciones()

    
    def cargarCancion(self,nombreCancion=None ,musicaDefault=True):
        if nombreCancion==None:
            self.nombreCancionSeleccionada=self.cancionDefault
        else:
            self.nombreCancionSeleccionada=nombreCancion
        if musicaDefault:
            self.carpetaCancionSeleccionada=self.carpetaMusicaDefault
        else:
            self.carpetaCancionSeleccionada=self.carpetaMusicaMia

    def getNom_cancionSelec_guardaBase(self):
        return self.carpetaCancionSeleccionada+self.nombreCancionSeleccionada

    def getNombre_cancionDefault_guardaBase(self):
        return self.carpetaMusicaDefault+self.cancionDefault

    def tocar(self):
        #C:\Users\ronal\Desktop\PROYECTO\IoT_domotica\GUI\CUERPO\RECURSOS\MUSICA\DEFAULT
        # Loading the song
        if self.nombreCancionSeleccionada==self.cancionDefault:
            self.pausar()
        else:
            mixer.music.load(self.direccionCarpetas + self.carpetaCancionSeleccionada + self.nombreCancionSeleccionada)
            # Setting the volume
            mixer.music.set_volume(0.7)
            # Start playing the song
            mixer.music.play()

    def pausar(self):
        mixer.music.pause()
    
    def detener(self):
        mixer.music.stop()

    def eliminarMiCancion(self,nombreCancion):
        #self.detener()
        mixer.quit()

        mixer.init()

        nombreCompleto=self.direccionCarpetas + self.carpetaCancionSeleccionada + self.nombreCancionSeleccionada
        #eliminando a la cancion de la lista
        self.listaCancionesMias.remove(nombreCancion)
        os.remove(nombreCompleto)
