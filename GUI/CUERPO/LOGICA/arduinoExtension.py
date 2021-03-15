# re utiliza el modulo re para la validacion
import os
import time
import datetime
from PyQt5.QtCore import pyqtSignal, QThread  # hilos
import serial

class ArduinoExtension_hilo(QThread):
    CHAR_SEGURIDAD="_"
    SEP_ENTRE_DATOS=","


    senal_temperatura=pyqtSignal(str) # no retornara el valor de la temperatura sensada por arduino
    senal_aplausoDetectado=pyqtSignal(bool)# nos avisara cuando se quiera prender el foco
    
    def __init__(self,velocidad,puerto):
        super().__init__()
        self.velocidad=velocidad 
        self.puerto=puerto
        #Conectandos a arduinos
        self.arduino=serial.Serial(port=self.puerto,baudrate=self.velocidad)#conectandonos a posible arduino
        self.terminarHilo=False

    def run(self):
        while not(self.terminarHilo):
            datos=self.arduino.readline().decode("utf-8") #si cuenta el salto de linea
            #print("datos:",datos,"char:",datos[0],"char:",datos[-2])
            if datos[0]==self.CHAR_SEGURIDAD and datos[-2]==self.CHAR_SEGURIDAD:
                listDatos=datos[1:-2] #primero quitamos los caracteres de seguridad y el salto de linea...
                listDatos=listDatos.split(self.SEP_ENTRE_DATOS) #ahora proseguimos a separar
                if listDatos[0]=='0':
                    self.senal_temperatura.emit(listDatos[1])
                else:
                    self.senal_aplausoDetectado.emit(True)


                