from PyQt5 import QtWidgets,Qt
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QPushButton,QGridLayout,QCheckBox,QTextEdit
from PyQt5.QtWidgets import  QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal,QObject,QTime
from PyQt5 import QtCore
#import numpy as np
import os
from functools import partial
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtGui import QDoubleValidator,QRegExpValidator
from PyQt5.QtCore import QRegExp

###############################################################
#  IMPORTACION DEL DISEÑO...
##############################################################
from CUERPO.DISENO.DEBERES.itemDeber_dise import Ui_Form

###############################################################
#  MIS LIBRERIAS...
##############################################################
from recursos import HuellaAplicacion

class ItemDeber(QtWidgets.QWidget,Ui_Form):
    senal_deberCumplido= pyqtSignal(int)#indicara quien es el objeto que quiere morir...
    #[id,nombre]
    

    def __init__(self,id,texto,idAlineacion,tamanoLetra):
        Ui_Form.__init__(self)
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)

        self.id=id


        # validacion del nombre de usuario...
        validator = QRegExpValidator(QRegExp("[^\^]{1,400}"))  # maximo solo 15 caracteres
        self.lineEdit_deber.setValidator(validator)
        self.lineEdit_deber.setText(texto)


        self.alinear(idAlineacion)
        self.cambiarTamano(tamanoLetra)

        #self.textEdit_deber.setMSize(30,30)
        self.estadoDeber.toggled.connect( self.verificarCumplio_deber )


    def alinear(self,idAlineo):
        if idAlineo==0:
            self.lineEdit_deber.setAlignment(QtCore.Qt.AlignLeft)
        elif idAlineo==1:
            self.lineEdit_deber.setAlignment(QtCore.Qt.AlignCenter) 
        elif idAlineo==2:
            self.lineEdit_deber.setAlignment(QtCore.Qt.AlignRight) 
        
    def cambiarTamano(self,nuevoTamano):
        self.lineEdit_deber.setFont(QFont('Arial',nuevoTamano))


    def verificarCumplio_deber(self):
        if self.estadoDeber.isChecked():
            ventanaDialogo = QMessageBox()
            ventanaDialogo.setIcon(QMessageBox.Question)
            ventanaDialogo.setWindowIcon( QIcon(HuellaAplicacion.ICONO_APLICACION)  )
            ventanaDialogo.setWindowTitle(HuellaAplicacion.NOMBRE_APLICACION)

            mensaje="Bien hecho, confirma de que haz cumplido :D" 
            ventanaDialogo.setText(mensaje)
            ventanaDialogo.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
            btn_yes = ventanaDialogo.button(QMessageBox.Yes)
            btn_yes.setText('Si')
            btn_no = ventanaDialogo.button(QMessageBox.No)
            btn_no.setText('No')
            ventanaDialogo.exec_()
            if ventanaDialogo.clickedButton()  ==  btn_yes:
                self.senal_deberCumplido.emit(self.id)
            else:
                self.estadoDeber.setChecked(False)
            
