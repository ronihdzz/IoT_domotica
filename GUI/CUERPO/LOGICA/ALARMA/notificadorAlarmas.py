from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal
from pygame import mixer

###############################################################
#  IMPORTACION DEL DISEÑO...
##############################################################
from CUERPO.DISENO.ALARMA.notificadorAlarmas_dise import  Ui_Dialog

###############################################################
#  MIS LIBRERIAS...
##############################################################
from CUERPO.LOGICA.ALARMA.baseDatos_alarma import BaseDatos_alarmas
from recursos import App_Alarmas,HuellaAplicacion

class NotificadorAlarmas(QtWidgets.QDialog, Ui_Dialog,HuellaAplicacion):
    '''
    El proposito de esta clase es mostrar los datos de la o las alarmas
    que deben sonar, asi como reproducir su canción de alarma y proveer
    una alternativa para poder cerrar el aviso.
    '''

    senal_alarmaSonando = pyqtSignal(bool)
    senal_horaDespertar_prenderLuz=pyqtSignal(bool)


    def __init__(self):
        Ui_Dialog.__init__(self)
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.setWindowModality(Qt.ApplicationModal)

        HuellaAplicacion.__init__(self)
    
        self.hayAlarmaSonando=False
        self.baseDatosAlarmas=BaseDatos_alarmas(App_Alarmas.NOMBRE_BASE_DATOS_ALARMAS)
        self.hoSli_estadoAlarma.sliderReleased.connect( self.checarEstadoRespuesta )
        self.textEdit_alarmas.setReadOnly(True)
        self.alarmaFuego_sonando=False
        self.notificadorAlarmas_activado=True
    
    def checarEstadoRespuesta(self):
        '''
        Cuando se este mostrando a la alarma y reproduciendo la canción de alarma, la unica
        manera en el que se podra cerrar ese aviso, cera deslizando una barra hacia la derecha,
        y solo cuando este completamente dezlizada hacia la derecha es cuando se cerrara el 
        aviso y eso es lo que hara este metodo,cuando detecte que la barra fue deslizada 
        completamente a la derecha entonces mandara a cerrar al aviso
        '''
        
        if self.hoSli_estadoAlarma.value()==self.hoSli_estadoAlarma.maximum():
            self.close()


    def closeEvent(self,event):
        '''
        Si se estaba reproduciendo musica, se dejara de reproducir, y se cambiar el 'value'
        del 'QSlider' a un valor igual a cero para que este completamente a la izquierda 
        nuevamente
        '''

        mixer.music.stop()
        if self.reproductorAudio!=None:
            self.reproductorAudio.stop()
        self.hoSli_estadoAlarma.setValue(0)

        event.accept()

    def activarAlarmas(self,listaIds_alarmas):
        '''
        Se encargara de mostrar las alarmas cuyos 'id' se encuentran dentro de la lista
        'listaIds_alarmas' y reproducira la canción de la alarma cuyo 'id' es igual al primer
        'id' de la lista: 'listaIdsAlarmas'

        Parámetros:
            listaAlarmas -- un dato de tipo 'list' el cual almacenara puros elementos de
            tipo 'int' los cuales seran los 'id' de las alarmas que se desea que se informe
            acerca de que ya deben sonar.
        '''
        
        if self.notificadorAlarmas_activado:
            datosNecesarios=self.baseDatosAlarmas.getDatosNecesariosParaSonarAlarma(listaIds=listaIds_alarmas)
            nombres= datosNecesarios[0]
            tiempo=datosNecesarios[1][0]
            cancion=datosNecesarios[1][1]
            asunto=datosNecesarios[1][2]

            nombres=",".join(nombres) 
            audio_asunto=None
            self.reproductorAudio=None
            if asunto==0: #despertar
                audio_asunto=App_Alarmas.AUDIO_YA_DESPIERTA
                self.senal_horaDespertar_prenderLuz.emit(True)
            elif asunto==1: #dormir
                audio_asunto=App_Alarmas.AUDIO_IR_DORMIR
            elif asunto==2: #debres
                audio_asunto=App_Alarmas.AUDIO_HAZ_DEBERES
            if audio_asunto!=None:
                self.reproductorAudio=mixer.Sound(audio_asunto)
                self.reproductorAudio.play ()

            #despertar,dormir,deberes y otro
            self.senal_alarmaSonando.emit(True)
            try:
                mixer.init()
                mixer.music.load(App_Alarmas.CARPETA_MUSICA+cancion)
                # Setting the volume
                mixer.music.set_volume(1)
                # Start playing the song
                mixer.music.play()
                self.textEdit_alarmas.setText("""<h1 style="text-align:center" >{}  </h1>
                <h3 style="text-align:center">{}</h3>""".format(tiempo,nombres) )
            except:
                self.textEdit_alarmas.setText("""<h1 style="text-align:center" >{}  </h1>
                <h3 style="text-align:center">{}</h3>
                <h6 style="text-align:center">Sin musica </h6>""".format(tiempo,nombres) )


        

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = NotificadorAlarmas()
    application.show()
    app.exec()
    #sys.exit(app.exec())

