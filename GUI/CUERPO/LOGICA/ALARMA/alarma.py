
class Alarma():
    DIAS_SEMANA=("lunes","martes","miercoles","jueves","viernes","sabado","domingo")


    def __init__(self,nombre="",sonido="",asunto=0,hora=0,minuto=0,diasActiva=[0,0,0,0,0,0,0],prendida=1):
        self.nombre=nombre
        self.asunto=asunto
        self.hora=hora
        self.minuto=minuto
        self.diasActiva=diasActiva
        self.prendida=prendida
        self.sonido=sonido
    
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

    def getHora_string(self):
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




    
    def to_tupla(self):
        alarmaTupla=[self.nombre,self.sonido,self.asunto,self.hora,self.minuto]+self.diasActiva+[self.prendida] 
        alarmaTupla=tuple(alarmaTupla)
        return alarmaTupla

    def __str__(self):
        return f"{self.hora}:{self.minuto}({self.asunto}), {self.nombre}: {self.getDias()}"
