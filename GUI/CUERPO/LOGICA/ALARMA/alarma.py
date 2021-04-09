
class HoraAlarma():
    
    def __init__(self,hora,minuto):
        self.hora=hora
        self.minuto=minuto

    
    def __str__(self):
        resultado=['0','0',':','0','0','am'] # hh:mm pm/am
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
        return  (  (self.hora*60) + self.minuto  )


    # mi instancia es menor que el otro
    def __lt__(self,otro):
        return self.getMinutos() < otro.getMinutos()

    # mi instancia es mayor que el otro
    def __gt__(self,otro):
        return self.getMinutos() > otro.getMinutos()

    # mi instancia es menor o igual que el otro
    def __le__(self,otro):
        return self.getMinutos() <= otro.getMinutos()

    # mi instancia es mayor o igual que el otro
    def __ge__(self, otro):
        return self.getMinutos() >= otro.getMinutos()

    # mi instancia es igual al otro
    def __eq__(self, otro):
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
        nombreDias=[]
        for c,diaRequerido in enumerate(self.diasActiva):
            if diaRequerido:
                nombreDias.append(  self.DIAS_SEMANA[c]     )
        return  ",".join(nombreDias)
    
    def to_tupla(self):
        alarmaTupla=[self.nombre,self.sonido,self.asunto,self.horaAlarma.hora,self.horaAlarma.minuto]+self.diasActiva+[self.prendida] 
        alarmaTupla=tuple(alarmaTupla)
        return alarmaTupla

    def __str__(self):
        return f"{self.horaAlarma.hora}:{self.horaAlarma.minuto}({self.asunto}), {self.nombre}: {self.getDias()}"


