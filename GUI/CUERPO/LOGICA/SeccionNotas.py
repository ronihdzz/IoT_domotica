from PyQt5 import QtWidgets,Qt
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QPushButton,QGridLayout,QCheckBox,QTextEdit,QTimeEdit,QLabel
from PyQt5.QtWidgets import  QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal,QObject
from PyQt5 import QtCore
#import numpy as np
import os
from functools import partial

###############################################################
#  IMPORTACION DEL DISEÑO...
##############################################################
from CUERPO.DISENO.seccionNotas_dise import  Ui_Form

###############################################################
#  MIS LIBRERIAS...
##############################################################

class SeccionNotas(QtWidgets.QWidget, Ui_Form):
    quierePreguntaImagen = pyqtSignal()
    def __init__(self):
        Ui_Form.__init__(self)
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)

 

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = SeccionNotas()
    application.show()
    app.exec()
    #sys.exit(app.exec())
