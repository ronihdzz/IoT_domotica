# re utiliza el modulo re para la validacion
import os
import time
import datetime
from PyQt5.QtCore import pyqtSignal, QThread  # hilos
import serial

class BluetoothSerial_hilo(QThread):
    CHAR_SEGURIDAD="_"
    SEP_ENTRE_DATOS=","

    IDS={
            "FOCO":"11",
            "VENTILADOR":"10",

            "APAGAR":"0",
            "PRENDER":"1",
            "CAMBIAR_COLOR_FOCO":"2",
            "FUEGO_DETECTADO":"3",
            "FUEGO_APAGADO":"4",
            "ORDEN_ATENDIDA":"5"
    }

    senal_ordenRealizada=pyqtSignal(bool) # no retornara el valor de la temperatura sensada por arduino
    senal_fuegoDetectado=pyqtSignal(bool)

    def __init__(self,velocidad,puerto):
        super().__init__()
        self.velocidad=velocidad 
        self.puerto=puerto
        #Conectandos a arduinos
        self.moduloBlutetooth=serial.Serial(port=self.puerto,baudrate=self.velocidad,timeout=0.5)#conectandonos a posible arduino
        self.terminarHilo=False
        self.datosMandar=None 

    def run(self):
        if self.datosMandar:
            mensajeMandar=self.empaquetarMensaje(self.datosMandar)
            print("DATOS A MANDAR:",self.datosMandar)
            print("DATOS EMPEQUETADOS:",mensajeMandar)

            self.moduloBlutetooth.write(mensajeMandar)
            mensajeRespuesta=self.moduloBlutetooth.readline()
            print("¿RECIBIDO?:",mensajeRespuesta)
            listaDatos=self.desempaquetarMensaje(mensajeRespuesta)
            print("¿RECIBIDO?:",listaDatos)
            if listaDatos:
                if listaDatos[0]==self.IDS["ORDEN_ATENDIDA"]:
                    print("¿RECIBIDO?:SI")
                    self.senal_ordenRealizada.emit(True)
                else:
                    print("¿RECIBIDO?:NO")
                    self.senal_ordenRealizada.emit(False)
            print("HILO TERMINADO....")

    def foco_prenderApagar(self,prender=False,apagar=False):
        datosMandar=[]
        datosMandar.append( self.IDS["FOCO"]  )
        if prender:
            datosMandar.append( self.IDS["PRENDER"]  )
        else:
            datosMandar.append( self.IDS["APAGAR"]  )
        self.datosMandar=datosMandar
        self.run()

    def foco_cambiarColor(self,idColor):
        datosMandar=[]
        datosMandar.append( self.IDS["FOCO"]  )
        datosMandar.append( self.IDS["CAMBIAR_COLOR_FOCO"] )
        datosMandar.append( str(idColor) )
        self.datosMandar=datosMandar
        self.run()

    def venti_prenderApagar(self,prender=False,apagar=False):
        datosMandar=[]
        datosMandar.append( self.IDS["VENTILADOR"]  )
        if prender:
            datosMandar.append( self.IDS["PRENDER"]  )
        else:
            datosMandar.append( self.IDS["APAGAR"]  )
        self.datosMandar=datosMandar
        self.run()
      
    def empaquetarMensaje(self,listaDatos):
        mensaje=self.SEP_ENTRE_DATOS.join(listaDatos)
        mensaje=self.CHAR_SEGURIDAD+mensaje+self.CHAR_SEGURIDAD
        mensajeEmpaquetado=mensaje.encode("utf-8")
        return mensajeEmpaquetado
    
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
