from PyQt5.QtWidgets import  QDialog,QApplication
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from functools import partial
from PyQt5.QtCore import Qt, pyqtSignal,QObject
from PyQt5.QtGui import QIcon
###############################################################
#  IMPORTACION DEL DISEÑO...
##############################################################
from  CUERPO.DISENO.SISTEMA_CONTROL.configLed_dise import Ui_Dialog
from recursos import HuellaAplicacion

###############################################################
#  MIS LIBRERIAS...
##############################################################


class Dialog_configLed(QtWidgets.QDialog, Ui_Dialog,HuellaAplicacion):
    senal_colorElegido= pyqtSignal(int)

    RUTA=":/SISTEMA_CONTROL/IMAGENES/SISTEMA_CONTROL/"
    TUPLA_IMAGENES=(
        ( ("foco1_blanco.png"),("rueda1_blanco.png") ),
        ( ("foco2_rojo.png"),("rueda2_rojo.png") ),
        ( ("foco3_verde.png"),("rueda3_verde.png") ),
        ( ("foco4_azul.png"),("rueda4_azul.png") ),
        ( ("foco5_amarillo.png"),("rueda5_amarillo.png") ),
        ( ("foco6_magenta.png"),("rueda6_magenta.png") ),
        ( ("foco7_cian.png"),("rueda7_cian.png") )
    )

    IMAGEN_RUEDA=""
    IMAGEN_RUEDA_GRANDE=""
    IMAGEN_FOCO_ON=""
    
    IMAGEN_FOCO_OFF=RUTA+"foco0c_default"

    #COLORES_RGB=( 
    #"(255,255,255)",#blanco
    #"(255,0,0)",#rojo
    #"(0,255,0)",#verde
    #"(0,0,255)",#azul
    #"(255,255,0)",#amarillo
    #"(255,0,255)",#magenta
    #"(0,255,255)"#cian
    #)



    def __init__(self):
        Ui_Dialog.__init__(self)
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        HuellaAplicacion.__init__(self)

        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.ApplicationModal)

        self.bel_aplicarColor.mouseReleaseEvent=lambda eve : self.guardarColor(self.idPorConfirmar)
        
        self.tuplaBotones=(self.btn_0,self.btn_1,self.btn_2,self.btn_3,self.btn_4,self.btn_5,self.btn_6)
        for n in range(len(self.tuplaBotones)):
            self.tuplaBotones[n].clicked.connect(partial(self.eligioColor,n))

        self.idColorFoco=0
        self.idPorConfirmar=0
    
    def eligioColor(self,idColor):
        self.idPorConfirmar=idColor
        self.bel_colorFoco.setStyleSheet(f"border-image:url({ self.RUTA+self.TUPLA_IMAGENES[idColor][0] });")
    
    def guardarColor(self,idColor):
        #CONVENCIO DE COLORES USADAS EN ARDUINO...
        # 0-blanco
        # 1-rojo
        # 2-verde
        # 3-azul
        # 4-amarillo
        # 5-magenta
        # 6-cian

        self.cambiarImagen(idColor)
        self.idColorFoco=idColor
        self.senal_colorElegido.emit(idColor)
          
        self.close()

    def cambiarImagen(self,idColor):
        self.IMAGEN_FOCO_ON=self.RUTA+self.TUPLA_IMAGENES[idColor][0]
        self.IMAGEN_RUEDA=self.RUTA+self.TUPLA_IMAGENES[idColor][1]
        # las imagenes con zoom del foco se tienen un 'r' mas al inicio de su nombre
        self.IMAGEN_RUEDA_GRANDE=self.RUTA+"r"+self.TUPLA_IMAGENES[idColor][1] 

    def closeEvent(self,event):
        #por si se sale de la pantalla solo moviendo los diferentes colores pero no eligiendo ninguno
        self.eligioColor(self.idColorFoco)
    
    def getImagenFoco_on(self):
        return self.IMAGEN_FOCO_ON
    
    def getImagenFoco_off(self):
        return self.IMAGEN_FOCO_OFF
    
    def getImagen_ruedaGrande(self):
        return self.IMAGEN_RUEDA_GRANDE
    
    def getImagen_ruedaChica(self):
        return self.IMAGEN_RUEDA


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = Dialog_configLed()
    application.show()
    app.exec()
    #sys.exit(app.exec())
