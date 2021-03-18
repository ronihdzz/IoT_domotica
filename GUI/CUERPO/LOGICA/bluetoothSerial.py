# re utiliza el modulo re para la validacion
import os
import time
import datetime
from PyQt5.QtCore import pyqtSignal, QThread  # hilos
import serial

class BluetoothSerial_hiloEscucha(QThread):
    CHAR_SEGURIDAD="_"
    SEP_ENTRE_DATOS=","

    #senal_temperatura=pyqtSignal(str) # no retornara el valor de la temperatura sensada por arduino
    #senal_aplausoDetectado=pyqtSignal(bool)# nos avisara cuando se quiera prender el foco
    
    def __init__(self,velocidad,puerto):
        super().__init__()
        self.velocidad=velocidad 
        self.puerto=puerto
        #Conectandos a arduinos
        self.moduloBlutetooth=serial.Serial(port=self.puerto,baudrate=self.velocidad)#conectandonos a posible arduino
        self.terminarHilo=False


    def run(self):
            print("hola mundo")
            self.moduloBlutetooth.write("_11,1_".encode("utf-8"))
            datos=self.moduloBlutetooth.readline().decode("utf-8") #si cuenta el salto de linea
            print("recibidos:",datos)
            
            self.moduloBlutetooth.write("_11,0_".encode("utf-8"))
            datos=self.moduloBlutetooth.readline().decode("utf-8") #si cuenta el salto de linea
            print("recibidos:",datos)
            
            self.moduloBlutetooth.write("_11,1_".encode("utf-8"))
            datos=self.moduloBlutetooth.readline().decode("utf-8") #si cuenta el salto de linea
            print("recibidos:",datos)




'''
class BluetoothSerial_hilo(QThread):
    CHAR_SEGURIDAD="_"
    SEP_ENTRE_DATOS=","

    #senal_temperatura=pyqtSignal(str) # no retornara el valor de la temperatura sensada por arduino
    #senal_aplausoDetectado=pyqtSignal(bool)# nos avisara cuando se quiera prender el foco
    
    def __init__(self,velocidad,puerto):
        super().__init__()
        self.velocidad=velocidad 
        self.puerto=puerto
        #Conectandos a arduinos
        self.moduloBlutetooth=serial.Serial(port=self.puerto,baudrate=self.velocidad)#conectandonos a posible arduino
        self.terminarHilo=False

    def run(self):
        while not(self.terminarHilo):
            datos=self.moduloBlutetooth.readline().decode("utf-8") #si cuenta el salto de linea
            print("recibidos:",datos)
            #print("datos:",datos,"char:",datos[0],"char:",datos[-2])
            if datos[0]==self.CHAR_SEGURIDAD and datos[-2]==self.CHAR_SEGURIDAD:
                mensaje=datos[1:-2] #primero quitamos los caracteres de seguridad y el salto de linea...
                mensaje=int(mensaje)
                print(mensaje)


'''
