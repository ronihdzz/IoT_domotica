from CUERPO.LOGICA.recursos import Recursos_IoT_Domotica
import os 
from PyQt5 import QtMultimedia
from PyQt5 import QtCore
from pygame import mixer
from PyQt5.QtWidgets import  QFileDialog
from os import getcwd


class ReproductorSonidosAlarmas(QtCore.QObject):
    def __init__(self,context,carpetaMusica):
        QtCore.QObject.__init__(self)
        self.carpetaMusica=carpetaMusica

        self.listaCanciones=self.cargarNombresCanciones()
        self.noCanciones=len(self.listaCanciones)
        self.context=context

        self.cargarNombresCanciones()

        mixer.init()

    
    def agregarUnaCancion(self):
        print("Agregando una cancion")                                                        
        song, _ = QFileDialog.getOpenFileName(self.context, "Sonido de mi elección","c://", "Formatos validos (*.mp3  *.wav )")
        print(song)





    def cargarNombresCanciones(self):
        archivosCarpeta=os.listdir(self.carpetaMusica)
        listaCanciones=[archivo for archivo in archivosCarpeta if archivo.endswith(".mp3")]
        print("Lista de canciones",listaCanciones)
        return listaCanciones
    
    def tocar(self,nombreCancion):
        nombreCancion=self.carpetaMusica+nombreCancion
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
