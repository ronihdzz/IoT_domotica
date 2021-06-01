from PyQt5 import QtWidgets,Qt
from PyQt5.QtWidgets import QWidget,QVBoxLayout
from PyQt5.QtWidgets import  QMessageBox,QMainWindow
from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QMainWindow,QLabel,QWidget,QPushButton, QVBoxLayout,QScrollArea,QMessageBox
from PyQt5.QtGui import QIcon

from PyQt5.Qt import QSizePolicy,Qt
from PyQt5 import QtCore

from collections import OrderedDict 
# A partir de Python 3.6 
#   Para la implementación CPython de Python, 
#   los diccionarios mantienen el orden de inserción de forma predeterminada
#En Python 3.7.0
#   La naturaleza de conservación del orden de inserción de los 
#   dictobjetos ha sido declarada como una parte oficial 
# Python> = 2.7 y <3.6
#   Utilice la collections.OrderedDictclase cuando necesite una dictque recuerde 
#   el orden de los elementos insertados.


###############################################################
#  IMPORTACION DEL DISEÑO...
##############################################################


###############################################################
#  MIS LIBRERIAS...
##############################################################
from CUERPO.LOGICA.ALARMA.ItemAlarmaVista import ItemAlarmaVista
from CUERPO.LOGICA.ALARMA.ItemAlarmaEdit import ItemAlarmaEdit
from CUERPO.LOGICA.ALARMA.baseDatos_alarma import BaseDatos_alarmas
from recursos import App_Alarmas,HuellaAplicacion
from CUERPO.LOGICA.ALARMA.reloj import Reloj
from CUERPO.LOGICA.ALARMA.notificadorAlarmas import NotificadorAlarmas
from CUERPO.LOGICA.ALARMA.checadorAlarma import ChecadorAlarma
from PyQt5.QtCore import pyqtSignal

###############################################################
#  MIS LIBRERIAS...
##############################################################
import IMAG_rc



class AdministradorAlarmas(QMainWindow,HuellaAplicacion):
    '''
    Esta clase mostrara todas las alarmas creadas, asi como tambien
    permitira agregar alarmas, editarlas y  eliminarlas.Cuando
    una alarma o un conjunto de alarmas deban sonar esta clase las
    mostrara.
    '''

    senal_horaDespertar_prenderLuz=pyqtSignal(bool)


    def __init__(self,noDia,hora,minuto,segundo):
        QMainWindow.__init__(self)
        HuellaAplicacion.__init__(self)

        self.MAX_ITEMS=20
        self.punteroNoItems=0

        # Diccionario que almacenara en sus 'keys' los id de los 'ItemAlarmaVista' que esten
        # presentes, y sus 'values' seran los estados de las 'ItemAlarmaVista'
        # Ejemplo: Si self.dictAlarmas={ 1:True,2:True,4:False,5:True   }
        # significaria que el existen aun los 'ItemAlarmaVista' con id=1,2,4,5
        # y que:
        #   A)El ItemAlarmaVista con id=1 esta activado
        #   B)El ItemAlarmaVista con id=2 esta activado
        #   C)El ItemAlarmaVista con id=4 esta desactivado
        #   D)El ItemAlarmaVista con id=5 esta activado
        # Si un 'ItemAlarmaVista' esta activado significa que dicha alarma si es el dia y la  hora de sonar 
        # entonces debe sonar, pero si 'ItemAlarmaVista' esta desactivada significa que dicha alarma aunque 
        # sea su hora y dia de sonar no sonara por que se encuentra desactivada
        self.dictAlarmas=OrderedDict() 
     
        ##############################################################################################################
        # CONFIGURACIONES DE LA TOOL BAR

        self.statusBar() 
        toolbar = self.addToolBar('')
        self.addToolBar(QtCore.Qt.BottomToolBarArea,toolbar) # ubicando a la toolbar en la posicion  inferior de la widget
        toolbar.setMovable(False) # restringir que la toolbar pueda ser movida por el usuario
        toolbar.setOrientation(QtCore.Qt.Horizontal) # posicion horizontal tool bar
        toolbar.setContextMenuPolicy(Qt.PreventContextMenu) # restringir el clic derecho sobre la toolbar para evitar que
                                                            # el usuario pueda desaparecerla

        toolbar.addWidget(self.get_expansorWidget() ) # agregando una widget con tal anchura que hara el todos 
                                                      # los iconos de la toolbar esten alineados a la izquierda
    
    
        self.crear_botonAgregadorItems() # creando boton agregador de items
        toolbar.addWidget(self.btnAgregarItem)
        toolbar.addWidget( self.get_separadorQAction() )

       ##############################################################################################################
        # BASES DE DATOS

        self.baseDatosAlarmas=BaseDatos_alarmas(App_Alarmas.NOMBRE_BASE_DATOS_ALARMAS)
        self.baseDatosAlarmas.crearBaseDatos()
        
        self.ventanaCreadoraAlarmas=ItemAlarmaEdit() # esta ventana se aparecera cada vez que se desea crear
                                                     # una nueva alarma


       ##############################################################################################################
        # CREANDO EL AREA EN DONDE APARECERAN LAS ALARMAS

        self.crear_pantallaMostradora() #crea los atributos: 'self.scroll', 'self.widget', 'self.vbox'
        #los cuales en conjunto permiten mostrar los deberes y en caso de ser demasiados hacer la famosa
        #barra deslizadora

        self.setGeometry(300, 300, 350, 250)

        ##############################################################################################################
        # CARGANDO ALARMAS EN CASO DE YA EXISTIR

        self.cargarAlarmas()

        ##############################################################################################################
        # CONECTANDO LAS ACCIONES DE LOS OBJETOS:

        self.ventanaCreadoraAlarmas.senal_alarmaCreada.connect(self.nuevaAlarmaCreada)
        self.btnAgregarItem.clicked.connect(self.crearUnaAlarma)
        self.prepararSincronizaciones(noDia,hora,minuto,segundo)



################################################################################################################################
#  C R E A D O R E S : 
################################################################################################################################

    def crear_botonAgregadorItems(self):
        '''
        Creara un atributo de instancia el cual sera un objeto  de la clase 'QPushButton()',
        la función de este boton sera agregar un 'itemDeber' al 'QVBoxLayout' cada vez que
        este sea presionado.

        El atributo de instancia creado se llamara:
            A) self.btnAgregarItem

        Este atributo de instancia en el metodo contructor  se anexara  a la toolbar y se vinculara  una
        señal de este con el metodo correspondiente.
        '''

        self.btnAgregarItem=QPushButton()
        self.btnAgregarItem.setStyleSheet("""
            QPushButton {
               	border-image: url(:/ALARMA/IMAGENES/ALARMA/plus_off.png);
            }
            QPushButton:hover {
               	border-image: url(:/ALARMA/IMAGENES/ALARMA/plus_on.png);
            }
            QPushButton:pressed {
                border-image: url(:/ALARMA/IMAGENES/ALARMA/plus_off.png);
            }   
        """)
        self.btnAgregarItem.setMinimumSize(30,30)


    def crear_pantallaMostradora(self):
        '''
        Creara 3 atributos de instancia cuyo objetivo sera mostrar los 'itemDeber' que el usuario vaya
        creando y en dado caso que el espacio ya no alcance para mostrarlos todos  'itemDeber', debera 
        aparecer una barra lateral que permitira visualizar todos los 'itemDeber'.Los 3 atributos de instancia
        trabajan en conjunto para cumplir lo mencionado anteriormente.Los atributos de instancia que se
        crearan son los siguientes:
            A) Nombre: self.scroll  ¿que es? un objeto de la clase QScrollArea()
            B) Nombre: self.widget  ¿que es? un objeto de la clase QWidget()
            C) Nombre: self.vbox    ¿que es? un objeto de la clase QVBoxLayout() 
        '''

        #Scroll Area Properties
        self.scroll_alarmas = QScrollArea()     # Scroll Area which contains the widgets, set as the centralWidget
        self.scroll_alarmas.setStyleSheet("""
                        *{
                        border:none;
                        background:#FFFFFF;
                        }
                        QScrollArea{
                            border-radius:20%;
                            padding:10px;
                            margin-bottom:15px;
                        }
                        QScrollBar{
                        background:#F7E5E5;
                        }
                        QScrollBar::handle{
                        background :#979797;
                        }
                        QScrollBar::handle::pressed{
                        background :  #193b58;
                        }
                        """)

        self.widget = QWidget()  # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()  # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        
        self.widget.setLayout(self.vbox)

        self.scroll_alarmas.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_alarmas.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_alarmas.setWidgetResizable(True)
        self.scroll_alarmas.setWidget(self.widget)
        self.setCentralWidget(self.scroll_alarmas)
        
    def get_separadorQAction(self):
        '''
        Retornara una instancia de la clase 'QLabel' con el objetivo de que este
        sirva como seperador entre los elementos que se colocan en la toolbar
        '''

        separadorQAction=QLabel()
        separadorQAction.setMinimumSize(10,2)
        return separadorQAction

    def get_expansorWidget(self):
        '''
        Retornara una instancia de la clase 'QWidget' con la caracteristica
        peculiar de que este objeto donde se coloque ocupara todo el espacio 
        horizontalmente, es decir si se coloca en la toolbar al principio,esto
        obligara a que todos los elementos de esta se recorran a la derecha,o
        si se coloca este objeto al ultimo en la toolbar este obligara que 
        todos los elemento se recorran a la izquierda en la toolbar
        '''

        expansorWidget=QWidget()
        expansorWidget.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        return expansorWidget


#######################################################################################################################3
# REVISANDO   LAS     ALARMAS
#######################################################################################################################3
    def prepararSincronizaciones(self,noDia,hora,minuto,segundo):
        '''
        Creara a los atributos de instancia necesarios para que estos en trabajo en equipo
        puedan cordinarse para  hacer posible que:  
            - Las alarmas registradas por el usuario suenen cuando deban sonar, ademas que
              cuando suenen toquen la canción debida  y que se puedan apagar tal cual como 
              se hace en celular.
        '''

        # El 'self.ChecadorAlarma' llevara una administración de las alarmas, por ende a el
        # es al que se le debe de preguntar si ya es hora de sonar de alguna alarma, cuando 
        # se le pregunte el lo checara y en caso de ser afirmativo mandara una señal con 
        # la lista de 'ids' de las alarmas que suenen en ese minuto consultado.
        self.checadorAlarma=ChecadorAlarma(noDia, hora, minuto )


        # El 'self.reloj' llevara el seguimiento del tiempo y dia en el se encuentra el sistema,
        # dicho reloj envia señales cada minuto que pasa y cada 24 horas por eso es clave aqui,
        # ya que cada minuto se consultada al 'self.ChecadoAlarma' si hay una alarma que deba
        # sonar y el reloj tiene la habilidad de avisarnos cada minuto.
        self.reloj=Reloj(noDia,hora,minuto,segundo)


        # El avisador sera el encargado de mostrar la o las alarmas cuyo tiempo es hora de sonar, 
        # asi que tocara la canción de la alarma que deba sonar en ese momento y no dejara de 
        # hacerlo hasta que el usuario apague dicha alarma
        self.avisador=NotificadorAlarmas()  


        # Sera el contador que ira cambiando los valores del atributo: 'self.reloj' a travez del metodo
        # 'clock' de 'self.reloj'
        self.contador=QTimer()
        

        ###########################################################################################################################
        # ASOCIANDO LAS SEÑALES DE LOS OBJETOS QUE SE ACABAN DE CREAR COMO ATRIBUTOS DE INSTANCIA

        # Señal que se emitira cuando suena una alarma con asunto: despertar, su finalidad es 
        # avisarle al sistema que es hora de despertar para que este reaccione de la manera
        # apropiada( ejemplo: prender un foco ya que es hora de despertar )
        self.avisador.senal_horaDespertar_prenderLuz.connect(   lambda x: 
                                                                self.senal_horaDespertar_prenderLuz.emit(True) 
                                                            )
        
        
        # Cada que haga 'clock'  el Qtimer, deben hacerse muchas cosas, entre ellas que se
        # llame al metodo 'clock' de 'self.reloj' para que lleve el registro del tiempo
        self.contador.timeout.connect(lambda : self.reloj.clock() )

        #self.reloj.clock()


        # Como la maxima resolución de las alarmas creadas son los minutos, entonces es mejor
        # revisar mejor cada minuto si ya es hora de sonar de una alarma, asi que por eso se 
        # consulta a 'self.checadorAlarma' una vez que 'self.reloj' registro un cambio de 
        # minuto.
        self.reloj.senal_minutoCambio.connect(  lambda listaDatos:
                                                self.checadorAlarma.revisar(
                                                    listaDatos[1],  # listaDatos[1]=hora 
                                                    listaDatos[2] ) # listaDatos[2]=minutos
                                                ) # listaDatos[0]=dia, sin embargo dicho dato no es requerido
        

        # El 'self.checadorAlarma' de alarmas solo lleva el registro de las alarmas que estan
        # programadas para sonar un dia en particular, por eso cuando se cambia
        # de dia, se le debe avisar al checador que ya es un dia diferente, para
        # que el pueda cargar las alarmas que suenan en ese nuevo dia.
        self.reloj.senal_diaCambio.connect( lambda listaDatos: 
                                            self.checadorAlarma.actualizarAlarmasHoy(
                                                listaDatos[0],   # listaDatos[0]=dia
                                                listaDatos[1],   # listaDatos[1]=hora  
                                                listaDatos[2] )  # listaDatos[2]=minutos
                                          )


        # Cuando 'self.checadorAlarma' detecta que una o mas de una alarma tienen que sonar en ese
        # minuto consultado, mandara la lista de los 'ids' de dichas alarmas atraves de la señal 
        # 'senal_alarmaDetectada', sin embargo antes de decirle a 'self.avisador' que la o las muestre, 
        # se debera revisar si esas alarmas  estan activadas, y si almenos una esta activada ahora
        # si decirle a 'self.avisador' que se prepare para mostrar dicha alarma 
        self.checadorAlarma.senal_alarmaDetectada.connect( self.filtrarAlarmasSonaran )
        

        # Cuando el 'self.avisador' haya hecho todos los preparativos para mostrar la o las 
        # alarmas que  deben sonar, activara la señal 'senal_alarmaSonando' y eso significa 
        # que es hora de mostrarlo lo que preparo el 'self.avisador'
        self.avisador.senal_alarmaSonando.connect( lambda : self.avisador.show() )


        # El 'Qtimer' debe sonar cada segundo
        self.contador.start(10)

    def filtrarAlarmasSonaran(self,listaIds):
        '''
        Apartir de 'listaIds' la cual es una lista que contiene los 'ids' de las alarmas que 
        deben sonar,revisara  si dichas alarmas con esos 'ids' se encuentran activadas, y todas 
        las que efectivamente se encuentren activadas las agrupara en otra lista para posteriormente 
        mandar esa lista al 'self.avisador' para que el pueda empezar a realizar los preparativos 
        necesarios para mostrar dicha alarma o alarmas.

        Parámetros:
            listaIds -- Es una lista de numeros enteros, los cuales representan los 'ids' de las alarmas
            que deben sonar pero aun no se sabe si dichas alarmas estan activadas o desactivadas.
        '''

        listaIds_alarmasActivadas=[]
        for idAlarma in listaIds:

            # El diccionario 'self.dictAlarmas' contine como 'keys' los 'ids' de las alarmas
            # registradas, y como 'values' sus estados(si se encuentra activada o desactiva)
            # por ende para saber si una alarma con un id=idAlarma se encuentra activada se 
            # hace lo siguiente:
            if self.dictAlarmas[idAlarma]:
                listaIds_alarmasActivadas.append(idAlarma)
        
        if len( listaIds_alarmasActivadas ) >0:
            self.avisador.activarAlarmas(listaIds_alarmasActivadas)

    
    def cargarAlarmas(self):
        '''
        Cargara todas las alarmas que se encuentren registradas en la base de datos
        para posteriormente mostrar a cada una de ellas por medio de un 'ItemAlarmaVista', 
        es importante aclarar que cada alarma requiere un 'ItemAlarmaVista', asi que
        si resultan ser: 'n' alarmas las que se cargan de la base de datos entonces
        seran 'n' 'ItemAlarmaVista' que se crearan donde cada 'ItemAlarmaVista' mostrara
        los datos principales de cada alarma cargada.

        Los 'ItemAlarmaVista' se almacenaran  en en el 'self.vbox' 
        '''

        listaAlarmas=self.baseDatosAlarmas.getTodas_alarmas()
        
        for alarma in listaAlarmas:

            # Este metodo creara un 'ItemAlarmaVista' a apartir de los datos proporcionador por
            # un objeto de tipo 'Alarma', porteriormente agregara al 'ItemAlarmaVista' al 'self.vbox'
            # para que se puede visualizar.
            self.agregarAlarma(alarma=alarma)  


    def crearUnaAlarma(self):
        '''
        Abrira la ventana: 'self.ventanaCreadoraAlarmas' con la finalidad
        de que el usuario pueda ingresar los datos de la alarma que desea
        crear, sin embarrgo en caso de que el usuario ya haya alcanzado el
        limite de alarmas que se pueden crear entonces mostrara un mensaje
        emergente indicando que el limite ha sido alcanzado y no se le 
        permitira crear otra alarma mas.
        '''

        if self.punteroNoItems<self.MAX_ITEMS:
            self.ventanaCreadoraAlarmas.modoTrabajo(modoEdicion=False)
            self.ventanaCreadoraAlarmas.show()
        else:
            mensaje="El numero maximo de alarmas que\n"
            mensaje+=f"puedes registrar es de: {self.MAX_ITEMS} alarmas\n"  
            mensaje+=f"y usted ya ha creado {self.MAX_ITEMS} alarmas."
            
            ventanaDialogo = QMessageBox()
            ventanaDialogo.setWindowIcon(QIcon(self.ICONO_APLICACION)  )
            ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)
            ventanaDialogo.setIcon(QMessageBox.Information)

            ventanaDialogo.setText(mensaje)
            ventanaDialogo.setStandardButtons(QMessageBox.Ok)
            btn_ok = ventanaDialogo.button(QMessageBox.Ok)
            btn_ok.setText('Entendido')
            ventanaDialogo.exec_()    

    def nuevaAlarmaCreada(self,alarmaEmpaquetada):
        '''
        Creara una instancia de la clase 'ItemAlarmaVista' apartir de los datos proporcionados 
        'alarmaEmpaquetado[0]' el cual es el primer y unico elemento del parametro de este metodo.
        Posteriormente adjuntara al 'ItemAlarmaVista' creado, al objeto de tipo 'QVBoxLayout' cuyo 
        nombre es 'self.vbox' con la finalidad de que el 'ItemAlarmaVista' se pueda apreciar.

        Este metodo tambien le avisara al 'self.checadorAlarma' que alarma se creo , pues existe
        la posibilidad de que la alarma que se acaba de crear tenga que sonar el dia de hoy, asi que
        es importante avisarle pues el es el que lleva la gestion de las alarmas que suenan y el que 
        avisa cuando estas deben sonar

        Parámetros:
            alarmaEmpaquetada -- Es una lista con un solo elemento en donde:
                A) alarmaEmpaquetada[0] : es un objeto de tipo 'Alarma' que contiene todos los datos
                de la alarma creada.
        '''

        alarmaCreada=alarmaEmpaquetada[0]

        # Se le avisa al 'self.checadorAlarma' que  alarma fue creada
        self.checadorAlarma.actuarAnte_anexionAlarma(alarmaCreada)

        # Se manda a crear la instancia 'ItemAlarmaVista' apartir de los datos proporcionados
        # por el objeto de tipo 'Alarma' cuyo nombre es 'alarmaCreada', posteiormente se anexa
        # a la instancia 'ItemAlarmaVista' al 'self.vbox' para que pueda ser visualizada
        self.agregarAlarma(alarmaCreada)


    def agregarAlarma(self,alarma):
            '''
            Creara una instancia de la clase 'ItemAlarmaVista' apartir de los datos proporcionados por el
            parametro cuyo nombre es 'alarma', posteriormente adjuntara dicha instancia al objeto de tipo:
            'QVBoxLayout' cuyo nombre es 'self.vbox' con la finalidad de que el 'ItemAlarmaVista' se pueda
            apreciar.

            Parámetros:
                alarma -- Es una instancia de la clase 'Alarma' la cual contiene
                todos los datos de la alarma que se creo. 
            '''
            
            itemAlarma=ItemAlarmaVista(alarma)
            itemAlarma.suHoraMorir.connect(self.borrarItem)
            itemAlarma.senal_alarmaActivada.connect(self.cambiarEstadoAlarma)
            itemAlarma.senal_alarmaEditada.connect(self.notificarEdicionUnaAlarma)

            self.dictAlarmas[alarma.id]=alarma.prendida
    
            self.vbox.addWidget(itemAlarma)
            self.punteroNoItems+=1
    
    def cambiarEstadoAlarma(self,datos):
        '''
        Cambiara el estado de una alarma apartir de los datos proporcionados por el 
        parametro 'datos'
        ¿Como cambiara el estado?
        Bueno pues existe un diccionario cuyo nombre es: 'self.dictAlarmas' el cual
        sus 'keys' son los ids de las alarmas registradas, y sus 'values' son los
        estados de dichas alarmas.Por ende si se desea editar el estado de una alarma
        se debera editar este diccionario que es el que lleva el control de las 
        alarmas registradas junto con sus estados respectivos.

        Parámetros:
            datos -- Es una lista que almacena dos elementos:
                A) datos[0]= es un dato de tipo 'entero' el cual representa el 'id' 
                de la alarma que cambio de estado
                B) datos[1]= es un dato de tipo 'bool'representa el estado al que 
                cambio:
                        b) Si datos[1]=True, significa que la alarma ahora se encuentra activada
                        b) Si datos[1]=False, significa que la alarma ahora se encuentra desactivada
                        ¿Que significa que una alarma este activada o desactivida?
                        Si una alarma tiene que sonar pero se encuentra desactivada, no 
                        se le permitira sonar, por lo contrario si una alarma se encuentra activada
                        y tiene que sonar se le permitira sonar
        '''

        idAlarma,fueActivada=datos
        self.dictAlarmas[idAlarma]=fueActivada

    def notificarEdicionUnaAlarma(self,alarmaEmpaquetada):
        '''
        Cada vez que una alarma haya sido editada se le debe notificar a 'self.checadorAlarma'
        con los datos de la alarma que fue editada a traves de una instancia de tipo 'Alarma',
        ya que el es el que lleva el registro de las alarmas que suenan el dia actual, y si en
        hay una edición en una alarma pueden ocurrir  varios escenarios:

            A) Una alarma que estaba programada para sonar el dia actual, con la edicion hecha, ya no
            suena el dia actual si no en otros dias.
            B) Una alarma que estaba programada para sonar el dia actual en un tiempo que aun no pasaba,
            con la edición hecha, ya paso su tiempo en el que tenia que sonar.
            C) Una alarma que no estaba programada para sonar el dia actual, despues de la edición hecha,
            resulta que debe sonar el dia actual.

        Por ende ante cualquier edición hecha se le debe notificar al 'self.checadorAlarma' para que el pueda
        evaluar los casos anteriormente mencionados y con ello seguir llevando el sistema de administración de
        alarmas correcto.

        Parámetros:
            alarmaEmpaquetada -- En una lista de un  sola elemento en donde:
                A) alarmaEmpaquetada[0] = Un objeto de tipo 'Alarma' que contiene todos los datos de la alarma
                que fue editada.
        '''

        alarmaEditada=alarmaEmpaquetada[0]
        self.checadorAlarma.actuarAnte_edicionUnaAlarma( alarmaEditada )


    def borrarItem(self,id_alarmaMorira):
        '''
        Borrara la alarma cuyo 'id'='id_alarmaMorira', para hacer esto borrara la alarma de la 
        base de datos asi como tambien borrara su respectivo 'ItemAlarmaVista' del 'QVBoxLayout' 
        cuyo nombre es 'self.vbox' el cual es el que muestra a todos los objetos creados de la 
        clase: 'ItemAlarmaVista', posteriormente le avisara al 'self.checadorAlarma' que alarma
        fue la eliminada para que en caso de a ver sido contemplada para sonar, ya sea descartada
        para sonar pues ya no existira dicha alarma.Antes de borrar la alarma procedera a 
        preguntarle al usuario si efectivamente desea borrar a la alarma y si el usuario responde 
        afirmativamente se procedera a borrar a la alarma.

        Parámetros:
            id_alarmaMorira -- Es un numero entero que representa el 'id' de la alarma que 
            se desea eliminar.
        '''
        
        
        # Las 'self.dictAlarmas.keys()' es una lista que almacena todos  los 'id' de todos los objetos de la clase
        # 'ItemAlarmaVista' creados, y los almacena como una estructura de datos 'cola'
        # El 'QVBoxLayout' almacena todos los objetos de la clase 'ItemAlarmaVista' como si fuera una lista y en forma de  'cola'
        # Si se desea eliminar el 'ItemAlarmaVista' del 'QVBoxLayot' debemos indicarle en que posición del 'QVBoxLayot' 
        # se encuentra dicho 'ItemAlarmaVista'.
        # Si tenemos el 'id' del 'ItemAlarmaVista' que se desea eliminar, bastara con encontrar en
        # que posición de la lista 'self.dictAlarmas.keys()' se encuentra  dicho 'id' para saber indirectamente en que 
        # posición se encuentra en el 'QVBoxLayout'.
        posItemMatar=list(self.dictAlarmas.keys()).index(id_alarmaMorira)

        widgetItem_alarmaVista_morira =self.vbox.itemAt(posItemMatar).widget()

        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Question)
        ventanaDialogo.setWindowIcon( QIcon(self.ICONO_APLICACION)  )
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje="¿Esta seguro que quieres\n" 
        mensaje+=f"eliminar la alarma numero: {posItemMatar+1}\n"
        mensaje+=f" cuyo nombre es: {widgetItem_alarmaVista_morira.nombreAlarma}?"

        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        btn_yes = ventanaDialogo.button(QMessageBox.Yes)
        btn_yes.setText('Si')
        btn_no = ventanaDialogo.button(QMessageBox.No)
        btn_no.setText('No')
        ventanaDialogo.exec_()
        if ventanaDialogo.clickedButton()  ==  btn_yes:
            # Eliminando el objeto 'itemDeber' de la lista layout 
            self.vbox.removeWidget(widgetItem_alarmaVista_morira)
            # Eliminando el objeto 'itemDeber' de la GUI
            widgetItem_alarmaVista_morira.setParent(None)
            # Eliminando al 'id' del diccionario.
            del self.dictAlarmas[id_alarmaMorira]

            self.punteroNoItems -= 1

            self.baseDatosAlarmas.eliminar(id_alarmaEliminar=id_alarmaMorira)

            self.checadorAlarma.actuarAnte_eliminacionUnaAlarma(id_alarma=id_alarmaMorira)
    
    def respaldarEstadosAlarma(self):
        '''
        Actualizara los valores de los estados de las alarmas en la base de datos, es ideal
        que este metodo se llame antes de cerrar el programa para que se haga el respaldo 
        de los estados de alarma.El motivo de hacer esto justo antes de ser cerrado el
        programa es por que  el usuario puede modificar con facilidad los estados de una
        alarma pero NO se desea  modificar el estado de una alarma instantaneamente 
        en la base de datos y para evitar eso entonces mejor se editan esos valores de la
        base de datos hasta que se cierra el programa. 
        '''

        # La lista de tuplas que requiere el metodo de la base de datos, debe seguir el 
        # siguiente orden:
        # [ (alarma1_estado,alarma1_id), (alarma2_estado,alarma2_id), ... (alarmaN_estado,alarmaN_id) ]
        tuplaRequerida=zip( self.dictAlarmas.values(),self.dictAlarmas.keys() )

        self.baseDatosAlarmas.actualizarEstadoAlarma( tupla_idsYestados_alarmas=tuplaRequerida )


    def closeEvent(self, event):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = AdministradorAlarmas(1,10,20,0)
    application.show()
    app.exec()

    ##sys.exit(app.exec())


