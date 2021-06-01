

class HoraAlarma():
    """
    Esta clase permite establecer la hora de una alarma, su presicion son los 
    minutos, es decir las instancias de  la clase 'HoraAlarma' solo pueden 
    ser expresadas con  horas y minutos.Tambien permite operaciones con operadores
    logicos entre instancias de la misma clase.
    """

    def __init__(self,hora,minuto):
        """
        El metodo constructor necesita forsozamente dos parametros,el dato de hora
        y el dato de minuto,ya que la clase HoraAlarma crea objetos de 'HoraAlarma' 
        con una prescion de minutos, es decir para estos objetos no hay segundos. """

        self.hora=hora
        self.minuto=minuto


    def __str__(self):
        """
        Realizara la conversión de la hora en sistema de 24 horas, a la hora
        en el sistema de 12 horas, posteriormente dicho resultado lo retonara
        como un dato de tipo string.

        Returns (Devoluciones):
            Dato de tipo string que  contenga la hora en el formato de 'sistema horario de 
            12 horas(ocupando AM PM)'
        """
        
        pm_am='P.M.'
        resultado=''

        hora=self.hora
        minuto=self.minuto

        if hora<12:
            pm_am='A.M.'
        elif hora>12:
            hora-=12
        if hora<10:
            resultado="0"
        resultado+=str(hora)+":"
        
        if minuto<10:
            resultado+="0"
        resultado+=str(minuto)

        resultado=resultado+" "+pm_am
        return resultado

    def getMinutos(self):
        '''
        Hara el calculo para obtener  el numero total de minutos a los que equivale
        la  instancia de la clase 'HoraAlarma', es decir obtendra la equivalencia en 
        minutos del atributo de instancia 'self.hora' y lo sumara con el atributo 
        'self.minuto', posteriormente retornara dicho resultado

        Returns (Devoluciones):
            Dato de tipo entero que representara el numero de minutos a los que equivale
            la instancia de la clase 'HoraAlarma'    
        '''

        return  (  (self.hora*60) + self.minuto  )

    def __lt__(self,otro):
        '''
        Con esto se permite que los objetos instanciados de la clase 'HoraAlarma' den un 
        resultado cuando les pidan reaccionar ante el operador logico: '<' (MENOR QUE).
        La pregunta que se hara este metodo para retornar una respuesta sera:
        ¿es mi instancia MENOR QUE la intancia que representa el parametro 'otro'?

        Parámetros:
            otro -- Es una instancia de la clase 'HoraAlarma'

        Returns (Devoluciones):
            Dato de tipo booleano  que representara la respuesta a la pregunta:
            ¿es mi instancia MENOR QUE la intancia que representa el parametro 'otro'?
                A) Si el dato que se retorna es igual a 'True', significara que 
                la instancia 'self' es MENOR QUE la instancia 'otro'
                B) Si el dato que se retorna es igual a 'False', significara que 
                la instancia 'self' es MAYOR O IGUAL QUE la instancia 'otro'
        '''

        return self.getMinutos() < otro.getMinutos()

    def __gt__(self,otro):
        '''
        Con esto se permite que los objetos instanciados de la clase 'HoraAlarma' den un 
        resultado cuando les pidan reaccionar ante el operador logico: '>' (MAYOR QUE).
        La pregunta que se hara este metodo para retornar una respuesta sera:
        ¿es mi instancia MAYOR QUE la intancia que representa el parametro 'otro'?

        Parámetros:
            otro -- Es una instancia de la clase 'HoraAlarma'

        Returns (Devoluciones):
            Dato de tipo booleano  que representara la respuesta a la pregunta:
            ¿es mi instancia mayor que la intancia que representa el parametro 'otro'?
                A) Si el dato que se retorna es igual a 'True', significara que 
                la instancia 'self' es MAYOR QUE la instancia 'otro'
                B) Si el dato que se retorna es igual a 'False', significara que 
                la instancia 'self' es MENOR O IGUAL QUE  la instancia 'otro'
        '''

        return self.getMinutos() > otro.getMinutos()

    def __le__(self,otro):
        '''
        Con esto se permite que los objetos instanciados de la clase 'HoraAlarma' den un 
        resultado cuando les pidan reaccionar ante el operador logico: '<=' (MENOR O IGUAL QUE).
        La pregunta que se hara este metodo para retornar una respuesta sera:
        ¿es mi instancia MENOR O IGUAL QUE la intancia que representa el parametro 'otro'?

        Parámetros:
            otro -- Es una instancia de la clase 'HoraAlarma'

        Returns (Devoluciones):
            Dato de tipo booleano  que representara la respuesta a la pregunta:
            ¿es mi instancia MENOR O IGUAL QUE la intancia que representa el parametro 'otro'?
                A) Si el dato que se retorna es igual a 'True', significara que 
                la instancia 'self' es MENOR O IGUAL QUE la instancia 'otro'
                B) Si el dato que se retorna es igual a 'False', significara que 
                la instancia 'self' es MAYOR QUE la instancia 'otro'
        '''

        return self.getMinutos() <= otro.getMinutos()

    def __ge__(self, otro):
        '''
        Con esto se permite que los objetos instanciados de la clase 'HoraAlarma' den un 
        resultado cuando les pidan reaccionar ante el operador logico: '>=' (MAYOR O IGUAL QUE).
        La pregunta que se hara este metodo para retornar una respuesta sera:
        ¿es mi instancia MAYOR O IGUAL QUE la intancia que representa el parametro 'otro'?

        Parámetros:
            otro -- Es una instancia de la clase 'HoraAlarma'

        Returns (Devoluciones):
            Dato de tipo booleano  que representara la respuesta a la pregunta:
            ¿es mi instancia MAYOR O IGUAL QUE la intancia que representa el parametro 'otro'?
                A) Si el dato que se retorna es igual a 'True', significara que 
                la instancia 'self' es MAYOR O IGUAL QUE la instancia 'otro'
                B) Si el dato que se retorna es igual a 'False', significara que 
                la instancia 'self' es MENOR QUE la instancia 'otro'
        '''

        return self.getMinutos() >= otro.getMinutos()

    def __eq__(self, otro):
        '''
        Con esto se permite que los objetos instanciados de la clase 'HoraAlarma' den un 
        resultado cuando les pidan reaccionar ante el operador logico: '==' (IGUAL QUE).
        La pregunta que se hara este metodo para retornar una respuesta sera:
        ¿es mi instancia IGUAL QUE la intancia que representa el parametro 'otro'?

        Parámetros:
            otro -- Es una instancia de la clase 'HoraAlarma'

        Returns (Devoluciones):
            Dato de tipo booleano  que representara la respuesta a la pregunta:
            ¿es mi instancia IGUAL QUE la intancia que representa el parametro 'otro'?
                A) Si el dato que se retorna es igual a 'True', significara que 
                la instancia 'self' es IGUAL QUE la instancia 'otro'
                B) Si el dato que se retorna es igual a 'False', significara que 
                la instancia 'self' es ES DIFERENTE QUE la instancia 'otro'
        '''

        return self.getMinutos() == otro.getMinutos()


class Alarma():
    '''
    Sera util para establecer un tipo de dato universal de tipo 'Alarma' acorde unicamente a las 
    necesidades de mi programa, con el fin de  que todos los demas scripts tengan un convencionalismo
    a la hora de comunicarse con cosas relacionados con las alarmas
    '''
    

    DIAS_SEMANA=("lunes","martes","miercoles","jueves","viernes","sabado","domingo")

    def __init__(self,id=None,nombre="",sonido=None,asunto=0,hora=0,minuto=0,diasActiva=[0,0,0,0,0,0,0],prendida=1):
        '''
        Parámetros: 
            id -- dato de tipo 'int' que representa el 'id' de la alarma
            nombre -- dato de tipo 'string' que representa el nombre de la alarma
            sonido -- dato de tipo 'string' que representa el nombre de la canción 
                        que se reproducira cuando sea hora de sonar de la alarma
            asunto -- dato de tipo de tipo 'int' con solo 3 posibles valores:
                A) asunto=1 singifica que el asunto es:  'despertar'
                B) asunto=2 significa que el asunto  es: 'dormir'
                C) asunto=3 significa que el asunto es: 'deberes'
                D) asunto= [-infinito,2] U [4,infinito] sinifica que el asunto es igual a 'otro
            minuto -- dato de tipo 'int' que representa  el minuto que sonara la alarma
            hora -- dato de tipo 'entero' que representa la hora en la que sonara la alarma
            diaActiva -- dato de tipo 'list' de tamaño igual a  7 elementos donde cada elemento
                            de la lista es un dato de tipo 'bool'. Cada posición de la lista 
                            representa un dia:
                                posicion=0 representa el dia lunes
                                posicion=1 representa el dia martes
                                        .
                                         .
                                posicion=6 representa el dia domingo
                            Cada valor de cada elemento de la lista representa si la alarma suena 
                            en el dia que corresponde a la posición en la que se encuentra el 
                            elemento, ejemplos: 
                                La siguiente lista dice que la alarma solo sonara el dia lunes:
                                    [True,False,False,False,False,False,False] 
                                La siguiente lista dice que la alarma sonara solo el dia lunes y domingo:
                                    [True,False,False,False,False,False,True] 
            prendida -- dato de tipo 'bool' que representa si la alarma se encuentra
            activada o desactivada:
                A) Si prendida=True significara que la alarma se encuentra activada
                B) Si prendida=False significara que la alarma se encuentra desactivada.
        
        Returns (Devoluciones):
            Una instancia de la clase 'Alarma'
        '''
        self.id=id
        self.nombre=nombre
        self.asunto=asunto
        self.diasActiva=diasActiva
        self.prendida=prendida
        self.sonido=sonido
        self.horaAlarma=HoraAlarma(hora,minuto)
    
    @staticmethod
    def tupla_toAlarma(tuplaDatos):
        """
        Creara una instancia de la clase 'Alarma', apartir de una tupla de datos, es decir funciona 
        casi igual que el metodo constructor, la unica diferencia es que en el metodo constructor 
        solicita 8 parametros, y esta funcion solicita 1 parametro el cual es una tupla, pero una 
        tupla con  14 elementos en el mismo orden que aparecen en el metodo constructor es decir 
        (id,nombre,sonido,asunto,minuto,diasActiva_elemento1,diasActiva_elemento1
        diasActiva_elemento2,diasActiva_elemento3,diasActiva_elemento4,diasActiva_elemento5
        diasActiva_elemento6,diasActiva_elemento7,prendida), una vez creada la instancia de la clase
        'Alarma', la retornara.

        Parámetros:
            tuplaDatos -- Un parametro de tipo 'tuple' con  un tamaño de 14 elementos, donde cada 
            elemento representa un valor correspondiente a un atributo de la clase alarma, los 
            elemento de la tupla siguen el siguiente  el siguiente orden:
            (id,nombre,sonido,asunto,minuto,diasActiva_elemento1,diasActiva_elemento1
            diasActiva_elemento2,diasActiva_elemento3,diasActiva_elemento4,diasActiva_elemento5
            diasActiva_elemento6,diasActiva_elemento7,prendida)
               
        Returns (Devoluciones):
            Una instancia de la clase 'Alarma'
        """

        id=tuplaDatos[0]
        nombre=tuplaDatos[1]
        sonido=tuplaDatos[2]
        asunto=tuplaDatos[3]
        hora=tuplaDatos[4]
        minuto=tuplaDatos[5]
        diasActiva=tuplaDatos[6:-1]
        prendida=tuplaDatos[-1]

        alarma=Alarma(id=id,nombre=nombre,sonido=sonido, asunto=asunto,hora=hora,minuto=minuto,
            diasActiva=diasActiva,prendida=prendida)

        return alarma        
    
    def getDias(self):
        """
        Hara un string el cual contendra los nombres de los dias en los que la alarma
        debe sonar, este string se generara apartir del atributo 'self.diaActivas'.Una
        vez hecho dicho string, lo retornora.

        Returns (Devoluciones):
              String con los nombres de los dias de la semana en los que la alarma debe 
              sonar, cada nombre estara separado por una coma.
        """

        nombreDias=[]
        for c,diaRequerido in enumerate(self.diasActiva):
            if diaRequerido:
                nombreDias.append(  self.DIAS_SEMANA[c]     )
        return  ",".join(nombreDias)
    
    def to_tupla(self,conId=False):
        """
        Creara  una tupla que contiene todos los atributos de la alarma, en el siguiente 
        orden: (nombre,sonido,asunto,minuto,diasActiva,prendida), una vez creada dicha 
        tupla, la retornara

        Returns (Devoluciones):
              Una tupla que contiene todos los atributos de la alarma, en el siguiente 
              orden: (nombre,sonido,asunto,minuto,diasActiva,prendida)
        """
        
        alarmaTupla=[self.id,self.nombre,self.sonido,self.asunto,self.horaAlarma.hora,self.horaAlarma.minuto]+self.diasActiva+[self.prendida]      
        if not(conId):
            alarmaTupla=alarmaTupla[1:]

        alarmaTupla=tuple(alarmaTupla)
        return alarmaTupla

    def __str__(self):
        """
        Definira lo que se debe imprimir cuando se mande imprimir la instancia de la clase, 
        el formato que seguira sera el siguiente:
            self.hora (self.asunto)
            self.nombre,self.getDias() 
                ejemplo 1:
                    9:36 pm (1) alarma1: lunes,martes,merccoles
                ejemplo 2:
                    7:00 am (2) alarTare: sabado,domingo  
        
        Returns (Devoluciones):
            Una 'string' respetando el formato previamente mencionado.
        """
        
        return f"{self.horaAlarma}({self.asunto}), {self.nombre}: {self.getDias()}"