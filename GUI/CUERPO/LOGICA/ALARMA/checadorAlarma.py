from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore

###############################################################
#  MIS LIBRERIAS...
##############################################################
from CUERPO.LOGICA.ALARMA.alarma import HoraAlarma
from CUERPO.LOGICA.ALARMA.baseDatos_alarma import BaseDatos_alarmas
from CUERPO.LOGICA.RECURSOS.recursos import Recursos_IoT_Domotica


class ChecadorAlarma(QtCore.QObject):
    '''El proposito de esta clase es tener un control, un seguimiento
    de las alarmas, para que suenen cuando tengan que sonar '''
    
    senal_alarmaDetectada=pyqtSignal(list)#esta senal contendra una lista
    #de tuplas donde cada tupla contendra el nombre y la 'HoraAlarma' de la
    #o las alarmas que ya tienen que sonar.


    def __init__(self,noDiaHoy,hora,minuto):
        '''Al crear un instancia debes decirle en que dia que hora y en que minuto 
        nos encontramos, para que  esta instancia tenga los suficientes datos para 
        saber que alarmas en particular son a las que tiene que dar seguimiento.
            A)'noDiaHoy'  es un dato de tipo entero en donde:
                0  significa que es el dia lunes
                1  significa que el el dia martes
                2  significa que es el dia miercoles
                .
                .
                .
            B) 'hora' es un dato de tipo entero que indica la hora a la cual nos encontramos,
            dado que el dia contiene 24 horas, el valor del parametro 'hora' estara delimitado
            por valores en el intervalor cerrado: [0,23]
            C)  'minuto' es un dato de tipo entero que indica en el minuto a la cual nos encontramos,
            dado que cada hora tiene 60 minutos, el valor del parametro 'minuto' estara delimitado
            por valores en el intervalor cerrado: [0,59]
        '''

        QtCore.QObject.__init__(self)
        self.punteroMinuto=minuto
        self.punteroHora=hora
        self.punteroDia=noDiaHoy

        self.dictAlarmas={}#las 'keys' sean los nombres de las
        #alarmas, y lo 'values' sean instancias la clase 'HoraAlarma'  las cuales
        #indicara a que hora dicha alarma debe sonar.
        #Ejemplo:
        #    { 'nombreAlarma_1': HoraAlarma(hora=10,minuto=15),
        #      'nombreAlarma_2': HoraAlarma(hora=7,minuto=15),
        #      'nombreAlarma_3': HoraAlarma(hora=19,minuto=30),
        #       } 

        self.baseDatosAlarmas=BaseDatos_alarmas(Recursos_IoT_Domotica.NOMBRE_BASE_DATOS_ALARMAS)
        self.actualizarAlarmasHoy(noDiaHoy,hora,minuto)

    def revisar(self,hora,minuto):
        '''El objetivo de este metodo es revisar si ya es la hora de sonar de
        la o las alarmas cuya 'HoraAlarma' sea menor a la instancia HoraAlarma 
        que se crea con los parametros 'hora' y 'alarma', en pocas palabras
        al llamar a este metodo le debes indicar que hora es atraves de los parametros
        'hora', 'minuto' y el metodo lo que hara es ver si hay alarmas que suenan en 
        ese tiempo, en caso de haber, emitara a la señal 'senal_alarmaDetectada' con 
        los datos de la o las alarmas que deben ya sonar.
        '''

        print(f"REVISION: {hora},{minuto}")
        listAlar_yaDebenSonar=[]

        self.punteroMinuto=minuto
        self.punteroHora=hora
        tiempoActual=HoraAlarma(hora,minuto)

        for nombreAlarma,horaSuena in self.dictAlarmas.items():
            print(f"{horaSuena}  <= {tiempoActual}")
            if horaSuena<=tiempoActual:
                listAlar_yaDebenSonar.append(  (nombreAlarma,horaSuena)  )
            else:
                break
        
        if listAlar_yaDebenSonar!=[]:
            self.senal_alarmaDetectada.emit( listAlar_yaDebenSonar )
            for nombreAlarma,_ in listAlar_yaDebenSonar:
                del self.dictAlarmas[nombreAlarma]

    def actuarAnte_eliminacionUnaAlarma(self,nombreAlarma):
        """Cuando el usuario elimina una alarma puede que sea una de 
        las alarmas que esta almacenada en: 'self.dictAlarmas' si ese
        es el caso entonces la alarma se debe elimar de 'self.dicAlarmas', ya
        que este almacena la alarmas que van a sonar el dia actual y si
        esa alarma ya no existe es indispensable eliminar de 'self.dictAlarmas'
        y eso es lo que hace este metodo, por tal motivo debe ser 
        llamado si es que ocurre esa accion """

        if nombreAlarma in self.dictAlarmas:
            del self.dictAlarmas[nombreAlarma]

    def actuarAnte_edicionUnaAlarma(self,alarma):
        '''Cuando una alarma es editada por el usuario, existe la posibilidad
        de que ya no quiere que suene este dia, o que quiere que suene en una 
        hora anterior a la actual o todo lo contrario, por tal motivo cuando
        se edita una alarma se deben revisar todos esos casos y actuar en consecuencia,
        por estas razones este metodo debe ser llamado si ocurre esa accion.
        Parametros:
            A) 'alarma'  es una instancia de la clase 'Alarma', esta instancia 
            contiene todos los datos de la alarma que edito el usuario
        '''

        if alarma.diasActiva[self.punteroDia]:
            if alarma.horaAlarma>HoraAlarma(self.punteroHora,self.punteroMinuto):
                    self.dictAlarmas[alarma.nombre]=alarma.horaAlarma
                    #ordenando de forma ascendente las horas de las alarmas
                    self.dictAlarmas=dict( sorted(self.dictAlarmas.items(),key=lambda x: x[1], reverse=False ) )
            else:
                if alarma.nombre in self.dictAlarmas:
                    del self.dictAlarmas[alarma.nombre]
        else:
            if alarma.nombre in self.dictAlarmas:
                del self.dictAlarmas[alarma.nombre]
    
    def actuarAnte_anexionAlarma(self,alarma):
        '''Cuando un usuario crea una alarma, existe la posibilidad
        de que esta alarma suene el dia actual, por tal motivo cuando
        se agrega una  alarma se debe revisar si esta alarma suena 
        el dia de hoy, por esta razon cuando se agrega una alarma se
        debe llamar este metodo.
        Parametros
            A) 'alarma'  es una instancia de la clase 'Alarma', esta instancia 
            contiene todos los datos de la alarma que edito el usuario
        '''

        if alarma.diasActiva[self.punteroDia]:
            if alarma.horaAlarma>HoraAlarma(self.punteroHora,self.punteroMinuto):
                    self.dictAlarmas[alarma.nombre]=alarma.horaAlarma
                    #ordenando de forma ascendente las horas de las alarmas
                    self.dictAlarmas=dict( sorted(self.dictAlarmas.items(),key=lambda x: x[1], reverse=False ) )


    def actualizarAlarmasHoy(self,noDiaHoy,hora,minuto):
        '''La clase 'ChecadorAlarma' tiene el objetivo de avisar cuando las alarmas
        deben sonar, por tal motivo debe estar constantemente revisando la 'HoraAlarma' 
        de las alarmas, para ello la metodologia que usa el 'ChecadorAlamas' es 
        descargar solo las alarmas del dia actual y cuya 'HoraAlarma' aun no haya pasado
        de lo hora actual, despues procede a almacenar su nombre y hora de dichas alarmas 
        en un diccionario de FORMA ORDENADA DESCENDENTE, por tal motivo CADA QUE SE TERMINA
        UN DIA, deben cargarse las alarmas del dia SIGUIENTE y de forma ordenada Y ESTO
        ES LO QUE HACE ESTE PARAMETRO.
            Parametros:
                A)'noDiaHoy'  es un dato de tipo entero en donde:
                    0  significa que es el dia lunes
                    1  significa que el el dia martes
                    2  significa que es el dia miercoles
                    .
                    .
                    .
                este parametro indica que dia es el nuevo actual.
                B) 'hora' es un dato de tipo entero que indica la hora a la cual nos encontramos,
                dado que el dia contiene 24 horas, el valor del parametro 'hora' estara delimitado
                por valores en el intervalor cerrado: [0,23]
                C)  'minuto' es un dato de tipo entero que indica en el minuto a la cual nos encontramos,
                dado que cada hora tiene 60 minutos, el valor del parametro 'minuto' estara delimitado
                por valores en el intervalor cerrado: [0,59]

        Este metodo cargara todos las alarmas  registradas para sonar el dia: 'noDiaHoy' y que
        suenan despues de la hora  'HoraAlarma'  que se crea con los parametros 'hora' y 'alarma'
        '''
        
        self.punteroDia=noDiaHoy
        self.punteroHora=hora
        self.punteroMinuto=minuto

        self.dictAlarmas=self.baseDatosAlarmas.getDictHoraAlarmas(noDiaHoy,self.punteroHora,self.punteroMinuto)
        print("Dia de hoy:",noDiaHoy)
        print("INFO ALARMAS EN COLOA:",self.dictAlarmas)



            
            
