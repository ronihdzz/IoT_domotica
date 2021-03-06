from PyQt5.QtWidgets import  QDialog,QApplication
from PyQt5 import QtWidgets

###############################################################
#  IMPORTACION DEL DISEÑO...
##############################################################
from CUERPO.DISENO.main_dise import Ui_Form

###############################################################
#  MIS LIBRERIAS...
##############################################################


class Main_IoT(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        Ui_Form.__init__(self)
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = Main_IoT()
    application.show()
    app.exec()
    #sys.exit(app.exec())
