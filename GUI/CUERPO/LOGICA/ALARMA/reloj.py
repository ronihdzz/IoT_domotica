from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore
from datetime import datetime

class Reloj(QtCore.QObject):
    senal_minutoCambio=pyqtSignal(list)
    senal_diaCambio=pyqtSignal(list)
    CAMBIO_MINUTO=0
    CAMBIO_DIA=2

    def __init__(self,dia,hora,minuto,segundo):
        QtCore.QObject.__init__(self)
        self.noDiaEntreSemana=dia
        self.minuto=minuto
        self.hora=hora
        self.segundo=segundo
    
    def clock(self):

        senalEmitir=None
        self.segundo+=1 #aumento el valor del atributo 'segundo' en 1
        if self.segundo>59:#aumentar el valor del atributo 'minuto' en 1
            self.segundo=0
            self.minuto+=1
            senalEmitir=self.CAMBIO_MINUTO
            print("CAMBIO MINUTO")
            if self.minuto>59:#aumentar el valor del atributo 'hora' en 1              
                self.minuto=0
                self.hora+=1
                if self.hora>23:
                    self.hora=0
                    self.noDiaEntreSemana+=1
                    senalEmitir=self.CAMBIO_DIA
                    print("CAMBIO DIaaaaaaaaaaaaaaaaaaaaaaaA")
                    if self.noDiaEntreSemana>6:
                        self.noDiaEntreSemana=0
    
        self.informarPosible_cambio(senalEmitir)

    def __str__(self):
        return f"{self.hora}:{self.minuto}"
    
    def informarPosible_cambio(self,id_senalEmitir=None):
        #print(self)
        if id_senalEmitir!=None:
            if id_senalEmitir==self.CAMBIO_MINUTO:
                self.senal_minutoCambio.emit( [self.noDiaEntreSemana,self.hora,self.minuto] )
                #self.actualizarTiempo()
                
            elif id_senalEmitir==self.CAMBIO_DIA:
                self.senal_diaCambio.emit([self.noDiaEntreSemana,self.hora,self.minuto])


    def actualizarTiempo(self):
        hoy=datetime.now()
        self.hora=hoy.hour
        self.minuto=hoy.minute
        self.segundo=hoy.second

        #da los numeros de dia entre semana  (0-lunes,1-martes,...)
        self.noDiaEntreSemana=hoy.weekday()   


'''
#https://stackoverflow.com/questions/47339044/pyqt5-timer-in-a-thread 
#https://stackoverflow.com/questions/48326817/pyqt5-qtimer-in-qthread-is-being-garbage-collected 
#https://stackoverflow.com/questions/47339044/pyqt5-timer-in-a-thread 

class DataCaptureThread(QThread):
    senal_minutoCambio=pyqtSignal(list)
    senal_diaCambio=pyqtSignal(list)
    CAMBIO_MINUTO=0
    CAMBIO_DIA=2

    def collectProcessData(self):
        print ("Collecting Process Data")

    def __init__(self):
        QThread.__init__(self)
        self.actualizarTiempo()
        self.contador= QTimer()
        self.contador.moveToThread(self)
        self.contador.timeout.connect(self.clock)

    def actualizarTiempo(self):
        hoy=datetime.now()
        self.hora=hoy.hour
        self.minuto=hoy.minute
        self.segundo=hoy.second
        #da los numeros de dia entre semana  (0-lunes,1-martes,...)
        self.noDiaEntreSemana=hoy.weekday()+1     #(1-lunes,2-martes,...)

    def clock(self):
        senalEmitir=None
        self.segundo+=1 #aumento el valor del atributo 'segundo' en 1
        if self.segundo>59:#aumentar el valor del atributo 'minuto' en 1
            self.segundo=0
            self.minuto+=1
            senalEmitir=self.CAMBIO_MINUTO
            if self.minuto>59:#aumentar el valor del atributo 'hora' en 1              
                self.minuto=0
                self.hora+=1
                if self.hora>23:
                    self.hora=0
                    self.noDiaEntreSemana+=1
                    senalEmitir=self.CAMBIO_DIA
                    if self.noDiaEntreSemana>6:
                        self.noDiaEntreSemana=0
        self.informarPosible_cambio(senalEmitir)
    
    def informarPosible_cambio(self,id_senalEmitir=None):
        print(self)
        if id_senalEmitir!=None:
            if id_senalEmitir==self.CAMBIO_MINUTO:
                hoy=datetime.now()
                minute=hoy.minute
                self.senal_minutoCambio.emit( [self.noDiaEntreSemana,self.hora,self.minuto] )
                self.actualizarTiempo()
                
            elif id_senalEmitir==self.CAMBIO_DIA:
                self.senal_diaCambio.emit([self.noDiaEntreSemana,self.hora,self.minuto])

    def __str__(self):
        return f"{self.hora}:{self.minuto}"


    def run(self):
        self.contador.start(1000)
        loop = QEventLoop()
        loop.exec_()

'''