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
from CUERPO.DISENO.itemAlarmaVista_dise import Ui_Form

###############################################################
#  MIS LIBRERIAS...
##############################################################
from CUERPO.LOGICA.ItemAlarmaEdit import ItemAlarmaEdit

class ItemAlarmaVista(QtWidgets.QWidget, Ui_Form):
    suHoraMorir= pyqtSignal(int)#indicara quien es el objeto que quiere morir...
    def __init__(self,id):
        Ui_Form.__init__(self)
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.btn_eliminar.clicked.connect(self.mandarSenalMuerto)
        self.id=id

        self.btn_editar.clicked.connect(self.editar)
        

        self.ESTADO=False
        self.deshabilitar()

    def editar(self):
        self.venEdicion=ItemAlarmaEdit()
        self.venEdicion.show()

    def deshabilitar(self):
        self.lineEdit_nombre.setEnabled(self.ESTADO)
        self.comBox_asunto.setEnabled(self.ESTADO)
        self.timeEdit_hora.setEnabled(self.ESTADO)
        self.cB_1.setEnabled(self.ESTADO)
        self.cB_2.setEnabled(self.ESTADO)
        self.cB_3.setEnabled(self.ESTADO)
        self.cB_4.setEnabled(self.ESTADO)
        self.cB_5.setEnabled(self.ESTADO)
        self.cB_6.setEnabled(self.ESTADO)
        self.cB_7.setEnabled(self.ESTADO)

        self.bel_1.setEnabled(self.ESTADO)
        self.bel_2.setEnabled(self.ESTADO)
        self.bel_3.setEnabled(self.ESTADO)
        self.bel_4.setEnabled(self.ESTADO)
        self.bel_5.setEnabled(self.ESTADO)
        self.bel_6.setEnabled(self.ESTADO)
        self.bel_7.setEnabled(self.ESTADO)

        self.bel_secNombre.setEnabled(self.ESTADO)
        self.bel_secAsunto.setEnabled(self.ESTADO)











    
    def mandarSenalMuerto(self):
        self.suHoraMorir.emit(self.id)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = ItemAlarmaVista()
    application.show()
    app.exec()
    #sys.exit(app.exec())





#FUENTE DE ICONOS:
#https://p.yusukekamiyamane.com/
#https://icons8.com/?utm_source=http%3A%2F%2Ficons8.com%2Fweb-app%2Fnew-icons%2Fall&utm_medium=link&utm_content=search-and-download&utm_campaign=yusuke
