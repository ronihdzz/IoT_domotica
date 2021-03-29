from CUERPO.LOGICA.recursos import Recursos_IoT_Domotica
import os 
from PyQt5 import QtMultimedia
from PyQt5 import QtCore
from pygame import mixer
from PyQt5.QtWidgets import  QFileDialog
from os import getcwd
from PyQt5.QtCore import pyqtSignal
import os




import shutil  #para copiar archivos
from mutagen.wave import WAVE  #para ver la duracion de las canciones
from mutagen.mp3 import MP3 

class ReproductorSonidosAlarmas(QtCore.QObject):
    MAX_DURACION=6*60 #6 minutos

    senal_cancionAgregada=pyqtSignal(str)


    def __init__(self,context,carpetaMusicaDefault,carpetaMusicaMia):
        QtCore.QObject.__init__(self)

        self.carpetaMusicaMia=carpetaMusicaMia
        self.carpetaMusicaDefault=carpetaMusicaDefault
        
        self.cargarNombresCanciones()


    
        self.context=context

        mixer.init()

    
    def agregarUnaCancion(self):
        print("Agregando una cancion")                                                        
        cancion,_= QFileDialog.getOpenFileName(self.context, "Sonido de mi elección","c://", "Formatos validos (*.mp3  *.wav )")
        if cancion:
            cancion = os.path.normpath(cancion) #normalizando la ruta
            soloNombreCancion = cancion.split(os.sep)[-1]
            
            
            origenArchivoCopiar=cancion
            destinoArchivoCopiar=self.carpetaMusicaMia+soloNombreCancion

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






    def cargarNombresCanciones(self):
        self.listaCancionesDefault=[]
        archivosCarpetaDefault=os.listdir(self.carpetaMusicaDefault)
        self.listaCancionesDefault=[archivo for archivo in archivosCarpetaDefault if archivo.endswith(".mp3") or  archivo.endswith(".wav")]        

        self.listaCancionesMias=[]
        archivosCarpetaMia=os.listdir(self.carpetaMusicaMia)
        self.listaCancionesMias=[archivo for archivo in archivosCarpetaMia if archivo.endswith(".mp3") or  archivo.endswith(".wav")]
        

    def tocar(self,nombreCancion,musicaDefault=True):
        #C:\Users\ronal\Desktop\PROYECTO\IoT_domotica\GUI\CUERPO\RECURSOS\MUSICA\DEFAULT
        if musicaDefault:
            ruta=self.carpetaMusicaDefault
        else:
            ruta=self.carpetaMusicaMia
        nombreCancion=ruta+nombreCancion


        # Loading the song
        mixer.music.load(nombreCancion)

        # Setting the volume
        mixer.music.set_volume(0.7)
        
        # Start playing the song
        mixer.music.play()

    def pausar(self):
        mixer.music.pause()
    
    def detener(self):
        mixer.music.stop()




'''
playlist = new QMediaPlaylist(player);
playlist->addMedia(QUrl("http://example.com/myfile1.mp3"));
playlist->addMedia(QUrl("http://example.com/myfile2.mp3"));
// ...
playlist->setCurrentIndex(1);
player->play();

'''

#https://www.youtube.com/watch?v=tF1U93I3-90


#https://python.hotexamples.com/es/examples/PyQt5.QtMultimedia/QMediaPlaylist/addMedia/python-qmediaplaylist-addmedia-method-examples.html
