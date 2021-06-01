
from PyQt5 import QtCore
from pygame import mixer
from PyQt5.QtWidgets import  QFileDialog

from PyQt5.QtCore import pyqtSignal
import os
from PyQt5.QtWidgets import QMessageBox

import shutil  #para copiar archivos
from mutagen.wave import WAVE  #para ver la duracion de las canciones
from mutagen.mp3 import MP3 
from PyQt5.QtGui import QIcon

from recursos import HuellaAplicacion

class ReproductorSonidosAlarmas(QtCore.QObject):
    """
    La función de las instancias que crean de esta clase es llevar una administración
    de canciones y reproducirlas cuando se llamen.
    """

    MAX_DURACION=6*60 #6 minutos
    senal_cancionAgregada=pyqtSignal(str)

    def __init__(self,context,direccionCarpetas,listasNombresCarpetas):
        '''
        La función de la instancia es:
            a) Llevar una administración de las  canciones que se  encuentran almacenadas en las 
            carpetas cuyos nombres vienen en 'listaNombresCarpetas' y cuyas carpetas  se ubican 
            en la direccion: 'direccionCarpetas'.
            Es importante mencinonar que cada carpeta que almacena canciones sera considerada 
            una lista de reproduccion.

            b) Reproducir las canciones que se digan
        
        Parámetros:
            self -- es la referencia del objeto que creo esta instancia
            direccionCarpetas -- dato de tipo 'str' que contiene la direccion de las
            carpetas que almacenan las canciones.
            Observación: La dirección es igual para todas las carpetas, lo cual significa
            que las carpeta que almacenan las canciones deben estar ubicadas en la misma
            direccion.
            listasNombresCarpetas -- dato de tipo 'list' que contiene los nombres de las
            carpetas que almacenan las canciones
        '''

        QtCore.QObject.__init__(self)

        self.direccionCarpetas=direccionCarpetas
        self.LISTA_DIR_LISTAS_REPRODUCCION=listasNombresCarpetas
        self.TOTAL_LISTAS_REPRODUCCION=len(self.LISTA_DIR_LISTAS_REPRODUCCION)
        
        self.context=context

        # (idListaReproduccion,nombre)
        self.datosCancionSeleccionada= ()


        self.dictTodasCanciones={}

        self.cargarNombresCanciones()


        mixer.init()
    #dame el nombre completo de la cancion seleccionada


    def cargarNombresCanciones(self):
        '''
        Creara un diccionario en donde: 
            Cada 'value' del diccionario  sera un numero entero apartir del cero el cual correspondera
            a cada lista de reproducción.
            Cada 'key' del diccionario sera otro diccionario en donde:
                Sus 'keys' seran los nombres de las canciones de esa lista de reproducción 
                Sus 'values' seran todos igual a True
        
        Ejemplo:
        El siguiente diccionario tiene 3 elementos, esto significa que tiene 3 listas de reproduccion, 
        con N canciones cada una.

        self.dictTodasCanciones={
                0: {nombreCancion1:True,nombreCancion2:True,nombreCancion3:True,... nombreCancionN:True  },
                1: {nombreCancion1:True,nombreCancion2:True,nombreCancion3:True,... nombreCancionN:True  },
                2: {nombreCancion1:True,nombreCancion2:True,nombreCancion3:True,... nombreCancionN:True  }
            }    
        '''

        for idListaReproduccion,nombreCarpeta_listaReproduccion in enumerate(self.LISTA_DIR_LISTAS_REPRODUCCION):
            archivosDeLaCarpeta=os.listdir( str(self.direccionCarpetas+nombreCarpeta_listaReproduccion) )
            self.dictTodasCanciones[idListaReproduccion]=dict( [ (archivo,True) for archivo in archivosDeLaCarpeta if archivo.endswith(".mp3") or  archivo.endswith(".wav") ]  )       

    def getNombresCanciones(self,idListaReproduccion):
        '''
        Este metodo se encargar de retornar una lista de los nombres de las canciones
        que estan almacenados en la lista de reproduccion cuyo id='idListaReproduccion'


        Parámetros:
            idListaReproduccion -- dato de tipo 'int' el cual representa el 'id' de la lista
            de reproducción de la cual se desea saber que canciones tiene almacenadas.

        Returns(devoluciones)
            dato de tipo 'list' donde cada elemento es un dato de tipo 'str' y representa el 
            nombre de una canción que se encuentra en la lista de reproducción cuyo 
            id='idListaReproduccion'
        '''

        return tuple(self.dictTodasCanciones[idListaReproduccion].keys())


    def agregarUnaCancion(self,idListaAlmacenara):
        '''
        Este metodo abrira el explorador de archivos para que  el usuario pueda elegir la canción que
        desea agregar,si el usuario escoge una canción este metodo copiara la  canción que el usuario 
        escogio en la carpeta donde se encuentre ubicada la lista de reproduccion con id='idListaAlmacenara' 
        si todo tuvo exito, emitira la señal: 'self.senal_cancionAgregada'. Si la canción que escogio el 
        usuario es mayor a 'self.MAX_DURACION' o si ya existe un nombre de canción registrado igual al que
        al nombre de la canción que el usuario escogio, entonces no se copiara la canción y se le explicara
        al usuario las razones por lo cual no se copio la canción.

        Parámetros:
            idListaAlmacenara -- dato de tipo 'int' que representa el 'id' de la lista de reproducción
            a la cual se desea agregar una canción, y en la que la canción agregara se copiara en la carpeta
            que representa a esa lista de reproducción
        '''

        print("Agregando una cancion")                                                        
        cancion,_= QFileDialog.getOpenFileName(self.context, "Sonido de mi elección","c://", "Formatos validos (*.mp3  *.wav )")
        if cancion:
            cancionCopiar_nombreFull = os.path.normpath(cancion) #normalizando la ruta
            cancionCopiar_soloNombre= cancionCopiar_nombreFull.split(os.sep)[-1]
            
            if len(cancionCopiar_soloNombre)>30:
                #.wav==4 caracteres
                #.mp3==4 caracteres
                #de esta manera reducimos el nombre de izquierda a derecha y no quitamos
                #la extension del archivo 
                cancionCopiar_soloNombre= (cancionCopiar_soloNombre[:26])+ (cancionCopiar_soloNombre[-4:])


            archivoCopiar=cancion
            #destinoArchivoCopiar=self.direccionCarpetas+self.carpetaMusicaMia+soloNombreCancion
            destinoArchivoCopiar=self.direccionCarpetas+self.LISTA_DIR_LISTAS_REPRODUCCION[idListaAlmacenara]+cancionCopiar_soloNombre

            if cancionCopiar_soloNombre.endswith(".wav"):
                infoCancion=WAVE(cancionCopiar_nombreFull)
            else:
                infoCancion=MP3(cancionCopiar_nombreFull)
            
            tamano=infoCancion.info.length #tiempo en segundos de la cancion
            print("Tamano cancion:",tamano)
            if tamano<self.MAX_DURACION:
                #Copiando cancion...
                if os.path.exists(destinoArchivoCopiar):
                    
                    ventanaDialogo = QMessageBox()
                    ventanaDialogo.setIcon(QMessageBox.Information)
                    ventanaDialogo.setWindowIcon( QIcon(HuellaAplicacion.ICONO_APLICACION)  )
                    ventanaDialogo.setWindowTitle(HuellaAplicacion.NOMBRE_APLICACION)


                    ventanaDialogo.setText("Ya has guardado una cancion con el mismo \n"
                    "nombre, por tal motivo no se realizo la copia\n""de la cancion seleccionada ")
                    ventanaDialogo.setStandardButtons(QMessageBox.Ok)
                    btn_ok = ventanaDialogo.button(QMessageBox.Ok)
                    btn_ok.setText('Entendido')
                    ventanaDialogo.exec_()
                else:
                    shutil.copyfile(cancionCopiar_nombreFull,destinoArchivoCopiar)
                    self.senal_cancionAgregada.emit(cancionCopiar_soloNombre)
                    self.dictTodasCanciones[idListaAlmacenara][cancionCopiar_soloNombre]=True
            else:
                print("La duracion del archivo no puede ser mayor a los 6 minutos")
                ventanaDialogo = QMessageBox()
                ventanaDialogo.setIcon(QMessageBox.Critical)
                ventanaDialogo.setWindowIcon( QIcon(HuellaAplicacion.ICONO_APLICACION)  )
                ventanaDialogo.setWindowTitle(HuellaAplicacion.NOMBRE_APLICACION)


                ventanaDialogo.setText("Lo sentimos pero no puede cargar\narchivos mayores a los 6 minutos")
                ventanaDialogo.setStandardButtons(QMessageBox.Ok)
                btn_ok = ventanaDialogo.button(QMessageBox.Ok)
                btn_ok.setText('Entendido')
                ventanaDialogo.exec_()


    def cargarCancion(self,nombreCancion=None,idListaAlmacenaCancion=None):
        '''
        En función del valor que tome el parametro 'nombreCancion', este metodo la buscara 
        en la lista de reproducción:
            a) Si el valor que toma el parametro  'idListaAlmacenaCancion' es igual a None, entonces
            buscara la canción en todas las listas de reproducción
            b) Si el valor que toma el parametro 'idListaAlmacenaCancion' es diferente de None, 
            entonces bucara la canción en la lista de reproduccion cuyo 'id' es igual a: 
            'idListaAlmacenaCancion' 
        
            Si encuentra a la canción  creara una tupla con los datos y en el orden siguiente:
                                (idListaAlmacenaCancion,nombreCancion) 
            posteriormente dicha tupla la almacenara en el atributo de instancia 
            'self.datosCancionSeleccionada'

            Si no encuentra el nombre de la canción creara una tupla con los datos y en el orden siguiente:
                                (None,None) 
            posteriormente dicha tupla la almacenara en el atributo de instancia 
            'self.datosCancionSeleccionada'
        
        El objetivo de este metodo es simular la selección de la canción que se deseara reproducir, 
        es decir, para reproducir una canción primero debe ser seleccionada, entonces este metodo
        es lo que hace, seleccionar la canción para que despues que se pida tocar, toque la canción
        seleccionada.

        Parámetros:
            nombreCancion -- dato de tipo 'str' el cual representara el nombre de la canción que
            se desea seleccionar
            idListaAlmacenaCancion -- dato de tipo 'int' el cual representara el 'id' de la lista
            de reproducción en la cual se encuentra la canción que se desea seleccionar.
        
        Returns(devoluciones)
            a) En caso de existir la canción que se desea seleccionar retornara un dato 
            de tipo 'int' el cual representa el 'id' de la lista de reproduccion en donde
            se encuentra la canción que se selecciono.
            b) En caso de no existir la canción que se desea seleccionar retornara un dato
            de tipo 'int' con el valor igual a -1.
            c) En caso de que la canción sea igual a la canción None, es decir a ninguna cancion,
            se retornara None.
        '''

        self.datosCancionSeleccionada=(None,None)
        if nombreCancion:
            if idListaAlmacenaCancion==None:
                idListaAlmacenaCancion=self.getIdListaReproduccion(nombreCancion=nombreCancion)
                if idListaAlmacenaCancion!=-1:
                    self.datosCancionSeleccionada=(idListaAlmacenaCancion,nombreCancion)
            else:
                if self.dictTodasCanciones[idListaAlmacenaCancion].get(nombreCancion,False):
                    self.datosCancionSeleccionada=(idListaAlmacenaCancion,nombreCancion)
                else:
                    idListaAlmacenaCancion=-1
            print(self.datosCancionSeleccionada)
            return idListaAlmacenaCancion
        return None
                
    def getNom_cancionSelec_guardaBase(self):
        '''
        Este metodo se encargara de crear un dato de tipo 'str' el cual almacenara  como se 
        guardara la canción seleccionada dentro de la base de datos que almacena la información
        de las alarmas.

        Returns(devoluciones):
            a) Si la canción seleccionada es diferente de None, retornara un dato de tipo 'str'
            el cual sera el nombre de como se guaradara la canción en la base de datos
            b) Si la canción seleccionada es igual a None, retornara None
        '''

        idListaAlmacenaCancion,nombreCancion=self.datosCancionSeleccionada
        if nombreCancion:
            nombreCarpetaAlmacenaCancion=self.LISTA_DIR_LISTAS_REPRODUCCION[idListaAlmacenaCancion]
            return nombreCarpetaAlmacenaCancion+nombreCancion
        return None 

        


    def tocar(self):
        '''
        Reproducira el sonido de la canción seleccionada, en caso de que la canción seleccionada
        sea igual a: None, tocara el silencio, es decir no tocara nada.
        '''
        
        idListaAlmacenaCancion,nombreCancion=self.datosCancionSeleccionada
        
        # Si no se ha seleccionado ninguna canción
        if nombreCancion==None:
            self.pausar()
        else:
            nombreCarpetaAlmacenaCancion=self.LISTA_DIR_LISTAS_REPRODUCCION[idListaAlmacenaCancion]
            mixer.music.load(self.direccionCarpetas+nombreCarpetaAlmacenaCancion+nombreCancion)
            # Setting the volume
            mixer.music.set_volume(0.7)
            # Start playing the song
            mixer.music.play()


    def getIdListaReproduccion(self,nombreCancion):
        '''
        Buscara la lista de reproduccion en la cual se encuentra almacenada el nombre
        de la cancion igual al valor que tendra el parametro: 'nombreCancion', una
        vez encontrada dicha lista de reproducción retornara el 'id' de esa lista de 
        reproducción, en caso de no existir dicho nombre de canción en ninguna lista
        de reproducción retornara -1.

        Parámetros:
            nombreCancion -- dato de tipo 'str' el cual almacenara el nombre de la canción
            de la cual se desea saber en que lista de reproducción se encuentra
        
        Returns(devoluciones):
            a) Si el nombre de la canción existe en una lista de reproducción retornara un dato
            de tipo 'int' el cual representara el 'id' de la lista de reproducción que almacena
            esa canción.
            b) Si el nombre de la canción no existe en la lista de reproducción retornara un
            dato de tipo 'int' con un valor igual a: -1
        '''

        existeCancion=False
        for c in range(self.TOTAL_LISTAS_REPRODUCCION):
            if self.dictTodasCanciones[c].get(nombreCancion,False):
                idListaAlmacenaCancion=c
                existeCancion=True
        if existeCancion:
            return idListaAlmacenaCancion
        else:
            return -1


    def pausar(self):
        '''
        Pausara la canción que se este reproduciendo, en caso de no existir ninguna canción,
        entonces no pasara nada.
        '''

        mixer.music.pause()
    
    def detener(self):
        '''
        Detendra la reproducción de canciones.
        '''
        mixer.music.stop()

    def eliminarMiCancion(self,nombreCancion,idListaAlmacenaCancion=None):
        '''
        Eliminara la canción cuyo valor sea igual al valor que almacenara el parametro
        'nombreCancion', la eliminara del diccionario: 'self.dictTodasCanciones' y 
        tambien la eliminara de la carpeta donde se encuentre dicha canción.

        Parámetros:
            nombreCanción -- dato de tipo 'str' que representara el nombre de la canción
            que se desea eliminar
            idListaAlmacenaCancion -- dato de tipo 'int' que representa el 'id' de la lista
            de reproducción que almacena a la canción que se desea eliminar
        '''

        mixer.quit()
        mixer.init()

        if idListaAlmacenaCancion==None:
            idListaAlmacenaCancion=self.getIdListaReproduccion(nombreCancion)
        
        nombreCarpetaAlmacenaCancion=self.LISTA_DIR_LISTAS_REPRODUCCION[idListaAlmacenaCancion]
        nombreCompleto=self.direccionCarpetas + nombreCarpetaAlmacenaCancion + nombreCancion
        
        del self.dictTodasCanciones[idListaAlmacenaCancion][nombreCancion]
        os.remove(nombreCompleto)
