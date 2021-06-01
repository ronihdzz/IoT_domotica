from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore
from datetime import datetime



class Reloj(QtCore.QObject):
    '''
    El objetivo de esta clase es llevar un control del tiempo en el se encuentra el sistema,
    y emitir señales cada dia y minuto cumplido, asi como tratar de evitar cualquier retraso 
    en el tiempo que se pueda llegar a tener.
    '''
    
    senal_minutoCambio=pyqtSignal(list)
    senal_diaCambio=pyqtSignal(list)
    CAMBIO_MINUTO=0
    CAMBIO_DIA=2

    def __init__(self,dia,hora,minuto,segundo):
        """
        Al crear un instancia debes decirle en que dia que hora y en que minuto 
        nos encontramos, para que  esta instancia tenga los suficientes datos para 
        saber el tiempo actual en el que se encuentra para posteriormente darle 
        seguimiento

        Parámetros:

            'dia' --  dato de tipo entero que representa los dias de la
            semana:
                0  significa que es el dia lunes
                1  significa que es el el dia martes
                2  significa que es el dia miercoles
                .
                .
                .
                6  significa que es el dia domingo
            Esto signigicia que su valor estara delimitado por los valores en el intervalo
            cerrado: [0,6]

             'hora' - -  dato de tipo entero que indica la hora a la cual nos encontramos,
            dado que el dia contiene 24 horas, el valor del parametro 'hora' estara delimitado
            por valores en el intervalo cerrado: [0,23]

            'minuto' -- dato de tipo entero que indica en el minuto a la cual nos encontramos,
            dado que cada hora tiene 60 minutos, el valor del parametro 'minuto' estara delimitado
            por valores en el intervalor cerrado: [0,59]
        """

        QtCore.QObject.__init__(self)
        self.noDiaDeLaSemana=dia
        self.minuto=minuto
        self.hora=hora
        self.segundo=segundo
    
    def clock(self):
        '''
        Este metodo áumentara en un segundo el tiempo registrado, por ende aumentara en uno el valor 
        del atributo 'self.segundo', y si al hacer ese aumento:
            b) El atributo 'self.segundo' es mayor a 59 tambien entonces: se aumentara en uno el valor 
            del atributo 'self.minuto' se igualara a cero el atributo 'self.segundo' y se emitira la 
            señal   'self.senal_minutoCambio'
            c) El atributo 'self.minuto' es igual a 59 y el atributo 'self.segundo' es mayor a 59, se
            aumentara en uno el valor del atributo 'self.hora' y se igualara a cero el valor de los 
            atributos 'self.segundo' y 'self.minuto'
            c) El atributo 'self.hora=23' y 'self.minuto=59' y 'self.segundo'>59, se aumentara en uno
            el valor de 'self.noDiaLaSemana' y se igualara a cero el valor de los atributos: 'self.hora'
            'self.minuto' y 'self.segundo' y se emitira la  señal 'self.senal_diaCambio'
            d) El atributo 'self.noDiaLaSemana=6' y 'self.hora=23' y 'self.minuto=59' y 'self.segundo'>59
            se igualara a cero el valor de los atributos: 'self.noDiaDeLaSemana' y 'self.hora' y 'self.minuto' 
            y 'self.segundo'  y se emitira la  señal 'self.senal_diaCambio'
        '''
        senalEmitir=None
        self.segundo+=1 #aumento el valor del atributo 'segundo' en 1
        if self.segundo>59:#aumentar el valor del atributo 'minuto' en 1
            self.segundo=0
            self.minuto+=1
            senalEmitir=self.CAMBIO_MINUTO
            #print("CAMBIO MINUTO")
            if self.minuto>59:#aumentar el valor del atributo 'hora' en 1              
                self.minuto=0
                self.hora+=1
                if self.hora>23:
                    self.hora=0
                    self.noDiaDeLaSemana+=1
                    senalEmitir=self.CAMBIO_DIA
                    #print("CAMBIO DIaaaaaaaaaaaaaaaaaaaaaaaA")
                    if self.noDiaDeLaSemana>6:
                        self.noDiaDeLaSemana=0
    
        self.informarPosible_cambio(senalEmitir)

    def __str__(self):
        return f"{self.hora}:{self.minuto}"
    
    def informarPosible_cambio(self,id_senalEmitir=None):
        '''
        En función del valor del parametro: 'id_senalEmitir'  emitira una señal corresponiente,
        en caso de que el valor del parametro 'id_senalEmitir' sea igual a None, no se emitira
        ninguna señal.
        '''

        if id_senalEmitir!=None:
            if id_senalEmitir==self.CAMBIO_MINUTO:
                self.senal_minutoCambio.emit( [self.noDiaDeLaSemana,self.hora,self.minuto] )
                
                # Debido a que se espera que se tenga un retraso de tiempo con el tiempo actual, se 
                # actualizan los valores de la instancia despues de que se mando la señal ya que
                # al actualizar el tiempo, lo unico que se espera es que se actualice el valor del
                # atributo 'self.segundo' y que este incremente al ser actualizado, pues se esperaba
                # un retraso en el tiempo no mayor a un 'minuto'. 
                
                #self.actualizarTiempo()
                
            elif id_senalEmitir==self.CAMBIO_DIA:
                self.senal_diaCambio.emit([self.noDiaDeLaSemana,self.hora,self.minuto])


    def actualizarTiempo(self):
        '''
        Se espera que el 'QTimer' que llama al metodo 'clock' de esta clase, pueda ser
        que se retrase por todos las diferentes cosas que hace el sistema, por tal motivo
        lo que hace este metodo es actualizar los valores del atributo 'self.hora', 'self.minuto'
        y 'self.segundo' con la finalidad de que actualice los retrasos que pudo llegar a tener.

        '''

        hoy=datetime.now()
        self.hora=hoy.hour
        self.minuto=hoy.minute
        self.segundo=hoy.second

        #da los numeros de dia entre semana  (0-lunes,1-martes,...)
        self.noDiaDeLaSemana=hoy.weekday()   


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