from PyQt5 import QtWidgets,Qt
from PyQt5.QtWidgets import QWidget,QVBoxLayout
from PyQt5.QtWidgets import  QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal,QTimer

###############################################################
#  IMPORTACION DEL DISEÑO...
##############################################################
from CUERPO.DISENO.ALARMA.administradorAlarmas_dise import  Ui_Form 

###############################################################
#  MIS LIBRERIAS...
##############################################################
from CUERPO.LOGICA.ALARMA.ItemAlarmaVista import ItemAlarmaVista
from CUERPO.LOGICA.ALARMA.ItemAlarmaEdit import ItemAlarmaEdit
from CUERPO.LOGICA.ALARMA.baseDatos_alarma import BaseDatos_alarmas
from CUERPO.LOGICA.RECURSOS.recursos import Recursos_IoT_Domotica
from CUERPO.LOGICA.ALARMA.reloj import Reloj
from CUERPO.LOGICA.ALARMA.notificadorAlarmas import NotificadorAlarmas
from CUERPO.LOGICA.ALARMA.checadorAlarma import ChecadorAlarma

class AdministradorAlarmas(QtWidgets.QWidget,Ui_Form):

    def __init__(self,noDia,hora,minuto,segundo):
        Ui_Form.__init__(self)
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)

        self.baseDatosAlarmas=BaseDatos_alarmas(Recursos_IoT_Domotica.NOMBRE_BASE_DATOS_ALARMAS)
        self.baseDatosAlarmas.crearBaseDatos()
        self.ventanaCreadoraAlarmas=ItemAlarmaEdit()

    

        self.widget = QWidget()  # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()  # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        self.widget.setLayout(self.vbox)

        #Scroll Area Properties
        self.scroll_alarmas.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_alarmas.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_alarmas.setWidgetResizable(True)
        self.scroll_alarmas.setWidget(self.widget)
        self.MAX_ITEMS=20
        self.punteroNoItems=0
        self.contadorIdsVivosMuertos = 0


        #self.btn_agregarItem.clicked.connect(partial(self.agregarAlarma,Alarma()))
        self.btn_agregarItem.clicked.connect(self.crearUnaAlarma)
        self.listaItemsRonianos=[]
        self.textPregunta=""
        self.listIdsItemsVivos=[]


        self.prepararSincronizaciones(noDia,hora,minuto,segundo)

        self.cargarAlarmas()
        self.ventanaCreadoraAlarmas.senal_alarmaCreada.connect(self.nuevaAlarmaCreada)



#######################################################################################################################3
# REVISANDO   LAS     ALARMAS
#######################################################################################################################3
    def prepararSincronizaciones(self,noDia,hora,minuto,segundo):

        self.checadorAlarma=ChecadorAlarma(noDia, hora, minuto )
        self.reloj=Reloj(noDia,hora,minuto,segundo)

        self.avisador=NotificadorAlarmas()    
        self.reloj.senal_minutoCambio.connect(self.consultarChecadorAlarmas)
        self.reloj.senal_diaCambio.connect(self.renovarAlarmas )


        self.checadorAlarma.senal_alarmaDetectada.connect( self.avisador.activarAlarmas )
        self.avisador.senal_alarmaSonando.connect( self.mostrarAvisadorAlarmas )

        
        self.contador=QTimer()
        self.contador.timeout.connect(self.clockContador)
        # Call start() method to modify the timer value
        self.contador.start(10)


    def mostrarAvisadorAlarmas(self):
        self.avisador.show()

    def renovarAlarmas(self,listaDatos):
        print("SOLCITANDO RENOVACION...")
        #listaDatos[0]=dia   listaDatos[1]=hora   listaDatos[2]=minutos
        self.checadorAlarma.actualizarAlarmasHoy( listaDatos[0],listaDatos[1],listaDatos[2] )

    def consultarChecadorAlarmas(self,listaDatos):
        #listaDatos[0]=dia   listaDatos[1]=hora   listaDatos[2]=minutos
        self.checadorAlarma.revisar(listaDatos[1],listaDatos[2])


    def clockContador(self):
         #self.hora=self.hora.addSecs(1)
         #self.timeEdit_tiempo.addSecs(1)
         #self.timeEdit_tiempo.setTime(self.hora)
         self.reloj.clock()


    def cargarAlarmas(self):
        listaAlarmas=self.baseDatosAlarmas.getTodas_alarmas()
        #(   ('Julian', 1, 9, 30, 1, 1, 1, 0, 0, 0, 0, 0), ....   )
        
        for alarma in listaAlarmas:
            self.agregarAlarma(alarma=alarma)


    def crearUnaAlarma(self):
        self.ventanaCreadoraAlarmas.modoTrabajo(modoEdicion=False)
        self.ventanaCreadoraAlarmas.show()

    def nuevaAlarmaCreada(self,alarma):
        #print(alarma[0])
        #print(type(alarma[0]))
        #self.senal_creoUnaAlarma.emit(alarma)
    
        alarma=alarma[0]

        self.checadorAlarma.actuarAnte_anexionAlarma(alarma)
        self.agregarAlarma(alarma)


    def notificarEdicionUnaAlarma(self,alarma):
        #self.senal_editoUnaAlarma.emit(alarma)
        self.checadorAlarma.actuarAnte_edicionUnaAlarma( alarma[0] )

    def agregarAlarma(self,alarma):
        if self.punteroNoItems<self.MAX_ITEMS:
            itemAlarma=ItemAlarmaVista(id=self.contadorIdsVivosMuertos)
            itemAlarma.cargarAlarma(alarma)
            itemAlarma.suHoraMorir.connect(self.borrarItem)
            itemAlarma.senal_alarmaEditada.connect(self.notificarEdicionUnaAlarma)
            self.listIdsItemsVivos.append(self.contadorIdsVivosMuertos)

            self.vbox.addWidget(itemAlarma)
            self.punteroNoItems+=1
            self.contadorIdsVivosMuertos+=1
        else:
            mensaje="El numero maximo de alarmas que\n"
            mensaje+=f"puedes registrar es de: {self.MAX_ITEMS} alarmas\n"  
            mensaje+=f"y usted ya ha creado {self.MAX_ITEMS} alarmas."
            ventanaDialogo = QMessageBox()
            ventanaDialogo.setIcon(QMessageBox.Information)
            ventanaDialogo.setWindowTitle('Error')
            ventanaDialogo.setText(mensaje)
            ventanaDialogo.setStandardButtons(QMessageBox.Ok)
            btn_ok = ventanaDialogo.button(QMessageBox.Ok)
            btn_ok.setText('Entendido')
            ventanaDialogo.exec_()



    def borrarItem(self,listaIdIs_itemAMatar):
        print("BORRAR: ",listaIdIs_itemAMatar)
        idItemAMatar=listaIdIs_itemAMatar[0] #id en el orden las widget
        nombreAlarma=listaIdIs_itemAMatar[1] #id en la base de datos

        posItemMatar=self.listIdsItemsVivos.index(idItemAMatar)

        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Question)
        ventanaDialogo.setWindowTitle('Salir')
        mensaje="¿Esta seguro que quieres\n" 
        mensaje+=f"eliminar la alarma numero: {posItemMatar+1}\n"
        mensaje+=f" cuyo nombre es: {nombreAlarma}?"
        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        btn_yes = ventanaDialogo.button(QMessageBox.Yes)
        btn_yes.setText('Si')
        btn_no = ventanaDialogo.button(QMessageBox.No)
        btn_no.setText('No')
        ventanaDialogo.exec_()
        if ventanaDialogo.clickedButton()  ==  btn_yes:
            layout=self.vbox
            noWidgetBorrar=posItemMatar
            widgetToRemove = layout.itemAt(noWidgetBorrar).widget()
            # remove it from the layout list
            layout.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.setParent(None)

            #self.listaItemsRonianos.pop(posItemMatar)
            self.listIdsItemsVivos.pop(posItemMatar)
            self.punteroNoItems -= 1

            self.baseDatosAlarmas.eliminar(nombreAlarma=nombreAlarma)
            #self.senal_eliminoUnaAlarma.emit(nombreAlarma)
            self.checadorAlarma.actuarAnte_eliminacionUnaAlarma(nombreAlarma)
            
    def closeEvent(self, event):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = AdministradorAlarmas(1,10,20,0)
    application.show()
    app.exec()

    ##sys.exit(app.exec())


