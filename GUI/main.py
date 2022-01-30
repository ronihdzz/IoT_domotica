#! /usr/bin/env python3
from PyQt5.QtWidgets import  QDialog,QApplication
from PyQt5 import QtWidgets
from functools import partial
from PyQt5.QtWidgets import (QMessageBox,QButtonGroup,QDialog)
from PyQt5.QtCore import QTimer, QTime, Qt,QDateTime,QDate,QCoreApplication
import datetime
import os
from PyQt5.QtGui import QIcon

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

from CUERPO.LOGICA.DEBERES.SeccionDeberes import SeccionDeberes
from CUERPO.LOGICA.SISTEMA_CONTROL.arduinoExtension import ArduinoExtension_hilo
from CUERPO.LOGICA.SISTEMA_CONTROL.bluetoothSerial import BluetoothSerial_hilo
from recursos import HuellaAplicacion,App_Principal



class Main_IoT(QtWidgets.QWidget, Ui_Form,HuellaAplicacion):

    def __init__(self):
        Ui_Form.__init__(self)
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        HuellaAplicacion.__init__(self)


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
        self.extencionArduino=ArduinoExtension_hilo(velocidad=9600,puerto=App_Principal.ARDUINO_NANO_EXTENSION) ########################### main.py
        #Hilo que nos permitira la comunicación entre la rasberry pi y el modulo Bluetooth HC-05:
        self.bluetooth=BluetoothSerial_hilo(velocidad=9600,puerto=App_Principal.BLUETOOTH_HC05) ########################### main.py

        #Asociando algunas señales de los hilos:
        self.extencionArduino.senal_prenderFoco.connect(self.cambiarEstadoFoco) ########################### main.py
        self.extencionArduino.senal_prenderVentilador.connect(self.cambiarEstadoVenti) ########################### main.py
        self.extencionArduino.senal_actTemp.connect(self.actualizarTemp) ########################### main.py


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
        self.seccionDeberes=SeccionDeberes()
        self.seccionAlarmas.reloj.senal_minutoCambio.connect(self.cambiarMinuteroRelojMostrador)
        self.seccionAlarmas.reloj.senal_diaCambio.connect( self.cambiarDiaDateEdit )

        #Agregando los widgets anteriores al 'tabWidget'
        self.stack_notas.addWidget(self.seccionDeberes)
        self.stack_alarmas.addWidget(self.seccionAlarmas)

        self.stack_alarmas.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        self.stack_notas.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )


# Otras configuraciones

        self.rb_controlManual.toggled.connect(self.cambiarControl)
        self.extencionArduino.senal_flamaDetectada.connect(self.actuarAnteFlama ) ########################### main.py

# Valores default:

        self.cargarEstadosSensores()

#Iniciando los hilos...

        self.extencionArduino.start() ########################### main.py
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
        '''
        El prendido y apagado del ventilador puede ser a a partir de dos formas:
            A) Control automatico
            B) Control manual

        Si se elige controlar de la forma automatica, los 'QSlider' que se encuentran
        por debajo de la imagen del foco y ventilador estaran deshabilitados, con la
        finalidad de que el usuario no los pueda manipular y estos solo cambiaran de
        posición de la siguiente manera:
            A) Si se detecta un sonido  de un aplauso  y el foco se encontraba apagado,
            se mandara a prender foco y con esto se movera el 'QSlider' que se
            encuentra debajo de la imagen del foco hacia la posición extrema derecha, por
            el contrario si de detecta un sonido de un aplauso y el foco se encontraba
            prendido, se mandara a apagar el foco y con esto se movera el 'QSlider' hacia
            la posicion extrema izquierda.
            B) Cuando se detecte una temperatura mayor o igual a la temperatura establecida
            se mandara a prender el ventildor y con esto se movera el 'QSilder' que se
            encuentra abajo de la imagen del ventilador hacia la posición extrema derecha, sin
            embargo si se detecta un temperatura menor a la establecida se mandara a apagar
            el ventilador y con esto se movera el 'QSlider' hacia la posición extrema izquierda

        Sin embargo si se decide controlar de forma manual, los 'QSlider' que se encuentran
        por debajo de la imagen del foco y ventilador se habilitaran con el objetivo de que el
        usuario los pueda mover y asi el usuario tenga el control del prendido y apagado del foco
        y ventilador, cabe mencionar que la unica forma en la que prendan el  foco y ventilador en
        control manual, es solo a travez de los movimientos que haga el usuario en los 'QSlider'

        Una vez mencionado lo anterior, por eso cada vez que se cambia de control este metodo se
        encargara en desactivar o activar a los 'QSlider' en función del tipo control al que se
        haya cambiado y tambien otros ajustes mas.

        '''

        controlManual=self.rb_controlManual.isChecked()

        #Si se cambio a control manual hay que activar  los sliders
        #para que el usuario pueda modificarlos
        self.hoSli_foco.setEnabled(controlManual)
        self.hoSli_venti.setEnabled(controlManual)


        # ¿es control automatico?
        if controlManual is False:

            # El prendido y apagado del ventilador cuando se esta en  control
            # automatico dependera de si la temperatura actual supero a la
            # temperatura establecida, y el 'objeto' que lleva ese seguimiento
            # es el objeto 'self.extencionArduino', por lo tanto cuando se
            # regresa a control automatico es necesario saber si para ese
            # 'objeto' el ventilador se encuentra prendido o apagado y prender
            # o apagar el ventilador en función de lo que diga, ya que cuando
            # se entra en control 'manual' es ignora al 'objeto' 'self.extensionArduino'
            # y por eso cada vez que se regresa al control automatico es necesario
            # saber en que estado se encuentra el ventilador para dicho objeto.
            self.cambiarEstadoVenti(prender=self.extencionArduino.ventilador_on) ########################### main.py

            # Hay que decirle a la extensionArduino cual fue el estado en el que
            # el usuario dejo al foco ya que el no sabia que al activar el modo
            # manual lo estabamos ignorando, por tal motivo hay que decirle en
            # que estado se encuentra el foco
            self.extencionArduino.foco_on=self.hoSli_venti.value() ########################### main.py
            #pass ########################### mainFast.py


#########################################################################################################################
#    F O C O :
# #######################################################################################################################

    def cambiarEstadoFoco(self,prender):
        '''
        Esto simula que alguien cambio la posicion del slider por ende al hacer eso se llamara
        a la función asociada la señal cuando se activa o desactiva el slider, es importante
        decir que este metodo solo servira si estamos en 'controlAutomatico' pues este  metodo
        fue pensado para  solo  ser llamado por  el control automatico, con esta restricción le
        quitamos el control de prendido y apagado del foco y ventilador al objeto 'self.extencionArduino'
        el cual el  seguira funcionando con o sin control automatico, solo que la diferencia sera que
        cuando se active el control manual, se va ignorar lo que diga el objeto 'self.extencionArduino'
        ya que no se esta en control automatico.
        '''

        if self.rb_controlAutomatico.isChecked():
            self.hoSli_foco.setValue( prender ) #prender=False=0 prender=True=1


    def prenderApagarFoco(self,prender):
        '''
        Este metodo es el que esta vinculado a la señal que emite un objeto de tipo 'QSlider'
        cuando este cambia de posicion  ¿pero a cual slider? Al slider cuyo nombre es 'hoSlid_foco'
        es decir cuando este cambia de posicion, se vinculara a este metodo y  como este slider
        solo tiene dos posibles posiciones, estas seran interpretadas de la siguiente manera:

            a) Posicion 0 -. Se quiere al foco apagado
            b) Posicion 1 -. Se quiere al foco prendido

        Este metodo tambien le mandara la orden respectiva  al objeto 'self.bluetooth' para que
        emita la comunicacion respectiva y asi prender o apagar el foco por  medio de comunicacion
        blueetooth
        '''

        if prender:
            self.bel_estadoFoco.setStyleSheet(f"border-image: url({ self.venConfig_foco.getImagenFoco_on() });")
            self.bluetooth.foco_prenderApagar(prender=True) ########################### main.py

        else:
            self.bel_estadoFoco.setStyleSheet(f"border-image: url({ self.venConfig_foco.getImagenFoco_off() });")
            self.bluetooth.foco_prenderApagar(apagar=True) ########################### main.py

    def cambiarColorFoco(self,idColorEligio):
        '''
        Este metodo estara vinculado a la señal cuyo nombre es: 'sena_colorElegido' la cual es una señal
        que  emite el objeto: 'self.venConfig_foco' y ocurre cuando el usuario ha realizado un cambio al
        color del foco, por ende este metodo lo que hara es primero cambiar la imagen de rueda de colores
        del boton que se encuentra en  la esquina superior derecha del foco, a una imagen de que de rueda
        de colores que represente el  color que el usuario escogio, y despues proseguira a mandarle la orden
        de cambio de color al objeto 'self.bluetooth' para que emita la comunicacion respectiva y asi hacer
        el cambio de color

        Parametro:
            idColorEligio -- dato de tipo 'int' que representa el color escogido por el usuario, en donde:
                    0-blanco
                    1-rojo
                    2-verde
                    3-azul
                    4-amarillo
                    5-magenta
                    6-cian
        '''

        self.btn_configFoco.setStyleSheet(f"""
                    QPushButton {'{'}
                        border-image: url( { self.venConfig_foco.getImagen_ruedaChica() });
                    {'}'}
                    QPushButton:hover {'{'}
                        border-image: url({ self.venConfig_foco.getImagen_ruedaGrande() });
                    {'}'}
                    QPushButton:pressed {'{'}
                        border-image: url({ self.venConfig_foco.getImagen_ruedaChica() });
                    {'}'} """)

        # self.hoSli_foco.value()=0=False=APAGADO    self.hoSli_foco.value()=1=True=PRENDIDO
        if self.hoSli_foco.value():
            self.bel_estadoFoco.setStyleSheet(f"border-image:url({ self.venConfig_foco.getImagenFoco_on() });")

        self.bluetooth.foco_cambiarColor(idColorEligio) ########################### main.py

#########################################################################################################################
#    V E N T I L A D O R :
# #######################################################################################################################


    def cambiarEstadoVenti(self,prender):
        '''
        Esto simula que alguien cambio la posicion del slider por ende al hacer eso se llamara  a la
        función asociada la señal cuando se activa o desactiva el slider, es importante decir  que
        este metodo solo servira si estamos en 'controlAutomatico' pues este  metodo fue pensado para
        solo  ser llamado por  el control automatico, con esta restricción le quitamos el control
        de prendido y apagado del foco y ventilador al objeto 'self.extencionArduino' el cual el
        seguira funcionando con o sin control automatico, solo que la diferencia sera que cuando se
        active el control manual, se va ignorar lo que diga el objeto 'self.extencionArduino' ya que
        no se esta en control automatico.
        '''

        #solo se efectura si el control automatico esta activado:
        if self.rb_controlAutomatico.isChecked():
            self.hoSli_venti.setValue( prender )  #prender=False=0  prender=True=1


    def prenderApagarVenti(self,prender):
        '''
        Este metodo es el que esta vinculado a la señal que emite un objeto de tipo slider cuando este
        cambia de posicion ¿pero a cual slider? Al slider cuyo nombre es 'hoSlid_venti' es decir cuando
        este cambia de posicion, se vinculara a este metodo y  como este slider solo tiene dos posibles
        posiciones, estas seran interpretadas de la siguiente manera:

            a) Posicion 0 -. Se quiere al ventilador apagado
            b) Posicion 1 -. Se quiere al ventilador prendido

        Este metodo tambien le mandara la orden respectiva  al objeto 'self.bluetooth' para que emita
        la comunicacion respectiva y asi prender o apagar el ventilador por  medio de comunicacion blueetooth
        '''

        if prender:
            self.bel_estadoVenti.setStyleSheet("border-image: url(:/SISTEMA_CONTROL/IMAGENES/SISTEMA_CONTROL/ventilador_on.png);")
            self.bluetooth.venti_prenderApagar(prender=True)  ########################### main.py
        else:
            self.bel_estadoVenti.setStyleSheet("border-image: url(:/SISTEMA_CONTROL/IMAGENES/SISTEMA_CONTROL/ventilador_off.png);")
            self.bluetooth.venti_prenderApagar(apagar=True)   ########################### main.py

    def cambiarTempPrendeVenti(self,nuevaTemp):
        '''
        Este metodo estara vinculado a la señal cuyo nombre es: 'senal_cambioTempPrendeVenti' la cual es
        una señal que  emite el objeto: 'self.venConfig_venti' y ocurre cuando el usuario a editado la
        temperatura a la cual quiere que se prenda el ventilador.
        La funcion de este metodo es notificar los nuevos cambios en el texto del 'QButton' el cual muestra
        la temperatura a la  cual se prendera el ventilador y tambien hacer el cabmio del valor que tiene
        registrado el objeto 'extensionArduino' pues una de las funciones  del objeto 'extensionArduino'
        es estar al pendiente cuando es hora de prender u apagar el ventilador  en funcion de los datos
        arrojados por el sensor de tempertura y las preferencias del usuario.

        Parametro:
            nuevTemp -- Es un dato de tipo 'float' que representa  el valor de la temperatura
            a la cual el usuario quiere que se prenda el ventilador
        '''

        #print("Nueva temp:",nuevaTemp)
        self.btn_configVenti.setText(str(nuevaTemp)+" [°C]")
        self.extencionArduino.tempPrenderaVenti=nuevaTemp ########################### main.py


    def actualizarTemp(self,nuevaTemp_str):
        '''
        Este metodo estara vinculado a la señal cuyo nombre es: 'senal_actTemp' la cual emitira el objeto
        cuyo nombre es: 'self.extencionArduino' cuando el detecte que la temperatura a cambiado y es hora
        de mostrarle esos cambios la usuario de forma visual.

        Parámetros:
            nuevaTemp_str -- dato de tipo 'str' que representa la temperatura nueva registrada.
        '''

        self.bel_temp.setText( nuevaTemp_str )

    def cargarEstadosSensores(self):
        '''
        Siempre al abrir la GUI esta tendra  a los sliders del foco y ventilador en la posicion 0, es decir
        el foco y el  ventilador estan apagados, y tambien tendra el check en el radio buttom del control
        automatico lo cual significa que esta en configuracion automatica.

        Es importnte mencionar que este metodo debe ser llamado antes de que  inicie el hilo extencionArduino
        ya que el puede cambiar los valores de la GUI, por tal motivo primero se busca cargar las configuraciones
        que fueron resguardadas antes de que se cerrara el programa por ultima vez.

        ¿Que datos se cargaran?
            A) El color de foco que fue escogido antes de que el usuario cerrara el programa la ultima vez.
            B) La temperatura a la cual es usuario escogio que se prendiera el ventilador antes de que el
            usuario cerrara el programa la ultima vez.

        '''

        if os.path.exists(App_Principal.ARCHIVO_ESTADOS_SENSORES) :
            with open(App_Principal.ARCHIVO_ESTADOS_SENSORES, 'r') as archivo:
                datos=archivo.read()
            COLOR_FOCO, TEMP_PRENDE_VENTILADOR=datos.split(",,,")
            COLOR_FOCO=int(COLOR_FOCO)
            TEMP_PRENDE_VENTILADOR=float(TEMP_PRENDE_VENTILADOR)
        else:
            COLOR_FOCO=0
            TEMP_PRENDE_VENTILADOR=100


        # Como ya esta conectada esta señal al hacer esto automaticamente
        # cambiara el valor 'doubleSpin', QButton' y del 'arduinoExtension'
        self.venConfig_venti.dSB_tempActVenti.setValue(TEMP_PRENDE_VENTILADOR)

        self.extencionArduino.tempPrenderaVenti=TEMP_PRENDE_VENTILADOR   ########################### main.py NO NECESARIO
        self.cambiarTempPrendeVenti( TEMP_PRENDE_VENTILADOR ) # poniendo en la etiqueta  NO ES NECESARIO

        self.prenderApagarFoco(prender=False) ########################### main.py
        self.extencionArduino.foco_on=False   ########################### main.py

        self.prenderApagarVenti(prender=False)     ########################### main.py
        self.extencionArduino.ventilador_on=False  ########################### main.py

        self.venConfig_foco.eligioColor(COLOR_FOCO)
        self.venConfig_foco.cambiarImagen(COLOR_FOCO)
        self.cambiarColorFoco(COLOR_FOCO)

        #Como el radiobutton tenia el check en automatico hay que llamar a este metodo por que este
        # solo es llamada cuando hay un cambio y si no lo llamamos no se desactivan los sliders
        self.cambiarControl()


    def respaldarEstadosSensores(self):
        '''
        Guardara los datos de la temperatura que escogio el usuario para que se prenda el ventilador,
        al igual que el color de foco, los datos los guardara en un archivo de texto cada uno de ellos
        separados entre ',,,' (3 comas)
        '''

        listaEstados=[]
        listaEstados.append( str( self.venConfig_foco.idColorFoco )  ) # COLOR_FOCO

        #listaEstados.append( str( self.extencionArduino.tempPrenderaVenti ) ) # TEMP_PRENDE_VENTILADOR  ########################### main.py NO NECESARIA

        listaEstados.append( str(self.venConfig_venti.temp_prendeVentilador) ) #TEMP_PRENDE_VENTILADOR
        datos=",,,".join(listaEstados)
        with open( App_Principal.ARCHIVO_ESTADOS_SENSORES , 'w' ) as archivo:
            archivo.write(datos)




#########################################################################################################################
#    O T R A S   F U N C I O N E S :
# #######################################################################################################################

    def closeEvent(self,event):
        '''
        Cuando el usuario le de clic izquierdo sobre el boton de cerra el programa, el metodo
        que se llamara es este, el cual le preguntara al usuario si esta seguro de cerrar el
        programa, en caso de que su respuesta sea afirmativa se cerrara el programa.
        '''

        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Question)
        ventanaDialogo.setWindowIcon( QIcon(self.ICONO_APLICACION)  )
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        ventanaDialogo.setText("¿Seguro que quieres salir?")
        ventanaDialogo.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        btn_yes = ventanaDialogo.button(QMessageBox.Yes)
        btn_yes.setText('Si')
        btn_no = ventanaDialogo.button(QMessageBox.No)
        btn_no.setText('No')
        ventanaDialogo.exec_()
        if ventanaDialogo.clickedButton()  ==  btn_yes:
            self.seccionDeberes.respaldarDeberes()
            self.respaldarEstadosSensores()
            self.seccionAlarmas.respaldarEstadosAlarma()
            event.accept()
        else:
            event.ignore()  # No saldremos del evento

    def resizeEvent(self, event):
        '''
        Cada vez que se detecta un cambio en el tamaño del programa, se actualizaran los tamaños
        que le pertenecen al widget que muestra las alarmas y al widget que muestra los deberes,
        con la finalidad de que ambos conserven el mismo tamaño y asi NINGUNO sea mas grande que
        otro y crezcan de igual forma.
        '''

        print("Window has been resized")
        QtWidgets.QWidget.resizeEvent(self, event)
        ancho=self.widget_alarmasNotas.width()
        alto=self.widget_alarmasNotas.height()

        #self.stack_alarmas.setMaximumHeight(alto//2 -50)
        self.stack_alarmas.setMinimumHeight(alto//2 -50)

        #self.stack_notas.setMaximumHeight(alto//2 -50)
        self.stack_notas.setMinimumHeight(alto//2 -50)
        print(ancho,alto)



if __name__ == "__main__":
    from PyQt5.QtCore import QCoreApplication,Qt
    from PyQt5.QtGui import QPixmap
    from PyQt5.QtWidgets import QSplashScreen
    import sys, time,os
    import recursos

    from logger import actualizarUbicacionLogger
    




    #print("Nombre completo del programa que se esta ejecutando: ",sys.argv)
    direccionTotal=sys.argv[0]

    direccionPartes=os.path.normpath(direccionTotal)
    direccionPartes=direccionPartes.split(os.sep)
    ruta_direccionTotal = os.sep.join( direccionPartes[:-1] )
    if len(direccionPartes)>1:
        ruta_direccionTotal+=os.sep

    #print("dirreccionPartes:",direccionPartes)
    #print("ruta total: ",ruta_direccionTotal)
    #ubicacionPrograma=direccionTotal[ :direccionTotal.find("mainFast.py") ]


    # recursos.App_Alarmas.App_PrincipalApp_Notas actualizarUbicaciones
    recursos.App_Alarmas.actualizarUbicaciones(ruta_direccionTotal)
    recursos.App_Deberes.actualizarUbicaciones(ruta_direccionTotal)
    recursos.App_Principal.actualizarUbicaciones(ruta_direccionTotal)

    actualizarUbicacionLogger()



    app = QApplication(sys.argv)
    splash_pix = QPixmap(App_Principal.IMAGEN_SPLASH_SCREEN)
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()

    # Simulate something that takes time
    time.sleep(1)
    form = Main_IoT()
    form.show()
    splash.finish(form)
    app.exec_()

    #app = QtWidgets.QApplication([])
    #application = Main_IoT()
    #application.show()
    #app.exec()
    #sys.exit(app.exec())