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
    
    #senal_colorElegido= pyqtSignal(int)

    def __init__(self):
        Ui_Dialog.__init__(self)
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.ApplicationModal)
        HuellaAplicacion.__init__(self)

    def activarDesactivar_alarmaFuego(self,activarAlarma):
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
