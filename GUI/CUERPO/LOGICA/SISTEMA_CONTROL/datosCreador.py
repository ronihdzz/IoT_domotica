from PyQt5.QtWidgets import  QDialog,QApplication
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMessageBox,QButtonGroup,QDialog)
from PyQt5.QtCore import Qt, pyqtSignal,QObject

###############################################################
#  IMPORTACION DEL DISEÑO...
##############################################################
from  CUERPO.DISENO.SISTEMA_CONTROL.datosCreador_dise import Ui_Dialog
###############################################################
#  MIS LIBRERIAS...
##############################################################


class Dialog_datosCreador(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        Ui_Dialog.__init__(self)
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)

        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        self.setWindowTitle(" ")
        self.setWindowModality(Qt.ApplicationModal)

        nombre="Roni Hernández"
        gmail="ronaldo.runing.r@gmail.com"
        likedin=" Roni Hernández "
        github="RoniHernandez99"
        repositorio="IoT_domotica"

        likedin_link="https://www.linkedin.com/in/roni-hern%C3%A1ndez-613a62173/"
        github_link="https://github.com/RoniHernandez99"
        repositorio_link="https://github.com/RoniHernandez99"

        datosCreador=f"""
        <h1>Programador:{nombre}<\h1>
        <h1 style="text-align:center" > < img src=":/SISTEMA_CONTROL/IMAGENES/SISTEMA_CONTROL/yoMero.jpg" /> </h1>
        <h3>Gmail:{gmail}<\h3>
        <h3>Liked in: <a href="{likedin_link}">{likedin}</a> <\h3>
        <h3>Github: <a href="{github_link}">{github}</a><\h3>
        <h3>Repositorio de todo el proyecto: <a href="{repositorio_link}">{repositorio}</a><\h3> """
        self.textBrowser_datosCreador.setHtml(datosCreador)

        self.textBrowser_datosCreador.setOpenLinks(True)
        self.textBrowser_datosCreador.setOpenExternalLinks(True)
        #self.textBrowser_datosCreador.setOpenLinks(False)
        #self.textBrowser_datosCreador.anchorClicked.connect(self.test)

    def test(self,argv_1):
        print(argv_1)
        print('!!!')

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = Dialog_datosCreador()
    application.show()
    app.exec()
    #sys.exit(app.exec())
