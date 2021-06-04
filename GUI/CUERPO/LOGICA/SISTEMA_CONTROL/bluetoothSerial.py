# re utiliza el modulo re para la validacion
import os
import time
import datetime
from PyQt5.QtCore import pyqtSignal, QThread  # hilos
import serial

class BluetoothSerial_hilo(QThread):
    '''
    Servira para comunicarnos con el 'BLUETOOTH_HC05' de forma serial, para que
    este a su vez se comunique con el 'Esp-32' y este pueda hacer lo siguiente:

        Prender o apagar el ventilador
        Prender o apagar el foco led rgb
        Cambiar de color del foco led rgb
    '''


    CHAR_SEGURIDAD="_"
    SEP_ENTRE_DATOS=","

    IDS={
            "FOCO":"11",
            "VENTILADOR":"10",

            "APAGAR":"0",
            "PRENDER":"1",
            "CAMBIAR_COLOR_FOCO":"2",
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
        '''
        Cada vez que se llame este metodo, el se encargara de mandar los datos contendios
        en el atributo de instancia llamado 'self.datosMandar', dichos datos los mandara
        atraves de comunicación Serial al 'BLUETOOTH_HC05'  y para que este a su vez se los 
        mande al 'Esp-32'
        '''

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
        '''
        Agrupara los datos en una lista para que formen la orden de:
            A) Prender el  foco en caso de que el parametro  'prender' sea igual a True
            b) Apagar el foco en caso de que el parametro 'apagar' sea igual a True
        Una vez creada la lista en donde cada elemento de ella representa una parte
        de la orden que se desea ejecutar, se proseguira a almacenar la lista en el 
        atributo: 'self.datosMandar' ya que el contenido de ese atributo es el que 
        utiliza el metodo 'run' para mandar una orden atraves de comunicación serial al 
        modulo 'BLUETOOTH_HC05'
        
        Parámetros:
            prender -- dato de tipo 'bool' que inidicara si se desea prender
            el foco
            apagar -- dato de tipo 'bool' que indicara si se desea apagar el foco
        '''

        datosMandar=[]
        datosMandar.append( self.IDS["FOCO"]  )
        if prender:
            datosMandar.append( self.IDS["PRENDER"]  )
        else:
            datosMandar.append( self.IDS["APAGAR"]  )
        self.datosMandar=datosMandar
        self.run()

    def foco_cambiarColor(self,idColor):
        '''
        Agrupara los datos en una lista para que formen la orden de cambiar
        el color del led rgb al color indicado por el parametro 'idColor' 
        Una vez creada la lista en donde cada elemento de ella representa una parte
        de la orden que se desea ejecutar, se proseguira a almacenar la lista en el 
        atributo: 'self.datosMandar' ya que el contenido de ese atributo es el que 
        utiliza el metodo 'run' para mandar una orden atraves de comunicación serial al 
        modulo 'BLUETOOTH_HC05'

        Parámetros:
            idColor -- dato de tipo 'int' que representa el color al que se desea prender
            el led rgb  en donde:
                    0-blanco
                    1-rojo
                    2-verde
                    3-azul
                    4-amarillo
                    5-magenta
                    6-cian

        '''

        datosMandar=[]
        datosMandar.append( self.IDS["FOCO"]  )
        datosMandar.append( self.IDS["CAMBIAR_COLOR_FOCO"] )
        datosMandar.append( str(idColor) )
        self.datosMandar=datosMandar
        self.run()

    def venti_prenderApagar(self,prender=False,apagar=False):
        '''
        Agrupara los datos en una lista para que formen la orden de:
            A) Prender el ventilador en caso de que el parametro  'prender' sea igual a True
            b) Apagar el ventilador en caso de que el parametro 'apagar' sea igual a True

        Una vez creada la lista en donde cada elemento de ella representa una parte
        de la orden que se desea ejecutar, se proseguira a almacenar la lista en el 
        atributo: 'self.datosMandar' ya que el contenido de ese atributo es el que 
        utiliza el metodo 'run' para mandar una orden atraves de comunicación serial al 
        modulo 'BLUETOOTH_HC05'
        
        Parámetros:
            prender -- dato de tipo 'bool' que inidicara si se desea prender
            el foco
            apagar -- dato de tipo 'bool' que indicara si se desea apagar el foco
        '''

        datosMandar=[]
        datosMandar.append( self.IDS["VENTILADOR"]  )
        if prender:
            datosMandar.append( self.IDS["PRENDER"]  )
        else:
            datosMandar.append( self.IDS["APAGAR"]  )
        self.datosMandar=datosMandar
        self.run()
      
    def empaquetarMensaje(self,listaDatos):
        '''
        Se encargara de agrupar los datos del parametro 'listaDatos' de la forma 
        en el que el  el esp-32 reconocera las ordenes que se desean realizar.
        '''

        mensaje=self.SEP_ENTRE_DATOS.join(listaDatos)
        mensaje=self.CHAR_SEGURIDAD+mensaje+self.CHAR_SEGURIDAD
        mensajeEmpaquetado=mensaje.encode("utf-8")
        return mensajeEmpaquetado
    
    def desempaquetarMensaje(self,mensaje):
        '''
        Se encargara de identificar los datos que vienen inmersos en el 'str' bajo el formato que 
        los manda el 'esp-32' :

            _DATO,DATO,DATO_\n\r
                donde:
                    _     es char seguridad
                    ,     separador
                    \n\r  es con lo que termina el mensaje

        Una vez identificado los datos los almacenara a cada uno de ellos en un  elemento de una lista y 
        poteriormente retornara a la lista.

        Parámetros:
            mensaje -- dato de tipo 'str' donde vienen contenidos los datos bajo el formato en que los 
            manda el 'esp-32'

        Returns(values):
            una lista con lo datos de la respuesta identificada del esp-32
        '''

        mensaje=mensaje.decode("utf-8")
        datos=None
        if len(mensaje)>4:#minimo debe de tener 5 datos
            if mensaje[0]==self.CHAR_SEGURIDAD and mensaje[-3]==self.CHAR_SEGURIDAD:
                mensaje=mensaje[1:-3] #primero quitamos los caracteres de seguridad y el salto de linea...
                datos=mensaje.split(self.SEP_ENTRE_DATOS)
        return datos
