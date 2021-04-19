# re utiliza el modulo re para la validacion
import os
import time
import datetime
from PyQt5.QtCore import pyqtSignal, QThread  # hilos
import serial



class ArduinoExtension_hilo(QThread):
    CHAR_SEGURIDAD="_"
    SEP_ENTRE_DATOS=","

    IDS={
            "TEMPERATURA":"1",
            "SONIDO_DETECTADO":"2",
            "FUEGO_DETECTADO":"3",
            "FUEGO_APAGADO":"4"
    }


    senal_flamaDetectada=pyqtSignal(bool)

    senal_prenderFoco=pyqtSignal(bool)


    senal_prenderVentilador=pyqtSignal(bool)#prender/apagar ventilador
    senal_actTemp=pyqtSignal(str) #actualizar temperatura 
    
    
    def __init__(self,velocidad,puerto,foco_on=False,ventilador_on=False,tempPrenderaVenti=100):
        super().__init__()
        
        #Atributos relacionados con la configuración del la comunicación del arduino
        self.velocidad=velocidad 
        self.puerto=puerto

        #Conectandonos con arduino..
        self.arduino=serial.Serial(port=self.puerto,baudrate=self.velocidad,timeout=1)#conectandonos a posible arduino
        
        #Atributos relacionados con el cheque constante de la flama...
        self.flamaDetectada=False

        #Atributos relacionados con el foco...
        self.foco_on=foco_on


        #Atributos relacionados con el ventilador...
        self.ventilador_on=ventilador_on
        self.tempActual=22 #La temperatura que se esta sensando
        self.tempPrenderaVenti=tempPrenderaVenti #La temperatura a la cual se va a prender el ventilador

        #Atributo que nos dara 
        self.terminarHilo=False
             

    def run(self):
        while not(self.terminarHilo):

            mensajeRecibido=self.arduino.readline()
            print("ARDUINO EXTENSION: ",mensajeRecibido)
            mensajeRecibido=self.desempaquetarMensaje(mensajeRecibido)
            print("ARDUINO EXTENSION: ",mensajeRecibido)

            if mensajeRecibido:
                if mensajeRecibido[0]==self.IDS["TEMPERATURA"]:
                    temp=mensajeRecibido[1] #dato string
                    self.procesarTemp(temp)

                elif mensajeRecibido[0]==self.IDS["SONIDO_DETECTADO"]:
                    print("BEEP")
                    self.procesarFoco()

                elif mensajeRecibido[0]==self.IDS["FUEGO_DETECTADO"]:
                    print("FUEGO")
                    self.senal_flamaDetectada.emit(True)
                    self.flamaDetectada=True
                    while self.flamaDetectada:
                        mensajeRecibido=self.arduino.readline()
                        mensajeRecibido=self.desempaquetarMensaje(mensajeRecibido)
                        if mensajeRecibido:
                            if mensajeRecibido[0]==self.IDS["FUEGO_APAGADO"]:
                                self.flamaDetectada=False
                                print("FUEGO APAGADO")
                                self.arduino.write(b"pwejfpwjofp")

    def desempaquetarMensaje(self,mensaje):
        # _DATO,DATO,DATO_\n\r
        # _  es char seguridad
        # ,  separador
        # \n\r es con lo que termina el mensaje
        mensaje=mensaje.decode("utf-8")
        datos=None
        if len(mensaje)>4:#minimo debe de tener 5 datos
            if mensaje[0]==self.CHAR_SEGURIDAD and mensaje[-3]==self.CHAR_SEGURIDAD:
                mensaje=mensaje[1:-3] #primero quitamos los caracteres de seguridad y el salto de linea...
                datos=mensaje.split(self.SEP_ENTRE_DATOS)
        return datos


    #procesar la temperatura:
    def procesarTemp(self,nuevaTemp_str):
        nuevaTemp_float=float(nuevaTemp_str)
        if abs( nuevaTemp_float - self.tempActual ) > 0.3:
            self.tempActual=nuevaTemp_float
            self.senal_actTemp.emit(nuevaTemp_str)

        if self.tempActual>=self.tempPrenderaVenti:
            if not(self.ventilador_on):
                self.senal_prenderVentilador.emit(True)
                self.ventilador_on=True
        else:
            if self.ventilador_on:
                self.senal_prenderVentilador.emit(False)
                self.ventilador_on=False
                
            
    
    def procesarFoco(self):
        if self.foco_on:
            self.senal_prenderFoco.emit(False)
        else:
            self.senal_prenderFoco.emit(True)
        self.foco_on=not(self.foco_on)