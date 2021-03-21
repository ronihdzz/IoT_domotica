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

        self.foco_prendido=False
        self.ventilador_prendido=False
        self.disenoManual=("#393939","#22B14C")
        self.disenoAutomatico=("#95DEE7","#95DEE7")


        self.tempActual=22 #temperatura actual...
        self.tempPrenderaVenti=100
        self.cambiarTempPrendeVenti(self.tempPrenderaVenti)


        self.venConfig_foco=Dialog_configLed()
        self.venConfig_venti=Dialog_configVenti(self.tempPrenderaVenti)
      

        self.venConfig_foco.senal_colorElegido.connect(self.cambiarColorFoco)
        self.venConfig_venti.senal_cambioTempPrendeVenti.connect(self.cambiarTempPrendeVenti)

        #Configuración de los parametros de automatización
        self.btn_configFoco.clicked.connect(self.configurarFoco)
        self.btn_configVenti.clicked.connect(self.configurarVenti)


        #Configuraciones de la extensión de arduino en la Rasberry pi
        #self.extencionArduino=ArduinoExtension_hilo(velocidad=9600,puerto="COM6")
        #self.bluetooth=BluetoothSerial_hilo(velocidad=9600,puerto="COM5")
         


        #self.extencionArduino.senal_temperatura.connect(self.actualizarTemp)
        #self.extencionArduino.senal_aplausoDetectado.connect(self.cambiarEstadoFoco)
        #self.extencionArduino.start()
        #self.bluetooth.start()

        self.hoSli_foco.valueChanged.connect(self.prenderApagarFoco)
        self.hoSli_venti.valueChanged.connect(self.prenderApagarVenti)
        self.hoSli_venti.setEnabled(False)
        #self.hoSli_foco.setEnabled(False)

        self.venConfig_venti.temp_prendeVentilador



        


        self.seccionAlarmas=SeccionAlarmas()
        self.seccionNotas=SeccionNotas()
        self.tabWidget.addTab(self.seccionNotas,"Anotaciones")
        self.tabWidget.addTab(self.seccionAlarmas,"Alarmas")
        
        self.rb_controlManual.toggled.connect(self.cambiarControl)
        self.rb_controlAutomatico.toggle() #lo seleccionamos

    def cambiarControl(self):
        if self.rb_controlManual.isChecked():
            diseno=self.disenoManual
        else:
            diseno=self.disenoAutomatico
        
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
        self.hoSli_foco.setStyleSheet(disenoHorizontal)
        self.hoSli_venti.setStyleSheet(disenoHorizontal)
    def cambiarEstadoFoco(self,dato):
        #esto simula que alguien cambio la posicion del slider
        #por ende al hacer eso se llamara a la función asociada
        #a la señal cuando se activa o desactiva el slider
        estado=not(self.foco_prendido)
        estado=int(estado)
        self.hoSli_foco.setValue( estado ) 
    
    def prenderApagarFoco(self,dato):
        self.foco_prendido=not(self.foco_prendido)
        if self.foco_prendido:
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

    def actualizarTemp(self,nuevaTemp):
        nuevaTemp=float(nuevaTemp)
        if abs(nuevaTemp-self.tempActual)>0.3:
            self.tempActual=nuevaTemp
            print("temp Registrada: {}".format(nuevaTemp))
            self.bel_temp.setText(str(self.tempActual))
        if nuevaTemp>=self.tempPrenderaVenti:
            if not(self.ventilador_prendido):
                self.hoSli_venti.setValue(1)
                #self.prenderApagarVenti(prender=True)
        else:
            if self.ventilador_prendido:
                self.hoSli_venti.setValue(0)
                #self.prenderApagarVenti(prender=False)


    def prenderApagarVenti(self,prender):
        self.ventilador_prendido=not(self.ventilador_prendido)
        print("*****************************************=",prender)
        #if self.ventilador_prendido:
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

    def configurarFoco(self):
        self.venConfig_foco.show()    
    def configurarVenti(self):
        self.venConfig_venti.show()
    def configurarAlarma(self):
        #self.venConfig_alarma.show()
        #self.scrollControl.agregarCheckBox()
        pass

    
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


'''
EDITAR...

QSlider {
    min-height: 40px;
    max-height: 40px;
}

QSlider::groove:horizontal {
    border: 1px solid #262626;
    height: 5px;
    background: #393939;
    margin: 0 12px;
}

QSlider::handle:horizontal {
    background: #22B14C;
	/*background-color: rgb(1, 255, 226);*/
    /*border: 5px solid #B5E61D;*/
    width: 15px;
    height: 80px;
    margin: 24px -12px;
}


AUTOMATICO...




'''
