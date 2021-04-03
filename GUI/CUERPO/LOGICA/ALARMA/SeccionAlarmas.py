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
from CUERPO.DISENO.seccionAlarmas_dise import  Ui_Form 

###############################################################
#  MIS LIBRERIAS...
##############################################################
from CUERPO.LOGICA.ALARMA.ItemAlarmaVista import ItemAlarmaVista
from CUERPO.LOGICA.ALARMA.ItemAlarmaEdit import ItemAlarmaEdit
from CUERPO.LOGICA.ALARMA.baseDatos_alarma import BaseDatos_alarmas
from CUERPO.LOGICA.recursos import Recursos_IoT_Domotica



class SeccionAlarmas(QtWidgets.QWidget,Ui_Form):
    quierePreguntaImagen = pyqtSignal()
    def __init__(self):
        Ui_Form.__init__(self)
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)

        self.baseDatosAlarmas=BaseDatos_alarmas(Recursos_IoT_Domotica.NOMBRE_BASE_DATOS_ALARMAS)
        self.baseDatosAlarmas.crearBaseDatos()
        self.ventanaCreadoraAlarmas=ItemAlarmaEdit()

    

        self.widget = QWidget()  # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()  # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        self.widget.setLayout(self.vbox)

        #Scroll Area Properties
        self.scroll_alarmas.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_alarmas.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_alarmas.setWidgetResizable(True)
        self.scroll_alarmas.setWidget(self.widget)
        self.MAX_ITEMS=20
        self.punteroNoItems=0
        self.contadorIdsVivosMuertos = 0


        #self.btn_agregarItem.clicked.connect(partial(self.agregarAlarma,Alarma()))
        self.btn_agregarItem.clicked.connect(self.crearUnaAlarma)
        self.listaItemsRonianos=[]
        self.textPregunta=""
        self.listIdsItemsVivos=[]
        
        self.cargarAlarmas()
        self.ventanaCreadoraAlarmas.senal_alarmaCreada.connect(self.nuevaAlarmaCreada)



    def cargarAlarmas(self):

        listaAlarmas=self.baseDatosAlarmas.getTodas_alarmas()
        #(   ('Julian', 1, 9, 30, 1, 1, 1, 0, 0, 0, 0, 0), ....   )
        
        for alarma in listaAlarmas:
            self.agregarAlarma(alarma=alarma)


    def crearUnaAlarma(self):
        self.ventanaCreadoraAlarmas.modoTrabajo(modoEdicion=False)
        self.ventanaCreadoraAlarmas.show()

    def nuevaAlarmaCreada(self,alarma):
        #print(alarma[0])
        #print(type(alarma[0]))
        alarma=alarma[0]
        self.agregarAlarma(alarma)

    def agregarAlarma(self,alarma):
        if self.punteroNoItems<self.MAX_ITEMS:
            itemAlarma=ItemAlarmaVista(id=self.contadorIdsVivosMuertos)
            itemAlarma.cargarAlarma(alarma)
            itemAlarma.suHoraMorir.connect(self.borrarItem)
            self.listIdsItemsVivos.append(self.contadorIdsVivosMuertos)

            self.vbox.addWidget(itemAlarma)
            self.punteroNoItems+=1
            self.contadorIdsVivosMuertos+=1
        else:
            QMessageBox.question(self, "DelphiPreguntas",
                                 "El numero maximo de items es de:\n"
                                 f"{self.MAX_ITEMS} items, y usted ya ha llegado\n"
                                 "a dicho limite.",
                                 QMessageBox.Ok)



    def borrarItem(self,listaIdIs_itemAMatar):
        print("BORRAR: ",listaIdIs_itemAMatar)
        idItemAMatar=listaIdIs_itemAMatar[0] #id en el orden las widget
        nombreAlarma=listaIdIs_itemAMatar[1] #id en la base de datos

        posItemMatar=self.listIdsItemsVivos.index(idItemAMatar)
        resultado = QMessageBox.question(self, "DelphiPreguntas",
                                            "¿Esta seguro que quieres\n"
                                            f"eliminar la alarma numero: {posItemMatar+1}\n"
                                            f" cuyo nombre es: {nombreAlarma}?",
                                            QMessageBox.Yes | QMessageBox.No)
        if resultado == QMessageBox.Yes:
            layout=self.vbox
            noWidgetBorrar=posItemMatar
            widgetToRemove = layout.itemAt(noWidgetBorrar).widget()
            # remove it from the layout list
            layout.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.setParent(None)

            #self.listaItemsRonianos.pop(posItemMatar)
            self.listIdsItemsVivos.pop(posItemMatar)
            self.punteroNoItems -= 1

            self.baseDatosAlarmas.eliminar(A=nombreAlarma)


    def closeEvent(self, event):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = SeccionAlarmas()
    application.show()
    app.exec()

    ##sys.exit(app.exec())


