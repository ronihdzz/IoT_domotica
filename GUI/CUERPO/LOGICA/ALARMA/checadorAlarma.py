from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore

###############################################################
#  MIS LIBRERIAS...
##############################################################
from CUERPO.LOGICA.ALARMA.alarma import Alarma,HoraAlarma
from CUERPO.LOGICA.ALARMA.baseDatos_alarma import BaseDatos_alarmas
from CUERPO.LOGICA.recursos import Recursos_IoT_Domotica

'''
Ordenar alarmas por hora...
Ordenar alarmas por minuto...

Las alarmas que coincidan en el mismo
minuto y hora, se avisaran al mismo 
tiempo...



'''

class ChecadorAlarma(QtCore.QObject):
    senal_alarmaDetectada=pyqtSignal(list)


    def __init__(self,noDiaHoy,hora,minuto):
        QtCore.QObject.__init__(self)
        self.punteroMinuto=minuto
        self.punteroHora=hora
        self.punteroDia=noDiaHoy

        

        self.dictAlarmas={}
        #{nombre:[hora,]}

        self.baseDatosAlarmas=BaseDatos_alarmas(Recursos_IoT_Domotica.NOMBRE_BASE_DATOS_ALARMAS)

        self.actualizarAlarmasHoy(noDiaHoy,hora,minuto)




    def revisar(self,hora,minuto):
        #Este metodo debe llamarse minimo cada minuto

        print(f"""
REVISION
TIEMPO:  {hora},{minuto}
ALARMAS: , {self.dictAlarmas} 
        """)

        listAlar_yaDebenSonar=[]

        self.punteroMinuto=minuto
        self.punteroHora=hora

        tiempoActual=HoraAlarma(hora,minuto)
        for nombreAlarma,horaSonar in self.dictAlarmas.items():
            print(f"{horaSonar}  <= {tiempoActual}")
            if horaSonar<=tiempoActual:
                listAlar_yaDebenSonar.append(  (nombreAlarma,horaSonar)  )
            else:
                break
        
        if listAlar_yaDebenSonar!=[]:
            self.senal_alarmaDetectada.emit( listAlar_yaDebenSonar )
            for nombreAlarma,_ in listAlar_yaDebenSonar:
                del self.dictAlarmas[nombreAlarma]
            #print(listAlar_yaDebenSonar)


    def actuarAnte_eliminacionUnaAlarma(self,nombreAlarma):
        if nombreAlarma in self.dictAlarmas:
            del self.dictAlarmas[nombreAlarma]

    def actuarAnte_edicionUnaAlarma(self,alarma):
        alarma=alarma[0]
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
        alarma=alarma[0]
        if alarma.diasActiva[self.punteroDia]:
            if alarma.horaAlarma>HoraAlarma(self.punteroHora,self.punteroMinuto):
                    self.dictAlarmas[alarma.nombre]=alarma.horaAlarma
                    #ordenando de forma ascendente las horas de las alarmas
                    self.dictAlarmas=dict( sorted(self.dictAlarmas.items(),key=lambda x: x[1], reverse=False ) )


        

    def actualizarAlarmasHoy(self,noDiaHoy,hora,minuto):
        #noDiasHoy= 1:'LUNES',2:'MARTES',3:'MIERCOLES',4:'JUEVES',5:'VIERNES',
        # 6:'SABADO',7:'DOMINGO'

        #obteniendo el diccionario de las horas de alarmas en donde
        #su llave es su nombre y su valor es su hora

        self.punteroDia=noDiaHoy
        self.punteroHora=hora
        self.punteroMinuto=minuto


        self.dictAlarmas=self.baseDatosAlarmas.getDictHoraAlarmas(noDiaHoy,self.punteroHora,self.punteroMinuto)
        print("Dia de hoy:",noDiaHoy)
        print("INFO ALARMAS EN COLOA:",self.dictAlarmas)



            
            
