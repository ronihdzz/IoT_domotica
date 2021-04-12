
import sys
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication,QSpinBox,QActionGroup,QLabel,QWidget,QPushButton, QVBoxLayout,QScrollArea,QMessageBox
from PyQt5.QtGui import QIcon,QFont

from PyQt5.Qt import QSizePolicy,Qt
import IMAG_rc



###############################################################
#  IMPORTACION DEL DISEÑO...
##############################################################


###############################################################
#  MIS LIBRERIAS...
##############################################################
from CUERPO.LOGICA.DEBERES.itemDeber import ItemDeber
from CUERPO.LOGICA.recursos import Recursos_IoT_Domotica

class SeccionNotas(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.ESTADO_ALINEO=0   #0=IZQUIERDA, 1=CENTRO, 2=DERECHA
        self.TAMANO_LETRA=12




        self.MAX_ITEMS=20
        self.punteroNoItems=0
        self.contadorIdsVivosMuertos = 0



        #self.btn_agregarItem.clicked.connect(partial(self.agregarAlarma,Alarma()))
        self.listaItemsRonianos=[]
        self.textPregunta=""
        self.listIdsItemsVivos=[]
        self.listPunterosItems=[]
        


        #Creando las accciones que ayudaran a alinear el texto
        alineacion_izquierda = QAction(QIcon(":/ICON/IMAGENES/izquierda.png"), 'Izquierda', self)
        alineacion_centro= QAction(QIcon(":/ICON/IMAGENES/centrado.png"), 'Centrado', self)
        alineacion_derecha= QAction(QIcon(":/ICON/IMAGENES/derecha.png"), 'Derecha', self)

        #habilitandolos para que puedan ser seleccionados
        alineacion_izquierda.setCheckable(True)
        alineacion_centro.setCheckable(True)
        alineacion_derecha.setCheckable(True)

        #Agrupando ciertas acciones para unicamente permitir la seleccion de una de ellas
        self.grupo_alineadores = QActionGroup(self)
        self.grupo_alineadores.addAction(alineacion_izquierda)
        self.grupo_alineadores.addAction(alineacion_centro)
        self.grupo_alineadores.addAction(alineacion_derecha)
  

        #exitAct.setShortcut('Ctrl+Q')
        #exitAct.setStatusTip('Exit application')
        #exitAct.triggered.connect(self.close)

        self.statusBar() 
        toolbar = self.addToolBar('Menu')
        toolbar.setMovable(False)

        toolbar.addWidget(self.get_expansorWidget() )    
        toolbar.addAction(alineacion_izquierda)
        toolbar.addSeparator()
        toolbar.addWidget( self.get_separadorQAction() )

        toolbar.addAction(alineacion_centro)
        toolbar.addSeparator()
        toolbar.addWidget( self.get_separadorQAction() )

        toolbar.addAction(alineacion_derecha)
        toolbar.addSeparator()
        toolbar.addWidget( self.get_separadorQAction() )

        self.spinBox_tam= QSpinBox()
        toolbar.addWidget(self.spinBox_tam)
        self.spinBox_tam.setMinimumSize(60,30)
        self.spinBox_tam.setFont(QFont('Arial', 12))
        toolbar.addWidget( self.get_separadorQAction() )


        #toolbar.addWidget(self.get_expansorWidget() )  
        self.btnAgregarItem=QPushButton()
        self.btnAgregarItem.setStyleSheet("""
            QPushButton {
                border-image: url(:/ICON/IMAGENES/plus_off.png);
            }
            QPushButton:hover {
                border-image: url(:/ICON/IMAGENES/plus_on.png);
            }
            QPushButton:pressed {
                border-image: url(:/ICON/IMAGENES/plus_off.png);
            }   
        """)
        self.btnAgregarItem.setMinimumSize(30,30)
        toolbar.addWidget(self.btnAgregarItem)
        toolbar.addWidget( self.get_separadorQAction() )



        #toolbar.addWidget(self.get_expansorWidget() )  

        self.setGeometry(300, 300, 350, 250)
        #self.setWindowTitle('Main window')
        self.show()



        

        # adding triggered action to the first action
        alineacion_derecha.triggered.connect( lambda x : self.alinear(2) )
        alineacion_centro.triggered.connect( lambda x : self.alinear(1)  )
        alineacion_izquierda.triggered.connect(lambda x : self.alinear(0)  )


        self.btnAgregarItem.clicked.connect(lambda : self.agregarNuevoItem("") )

        self.spinBox_tam.valueChanged.connect(self.cambiarTamano_letra)


        self.scroll = QScrollArea()     # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()         # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()       # The Vertical Box that contains the Horizontal Boxes of  labels and buttons


        #self.vbox.addWidget(object)
        
        
        self.widget.setLayout(self.vbox)

        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.setCentralWidget(self.scroll)


        alineacion_izquierda.trigger()
        self.spinBox_tam.setValue(self.TAMANO_LETRA)
        self.spinBox_tam.setMinimum(4)
        self.spinBox_tam.setMaximum(18)
        toolbar.setContentsMargins(0,5,0,0) #arriba,abajo,izquierda,derecha

        self.cargarDeberes()

        
    

    def alinear(self,idAlineo):
        self.ESTADO_ALINEO=idAlineo
        for item in self.listPunterosItems:
            item.alinear(self.ESTADO_ALINEO)        
                
    def cargarDeberes(self):
        datos=""
        try:
            with open(Recursos_IoT_Domotica.ARCHIVO_DEBERES,'r') as archivoDeberes:
                datos=archivoDeberes.read()
        except FileNotFoundError:
            pass

        listaDeberes=datos.split(Recursos_IoT_Domotica.SEPARADOR_DEBERES)
        if listaDeberes==[]:
            pass


    def agregarNuevoItem(self,textoDeber):
        if self.punteroNoItems<self.MAX_ITEMS:
            itemDeber=ItemDeber(id=self.contadorIdsVivosMuertos,texto=textoDeber,idAlineacion=self.ESTADO_ALINEO,
            tamanoLetra=self.TAMANO_LETRA)
            itemDeber.senal_deberCumplido.connect(self.borrarItem)

            self.listIdsItemsVivos.append(self.contadorIdsVivosMuertos)
            self.listPunterosItems.append(itemDeber)
            self.vbox.addWidget(itemDeber)
            self.punteroNoItems+=1
            self.contadorIdsVivosMuertos+=1

        else:
            QMessageBox.question(self, "DelphiPreguntas",
                                 "El numero maximo de items es de:\n"
                                 f"{self.MAX_ITEMS} items, y usted ya ha llegado\n"
                                 "a dicho limite.",
                                 QMessageBox.Ok)


    def borrarItem(self,id):
        idItemAMatar=id

        posItemMatar=self.listIdsItemsVivos.index(idItemAMatar)
        layout=self.vbox
        noWidgetBorrar=posItemMatar
        widgetToRemove = layout.itemAt(noWidgetBorrar).widget()
        # remove it from the layout list
        layout.removeWidget(widgetToRemove)
        # remove it from the gui
        widgetToRemove.setParent(None)

        #self.listaItemsRonianos.pop(posItemMatar)
        self.listIdsItemsVivos.pop(posItemMatar)
        self.listPunterosItems.pop(posItemMatar)
        self.punteroNoItems -= 1

    def get_separadorQAction(self):
        separadorQAction=QLabel()
        separadorQAction.setMinimumSize(10,2)
        return separadorQAction

    def get_expansorWidget(self):
        expansorWidget=QWidget()
        expansorWidget.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        return expansorWidget

    def cambiarTamano_letra(self,nuevoValor):
        self.TAMANO_LETRA=nuevoValor
        for item in self.listPunterosItems:
            item.cambiarTamano(nuevoValor)





def main():
    app = QApplication(sys.argv)
    ex = SeccionNotas()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()