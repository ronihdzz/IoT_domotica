from PyQt5 import QtWidgets,Qt
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QPushButton,QGridLayout,QCheckBox,QTextEdit,QTimeEdit,QLabel


###########################################################################################################################################
# PRUEBA DE LA COORDINACION DE LAS ALARMAS
###########################################################################################################################################


#from CUERPO.LOGICA.ALARMA.SeccionAlarmas import SeccionAlarmas

#app = QtWidgets.QApplication([])
#application = SeccionAlarmas()
#application.show()
#app.exec()


###########################################################################################################################################
# PRUEBA DE LA BASE DE DATOS DE LAS ALARMAS
###########################################################################################################################################


from CUERPO.LOGICA.ALARMA.baseDatos_alarma import BaseDatos_alarmas
from CUERPO.LOGICA.ALARMA.alarma import Alarma
from CUERPO.LOGICA.recursos import Recursos_IoT_Domotica



baseDatosAlarmas=BaseDatos_alarmas(Recursos_IoT_Domotica.NOMBRE_BASE_DATOS_ALARMAS)
baseDatosAlarmas.crearBaseDatos()

#r=baseDatosAlarmas.getNombresAlarmasCon(cancion="SIN MUSICA")

#baseDatosAlarmas.eliminarCancion(cancionEliminar="RONI",
#cancionDefault=Recursos_IoT_Domotica.NOMBRE_SONIDO_NULL)

#roni.crearBaseDatos()

'''
#roni.addAlarma( Alarma(nombre="Roni",asunto=0,hora=0,minuto=0,diasActiva=[0,0,0,0,0,0,0],prendida=1) )
#roni.addAlarma( Alarma(nombre="Jorge",asunto=0,hora=0,minuto=0,diasActiva=[0,0,0,0,0,0,0],prendida=1) )
#roni.addAlarma( Alarma(nombre="Ariana",asunto=0,hora=0,minuto=0,diasActiva=[0,0,0,0,0,0,0],prendida=1) )
#roni.addAlarma( Alarma(nombre="Pedro",asunto=0,hora=0,minuto=0,diasActiva=[0,0,0,0,0,0,0],prendida=1) )

'''

