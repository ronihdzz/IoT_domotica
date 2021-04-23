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
    senal_alarmaSonando = pyqtSignal(bool)
    def __init__(self):
        Ui_Dialog.__init__(self)
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        #textEdit_alarmas
        #hoSli_estadoAlarma
        #setWindowFlags(Qt::Window | Qt::WindowTitleHint | Qt::CustomizeWindowHint);
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
        if self.hoSli_estadoAlarma.value()==self.hoSli_estadoAlarma.maximum():
            self.close()


    def closeEvent(self,event):
        mixer.music.stop()
        event.accept()
        if self.reproductorAudio!=None:
            self.reproductorAudio.stop()
        self.hoSli_estadoAlarma.setValue(0)

    def activarAlarmas(self,listaAlarmas):
            # [ (nombre,horaAlarma), (nombre,horaAlarma), ... ]
        if self.notificadorAlarmas_activado:
            nombres= [nombre for nombre, _ in listaAlarmas ] 
            tiempo=listaAlarmas[0][1]
            nombreUnaAlarma=nombres[0]
            nombres=",".join(nombres)
            cancion,asunto=self.baseDatosAlarmas.getSonidoAsunto_alarma(nombreUnaAlarma)
            audio_asunto=None
            self.reproductorAudio=None
            if asunto==0: #despertar
                audio_asunto=App_Alarmas.AUDIO_YA_DESPIERTA
            elif asunto==1: #dormir
                audio_asunto=App_Alarmas.AUDIO_IR_DORMIR
            elif asunto==2: #debres
                audio_asunto=App_Alarmas.AUDIO_HAZ_DEBERES
            if audio_asunto!=None:
                self.reproductorAudio=mixer.Sound(audio_asunto)
                self.reproductorAudio.play ()

            #despertar,dormir,deberes y otro

            print("Mostrando alarmas....")
            print(listaAlarmas)
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
