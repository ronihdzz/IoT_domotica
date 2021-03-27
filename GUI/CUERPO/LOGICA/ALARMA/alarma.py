
class Alarma():
    DIAS_SEMANA=("lunes","martes","miercoles","jueves","viernes","sabado","domingo")

    def __init__(self,nombre="",asunto=0,hora=0,minuto=0,diasActiva=[0,0,0,0,0,0,0],prendida=1):
        self.nombre=nombre
        self.asunto=asunto
        self.hora=hora
        self.minuto=minuto
        self.diasActiva=diasActiva
        self.prendida=prendida
    
    def getDias(self):
        nombreDias=[]
        for c,diaRequerido in enumerate(self.diasActiva):
            if diaRequerido:
                nombreDias.append(  self.DIAS_SEMANA[c]     )
        return  ",".join(nombreDias)
    
    def to_tupla(self):
        alarmaTupla=[self.nombre,self.asunto,self.hora,self.minuto]+self.diasActiva+[self.prendida] 
        alarmaTupla=tuple(alarmaTupla)
        return alarmaTupla

    def __str__(self):
        return f"{self.hora}:{self.minuto}({self.asunto}), {self.nombre}: {self.getDias()}"
