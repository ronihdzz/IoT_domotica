from logging import debug, log
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
from logger import logger


class ItemDeber(QtWidgets.QWidget,Ui_Form):
    '''
    Los objetos de esta clase estaran compuestos de:
        A) Un 'QLineEdit' -.Este servira para que escriba el texto del deber.
        B) Un 'QCheckBox' -.Este servira para ser seleccionado cuando el deber 
        haya sido cumplido.
    
    Los objetos de esta clase tendran metodos que permitan cambiar el tamaño
    del texto del deber asi como la posicion del texto del deber, entre otras 
    cosas.

    Cuando se crea un instancia de esta clase, se le asignara un 'id' unico
    el cual sera igual valor de la variable estatica: 'NUMERO_ITEM_DEBER_CREADOS'
    en ese momento.  

    ¿Por que el id de la instancia que se crea sera igual al numero de instancias
    creadas hasta ese momento?

    Supongamos que se abre el programa y hasta el momento no se ha creado ninguna 
    instancia de la clase 'ItemDeber' pero despues se crea una, y se le asigna el 
    'id'=1, despues se crea una mas y se le asigna el 'id'=2 despues se crea otra mas 
    y se le asigna el 'id'=3 despues se crea otro mas y se le asigna el 'id'=4.

    ¿que pasa si se elimina la instancia con 'id'=2? R=Pues ya solo sobrarian las 
    instancias con 'id' iguales a: 1,3 y 4  es decir ya solo sobrarian 3 instancias. 
    Ahora supongamos que se crea otra instancia ¿que valor de 'id' se le deberia 
    asignar para que sea unico e irrepetible entre las instancias creadas hasta ese
    momento? 
    A) Si le asignaramos como 'id' el numero de instancias existentes entonces le deberia 
    asignar el valor 3 como 'id', sin embargo ese 'id' ya fue asignado y aun sigue existiendo 
    la instancias con dicho 'id' asi que no serviria la idea de asignar como valor de 'id' 
    instancias vivas hasta ese momento
    B) Si le asignaramos como valor 'id' el numero de instancias que se han creado no importando 
    si ya fueron eliminadas o siguen ahi, entonces se le deberia asignar el 'id'=5 el cual es 
    complemente diferente a los 'id' de las instnacias aun vivas y muertas, por ende eso es lo que 
    hago se hace para asignarle un 'id' unico a cada instancia  que se ha creado desde que se
    abrio el programa.
    '''
    senal_deberCumplido= pyqtSignal(int)   # esta señal se emitira cuando el usuario haya dado clic sobre
                                           # el checbox y emitira el 'id'
    NUMERO_ITEM_DEBER_CREADOS=0    # llevara el conteo de todas las instancias realizadas de la clase
                                   # 'ItemDeber'
    
    def __init__(self,idAlineacion,tamanoLetra,texto=None):
        Ui_Form.__init__(self)
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)

        # El 'id' de la instancia sera igual al numero de instancias generados de la clase hasta ese momento 
        self.id=ItemDeber.NUMERO_ITEM_DEBER_CREADOS
        
        # Como ya se esta creando una instancia mas, entonces se actualiza el valor de: 'NUMERO_ITEM_DEBER_CREADOS' 
        ItemDeber.NUMERO_ITEM_DEBER_CREADOS=ItemDeber.NUMERO_ITEM_DEBER_CREADOS+1

    
        # validación = no se permite escribir los acentos circunflejos  '^' debido a que estos son los utilizados
        # para separar los deberes que se respaldaran en un archivo de texto, no se permiten mas de 400 caracteres
        validator = QRegExpValidator(QRegExp("[^\^]{1,400}"))  
        self.lineEdit_deber.setValidator(validator)
        
        # se cargara el texto del deber en caso de existir
        if texto!=None and type(texto)==str:
            self.lineEdit_deber.setText(texto)
        else:
            self.lineEdit_deber.setText('')

        logger.debug("Creando una instancia de las clase: ItemDeber, nombre asignado= '{}'".format(self) )


        self.alinear(idAlineacion)
        self.cambiarTamano(tamanoLetra)
        
        # senal que se activa cuando el checbox es seleccionado
        self.estadoDeber.toggled.connect( self.verificarCumplio_deber )

        self.lineEdit_deber.setStyleSheet("border:1px solid #C4C8C0; border-radius:10%")

        
    
    def __str__(self):
        return "Deber_{}_{}".format(self.id,self.lineEdit_deber.text() )

    def alinear(self,idAlineo):
        '''
        Ajustara el texto del atributo de instancia 'self.lineEdit_deber' en funcion
        del valor del parametro 'idAlineo'

        Parámetros:
            idAlineo -- Numero natural entero. 
            Posibles valores:
                A) Si 'idAlineo'=0 significa que se desea alinear el texto a la izquierda
                B) Si 'idAlineo'=1 significa que se desea alinear el texto al centro
                C) Si 'idAlineo'=2 significa que se desea alinear el texto a la derecha
        '''

        logger.debug(f'{self}, cambiando a posición de texto={idAlineo}')

        if idAlineo==0:
            self.lineEdit_deber.setAlignment(QtCore.Qt.AlignLeft)
        elif idAlineo==1:
            self.lineEdit_deber.setAlignment(QtCore.Qt.AlignCenter) 
        elif idAlineo==2:
            self.lineEdit_deber.setAlignment(QtCore.Qt.AlignRight) 
        
    def cambiarTamano(self,nuevoTamano):
        '''
        Cambiara el tamaño del texto del atributo de instancia 'self.lineEdit_deber'
        al valor del parametro 'nuevoTamano'

        Parámetros:
            nuevoTamano -- Numero natural entero que indica el valor del nuevo tamaño
            de letra del texto del atributo 'self.lineEdit_deber'
        '''

        logger.debug(f'{self}, cambiando el tamaño de letra a tamaño={nuevoTamano}')

        self.lineEdit_deber.setFont(QFont('Arial',nuevoTamano))


    def verificarCumplio_deber(self):
        '''
        Cada vez que el usuario seleccione el checbox o mejor dicho al atributo:
        'self.estadoDeber' significara que ya ha realizado el deber y por ende
        el deber debe mandarse la señal para que  sea eliminado, pero como siempre 
        los errores pueden ocurrir asi que antes de  mandar la señal para indicar 
        que el deber debe ser eliminado, se le preguntara al usuario si efectivamente 
        ya ha cumplido el deber al deber, en caso de que se responda afirmativo
        se mandara la señal para el deber sea eliminado.
        '''
        
        # ¿el checkbox fue seleccionado?
        if self.estadoDeber.isChecked(): 
            # preguntar si efectivamente ya se termino el deber
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
                # debido a que se confirmo positivamente entonces se proseguira a mandar
                # la señal para que esta instancia sea eliminada de la seccion de deberes.
                self.senal_deberCumplido.emit(self.id)
            else:
                self.estadoDeber.setChecked(False)