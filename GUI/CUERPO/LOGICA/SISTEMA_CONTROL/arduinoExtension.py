# re utiliza el modulo re para la validacion
import os
import time
import datetime
from PyQt5.QtCore import pyqtSignal, QThread  # hilos
import serial



class ArduinoExtension_hilo(QThread):
    '''
    Hilo que servira para comunicarse con el arduino nano, el cual contiene
    el microfono, el sensor de temperatura y el sensor detector de flama. 

    Este hilo sera el indicado de hacer lo siguiente:
        A) Avisar cada vez que se detecte el aplauso por medio del microfono que se encuentra 
        en el arduino nano, y asi mandar la señal para prender u apagar el foco de forma automatica
        B) Avisar cuando se deba prender u apagar el ventilador, pues este hilo sera el encargado de 
        detectar cuando se ha superado la temperatura establecida por el usuario para que se prenda
        el ventilador.
        C) Avisar cuando el sensor de flama que se encuentra en el arduino nano ha detectado fuego
    
    Dato que constantemente esta realizando operaciones se programa este comportamiento en una Hilo
    '''


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
    senal_prenderVentilador=pyqtSignal(bool) # prender/apagar ventilador
    senal_actTemp=pyqtSignal(str) # actualizar temperatura 
    
    
    def __init__(self,velocidad,puerto,foco_on=False,ventilador_on=False,tempPrenderaVenti=100):
        super().__init__()
        
        # Atributos relacionados con la configuración del la comunicación del arduino
        self.velocidad=velocidad 
        self.puerto=puerto

        # Conectandonos con arduino..
        self.arduino=serial.Serial(port=self.puerto,baudrate=self.velocidad,timeout=1)

        # Atributo relacionado con el cheque constante de la flama...
        self.flamaDetectada=False


        self.foco_on=foco_on
        self.ventilador_on=ventilador_on
        
        self.tempActual=10000 # La temperatura que se esta sensando
        self.tempPrenderaVenti=tempPrenderaVenti # La temperatura a la cual se va a prender el ventilador

        # Si el siguiente parametro es igual a True, el hilo terminara de ejecutarse
        self.terminarHilo=False
             

    def run(self):
        '''
        Mientras el parametro 'self.terminarHilo' no sea igual a True, el proceso se ejecutara,
        lo primero que hara es recibir una linea de información que manda arduino a partir del
        puerto serial, posteriormente habra un metodo que procesara esas linea de  datos mandados 
        para saber que tipo que tipo de acción quiere que hagamos el arduino nano
        '''


        while not(self.terminarHilo):

            mensajeRecibido=self.arduino.readline()
            print("ARDUINO EXTENSION: ",mensajeRecibido)
            mensajeRecibido=self.desempaquetarMensaje(mensajeRecibido)
            print("ARDUINO EXTENSION: ",mensajeRecibido)

            if mensajeRecibido:
                if mensajeRecibido[0]==self.IDS["TEMPERATURA"]:
                    temp=mensajeRecibido[1] # dato string
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
                                self.senal_flamaDetectada.emit(False)
                                print("FUEGO APAGADO")
                                self.arduino.write(b"pwejfpwjofp")

    def desempaquetarMensaje(self,mensaje):
        '''
        Parámetro:
            mensaje -- dato de tipo 'str' el cual contendra la accion a realizar, el mensaje
            sigue el siguiente formato: '_DATO,DATO,DATO_\n\r' en donde:
                                    _   es char seguridad
                                    ,   separador entre los datos 
                                 \n\r   es con lo que termina el mensaje
            
        
        Returns(devoluciones):
            Una vez separados todos los datos que mando el arduino, se pondra a cada unos
            de ellos y eso sera lo que se retornara.
        '''

        mensaje=mensaje.decode("utf-8")
        datos=None
        if len(mensaje)>4:# minimo debe de tener 5 datos
            if mensaje[0]==self.CHAR_SEGURIDAD and mensaje[-3]==self.CHAR_SEGURIDAD:
                mensaje=mensaje[1:-3] # primero quitamos los caracteres de seguridad y el salto de linea...
                datos=mensaje.split(self.SEP_ENTRE_DATOS)
        return datos


    #procesar la temperatura:
    def procesarTemp(self,nuevaTemp_str):
        '''
        Si detecta que el valor de temperatura que contiene el parametro: 'nuevaTemp_str' tiene un 
        una diferencia de 0.3 [°], entonces emitira una señal con el valor nuevo de temperatura.
        Si detecta que la temperatura   que contiene que el parametro 'nuevaTemp_str'
        es mayor o igual a la establecidad para prender el ventilador o apagarlo se mandara una señal
        para avisar de que es momento de prender el ventilador o de apagar el ventilador.
        
        Parámetro:
            nuevaTemp -- dato de tipo 'str' el cual representara la temperatura actual registrada.
        
        '''

        try:

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
        except Exception as e:
            print("Error al procesar dato de temperatura: ",e)
                    
            
    
    def procesarFoco(self):
        '''
        Si el atributo 'self.foco_on' es igual a True, se mandara a prender el foco
        Si el atributo 'self.foco_on' es igual a False, se mandara apagara el foco
        '''

        if self.foco_on:
            self.senal_prenderFoco.emit(False)
        else:
            self.senal_prenderFoco.emit(True)
            
        self.foco_on=not(self.foco_on)