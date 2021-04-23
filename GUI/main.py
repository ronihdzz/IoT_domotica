from PyQt5.QtWidgets import  QDialog,QApplication
from PyQt5 import QtWidgets
from functools import partial
from PyQt5.QtWidgets import (QMessageBox,QButtonGroup,QDialog)
from PyQt5.QtCore import QTimer, QTime, Qt,QDateTime,QDate,QCoreApplication
import datetime
import os

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
from CUERPO.LOGICA.SISTEMA_CONTROL.alertadorFuego import Dialog_alertadorFuego
from CUERPO.LOGICA.ALARMA.administradorAlarmas import AdministradorAlarmas

from CUERPO.LOGICA.DEBERES.SeccionNotas import SeccionNotas
from CUERPO.LOGICA.SISTEMA_CONTROL.arduinoExtension import ArduinoExtension_hilo
from CUERPO.LOGICA.SISTEMA_CONTROL.bluetoothSerial import BluetoothSerial_hilo
from CUERPO.LOGICA.RECURSOS.recursos import Recursos_IoT_Domotica


#El diseno default son los sliders apagados la temp con 100 y el radio buttom en automatico

class Main_IoT(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        Ui_Form.__init__(self)
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)

#Cuadros emergentes de dialogos:
        #cuadro de dialogo que nos permitira modicar el color al cual se prendera el led
        self.venConfig_foco=Dialog_configLed()
        # cuadro de dialogo que nos permitira editar la temperatura a la cual se prendera el ventilador
        self.venConfig_venti=Dialog_configVenti()       
        self.venDatosCreador=Dialog_datosCreador()
        self.venAlertadorFuego=Dialog_alertadorFuego()
      

        #Asociando las señales de los cuadros emergentes de dialogo
        self.venConfig_foco.senal_colorElegido.connect(self.cambiarColorFoco)
        self.venConfig_venti.senal_cambioTempPrendeVenti.connect(self.cambiarTempPrendeVenti)
        
        #Botones que nos permitiran llamar a los cuadros de dialogo:
        self.btn_configFoco.clicked.connect( lambda : self.venConfig_foco.show() ) 
        self.btn_configVenti.clicked.connect( lambda : self.venConfig_venti.show() )
        self.btn_info.clicked.connect( lambda  : self.venDatosCreador.show() )
        

#Hilos:
        #Hilo que nos permitira la comunicación entre la rasberry pi y el arduino nano:
        self.extencionArduino=ArduinoExtension_hilo(velocidad=9600,puerto=Recursos_IoT_Domotica.ARDUINO_NANO_EXTENSION)
        #Hilo que nos permitira la comunicación entre la rasberry pi y el modulo Bluetooth HC-05:
        self.bluetooth=BluetoothSerial_hilo(velocidad=9600,puerto=Recursos_IoT_Domotica.BLUETOOTH_HC05)
         
        #Asociando algunas señales de los hilos:
        self.extencionArduino.senal_prenderFoco.connect(self.cambiarEstadoFoco)
        self.extencionArduino.senal_prenderVentilador.connect(self.cambiarEstadoVenti)
        self.extencionArduino.senal_actTemp.connect(self.actualizarTemp)


# Horizontal Sliders:
        # Asociando la señal del horizontal slider que emite cuando cambia de posición,
        # con el motivo de permitirnos  apagar o prender el foco:
        self.hoSli_foco.valueChanged.connect(self.prenderApagarFoco)
        # Asociando el horizontal slider que emite cuando cambia de posición,
        # con el motivo de permitirnos  apagar o prender el ventilador:
        self.hoSli_venti.valueChanged.connect(self.prenderApagarVenti)


# Detalles de alarma y notas:
        tiempo = QTime.currentTime() # obteniendo la hora actual
        self.timeEdit_tiempo.setTime(tiempo) # mostrando la hora
        self.fechaHoy=QDate.currentDate() # objeto que nos ayudara a llevar un control de la fecha
        noDiaEntreSemana=self.fechaHoy.dayOfWeek()-1  # donde 1 es el lunes y 7 es el domingo. 
        self.dateEdit_fecha.setDate(self.fechaHoy)#mostrando la fecha actual (nombreDia/dia/mes/año)
        # objeto que nos ayudara llevar un conteo de la hora del dia
        self.hora=QTime(tiempo.hour(),  tiempo.minute(),  tiempo.second(), 0 )

        #Creando la aplicacion de  alarmas y notas
        self.seccionAlarmas=AdministradorAlarmas(noDiaEntreSemana,tiempo.hour(),tiempo.minute(),tiempo.second() ) 
        self.seccionNotas=SeccionNotas() 
        self.seccionAlarmas.reloj.senal_minutoCambio.connect(self.cambiarMinuteroRelojMostrador)
        self.seccionAlarmas.reloj.senal_diaCambio.connect( self.cambiarDiaDateEdit )

        #Agregando los widgets anteriores al 'tabWidget' 
        self.tabWidget.addTab(self.seccionNotas,"Notas")
        self.tabWidget.addTab(self.seccionAlarmas,"Alarmas")

# Otras configuraciones 
        self.rb_controlManual.toggled.connect(self.cambiarControl)
        self.extencionArduino.senal_flamaDetectada.connect(self.actuarAnteFlama )
        
# Valores default:
        self.cargarEstadosSensores()
    
#Iniciando los hilos...
        self.extencionArduino.start()
        #self.bluetooth.start() ESTA YA FUE LLAMADO

    def actuarAnteFlama(self,flamaDetectada):
        if flamaDetectada:
            self.venAlertadorFuego.show()
            self.venAlertadorFuego.activarDesactivar_alarmaFuego(flamaDetectada)
            self.seccionAlarmas.avisador.notificadorAlarmas_activado=False
        else:
            self.venAlertadorFuego.activarDesactivar_alarmaFuego(flamaDetectada)
            self.seccionAlarmas.avisador.notificadorAlarmas_activado=True


    def cambiarMinuteroRelojMostrador(self):
         self.hora=self.hora.addSecs(60)
         self.timeEdit_tiempo.setTime(self.hora)
    
    def cambiarDiaDateEdit(self):
        self.fechaHoy=self.fechaHoy.addDays(1) 
        self.dateEdit_fecha.setDate( self.fechaHoy )


#########################################################################################################################
#    C O N T R O L      D E L     S I S T E M A 
# #######################################################################################################################    
    def cambiarControl(self):
        '''Cambiara el diseño de los horizontal sliders en función de si
        se configuro un control automatico o manual del sistema
        '''
        
        controlManual=self.rb_controlManual.isChecked()
        
        #Si se cambio a control manual hay que activar  los sliders
        #para que el usuario pueda modificarlos
        self.hoSli_foco.setEnabled(controlManual)
        self.hoSli_venti.setEnabled(controlManual)


        #Si pasamos de control manual a control automatico...
        if not(controlManual):
            #prender el ventilador si asi lo temperatura pues ya no le hacemos
            #caso al usaurio, si no unicamente al sensor de temperatura
            self.cambiarEstadoVenti(prender=self.extencionArduino.ventilador_on)
            #hay que decirle a la extensionArduino cual fue el estado en el que 
            #el usuario dejo al foco ya que el no sabia que al activar el modo
            #manual lo estabamos ignorando, por tal motivo hay que decirle en 
            #que estado se encuentra el foco
            self.extencionArduino.foco_on=self.hoSli_venti.value() 

#########################################################################################################################
#    F O C O :
# #######################################################################################################################    

    def cambiarEstadoFoco(self,prender):
        '''Esto simula que alguien cambio la posicion del slider
        por ende al hacer eso se llamara a la función asociada la 
        señal cuando se activa o desactiva el slider, es importante
        que este metodo solo servira si estamos en 'controlAutomatico'
        pues este  metodo fue pensado para solo  ser llamado por 
        el control automatico'''

        if self.rb_controlAutomatico.isChecked():
            self.hoSli_foco.setValue( prender ) #prender=False=0 prender=True=1


    def prenderApagarFoco(self,prender):
        '''Este metodo es el que esta vinculado a la señal que
        emite un objeto de tipo slider cuando este cambia de posicion 
        ¿pero a cual slider? Al slider cuyo nombre es 'hoSlid_foco' 
        es decir cuando este cambia de posicion, se vinculara a este
        metodo y  como este slider solo tiene dos posibles posiciones,
        estas seran interpretadas de la siguiente manera:
            a) Posicion 0 -. Se quiere al foco apagado
            b) Posicion 1 -. Se quiere al foco prendido

        Este metodo tambien le mandara la orden respectiva  al objeto 'self.bluetooth'
        para que emita la comunicacion respectiva y asi prender o apagar el foco por 
        medio de comunicacion blueetooth
        '''

        if prender:
            self.bel_estadoFoco.setStyleSheet("border-image: url(:/SISTEMA_CONTROL/IMAGENES/SISTEMA_CONTROL/foco_on.png);")
            self.bluetooth.foco_prenderApagar(prender=True)
        else:
            self.bel_estadoFoco.setStyleSheet("border-image: url(:/SISTEMA_CONTROL/IMAGENES/SISTEMA_CONTROL/foco_off.png);")
            self.bluetooth.foco_prenderApagar(apagar=True)
            
    def cambiarColorFoco(self,idColorEligio):
        '''Este metodo estara vinculada a la señal cuyo nombre es:
        'sena_coloElegido' la cual es una señal que  emite el objeto:
        'self.venConfig_foco' y ocurre cuando el usuario ha reliazado
        un cambio de color, por ende este metodo lo que hara es primero
        cambiar el boton que se encuentra en la esquina superior derecha
        del foco, al color que el usuario escogio, y despues proseguira 
        a mandarle la orden de cambio de color al objeto 'self.bluetooth'
        para que emita la comunicacion respectiva y asi hacer el cambio de 
        color

        Parametro:
            listaDatos-. Es una lista que contiene dos elementos
                A) El primer elemento es un string que contiene
                el valor rgb del color que se escogio
                B) El segundo elemento es un string que represent
                el 'id' del numero de color que se escogio
        '''
        idColor=idColorEligio
        colorRGB=Dialog_configLed.COLORES_RGB[ idColor  ]  #listDatos[1]
        self.btn_configFoco.setStyleSheet("""border :3px solid black;
                                            border-radius: 15px;
                                            background-color: rgb{};""".format(colorRGB))
        print("Color recibido:",idColor)
        self.bluetooth.foco_cambiarColor(idColor)

#########################################################################################################################
#    V E N T I L A D O R : 
# #######################################################################################################################    


    def cambiarEstadoVenti(self,prender):
        '''Esto simula que alguien cambio la posicion del slider
        por ende al hacer eso se llamara a la función asociada la 
        señal cuando se activa o desactiva el slider, es importante decir
        que este metodo solo servira si estamos en 'controlAutomatico'
        pues este  metodo fue pensado para solo  ser llamado por 
        el control automatico'''

        #solo se efectura si el control automatico
        #esta activado:
        if self.rb_controlAutomatico.isChecked():
            self.hoSli_venti.setValue( prender )  #prender=False=0 prender=True=1  


    def prenderApagarVenti(self,prender):
        '''Este metodo es el que esta vinculado a la señal que
        emite un objeto de tipo slider cuando este cambia de posicion 
        ¿pero a cual slider? Al slider cuyo nombre es 'hoSlid_venti' 
        es decir cuando este cambia de posicion, se vinculara a este
        metodo y  como este slider solo tiene dos posibles posiciones,
        estas seran interpretadas de la siguiente manera:
            a) Posicion 0 -. Se quiere al ventilador apagado
            b) Posicion 1 -. Se quiere al ventilador prendido

        Este metodo tambien le mandara la orden respectiva  al objeto 'self.bluetooth'
        para que emita la comunicacion respectiva y asi prender o apagar el ventilador por 
        medio de comunicacion blueetooth
        '''

        if prender:
            self.bel_estadoVenti.setStyleSheet("border-image: url(:/SISTEMA_CONTROL/IMAGENES/SISTEMA_CONTROL/ventilador_on.png);")
            self.bluetooth.venti_prenderApagar(prender=True)
        else:
            self.bel_estadoVenti.setStyleSheet("border-image: url(:/SISTEMA_CONTROL/IMAGENES/SISTEMA_CONTROL/ventilador_off.png);")
            self.bluetooth.venti_prenderApagar(apagar=True)

    def cambiarTempPrendeVenti(self,nuevaTemp):
        '''Este metodo estara vinculado a la señal cuyo nombre es:
        'senal_cambioTempPrendeVenti' la cual es una señal que  emite el objeto:
        'self.venConfig_venti' y ocurre cuando el usuario a editado la temperatura
        a la cual quiere que se prenda el ventilador.
        La funcion de este metodo es notificar los cambios a la 'QLabel' que muestra
        la temperatura a la cual se prendera el ventilador y tambien al objeto 
        'extensionArduino' pues una de las funciones del objeto 'extensionArduino' 
        es estar al pendiente cuando es hora de prender u apagar el ventilador en
        funcion de los datos arrojados por el sensor de tempertura y las preferencias
        del usuario.
        Parametro:
            nuevTemp=> Es un dato de tipo FLOAT que representa  el valor de la temperatura
            a la cual el usuario quiere que se prenda el ventilador'''

        print("Nueva temp:",nuevaTemp)
        self.btn_configVenti.setText(str(nuevaTemp)+" [°C]")
        self.extencionArduino.tempPrenderaVenti=nuevaTemp
        

    def actualizarTemp(self,nuevaTemp_str):
        '''Este metodo estara vinculado a la señal cuyo nombre es: 'senal_actTemp'
        la cual emitira el objeto cuyo nombre es: 'self.extencionArduino' cuando
        el detecte que la temperatura a cambiado y es hora de mostrarle esos
        cambios la usuario de forma visual.
        '''

        self.bel_temp.setText( nuevaTemp_str )

    def cargarEstadosSensores(self):
        '''La GUI tiene a los sliders del foco y ventilador en la posicion 0,
        es decir el foco y el ventilador estan apagados, y tiene check en el
        radio buttom del control auotmatico lo cual significa que esta en 
        configuracion automatica.
        Es importnte mencionar que este metodo debe ser llamado antes de que 
        inicie el hilo extencionArduino ya que el puede cambiar los valores
        de la GUI, por tal motivo primero se busca cargar las configuraciones
        default.
        ''' 
        if os.path.exists(Recursos_IoT_Domotica.ARCHIVO_ESTADOS_SENSORES) :
            with open(Recursos_IoT_Domotica.ARCHIVO_ESTADOS_SENSORES, 'r') as archivo:
                datos=archivo.read()
            COLOR_FOCO, TEMP_PRENDE_VENTILADOR=datos.split(",,,")
            COLOR_FOCO=int(COLOR_FOCO)
            TEMP_PRENDE_VENTILADOR=float(TEMP_PRENDE_VENTILADOR)
        else:
            COLOR_FOCO=0
            TEMP_PRENDE_VENTILADOR=100 #DEBE SER UN DATO DE TIPO STRING


        #Como ya esta conectada esta señal al hacer esto automaticamente tambien
        #cambiara el valor 'doubleSpin' y de la 'label' y del 'arduinoExtension'
        self.venConfig_venti.dSB_tempActVenti.setValue(TEMP_PRENDE_VENTILADOR)
        #self.extensionArduino.tempPrenderaVenti=TEMP_PRENDE_VENTILADOR
        self.cambiarTempPrendeVenti( TEMP_PRENDE_VENTILADOR )#poniendo en la etiqueta la 

        self.prenderApagarFoco(prender=False)
        self.extencionArduino.foco_on=False

        self.prenderApagarVenti(prender=False)
        self.extencionArduino.ventilador_on=False

        self.cambiarColorFoco(COLOR_FOCO)

        #Como el radiobutton tenia el check en automatico hay que llamar
        #a este metodo por que este solo es llamada cuando hay un cambio
        #y si no lo llamamos no se desactivan los sliders
        self.cambiarControl()


        
            
    def respaldarEstadosSensores(self):
        listaEstados=[]
        listaEstados.append( str( self.venConfig_foco.idColorFoco )  ) #COLOR_FOCO
        listaEstados.append( str( self.extencionArduino.tempPrenderaVenti ) ) #TEMP_PRENDE_VENTILADOR
        datos=",,,".join(listaEstados)
        with open( Recursos_IoT_Domotica.ARCHIVO_ESTADOS_SENSORES , 'w' ) as archivo:
            archivo.write(datos)




#########################################################################################################################
#    O T R A S   F U N C I O N E S : 
# #######################################################################################################################    

    def closeEvent(self,event):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Question)
        ventanaDialogo.setWindowTitle('Salir')
        ventanaDialogo.setText("¿Seguro que quieres salir?")
        ventanaDialogo.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        btn_yes = ventanaDialogo.button(QMessageBox.Yes)
        btn_yes.setText('Si')
        btn_no = ventanaDialogo.button(QMessageBox.No)
        btn_no.setText('No')
        ventanaDialogo.exec_()
        if ventanaDialogo.clickedButton()  ==  btn_yes:
            self.seccionNotas.respaldarDeberes()
            self.respaldarEstadosSensores()
            event.accept()
        else:
            event.ignore()  # No saldremos del evento


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = Main_IoT()
    application.show()
    app.exec()
    #sys.exit(app.exec())

