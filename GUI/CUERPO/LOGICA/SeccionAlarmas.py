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
from CUERPO.LOGICA.ItemAlarmaVista import ItemAlarmaVista



class SeccionAlarmas(QtWidgets.QWidget, Ui_Form):
    quierePreguntaImagen = pyqtSignal()
    def __init__(self):
        Ui_Form.__init__(self)
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)

        self.SEPARADOR_ITEMS = "-*^~^*-"

        self.widget = QWidget()  # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()  # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        self.widget.setLayout(self.vbox)

        #Scroll Area Properties
        self.scroll_alarmas.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_alarmas.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_alarmas.setWidgetResizable(True)
        self.scroll_alarmas.setWidget(self.widget)
        self.MAX_ITEMS=6
        self.punteroNoItems=0
        self.contadorIdsVivosMuertos = 0
        
        
        self.btn_agregarItem.clicked.connect(partial(self.agregarCheckBox,"",False))
        self.listaItemsRonianos=[]
        self.textPregunta=""
        self.listIdsItemsVivos=[]


    def closeEvent(self, event):
        pass

        
    def agregarCheckBox(self,texto="",estado=0):
        if self.punteroNoItems<self.MAX_ITEMS:
            itemAlarma=ItemAlarmaVista(self.contadorIdsVivosMuertos)
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
    def borrarTodosItems(self):
        print("BORRAREMOS ",self.punteroNoItems," items,,,")
        print("lista de posiciones...",self.listIdsItemsVivos)

        #Debemos hacer una copia a esa lista ya que cuando
        #estemos eliminando elemento por elemento puede
        #suceder un error...
        copyList=self.listIdsItemsVivos.copy()
        print("COPY...",copyList)

        for x in copyList:
            self.borrarItem(x,False)


    def borrarItem(self,idItemAMatar,ordenAutomatica=True):
        posItemMatar=self.listIdsItemsVivos.index(idItemAMatar)
        resultado=QMessageBox.Yes
        if ordenAutomatica:
            resultado = QMessageBox.question(self, "DelphiPreguntas",
                                             "¿Esta seguro que quieres\n"
                                             f"eliminar el item numero {posItemMatar+1}?",
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


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = SeccionAlarmas()
    application.show()
    app.exec()
    #sys.exit(app.exec())


