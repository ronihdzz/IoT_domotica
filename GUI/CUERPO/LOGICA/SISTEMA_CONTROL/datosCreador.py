from PyQt5.QtWidgets import  QDialog,QApplication
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMessageBox,QButtonGroup,QDialog)
from PyQt5.QtCore import Qt, pyqtSignal,QObject
from PyQt5.QtGui import QIcon

###############################################################
#  IMPORTACION DEL DISEÑO...
##############################################################
from  CUERPO.DISENO.SISTEMA_CONTROL.datosCreador_dise import Ui_Dialog
###############################################################
#  MIS LIBRERIAS...
##############################################################
from recursos import HuellaAplicacion

class Dialog_datosCreador(QtWidgets.QDialog, Ui_Dialog,HuellaAplicacion):
    def __init__(self):
        Ui_Dialog.__init__(self)
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.ApplicationModal)
        HuellaAplicacion.__init__(self)

        nombre="Roni Hernández"
        gmail="ronaldo.runing.r@gmail.com"
        likedin=" Roni Hernández "
        github="RoniHernandez99"
        repositorio="IoT_domotica"
        fotoProgramador=":/SISTEMA_CONTROL/IMAGENES/SISTEMA_CONTROL/yoMero2.jpg"


        likedin_link="https://www.linkedin.com/in/roni-hern%C3%A1ndez-613a62173/"
        github_link="https://github.com/RoniHernandez99"
        repositorio_link="https://github.com/RoniHernandez99"


        likedin_html=f'<span style=" font-size:13px;font-family:TamilSangamMN;"><a href="{likedin_link}" style="color:black;text-decoration:none;">{likedin}</a></span>'
        github_html=f'<span style=" font-size:13px;font-family:TamilSangamMN;"><a href="{github_link}" style="color:black;text-decoration:none;">{github}</a></span>'

        self.textBrowser_repositorio.setOpenLinks(True)
        self.textBrowser_repositorio.setOpenExternalLinks(True)


        self.bel_gmail.setTextInteractionFlags(Qt.TextSelectableByMouse)

        #self.textBrowser_nombreProgra.setOpenLinks(True)
        #self.textBrowser_nombreProgra.setOpenExternalLinks(True)

        self.textBrowser_repositorio.setHtml(f"""
            <span style=" font-size:13px;font-family: TamilSangamMN;">Repositorio de todo el proyecto</span></p>
            <span style=" font-size:13px;font-family: TamilSangamMN;"><a href="{repositorio_link}"  style="color:black;"> <b>{repositorio}<\b> </a></span>
        """)

        self.textBrowser_nombreProgra.setHtml(f"""
        <p align="center"><span style="font-size:13px; font-family:TamilSangamMN; style='text-align:center">Desarrollador</span>
        <br>
        <span style="font-size:16px;font-family: TamilSangamMN;text-align:center;"><b>{nombre}</b></span>
        </p>""")

        self.bel_fotoProgramador.setStyleSheet(f"""
                    border-image: url({fotoProgramador});
                    border-radius:87%;""")
        


        self.bel_likedin.setText(likedin_html)
        self.bel_github.setText(github_html)
        self.bel_gmail.setText(gmail)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = Dialog_datosCreador()
    application.show()
    app.exec()
    #sys.exit(app.exec())
