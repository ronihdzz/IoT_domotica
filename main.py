from PyQt5.QtWidgets import  QDialog,QApplication
from PyQt5 import QtWidgets
from functools import partial

###############################################################
#  IMPORTACION DEL DISEÑO...
##############################################################
from CUERPO.DISENO.main_dise import Ui_Form
###############################################################
#  MIS LIBRERIAS...
##############################################################
from CUERPO.LOGICA.configLed import Dialog_configLed
from CUERPO.LOGICA.configVenti import Dialog_configVenti
from CUERPO.LOGICA.configAlarma import Dialog_configAlarma

class Main_IoT(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        Ui_Form.__init__(self)
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)

        self.venConfig_foco=Dialog_configLed()
        self.venConfig_venti=Dialog_configVenti()
        self.venConfig_alarma=Dialog_configAlarma()

        self.btn_configFoco.clicked.connect(self.configurarFoco)
        self.btn_configVenti.clicked.connect(self.configurarVenti)

        self.btn_configAlarm.clicked.connect(self.configurarAlarma)

    def configurarFoco(self):
        self.venConfig_foco.show()
    
    def configurarVenti(self):
        self.venConfig_venti.show()
    def configurarAlarma(self):
        self.venConfig_alarma.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = Main_IoT()
    application.show()
    app.exec()
    #sys.exit(app.exec())
