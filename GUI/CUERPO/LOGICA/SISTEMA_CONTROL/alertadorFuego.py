from PyQt5.QtWidgets import  QDialog,QApplication
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from functools import partial
from PyQt5.QtCore import Qt, pyqtSignal,QObject
from pygame import mixer
from PyQt5.QtGui import QIcon
###############################################################
#  IMPORTACION DEL DISEÑO...
##############################################################
from  CUERPO.DISENO.SISTEMA_CONTROL.alertadorFuego_dise import Ui_Dialog
###############################################################
#  MIS LIBRERIAS...
##############################################################
from recursos import App_Principal,HuellaAplicacion

class Dialog_alertadorFuego(QtWidgets.QDialog, Ui_Dialog,HuellaAplicacion):
    '''
    Servira para alertar de la presencia de fuego.
    '''


    def __init__(self):
        Ui_Dialog.__init__(self)
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.ApplicationModal)
        HuellaAplicacion.__init__(self)

    def activarDesactivar_alarmaFuego(self,activarAlarma):
        '''
        Ejecutara el sonido de alerta de fuego si el parametro 'activarAlarma' toma
        el valor de 'True' en caso contrario 'Apagara' dicho sonido

        Parámetros:
            activarAlarma -- dato de tipo 'bool' que indicara si se desea prender o apagar
            la alarma de fuego
                Si activarAlarma es igual a 'True' significara que se desea activar la alarma
                de incendios y por lo tanto ejecutar el sonido
                Si activarAlarma es igual a 'False' significara que se desea desactivar la alarma
                de incendios y por lo tanto dejar de ejecutar el sonido
        '''

        if activarAlarma:
            mixer.init()
            mixer.music.load(App_Principal.SONIDO_INCENDIO)
            mixer.music.set_volume(1)
            mixer.music.play(-1)
        else:
            mixer.music.stop()
            self.close()  



if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = Dialog_alertadorFuego()
    application.show()
    app.exec()
    #sys.exit(app.exec())
