from PyQt5 import QtWidgets,Qt
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QPushButton,QGridLayout,QCheckBox,QTextEdit
from PyQt5.QtWidgets import  QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal,QObject
from PyQt5 import QtCore
#import numpy as np
import os
from functools import partial

###############################################################
#  IMPORTACION DEL DISEÑO...
##############################################################
from CUERPO.DISENO.itemAlarmaEdit_dise import Ui_Dialog

###############################################################
#  MIS LIBRERIAS...
##############################################################

class ItemAlarmaEdit(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        Ui_Dialog.__init__(self)
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)

                
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        self.setWindowTitle(" ")
        self.setWindowModality(Qt.ApplicationModal)

    
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = ItemAlarmaEdit()
    application.show()
    app.exec()
    #sys.exit(app.exec())





#FUENTE DE ICONOS:
#https://p.yusukekamiyamane.com/
#https://icons8.com/?utm_source=http%3A%2F%2Ficons8.com%2Fweb-app%2Fnew-icons%2Fall&utm_medium=link&utm_content=search-and-download&utm_campaign=yusuke
