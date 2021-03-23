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

        self.hora="9:30"
        self.nombre="Roni"
        self.dias="lu,ma,mi,ju"
        self.tipo="depertar"
        

        self.btn_editar.clicked.connect(self.editar)
        self.textEdit_alarma.setText("""<h2>{}({})</h2>
        <h5>{}:{}</h5>
        """.format(self.hora,self.tipo,self.nombre,self.dias))

        self.textEdit_alarma.setReadOnly(True)

        self.hoSli_estado.valueChanged.connect(self.activarDesactivarAlarma)
        self.hoSli_estado.setValue(1)

    
    def activarDesactivarAlarma(self):
        if self.hoSli_estado.value():
            self.textEdit_alarma.setEnabled(True)
        #Si el control requerido es el control automatico,
        #se pondra otro diseño especial a los horizontal sliders...
        else:
            self.textEdit_alarma.setEnabled(False)


    def editar(self):
        self.venEdicion=ItemAlarmaEdit()
        self.venEdicion.show()
    
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
