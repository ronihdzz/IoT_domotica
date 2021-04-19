class HoraAlarma():
    """Esta clase permite establecer la hora de una alarma,
    su presicion son los minutos, es decir las instancias de 
    la clase 'HoraAlarma' solo pueden ser expresadas con 
    horas y minutos.Tambien permite operaciones de operadores
    logicos entre instancias de la misma clase."""


    def __init__(self,hora,minuto):
        """El metodo constructor necesita forsozamente dos parametros,el dato de hora
        y el dato de minuto,ya que la clase HoraAlarma crea objetos de 'HoraAlarma' 
        con una prescion de minutos, es decir para estos objetos no hay segundos. """
        self.hora=hora
        self.minuto=minuto

    def __str__(self):
        """Returnara un string que contenga la hora en el formato
        de 'sistema horario de 12 horas(ocupando AM PM)' """
        
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
        '''Retornara el numero total de minutos a los que equivale
        la 'HoraAlarma', es decir convierte las horas a minutos y 
        las suma con los minutos.
        '''
        return  (  (self.hora*60) + self.minuto  )

    def __lt__(self,otro):
        '''Con esto permito que los objetos de mi clase 'HoraAlarma'
        sean capaces de atender operadores logicos, siendo mas especifico
        que sepa que hacer cuando le pidan reaccionar ante el operador 
        logico: '<' (menor que), ¿es mi instancia menor que el otro?,
        returnara una variable booleana en función de si la condición es
        verdadera o falsa
        '''
        return self.getMinutos() < otro.getMinutos()

    def __gt__(self,otro):
        '''Con esto permito que los objetos de mi clase 'HoraAlarma'
        sean capaces de atender operadores logicos, siendo mas especifico
        que sepa que hacer cuando le pidan reaccionar ante el operador 
        logico: '>' (mayor que), ¿es mi instancia mayor que el otro?,
        returnara una variable booleana en función de si la condición es
        verdadera o falsa
        '''
        return self.getMinutos() > otro.getMinutos()

    def __le__(self,otro):
        '''Con esto permito que los objetos de mi clase 'HoraAlarma'
        sean capaces de atender operadores logicos, siendo mas especifico
        que sepa que hacer cuando le pidan reaccionar ante el operador 
        logico: '<=' (menor o igual que), ¿es mi instancia menor o igual que el otro?,
        returnara una variable booleana en función de si la condición es
        verdadera o falsa
        '''
        return self.getMinutos() <= otro.getMinutos()

    def __ge__(self, otro):
        '''Con esto permito que los objetos de mi clase 'HoraAlarma'
        sean capaces de atender operadores logicos, siendo mas especifico
        que sepa que hacer cuando le pidan reaccionar ante el operador 
        logico: '>=' (mayor o igual que), ¿es mi instancia maoyor o igual que el otro?,
        returnara una variable booleana en función de si la condición es
        verdadera o falsa
        '''
        return self.getMinutos() >= otro.getMinutos()

    def __eq__(self, otro):
        '''Con esto permito que los objetos de mi clase 'HoraAlarma'
        sean capaces de atender operadores logicos, siendo mas especifico
        que sepa que hacer cuando le pidan reaccionar ante el operador 
        logico: '==' (igual que ), ¿es mi instancia igual que el otro?,
        returnara una variable booleana en función de si la condición es
        verdadera o falsa
        '''
        return self.getMinutos() == otro.getMinutos()


class Alarma():
    DIAS_SEMANA=("lunes","martes","miercoles","jueves","viernes","sabado","domingo")

    def __init__(self,nombre="",sonido="",asunto=0,hora=0,minuto=0,diasActiva=[0,0,0,0,0,0,0],prendida=1):
        self.nombre=nombre
        self.asunto=asunto
        self.diasActiva=diasActiva
        self.prendida=prendida
        self.sonido=sonido
        self.horaAlarma=HoraAlarma(hora,minuto)
    
    @staticmethod
    def tupla_toAlarma(tuplaDatos):
        """Retorna una instancia de alarma, apartir de una tupla de datos, es decir
        funciona casi igual que el metodo constructor, la unica diferencia es que en
        el metodo constructor solicita 7 parametros, y esta funcion solicita 1 parametro
        el cual es una tupla, pero una tupla con  7 elementos en el mismo orden
        que aparecen en el metodo constructor es decir
        (nombre,sonido,asunto,minuto,diasActiva,prendida).Este metodo hace lo inverso
        que el metodo 'to_tupla(self)', pues apartir de una tupla retorna una instancia de 
        la clase 'Alarma' """

        nombre=tuplaDatos[0]
        sonido=tuplaDatos[1]
        asunto=tuplaDatos[2]
        hora=tuplaDatos[3]
        minuto=tuplaDatos[4]
        diasActiva=tuplaDatos[5:-1]
        prendida=tuplaDatos[-1]

        alarma=Alarma(nombre=nombre,sonido=sonido, asunto=asunto,hora=hora,minuto=minuto,
            diasActiva=diasActiva,prendida=prendida)

        return alarma        
    
    def getDias(self):
        """Retorna un string con los nombres de los dias de la semana cada 
        uno separado con una coma."""
        nombreDias=[]
        for c,diaRequerido in enumerate(self.diasActiva):
            if diaRequerido:
                nombreDias.append(  self.DIAS_SEMANA[c]     )
        return  ",".join(nombreDias)
    
    def to_tupla(self):
        """Retorna una tupla que contiene todos los atributos de la alarma, 
        en el siguiente orden: (nombre,sonido,asunto,minuto,diasActiva,prendida)"""

        alarmaTupla=[self.nombre,self.sonido,self.asunto,self.horaAlarma.hora,self.horaAlarma.minuto]+self.diasActiva+[self.prendida] 
        alarmaTupla=tuple(alarmaTupla)
        return alarmaTupla

    def __str__(self):
        """La forma de imprimir las instancias de alarmas es la siguiente:
        hora (asunto)
        nombre,dias que suena
            ejemplo 1:
                9:36 pm (1) alarma1: lunes,martes,merccoles
            ejemplo 2:
                7:00 am (2) alarTare: sabado,domingo  
        """
        return f"{self.horaAlarma}({self.asunto}), {self.nombre}: {self.getDias()}"