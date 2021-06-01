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
    El proposito de esta clase es crear  instancia que  muestren los datos de una 
    alarma de forma visual, a traves de widgets, asi como proveer las herramientas
    para que el usuario pueda editar  o borrar una alarma en especifico y avisar 
    cuando esto suceda
    '''

    suHoraMorir= pyqtSignal(int)    # indicara quien es el objeto que quiere morir...
                                    # id

    senal_alarmaEditada=pyqtSignal(list)    # indicara quien es el objeto que fue editado...
                                            # [id,nombre]

    senal_alarmaQuiereEdicion=pyqtSignal(str) # indicara el nombre de la  alarma que quiere ser editada...
                                              #  nombreAlarma

    senal_alarmaActivada=pyqtSignal(list)  # senal_alarmaActivada=True, significa que la alarma esta activada
                                           # [id,True/False]                              



    def __init__(self,alarma):
        '''
        Parámetros:
            alarma -- Una instancia de la clase 'Alarma' el cual cotiene todos los datos
            de la alarma que quiere se quiere mostrada.
        '''

        Ui_Form.__init__(self)
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.btn_eliminar.clicked.connect(self.mandarSenalMuerto)
        self.id=alarma.id
        self.nombreAlarma=alarma.nombre
        
        self.btn_editar.clicked.connect(self.editar)
        self.textEdit_alarma.setReadOnly(True)
        self.hoSli_estado.valueChanged.connect(self.activarDesactivarAlarma)
        self.hoSli_estado.setValue(1)
        self.textEdit_alarma.setStyleSheet("border:1px solid #C4C8C0; border-radius:10%;")

        self.cargarAlarma(alarma)
    
    def cargarNuevoId(self,nuevoId):
        '''
        Cambiara el valor del 'id' del objeto.

        Parámetro:
            nuevoId -- dato de tipo 'int' que representara el nuevo valor de 'id'
            al cual se desea cambiar.
        '''

        self.id=nuevoId
    
    def cargarAlarma(self,alarma):
        '''
        Mostrara de forma visual los datos MAS RELEVANTES de la alarma en la widget, la
        forma y el orden en el que mostrara los datos sera el siguiente:
            
            Hora a la que suena la alarma
            nombre de la alarma : nombre de los dias en los que suena

            Ejemplo 1:
                9:36 pm
                escuela: lunes, martes, miercoles, jueves, viernes

            Ejemplo 2:
                6:40 am
                entrenamiento: lunes,martes,miercoles,jueves,viernes,sabado 
        
        Parámetros: 
            alarma -- es una instancia de la clase 'Alarma', y dicha instancia contiene todos 
            los datos  de la alarma de la cual se pretende mostrar los datos ya mencionados.
        '''

        self.nombreAlarma=alarma.nombre
        horaAlarma=QTime()
        horaAlarma.setHMS(alarma.horaAlarma.hora,alarma.horaAlarma.minuto,0)
        horaAlarma=horaAlarma.toString("hh:mm")
        print("HORA:",horaAlarma)
        
        
        self.textEdit_alarma.setText("""<h2>{}  </h2>
        <h4>{}: {}</h4>
        """.format(alarma.horaAlarma,alarma.nombre,alarma.getDias() ) )

        if alarma.prendida:
            self.hoSli_estado.setValue(1)
        else:
            self.hoSli_estado.setValue(0)

    
    def activarDesactivarAlarma(self):
        '''
        Este metodo deshabilitara el 'textEdit_alarma' el cual es el  que contiene los 
        datos de alarma, para que simule el efecto  visual que de entender que la alarma
        se encuentra desactivada, posteriormente mandara una señal con el objetivo de avisar
        que esta alarma fue desactivada y por ende se actue en consecuencia 
        '''

        if self.hoSli_estado.value():
            self.textEdit_alarma.setEnabled(True)
            self.senal_alarmaActivada.emit( [self.id,True] )
        else:
            self.textEdit_alarma.setEnabled(False)
            self.senal_alarmaActivada.emit( [self.id,False] )

    def editar(self):
        '''
        Abrira la ventana 'editor de alarma en modo de trabajo de edicion, lo cual significara que 
        dicho editorcargara todos los datos de la alarma que se quiere editar y permitira modificarlos
        y despues guardar esos cambios
        '''

        self.ventana=ItemAlarmaEdit()
        self.ventana.modoTrabajo(modoEdicion=True,idAlarma=self.id)
        self.ventana.senal_alarmaEditada.connect(self.alarmaEditada)
        self.ventana.senal_editorCreador_cerrado.connect(self.eliminar_cuadroDilogo)
        self.ventana.show()

    def alarmaEditada(self,alarma):
        '''
        Este metodo se llamara si es que la alarma que se queria editar, ya fue
        editada con exito y los cambios guardados, pues este metodo tiene como
        objetivo avisar que una alarma fue editada mandando una señal la cual
        mandara  una instancia de la clase 'Alarma' con todos los datos de la 
        alarma que fue editada

        Parametros:
            alarma -. Es una lista de un solo elemento que contiene una instancia
            de la clase 'Alarma' con todos los datos de la alarma que fue editada
        '''

        self.senal_alarmaEditada.emit(alarma)
        alarma=alarma[0]
        self.cargarAlarma(alarma)


    def mandarSenalMuerto(self):
        '''
        Cada vez que se presione el QButton: 'self.btn_eliminar' signficara que
        se desea eliminar  este widget o mejor dicho la alarma que representa visualmente 
        este widget  asi que cuando esta acción sucede se manda una senal para informar
        que se desea eliminar.
        '''

        self.suHoraMorir.emit( self.id )

    def eliminar_cuadroDilogo(self,dato):
        '''
        Este metodo se llamara cuando se termine de usar la ventana que
        permite editar a las alarmas, ya que esto libera recursos al sistema
        '''

        del (self.ventana)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = ItemAlarmaVista()
    application.show()
    app.exec()






