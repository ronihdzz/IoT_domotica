from PyQt5.QtWidgets import  QDialog,QApplication
from PyQt5 import QtWidgets
from functools import partial
from PyQt5.QtWidgets import (QMessageBox,QButtonGroup,QDialog)

###############################################################
#  IMPORTACION DEL DISEÑO...
##############################################################
from CUERPO.DISENO.main_dise import Ui_Form
###############################################################
#  MIS LIBRERIAS...
##############################################################
from CUERPO.LOGICA.configLed import Dialog_configLed
from CUERPO.LOGICA.configVenti import Dialog_configVenti
from CUERPO.LOGICA.SeccionAlarmas import SeccionAlarmas
from CUERPO.LOGICA.SeccionNotas import SeccionNotas
from CUERPO.LOGICA.arduinoExtension import ArduinoExtension_hilo
from CUERPO.LOGICA.bluetoothSerial import BluetoothSerial_hilo


class Main_IoT(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        Ui_Form.__init__(self)
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)


        self.disenoManual=("#393939","#22B14C") #diseño de los horizontal sliders
        #cuando se quiere contralar de forma manual el foco y el ventilador
        self.disenoAutomatico=("#95DEE7","#95DEE7")#diseño de los horizontal sliders
        #cuando se quiere controlar de forma automatico al ventilador


        self.tempActual=22 #La temperatura que se esta sensando
        self.tempPrenderaVenti=100 #La temperatura a la cual se va a prender el ventilador
        self.cambiarTempPrendeVenti(self.tempPrenderaVenti)#poniendo en la etiqueta la 
        #temperatura a la cual nos encontramos


#Cuadros emergentes de dialogos:

        self.venConfig_foco=Dialog_configLed()#cuadro de dialogo que nos permitira
        #modicar el color al cual se prendera el led
        self.venConfig_venti=Dialog_configVenti(self.tempPrenderaVenti)#cuadro de dialogo
        #que nos permitira editar la temperatura a la cual se prendera el ventilador
      

        #Asociando las señales de los cuadros de dialogo con funciones:
        self.venConfig_foco.senal_colorElegido.connect(self.cambiarColorFoco)
        self.venConfig_venti.senal_cambioTempPrendeVenti.connect(self.cambiarTempPrendeVenti)

        #Botones que nos permitiran llamar a los cuadros de dialogo:
        self.btn_configFoco.clicked.connect(self.configurarFoco)
        self.btn_configVenti.clicked.connect(self.configurarVenti)

#Hilos:

        #Hilo que nos permitira la comunicación entre la rasberry pi y el arduino nano:
        #self.extencionArduino=ArduinoExtension_hilo(velocidad=9600,puerto="COM6")

        #Hilo que nos permitira la comunicación entre la rasberry pi y el modulo Bluetooth HC-05:
        #self.bluetooth=BluetoothSerial_hilo(velocidad=9600,puerto="COM5")
         

        #Asociando algunas señales de los hilos:
        #self.extencionArduino.senal_temperatura.connect(self.actualizarTemp)
        #self.extencionArduino.senal_aplausoDetectado.connect(self.cambiarEstadoFoco)

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



#Seccion de alarmas y notas
        self.seccionAlarmas=SeccionAlarmas() #creando widget de alarmas
        self.seccionNotas=SeccionNotas() #creando widget de notas
        #Agregando los widgets anteriores al 'tabWidget' 
        self.tabWidget.addTab(self.seccionNotas,"Anotaciones")
        self.tabWidget.addTab(self.seccionAlarmas,"Alarmas")
        

#Valores default:
        self.rb_controlAutomatico.toggle() #Como valor por default nos decantamos por un
        #control automatico
        self.cambiarControl() #para que se activen los colores respectivos al control automatico

        self.prenderApagarVenti(prender=False)
        self.prenderApagarFoco(prender=False)


        



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
        if self.rb_controlManual.isChecked():
            diseno=self.disenoManual 
            controlManual=True
        #Si el control requerido es el control automatico,
        #se pondra otro diseño especial a los horizontal sliders...
        else:
            diseno=self.disenoAutomatico
            controlManual=False
        
        disenoHorizontal="""QSlider {min-height: 40px;max-height: 40px;}
        QSlider::groove:horizontal {
            border: 1px solid #262626;
            height: 5px;
            margin: 0 12px;
            background:"""+diseno[0]+";}"
        disenoHorizontal+="""QSlider::handle:horizontal {
            width: 15px;
            height: 80px;
            margin: 24px -12px;
            background:"""+diseno[1]+"};"
        
        #Editando el diseños de los horizontal sliders:
        self.hoSli_foco.setStyleSheet(disenoHorizontal)
        self.hoSli_venti.setStyleSheet(disenoHorizontal)
        self.hoSli_foco.setEnabled(controlManual)
        self.hoSli_venti.setEnabled(controlManual)


#########################################################################################################################
#    F O C O :
# #######################################################################################################################    


    def configurarFoco(self):
        '''Mostrara el cuadro de dialogo que nos permitira modicar
        el color del foco
        '''
        self.venConfig_foco.show()    

    def cambiarEstadoFoco(self,dato):
        #esto simula que alguien cambio la posicion del slider
        #por ende al hacer eso se llamara a la función asociada
        #a la señal cuando se activa o desactiva el slider

        #solo se efecturan los cambios si el control automatico
        #esta activado
        if self.rb_controlAutomatico.isChecked():
            estado=not(self.hoSli_foco.value())
            self.hoSli_foco.setValue( estado ) 
    
    def prenderApagarFoco(self,prender=False):
        if prender:
            self.bel_estadoFoco.setStyleSheet("border-image: url(:/ICON/IMAGENES/foco_on.png);")
            #self.bluetooth.foco_prenderApagar(prender=True)
        else:
            self.bel_estadoFoco.setStyleSheet("border-image: url(:/ICON/IMAGENES/foco_off.png);")
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
    
    def prenderApagarVenti(self,prender=False):
        if prender:
            self.bel_estadoVenti.setStyleSheet("border-image: url(:/ICON/IMAGENES/ventilador_on.png);")
            #self.bluetooth.venti_prenderApagar(prender=True)
        else:
            self.bel_estadoVenti.setStyleSheet("border-image: url(:/ICON/IMAGENES/ventilador_off.png);")
            #self.bluetooth.venti_prenderApagar(apagar=True)
            
    def cambiarTempPrendeVenti(self,nuevaTemp):
        print("Nueva temp:",nuevaTemp)
        self.btn_configVenti.setText(str(nuevaTemp)+" [°C]")
        self.tempPrenderaVenti=nuevaTemp


    def actualizarTemp(self,nuevaTemp):
        nuevaTemp=float(nuevaTemp)
        if abs(nuevaTemp-self.tempActual)>0.3:
            self.tempActual=nuevaTemp
            print("temp Registrada: {}".format(nuevaTemp))
            self.bel_temp.setText(str(self.tempActual))

        #solo se efectura si el control automatico
        #esta activado:
        if self.rb_controlAutomatico.isChecked():
            if nuevaTemp>=self.tempPrenderaVenti:
                if not( self.hoSli_venti.value() ):
                    self.hoSli_venti.setValue(1)
            else:
                if self.hoSli_venti.value():
                    self.hoSli_venti.setValue(0)
                    

#########################################################################################################################
#    O T R A S   F U N C I O N E S : 
# #######################################################################################################################    

    def closeEvent(self,event):
        resultado = QMessageBox.question(self, "Salir ...",
                                            "¿Seguro que quieres salir?",
                                            QMessageBox.Yes | QMessageBox.No)
        if resultado == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()  # No saldremos del evento


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = Main_IoT()
    application.show()
    app.exec()
    #sys.exit(app.exec())

