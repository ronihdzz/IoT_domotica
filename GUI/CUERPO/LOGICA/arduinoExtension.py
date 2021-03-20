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


    senal_temperatura=pyqtSignal(str) # no retornara el valor de la temperatura sensada por arduino
    senal_aplausoDetectado=pyqtSignal(bool)# nos avisara cuando se quiera prender el foco
    senal_flamaDetectada=pyqtSignal(bool)
    senal_prenderVentilador=pyqtSignal(bool)
    
    
    def __init__(self,velocidad,puerto):
        super().__init__()
        self.velocidad=velocidad 
        self.puerto=puerto
        #Conectandos a arduinos
        self.arduino=serial.Serial(port=self.puerto,baudrate=self.velocidad,timeout=1)#conectandonos a posible arduino
        self.terminarHilo=False
        self.flamaDetectada=False

    def run(self):
        while not(self.terminarHilo):

            mensajeRecibido=self.arduino.readline()
            print("ARDUINO EXTENSION: ",mensajeRecibido)
            mensajeRecibido=self.desempaquetarMensaje(mensajeRecibido)
            print("ARDUINO EXTENSION: ",mensajeRecibido)

            if mensajeRecibido:
                if mensajeRecibido[0]==self.IDS["TEMPERATURA"]:
                    print("Temp: {}".format(mensajeRecibido[1]))
                    self.senal_temperatura.emit(mensajeRecibido[1])
                elif mensajeRecibido[0]==self.IDS["SONIDO_DETECTADO"]:
                    print("BEEP")
                    self.senal_aplausoDetectado.emit(True)
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


                