from PyQt5 import QtWidgets,Qt
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QPushButton,QGridLayout,QCheckBox,QTextEdit,QMenu
from PyQt5.QtWidgets import  QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal,QObject,QEvent
from PyQt5 import QtCore


#import numpy as np
import os
from functools import partial
from PyQt5.QtCore import QTimer, QTime, Qt,QObject,pyqtSignal

###############################################################
#  IMPORTACION DEL DISEÑO...
##############################################################
from CUERPO.DISENO.itemAlarmaEdit_dise import Ui_Dialog

###############################################################
#  MIS LIBRERIAS...
##############################################################
from CUERPO.LOGICA.ALARMA.alarma import Alarma
from CUERPO.LOGICA.ALARMA.baseDatos_alarma import BaseDatos_alarmas
from CUERPO.LOGICA.recursos import Recursos_IoT_Domotica
from CUERPO.LOGICA.ALARMA.reproductorSonidosAlarmas import ReproductorSonidosAlarmas

#https://learndataanalysis.org/source-code-how-to-implement-context-menu-to-a-qlistwidget-pyqt5-tutorial/
#https://stackoverflow.com/questions/59798284/pyqt-multiple-objects-share-context-menu

class ItemAlarmaEdit(QtWidgets.QDialog,Ui_Dialog):

    senal_alarmaCreada=pyqtSignal(list)
    senal_alarmaEditada=pyqtSignal(list)
    def __init__(self):
        Ui_Dialog.__init__(self)
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.baseDatosAlarmas=BaseDatos_alarmas(Recursos_IoT_Domotica.NOMBRE_BASE_DATOS_ALARMAS)
        self.reproductor=ReproductorSonidosAlarmas(self,Recursos_IoT_Domotica.CARPETA_MUSICA)

            
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        self.setWindowTitle(" ")
        self.setWindowModality(Qt.ApplicationModal)

        self.tuplaDias_rb=(self.cB_1, self.cB_2, self.cB_3, self.cB_4,
        self.cB_5, self.cB_6, self.cB_7  )
        self.mostrarSonidosParaAlarma()
        


        self.btn_finalizar.clicked.connect(self.terminar)
        self.btn_addCancion.clicked.connect(self.agregarUnaCancion)
        self.listWidget_sonidosAlarmas.itemDoubleClicked.connect(self.reproducirSonidoAlarma)


        self.listWidget_sonidosAlarmas.installEventFilter(self)



    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and source is  self.listWidget_sonidosAlarmas:
            menu = QMenu()
            menu.addAction('Action 1')
            menu.addAction('Action 2')
            menu.addAction("Eliminar",self.correr)
            if menu.exec_(event.globalPos()):
                item = source.itemAt(event.pos())
                print(item.text())
            return True
        return super().eventFilter(source, event)
    
    def correr(self):
        print("Corriendo")

    def agregarUnaCancion(self):
        self.reproductor.agregarUnaCancion()

    def modoTrabajo(self,modoEdicion=False,alarma=None):
        if modoEdicion:
            if alarma:
                self.nombreAlarmaEditar=alarma.nombre #el nombre es el id de cada alarma registrada
                self.mostrarAlarmaEditar(alarma)
        else:
            self.mostrarAlarmaBlanco() 

        self.modoEdicion=modoEdicion
        
    def reproducirSonidoAlarma(self,item):
        #id=self.listWidget_sonidosAlarmas.currentRow()
        nombreCancion=item.text()
        self.reproductor.tocar(nombreCancion)


    def mostrarSonidosParaAlarma(self):
        listaCanciones=self.reproductor.listaCanciones
        for cancion in listaCanciones:
            self.listWidget_sonidosAlarmas.addItem(cancion)

    def mostrarAlarmaEditar(self,alarma):
        self.lineEdit_nombre.setText(alarma.nombre)

        for c,diaRequerido in enumerate(alarma.diasActiva):
            if diaRequerido:
                self.tuplaDias_rb[c].setChecked(True)
            else:
                self.tuplaDias_rb[c].setChecked(False)

        self.comBox_asunto.setCurrentIndex(alarma.asunto)

        horaAlarma=QTime()
        horaAlarma.setHMS(alarma.hora,alarma.minuto,0)
        self.timeEdit_hora.setTime( horaAlarma )


    def mostrarAlarmaBlanco(self):
        self.mostrarAlarmaEditar( Alarma() )

    def terminar(self):
        nombre=self.lineEdit_nombre.text()
    
        #Guardando los dias que son...
        diasActiva=[0,0,0,0,0,0,0] 
        for c,rb_dia in enumerate(self.tuplaDias_rb):
            if rb_dia.isChecked():
                diasActiva[c]=1

        #Guardando el asunto:
        asunto=self.comBox_asunto.currentIndex()

        hora=self.timeEdit_hora.time().hour()
        minuto=self.timeEdit_hora.time().minute()

        alarma=Alarma(nombre=nombre,asunto=asunto,hora=hora,minuto=minuto,diasActiva=diasActiva)
       
        if not(self.modoEdicion):
            self.senal_alarmaCreada.emit([alarma])
            self.baseDatosAlarmas.addAlarma(alarma)
        else:
            self.senal_alarmaEditada.emit([alarma])
            self.baseDatosAlarmas.eliminar(A=self.nombreAlarmaEditar)
            self.baseDatosAlarmas.addAlarma(alarma)

        self.close()

    def closeEvent(self,event):
        self.reproductor.detener()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = ItemAlarmaEdit()
    application.show()
    app.exec()
    #sys.exit(app.exec())





#FUENTE DE ICONOS:
#https://p.yusukekamiyamane.com/
#https://icons8.com/?utm_source=http%3A%2F%2Ficons8.com%2Fweb-app%2Fnew-icons%2Fall&utm_medium=link&utm_content=search-and-download&utm_campaign=yusuke
