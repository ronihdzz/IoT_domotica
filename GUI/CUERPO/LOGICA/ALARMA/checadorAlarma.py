from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore

###############################################################
#  MIS LIBRERIAS...
##############################################################
from CUERPO.LOGICA.ALARMA.alarma import HoraAlarma
from CUERPO.LOGICA.ALARMA.baseDatos_alarma import BaseDatos_alarmas
from recursos import App_Alarmas

class ChecadorAlarma(QtCore.QObject):
    '''
    El proposito de esta clase es tener un control, un seguimiento de las alarmas, para
    que suenen cuando tengan que sonar
    '''
    
    senal_alarmaDetectada=pyqtSignal(list) # esta senal contendra una lista con los 'id' de la 
                                           # o las alarmas que ya tienen que sonar.


    def __init__(self,noDiaHoy,hora,minuto):
        '''
        Al crear un instancia debes decirle en que dia que hora y en que minuto 
        nos encontramos, para que  esta instancia tenga los suficientes datos para 
        saber que alarmas en particular son a las que tiene que dar seguimiento.

        Parámetros:

            'noDiaHoy' --  dato de tipo entero que representa los dias de la
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
        '''

        QtCore.QObject.__init__(self)
        
        self.punteroMinuto=minuto
        self.punteroHora=hora
        self.punteroDia=noDiaHoy


        # El atributo de instancia 'self.dictAlarmas' es un diccionario que contiene datos claves
        # de las alarmas que sonaran el dia actual, dicho diccionario sus 'keys' seran los 'id' de
        # las alarmas, y lo 'values' seran instancias la clase 'HoraAlarma' los cuales indicaran a 
        # que hora dicha alarma debe sonar.
        # Ejemplo:
        #    { 'idAlarma_1': HoraAlarma(horaAlarma_1,minutoAlarma_1),
        #      'idAlarma_2': HoraAlarma(horaAlarma_2,minutoAlarma_2),
        #      'idAlarma_3': HoraAlarma(horaAlarma_3,minutoAlarma_3),
        #       } 
        self.dictAlarmas={}

        self.baseDatosAlarmas=BaseDatos_alarmas(App_Alarmas.NOMBRE_BASE_DATOS_ALARMAS)
        self.actualizarAlarmasHoy(noDiaHoy,hora,minuto)

    def revisar(self,hora,minuto):
        '''
        El objetivo de este metodo es revisar si ya es la hora de sonar de la o las alarmas cuya 
        'HoraAlarma' sea menor a la instancia HoraAlarma  que se crea con los parametros 'hora' y
        'alarma', en pocas palabras al llamar a este metodo le debes indicar la hora actual atraves 
        de los parametros 'hora', 'minuto' y el metodo lo que hara es ver si hay alarmas que suenan en 
        ese tiempo, en caso de exitir, emitara a la señal 'senal_alarmaDetectada' la cual mandara una 
        lista con los 'id' de la o las alarmas que ya deben  sonar

        Parámetros:
            'hora' -- dato de tipo entero que indica la hora a la cual nos encontramos, dado que el dia 
            contiene 24 horas, el valor del parametro 'hora' estara delimitado por valores en el intervalo 
            cerrado: [0,23]
            'minuto' --  dato de tipo entero que indica en el minuto a la cual nos encontramos, dado que 
            cada  hora tiene 60 minutos, el valor del parametro 'minuto' estara delimitado por valores en el
            intervalor cerrado: [0,59]
        '''

        #print(f"REVISION: {hora},{minuto}")
        listAlar_yaDebenSonar=[]

        self.punteroMinuto=minuto
        self.punteroHora=hora
        tiempoActual=HoraAlarma(hora,minuto)

        for idAlarma,horaSuena in self.dictAlarmas.items():
            #print(f"{horaSuena}  <= {tiempoActual}")
            if horaSuena<=tiempoActual:
                listAlar_yaDebenSonar.append( idAlarma )
            else:
                break

        if listAlar_yaDebenSonar!=[]:
            self.senal_alarmaDetectada.emit( listAlar_yaDebenSonar )
            for idAlarma in listAlar_yaDebenSonar:
                del self.dictAlarmas[idAlarma]

    def actuarAnte_eliminacionUnaAlarma(self,id_alarma):
        """
        Cuando el usuario elimina una alarma puede que sea una de  las alarmas que esta 
        almacenada en: 'self.dictAlarmas' si ese es el caso entonces la alarma se debe 
        eliminar de 'self.dicAlarmas', ya que este almacena la alarmas que van a sonar 
        el dia actual y si esa alarma ya no existe es indispensable eliminar de 'self.dictAlarmas'
        y eso es lo que hace este metodo, por tal motivo debe ser  llamado si es que ocurre 
        esa accion 

        Parámetros:
            id_alarma -- dato de tipo 'int' que representara al 'id' de la alarma que se elimino
        """

        if id_alarma in self.dictAlarmas:
            del self.dictAlarmas[id_alarma]

    def actuarAnte_edicionUnaAlarma(self,alarmaEdito):
        '''
        Cuando una alarma es editada por el usuario, existe la posibilidad de que ya no quiere que
        suene este dia, o que quiere que suene en una  hora anterior a la actual o todo lo contrario,
        por tal motivo cuando se edita una alarma se deben revisar todos esos casos y actuar en consecuencia,
        por estas razones este metodo debe ser llamado si ocurre esa accion.

        Parametros:
            'alarmaEdito' -- es una instancia de la clase 'Alarma', esta instancia  contiene todos
             los datos de la alarma que edito el usuario
        '''

        # la alarma que se edito ¿suena en el dia actual?
        if alarmaEdito.diasActiva[self.punteroDia]: 
            # ¿la hora a la que suena la alarma que se edito es mayor a la hora actual?
            if alarmaEdito.horaAlarma>HoraAlarma(self.punteroHora,self.punteroMinuto):
                    self.dictAlarmas[alarmaEdito.id]=alarmaEdito.horaAlarma
                    #ordenando de forma ascendente las horas de las alarmas
                    self.dictAlarmas=dict( sorted(self.dictAlarmas.items(),key=lambda x: x[1], reverse=False ) )
            else:
                # la alarma que se edito no suena en un hora mayor a la actual, pero
                # ¿ esa alarma estaba en el diccionario ?
                if alarmaEdito.id in self.dictAlarmas: 
                    del self.dictAlarmas[alarmaEdito.id]
        else:
            # la alarma que se edito no suena en el dia  actual, pero
            # ¿ esa alarma estaba en el diccionario ?
            if alarmaEdito.id in self.dictAlarmas:
                del self.dictAlarmas[alarmaEdito.id]
    
    def actuarAnte_anexionAlarma(self,alarmaAgrego):
        '''
        Cuando un usuario crea una alarma, existe la posibilidad de que esta alarma suene el dia actual, 
        por tal motivo cuando se agrega una  alarma se debe revisar si esta alarma suena el dia de hoy, 
        por esta razon cuando se agrega una alarma se debe llamar este metodo.
        Parametros
            'alarmaAgrego' -- es una instancia de la clase 'Alarma', esta instancia  contiene todos los 
            datos de la alarma que edito el usuario
        '''

        # ¿la alarma que se agrego suena el dia actual?
        if alarmaAgrego.diasActiva[self.punteroDia]:
            # ¿la hora a la que suena la alarma que se agrego es mayor a la hora actual?
            if alarmaAgrego.horaAlarma>HoraAlarma(self.punteroHora,self.punteroMinuto):
                    self.dictAlarmas[alarmaAgrego.id]=alarmaAgrego.horaAlarma
                    # ordenando de forma ascendente las horas de las alarmas
                    self.dictAlarmas=dict( sorted(self.dictAlarmas.items(),key=lambda x: x[1], reverse=False ) )


    def actualizarAlarmasHoy(self,noDiaHoy,hora,minuto):
        '''
        La clase 'ChecadorAlarma' tiene el objetivo de avisar cuando las alarmas deben sonar, 
        por tal motivo debe estar constantemente revisando la 'HoraAlarma'  de las alarmas, 
        para ello la metodologia que usa el 'ChecadorAlamas' es  descargar solo las alarmas 
        del dia actual y cuya 'HoraAlarma' aun no haya pasado de lo hora actual, despues procede
        a almacenar su nombre y hora de dichas alarmas en un diccionario de FORMA ORDENADA ASCENDENTE, 
        por tal motivo CADA QUE SE TERMINA UN DIA, deben cargarse las alarmas del dia SIGUIENTE y de 
        forma ordenada.

        Parámetros:
            noDiaHoy -- indica que dia es el nuevo actual, es un dato de tipo 
            entero que representa los dias de la semana:
                0  significa que es el dia lunes
                1  significa que es el el dia martes
                2  significa que es el dia miercoles
                .
                .
                .
                6  significa que es el dia domingo
            Esto signigicia que su valor estara delimitado por los valores en el intervalo
            cerrado: [0,6]
                
            hora -- es un dato de tipo entero que indica la hora a la cual nos encontramos,
            dado que el dia contiene 24 horas, el valor del parametro 'hora' estara delimitado
            por valores en el intervalor cerrado: [0,23]

            minuto -- es un dato de tipo entero que indica en el minuto a la cual nos encontramos,
            dado que cada hora tiene 60 minutos, el valor del parametro 'minuto' estara delimitado
            por valores en el intervalor cerrado: [0,59]

        Este metodo cargara todos las alarmas  registradas para sonar el dia: 'noDiaHoy' y que
        suenan despues de la hora  'HoraAlarma'  que se crea con los parametros 'hora' y 'alarma'
        '''
        
        self.punteroDia=noDiaHoy
        self.punteroHora=hora
        self.punteroMinuto=minuto

        self.dictAlarmas=self.baseDatosAlarmas.getDictHoraAlarmas(noDiaHoy,self.punteroHora,self.punteroMinuto)
        #print("Dia de hoy:",noDiaHoy)
        #print("INFO ALARMAS EN COLOA:",self.dictAlarmas)



            
            
