from PyQt5.QtWidgets import  QDialog,QApplication
from PyQt5 import QtWidgets
from functools import partial
from PyQt5.QtWidgets import (QMessageBox,QButtonGroup,QDialog)
from PyQt5.QtCore import QTimer, QTime, Qt,QDateTime,QDate,QCoreApplication
import datetime

###############################################################
#  IMPORTACION DEL DISEÑO...
##############################################################
from CUERPO.DISENO.SISTEMA_CONTROL.main_dise import Ui_Form
###############################################################
#  MIS LIBRERIAS...
##############################################################
from CUERPO.LOGICA.SISTEMA_CONTROL.configLed import Dialog_configLed
from CUERPO.LOGICA.SISTEMA_CONTROL.configVenti import Dialog_configVenti
from CUERPO.LOGICA.SISTEMA_CONTROL.datosCreador import Dialog_datosCreador
from CUERPO.LOGICA.ALARMA.administradorAlarmas import AdministradorAlarmas

from CUERPO.LOGICA.DEBERES.SeccionNotas import SeccionNotas
from CUERPO.LOGICA.SISTEMA_CONTROL.arduinoExtension import ArduinoExtension_hilo
from CUERPO.LOGICA.SISTEMA_CONTROL.bluetoothSerial import BluetoothSerial_hilo


class Main_IoT(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        Ui_Form.__init__(self)
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)

        self.tempActual=22 #La temperatura que se esta sensando
        self.tempPrenderaVenti=100 #La temperatura a la cual se va a prender el ventilador



#Cuadros emergentes de dialogos:

        self.venConfig_foco=Dialog_configLed()#cuadro de dialogo que nos permitira
        #modicar el color al cual se prendera el led
        self.venConfig_venti=Dialog_configVenti(self.tempPrenderaVenti)#cuadro de dialogo
        #que nos permitira editar la temperatura a la cual se prendera el ventilador

        self.venDatosCreador=Dialog_datosCreador()
      

        #Asociando las señales de los cuadros de dialogo con funciones:
        self.venConfig_foco.senal_colorElegido.connect(self.cambiarColorFoco)
        self.venConfig_venti.senal_cambioTempPrendeVenti.connect(self.cambiarTempPrendeVenti)

        #Botones que nos permitiran llamar a los cuadros de dialogo:
        self.btn_configFoco.clicked.connect(self.configurarFoco)
        self.btn_configVenti.clicked.connect(self.configurarVenti)
        self.btn_info.clicked.connect( lambda x : self.venDatosCreador.show() )

#Hilos:

        #Hilo que nos permitira la comunicación entre la rasberry pi y el arduino nano:
        #self.extencionArduino=ArduinoExtension_hilo(velocidad=9600,puerto="COM6")

        #Hilo que nos permitira la comunicación entre la rasberry pi y el modulo Bluetooth HC-05:
        #self.bluetooth=BluetoothSerial_hilo(velocidad=9600,puerto="COM5")
         
        #Asociando algunas señales de los hilos:
    
        #self.extencionArduino.senal_prenderFoco.connect(self.cambiarEstadoFoco)
        #self.extencionArduino.senal_prenderVentilador.connect(self.cambiarEstadoVenti)
        
        #self.extencionArduino.senal_actTemp.connect(self.actualizarTemp)

#Iniciando los hilos...
        #self.extencionArduino.start()
        #self.bluetooth.start()



#Horizontal Sliders:

        #Asociando la señal del horizontal slider que emite cuando cambia de posición,
        # con el motivo de permitirnos  apagar o prender el foco:
        self.hoSli_foco.valueChanged.connect(self.prenderApagarFoco)

        #Asociando el horizontal slider que emite cuando cambia de posición,
        # con el motivo de permitirnos  apagar o prender el ventilador:
        self.hoSli_venti.valueChanged.connect(self.prenderApagarVenti)


#Radio botton(alternadores de control automatico o manual):
        #Cuando el radio boton que nos permite tener un control manual 
        # del sistema emite la señal que ha cambiado su valor, lo ligamos
        # a la funcion 'cambiarControl'
        self.rb_controlManual.toggled.connect(self.cambiarControl)

        self.rb_controlAutomatico.toggle() #Como valor por default nos decantamos por un
        #control automatico


#Ajustando fechas
  
        tiempo = QTime.currentTime() 
        self.timeEdit_tiempo.setTime(tiempo)
        #print ( tiempo.toString(Qt.DefaultLocaleLongDate) )

        self.fechaHoy=QDate.currentDate()
        #donde 1 es el lunes y 7 es el domingo.
        #https://zetcode.com/gui/qt5/datetime/
        noDiaEntreSemana=self.fechaHoy.dayOfWeek()-1  
        
        self.dateEdit_fecha.setDate(self.fechaHoy)
        #print (fecha.toString ()) 

        print("SEMANA QUE PASO:",noDiaEntreSemana)

        self.hora=QTime(tiempo.hour(),  tiempo.minute(),  tiempo.second(), 0 )


#Seccion de alarmas y notas
        self.seccionAlarmas=AdministradorAlarmas(noDiaEntreSemana,tiempo.hour(),tiempo.minute(),tiempo.second() ) #creando widget de alarmas
        self.seccionNotas=SeccionNotas() #creando widget de notas
        self.seccionAlarmas.reloj.senal_minutoCambio.connect(self.cambiarMinuteroRelojMostrador)

        self.seccionAlarmas.reloj.senal_diaCambio.connect(lambda x : self.dateEdit_fecha.setDate( self.fechaHoy.addDays(1)  )  )


        #Agregando los widgets anteriores al 'tabWidget' 
        self.tabWidget.addTab(self.seccionNotas,"Anotaciones")
        self.tabWidget.addTab(self.seccionAlarmas,"Alarmas")
        
#Valores default:
        self.rb_controlAutomatico.toggle() #Como valor por default nos decantamos por un
        #control automatico
        self.cambiarControl() #para que se activen los colores respectivos al control automatico

        self.prenderApagarVenti(prender=False)
        self.prenderApagarFoco(prender=False)

        self.cambiarTempPrendeVenti(self.tempPrenderaVenti)#poniendo en la etiqueta la 
        #temperatura a la cual nos encontramos


    def cambiarMinuteroRelojMostrador(self):
         self.hora=self.hora.addSecs(60)
         #self.timeEdit_tiempo.addSecs(1)
         self.timeEdit_tiempo.setTime(self.hora)

#########################################################################################################################
#    C O N T R O L      D E L     S I S T E M A 
# #######################################################################################################################    
    def cambiarControl(self):
        '''Cambiara el diseño de los horizontal sliders en función de si
        se configuro un control automatico o manual del sistema
        '''
        #Si el control requerido es el control manual,
        #se pondra un diseño especial a los horizontal
        #sliders...
        controlManual=self.rb_controlManual.isChecked()
        
        #Editando el diseños de los horizontal sliders:
        self.hoSli_foco.setEnabled(controlManual)
        self.hoSli_venti.setEnabled(controlManual)


        #Como el ventilador depende de la temperatura es importante poner en contexto
        #a lo que el hilo esta haciendo
        
        #self.cambiarEstadoVenti(prender=self.extencionArduino.ventilador_on)
        #self.extencionArduino.foco_on=self.hoSli_venti.value() 

#########################################################################################################################
#    F O C O :
# #######################################################################################################################    

    def configurarFoco(self):
        '''Mostrara el cuadro de dialogo que nos permitira modicar
        el color del foco
        '''
        self.venConfig_foco.show()    

    def cambiarEstadoFoco(self,prender):
        #esto simula que alguien cambio la posicion del slider
        #por ende al hacer eso se llamara a la función asociada
        #a la señal cuando se activa o desactiva el slider

        #solo se efecturan los cambios si el control automatico
        #esta activado
        if self.rb_controlAutomatico.isChecked():
            self.hoSli_foco.setValue( prender ) #prender=False=0 prender=True=1


    def prenderApagarFoco(self,prender):
        if prender:#
            self.bel_estadoFoco.setStyleSheet("border-image: url(:/SISTEMA_CONTROL/IMAGENES/SISTEMA_CONTROL/foco_on.png);")
            #self.bluetooth.foco_prenderApagar(prender=True)
        else:
            self.bel_estadoFoco.setStyleSheet("border-image: url(:/SISTEMA_CONTROL/IMAGENES/SISTEMA_CONTROL/foco_off.png);")
            #self.bluetooth.foco_prenderApagar(apagar=True)
            
    def cambiarColorFoco(self,listDatos):
        idColor=listDatos[0]
        colorRGB=listDatos[1]
        self.btn_configFoco.setStyleSheet("""border :3px solid black;
                                            border-radius: 15px;
                                            background-color: rgb{};""".format(colorRGB))
        print("Color recibido:",idColor)
        #self.bluetooth.foco_cambiarColor(idColor)

#########################################################################################################################
#    V E N T I L A D O R : 
# #######################################################################################################################    

    def configurarVenti(self):
        '''Mostrar el cuadro de dialogo que nos permitira
        editar la temperatura a la cual el ventilador
        se preder automaticamente...'''
        self.venConfig_venti.show()


    def cambiarEstadoVenti(self,prender):
        #solo se efectura si el control automatico
        #esta activado:
        if self.rb_controlAutomatico.isChecked():
            self.hoSli_venti.setValue( prender )  #prender=False=0 prender=True=1  


    def prenderApagarVenti(self,prender):
        if prender:
            self.bel_estadoVenti.setStyleSheet("border-image: url(:/SISTEMA_CONTROL/IMAGENES/SISTEMA_CONTROL/ventilador_on.png);")
            #self.bluetooth.venti_prenderApagar(prender=True)
        else:
            self.bel_estadoVenti.setStyleSheet("border-image: url(:/SISTEMA_CONTROL/IMAGENES/SISTEMA_CONTROL/ventilador_off.png);")
            #self.bluetooth.venti_prenderApagar(apagar=True)

    def cambiarTempPrendeVenti(self,nuevaTemp):
        print("Nueva temp:",nuevaTemp)
        self.btn_configVenti.setText(str(nuevaTemp)+" [°C]")
        #self.extencionArduino.tempPrenderaVenti=nuevaTemp

    def actualizarTemp(self,nuevaTemp_str):
        self.bel_temp.setText( nuevaTemp_str )
            

#########################################################################################################################
#    O T R A S   F U N C I O N E S : 
# #######################################################################################################################    

    def closeEvent(self,event):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Question)
        ventanaDialogo.setWindowTitle('Salir')
        #QCoreApplication.translate('A', "Hello")
        ventanaDialogo.setText("¿Seguro que quieres salir?")
        ventanaDialogo.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        btn_yes = ventanaDialogo.button(QMessageBox.Yes)
        btn_yes.setText('Si')
        btn_no = ventanaDialogo.button(QMessageBox.No)
        btn_no.setText('No')
        ventanaDialogo.exec_()
        if ventanaDialogo.clickedButton()  ==  btn_yes:
            self.seccionNotas.respaldarDeberes()
            event.accept()
        else:
            event.ignore()  # No saldremos del evento


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = Main_IoT()
    application.show()
    app.exec()
    #sys.exit(app.exec())

