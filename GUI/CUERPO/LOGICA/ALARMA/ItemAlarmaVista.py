from PyQt5 import QtWidgets,Qt
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QPushButton,QGridLayout,QCheckBox,QTextEdit
from PyQt5.QtWidgets import  QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal,QObject,QTime
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
from CUERPO.LOGICA.ALARMA.alarma import Alarma
from CUERPO.LOGICA.ALARMA.ItemAlarmaEdit import ItemAlarmaEdit




class ItemAlarmaVista(QtWidgets.QWidget,Ui_Form):
    suHoraMorir= pyqtSignal(list)#indicara quien es el objeto que quiere morir...
    #[id,nombre]
    senal_alarmaEditada=pyqtSignal(bool)


    senal_alarmaQuiereEdicion=pyqtSignal(str)
    #nombreAlarma
    

    def __init__(self,id):
        Ui_Form.__init__(self)
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.btn_eliminar.clicked.connect(self.mandarSenalMuerto)
        self.id=id
        self.nombreAlarma=None
        
        self.btn_editar.clicked.connect(self.editar)
        self.textEdit_alarma.setReadOnly(True)
        self.hoSli_estado.valueChanged.connect(self.activarDesactivarAlarma)
        self.hoSli_estado.setValue(1)
    
    def cargarAlarma(self,alarma):
        self.nombreAlarma=alarma.nombre

        horaAlarma=QTime()
        horaAlarma.setHMS(alarma.hora,alarma.minuto,0)
        horaAlarma=horaAlarma.toString("hh:mm")
        print("HORA:",horaAlarma)
        
        self.textEdit_alarma.setText("""<h1>{}  </h1>
        <h3>{}: {}</h3>
        """.format(alarma.getHora_string(),alarma.nombre,alarma.getDias() ) )
    
    def activarDesactivarAlarma(self):
        if self.hoSli_estado.value():
            self.textEdit_alarma.setEnabled(True)
        #Si el control requerido es el control automatico,
        #se pondra otro diseño especial a los horizontal sliders...
        else:
            self.textEdit_alarma.setEnabled(False)


    def editar(self):
        self.ventana=ItemAlarmaEdit()
        #getDatosAlarma(self,nombreAlarma):
        self.ventana.modoTrabajo(modoEdicion=True,nombreAlarma=self.nombreAlarma)
        self.ventana.senal_alarmaEditada.connect(self.alarmaEditada)
        self.ventana.show()
        #del (self.ventana)

    def alarmaEditada(self,alarma):
        #print(alarma[0])
        #print(type(alarma[0]))
        alarma=alarma[0]
        self.cargarAlarma(alarma)
        self.senal_alarmaEditada.emit(True)
        del(self.ventana)


    def mandarSenalMuerto(self):
        self.suHoraMorir.emit( [self.id,self.nombreAlarma] )



if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = ItemAlarmaVista()
    application.show()
    app.exec()
    #sys.exit(app.exec())





#FUENTE DE ICONOS:
#https://p.yusukekamiyamane.com/
#https://icons8.com/?utm_source=http%3A%2F%2Ficons8.com%2Fweb-app%2Fnew-icons%2Fall&utm_medium=link&utm_content=search-and-download&utm_campaign=yusuke
