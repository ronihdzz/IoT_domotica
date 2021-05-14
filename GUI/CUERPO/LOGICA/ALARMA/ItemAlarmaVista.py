from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal,QTime
###############################################################
#  IMPORTACION DEL DISEÑO...
##############################################################
from CUERPO.DISENO.ALARMA.itemAlarmaVista_dise import Ui_Form

###############################################################
#  MIS LIBRERIAS...
##############################################################
from CUERPO.LOGICA.ALARMA.ItemAlarmaEdit import ItemAlarmaEdit


class ItemAlarmaVista(QtWidgets.QWidget,Ui_Form):
    '''
    El proposito de esta clase es crear  instancias de esta clase para
    que  muestren los datos de una alarma de forma visual, a traves de
    widgets, asi como proveer las herramientas para que el usuario pueda
    editar  o borrar una alarma en especifico y avisar cuando esto suceda

    '''

    suHoraMorir= pyqtSignal(list)#indicara quien es el objeto que quiere morir...
    #[id,nombre]

    senal_alarmaEditada=pyqtSignal(list)#indicara quien es el objeto que fue editado...
    #[id,nombre]

    senal_alarmaQuiereEdicion=pyqtSignal(str)#indicara el nombre de la  alarma que quiere ser editada...
    #nombreAlarma

    
    

    def __init__(self,id):
        '''El unico parametro que necesita el un id, el cual debe ser
        unico entre todos los objetos que se crean de esta clase, ya que
        con este se identificara cada alarma. '''

        Ui_Form.__init__(self)
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.btn_eliminar.clicked.connect(self.mandarSenalMuerto)
        self.id=id
        self.nombreAlarma=None
        
        self.btn_editar.clicked.connect(self.editar)
        self.textEdit_alarma.setReadOnly(True)
        self.hoSli_estado.valueChanged.connect(self.activarDesactivarAlarma)
        self.hoSli_estado.setValue(1)
        self.textEdit_alarma.setStyleSheet("border:1px solid #C4C8C0; border-radius:10%;")
    
    def cargarAlarma(self,alarma):
        '''
        Mostrara de forma visual los datos MAS RELEVANTES de la alarma
        en la widget.
        El parametro 'alarma' en una instancia de la clase 'Alarma', y
         dicha instancia contiene todos los datos de la alarma que se
         pretende mostrar.
        '''

        self.nombreAlarma=alarma.nombre
        horaAlarma=QTime()
        horaAlarma.setHMS(alarma.horaAlarma.hora,alarma.horaAlarma.minuto,0)
        horaAlarma=horaAlarma.toString("hh:mm")
        print("HORA:",horaAlarma)
        
        
        self.textEdit_alarma.setText("""<h2>{}  </h2>
        <h4>{}: {}</h4>
        """.format(alarma.horaAlarma,alarma.nombre,alarma.getDias() ) )
    
    def activarDesactivarAlarma(self):
        '''Este meotodo deshabilitara el 'textEdit_alarma' que contiene
        los datos de alarma, con el unico efecto que adquiera un efecto
        visual como de que si dicha alarma este desactivada. '''

        if self.hoSli_estado.value():
            self.textEdit_alarma.setEnabled(True)
        else:
            self.textEdit_alarma.setEnabled(False)

    def editar(self):
        '''Abrira el editor de alarma en modo de trabajo de edicion,
        lo cual significara que dicho editor cargara todos los datos
        de la alarma que se quiere editar.
        '''

        self.ventana=ItemAlarmaEdit()
        self.ventana.modoTrabajo(modoEdicion=True,nombreAlarma=self.nombreAlarma)
        self.ventana.senal_alarmaEditada.connect(self.alarmaEditada)
        self.ventana.senal_editorCreador_cerrado.connect(self.eliminar_cuadroDilogo)
        self.ventana.show()

    def alarmaEditada(self,alarma):
        '''Este metodo se llamara si es que la alarma que se queria editar, si fue
        editada, en tal caso se debe avisar que dicha alamar fue editada y eso es
        lo que hace este metodo mandando una senal que se encarga de avisar.

        Parametros:
            alarma -. Es una lista de un solo elemento que contiene la instancia
            de la clase Alarma, con todos los datos de la alarma que fue editada
        '''

        self.senal_alarmaEditada.emit(alarma)
        alarma=alarma[0]
        self.cargarAlarma(alarma)


    def mandarSenalMuerto(self):
        '''Cuando se desee eliminar la este widget o mejor dicho la alarma que
        representa visualmente este widget se debe notificar mandando una senal
        acerca de esta peticion'''

        self.suHoraMorir.emit( [self.id,self.nombreAlarma] )

    def eliminar_cuadroDilogo(self,dato):
        '''Este metodo se llamara cuando se termine de usar la ventana que
        permite editar a las alarmas, ya que esto libera recursos al sistema'''

        del (self.ventana)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = ItemAlarmaVista()
    application.show()
    app.exec()






