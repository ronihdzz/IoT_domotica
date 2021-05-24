
import sys
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication,QSpinBox,QActionGroup,QLabel,QWidget,QPushButton, QVBoxLayout,QScrollArea,QMessageBox
from PyQt5.QtGui import QIcon,QFont
from PyQt5.Qt import QSizePolicy,Qt
from PyQt5 import QtCore


###############################################################
#  IMPORTACION DEL DISEÑO...
##############################################################


###############################################################
#  MIS LIBRERIAS...
##############################################################
from CUERPO.LOGICA.DEBERES.itemDeber import ItemDeber
from recursos import App_Deberes,HuellaAplicacion
import IMAG_rc
from logger import logger


class SeccionDeberes(QMainWindow,HuellaAplicacion):
    '''
    El objetivo de esta clase  sera mostrar todo el sistema que permite
    agregar deberes, eliminar los deberes cuando se cumplen,cambiar la posicion del texto de los deberes 
    y cambiar el tamaño del texto de los deberes, por ello esta clase basicamente estara compuesta de
    una apartado en donde se mostraran todos los deberes a realizar  y unos botones que permitieran hacer
    lo mencionado anteriormente.  
    '''

    def __init__(self):
        QMainWindow.__init__(self)
        HuellaAplicacion.__init__(self)

        #Valores default del texto de los deberes
        self.ESTADO_ALINEO=0   #0=izquierdo, 1=centro, 2=derecha
        self.TAMANO_LETRA=12
        self.MAX_ITEMS=20   

        #Variable para controlar el numero de items dezplegados
        self.punteroNoItems=0

        self.listIdsItemsVivos=[]
        self.listPunterosItems=[]
        self.siguienteItemEliminar=None
        
        
        ##############################################################################################################
        # CONFIGURACIONES DE LA TOOL BAR

        self.statusBar() 
        toolbar = self.addToolBar('')
        self.addToolBar(QtCore.Qt.BottomToolBarArea,toolbar) # ubicando a la toolbar en la posicion  inferior de la widget
        toolbar.setStyleSheet(" *{background:#d8d8d8; border:none} QToolButton:checked {background-color:#94DCD3; border:none; } ")
        toolbar.setMovable(False) # restringir que la toolbar pueda ser movida por el usuario
        toolbar.setOrientation(QtCore.Qt.Horizontal) # posicion horizontal tool bar
        toolbar.setContextMenuPolicy(Qt.PreventContextMenu) # restringir el clic derecho sobre la toolbar para evitar que
                                                            # el usuario pueda desaparecerla

        toolbar.addWidget(self.get_expansorWidget() ) # agregando una widget con tal anchura que hara el todos 
                                                      # los iconos de la toolbar esten alineados a la izquierda
        
        self.crear_accionesParaPosiciones() # crear los atributos 'self.alineacion_izquierda','self.alineacion_centro'
                                            # 'self.alineacion_derecha' los cuales son acciones que serviran para
                                            #editar las posicion del texto de los deberes
        toolbar.addAction(self.alineacion_izquierda)
        toolbar.addSeparator() 
        toolbar.addWidget( self.get_separadorQAction() ) # agrendado widget entre cada objeto de la toobar para que tengan separacion entre si
        toolbar.addAction(self.alineacion_centro)
        toolbar.addSeparator()
        toolbar.addWidget( self.get_separadorQAction() )
        toolbar.addAction(self.alineacion_derecha)
        toolbar.addSeparator()
        toolbar.addWidget( self.get_separadorQAction() )

        self.crearSpin_cambiadorTamanoLetra() # creando atributo: 'self.spinBox_tam' el  serviara
                                              # para modificar el tamaño del texto de los deberes
        toolbar.addWidget(self.spinBox_tam)
        toolbar.addWidget( self.get_separadorQAction() )

        self.crear_botonAgregadorItems() # creando atributo 'self.btnAgregarItem' el cual servira para
                                         # agregar deberes
    
        toolbar.addWidget(self.btnAgregarItem)
        toolbar.addWidget( self.get_separadorQAction() )

        ##############################################################################################################
        # CREANDO EL AREA EN DONDE APARECERAN LOS DEBERES

        self.crear_pantallaMostradora() #crea los atributos: 'self.scroll', 'self.widget', 'self.vbox'
        #los cuales en conjunto permiten mostrar los deberes y en caso de ser demasiados hacer la famosa
        #barra deslizadora
 
        ##############################################################################################################
        # CARGANDO DEBERES EN CASO DE YA EXISTIR

        logger.debug('Sistema de deberes cargado')
        self.cargarDeberes()
        
        self.setGeometry(300, 300, 350, 250)

        ##############################################################################################################
        # CONECTANDO LAS ACCIONES DE LOS OBJETOS:

        self.alineacion_derecha.triggered.connect( lambda x : self.alinear(2) )
        self.alineacion_centro.triggered.connect( lambda x : self.alinear(1)  )
        self.alineacion_izquierda.triggered.connect(lambda x : self.alinear(0)  )
        self.btnAgregarItem.clicked.connect( self.agregarNuevo_itemDeber )

        self.spinBox_tam.valueChanged.connect(self.cambiarTamano_letra)
        #toolbar.setContentsMargins(0,0,0,0) #arriba,abajo,izquierda,derecha



################################################################################################################################
#  C R E A D O R E S : 
################################################################################################################################
    def crear_accionesParaPosiciones(self):
        '''
        Creara 3 atributos de instancia que seran objetos de la clase 'QAction', el objetivo 
        de estos 3 atributos de instancia es permitir al usuario modificar la posición del texto 
        de los deberes, aparte esta metodo tambien les asigna una imagen como icono a las 'QAction'
        y tambien los agrupa de tal manera  que solo una de las 'QAction' puedo estar seleccionado  
        a la vez.
        Los atributos de instancia que se crean y que son objetos de tipo 'QAction' son los siguientes:
            A) self.alineacion_izquierda 
            B) self.alineacion_centro
            C) sel.alineacion_derecha
        
        Estos atributos de instancia en el metodo contructor  se anexaran  a la toolbar y se vincularan algunas
        señales de estos con los metodos correspondientes.
        '''

        # Creando los 'QAction' asi como asignandoles nombres y aparte iconos:
        self.alineacion_izquierda = QAction(QIcon(":/DEBERES/IMAGENES/DEBERES/izquierda.png"), 'Izquierda', self)
        self.alineacion_centro= QAction(QIcon(":/DEBERES/IMAGENES/DEBERES/centrado.png"), 'Centrado', self)
        self.alineacion_derecha= QAction(QIcon(":/DEBERES/IMAGENES/DEBERES/derecha.png"), 'Derecha', self)

        # Permitiendo que las 'QAction' puedan ser seleccionadas
        self.alineacion_izquierda.setCheckable(True)
        self.alineacion_centro.setCheckable(True)
        self.alineacion_derecha.setCheckable(True)

        # Agrupando las acciones que permitiran al usuario alinear el texto de sus deberes, 
        # con la finalidad de que solo una de las acciones  pueda ser seleccionada a la vez
        self.grupo_alineadores = QActionGroup(self)
        self.grupo_alineadores.addAction(self.alineacion_izquierda)
        self.grupo_alineadores.addAction(self.alineacion_centro)
        self.grupo_alineadores.addAction(self.alineacion_derecha)


    def crearSpin_cambiadorTamanoLetra(self):
        '''
        Creara un atributo de instancia que sera un objeto de la clase 'QSpinBox()',el cual 
        servira para modificar el tamaño de la letra de los deberes creados por el 
        usuario.Este  metodo tambien  establece los valores minimos y maximos que puede 
        tomar el 'QSpingBox()' asi como un diseño que fue obtenido de: 
        https://doc.qt.io/qt-5/stylesheet-examples.html?fbclid=IwAR0uwd2xHO8AbXTjOBUq9ZoIMLjhcUGaw7mg1gpbZc7DEGG6mrqyltLfuqs

        El atributo de instancia creado se llamara:
            A) self.spingBox_tam

        Este atributo de instancia en el metodo contructor  se anexara  a la toolbar y se vinculara  una
        señal de este con el metodo correspondiente.
        '''
        
        self.spinBox_tam= QSpinBox()
        self.spinBox_tam.setMinimumSize(60,30)
        self.spinBox_tam.setFont(QFont('Arial', 12))
        self.spinBox_tam.setMinimum(10)
        self.spinBox_tam.setMaximum(25)
        self.spinBox_tam.setValue(self.TAMANO_LETRA)

        self.spinBox_tam.setStyleSheet("""
        QSpinBox {
            padding-right: 15px; /* make room for the arrows */
            border-image: url(:/PYQT5/IMAGENES/pyqt5/frame.png) 4;
            border-width: 3;
        }
        QSpinBox::up-button {
            subcontrol-origin: border;
            subcontrol-position: top right; /* position at the top right corner */
            width: 16px; /* 16 + 2*1px border-width = 15px padding + 3px parent border */
            border-image: url(:/PYQT5/IMAGENES/pyqt5/spinup.png) 1;
            border-width: 1px;
        }
        QSpinBox::up-button:hover {
            border-image: url(:/PYQT5/IMAGENES/pyqt5/spinup_hover.png) 1;
        }
        QSpinBox::up-button:pressed {
            border-image: url(:/PYQT5/IMAGENES/pyqt5/spinup_pressed.png) 1;
        }
        QSpinBox::up-arrow {
            image: url(:/PYQT5/IMAGENES/pyqt5/up_arrow.png);
            width: 7px;
            height: 7px;
        }
        QSpinBox::up-arrow:disabled, QSpinBox::up-arrow:off { /* off state when value is max */
        image: url(:/PYQT5/IMAGENES/pyqt5/up_arrow_disabled.png);
        }
        QSpinBox::down-button {
            subcontrol-origin: border;
            subcontrol-position: bottom right; /* position at bottom right corner */
            width: 16px;
            border-image: url(:/PYQT5/IMAGENES/pyqt5/spindown.png) 1;
            border-width: 1px;
            border-top-width: 0;
        }
        QSpinBox::down-button:hover {
            border-image: url(:/PYQT5/IMAGENES/pyqt5/spindown_hover.png) 1;
        }
        QSpinBox::down-button:pressed {
            border-image: url(:/PYQT5/IMAGENES/pyqt5/spindown_pressed.png) 1;
        }
        QSpinBox::down-arrow {
            image: url(:/PYQT5/IMAGENES/pyqt5/down_arrow.png);
            width: 7px;
            height: 7px;
        }
        QSpinBox::down-arrow:disabled,
        QSpinBox::down-arrow:off { /* off state when value in min */
        image: url(:/images/down_arrow_disabled.png);
        }
        """)

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

        self.scroll = QScrollArea()
        self.scroll.setStyleSheet("""
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
        """) #sin borde
        self.widget = QWidget()    # Widget que contendra al 'QVBoxLayout'
        self.vbox = QVBoxLayout()  # El 'QVBoxLayout' que almacenara todos los 'itemDeber' que el usuario cree
                
        self.widget.setLayout(self.vbox)


        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.setCentralWidget(self.scroll)

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


################################################################################################################################
#  METODOS     DE    ACCIONES:
################################################################################################################################

    def alinear(self,idAlineo):
        '''
        Hara que todo el texto de todos los 'QLineEdit' que almacenan el contenido de los deberes 
        cambie de posicion, en función del valor del parametro 'idAlineo'

        Parámetros:
            idAlineo -- numero entero que indicara la posición que tomara el texto de todos los 
            'QLineEdit' que almacenan los deberes.
                A) Si 'idAlineo'=0 significa alinear el texto a la izquierda
                B) Si 'idAlineo'=1 significa alinear el texto al centro
                C) Si 'idAlineo'=2 significa alinear el texto a la derecha
        '''

        logger.debug('Solicitud de  cambio de posición del texto de  deberes a posicion={}, recibida'.format(idAlineo))

        self.ESTADO_ALINEO=idAlineo

        # iterando por cada 'itemDeber' para cambiar la posicion del texto de sus 'QLineEdit'
        for noItem in range( self.punteroNoItems ):        
            objeto_itemDeber = self.vbox.itemAt(noItem).widget()
            objeto_itemDeber.alinear(self.ESTADO_ALINEO)        

    def cambiarTamano_letra(self,nuevoValor):
        '''
        Hara que todo el texto de todos los 'QLineEdit' que almacenan el contenido de los deberes 
        cambie su tamaño de letra al valor que almacenara el paremetro 'nuevoValor'

        Parámetros:
            nuevoValor -- numero entero que indicara el tamaño de letra al cual cambiar el texto que almacenan 
            todos los 'QLineEdit'
        '''

        logger.debug('Solicitud de cambio de tamaño de letra del texto de deberes a tamaño={}, recibida'.format(nuevoValor))

        self.TAMANO_LETRA=nuevoValor

        # iterando por cada 'itemDeber' para cambiar  el tamaño del texto de sus 'QLineEdit' 
        for noItem in range( self.punteroNoItems ):        
            objeto_itemDeber = self.vbox.itemAt(noItem).widget()
            objeto_itemDeber.cambiarTamano(nuevoValor)   



    def agregarNuevo_itemDeber(self,textoDeber=None):
        '''
        Se encarga de crear un  'itemDeber' y adjuntarlos al 'QVBoxLayout' de la GUI para que 
        se pueda visualizar, cabe recordar que un 'itemDeber' es un objeto que al  usuario 
        escribir sus deberes o ver los deberes que  escribio antes de cerrar la aplicación.

        Parámetros
            textoDeber -- en un dato de tipo string que representa el deber del usuario
        '''

        logger.debug('Solicitud de agregar a un nuevo itemDeber, recibida')

        # Antes de crear una nuevo deber se debe comprobar si aun no se ha sobrepasado 
        # el limite de creacion de numero de deberes
        if self.punteroNoItems<self.MAX_ITEMS:
            objeto_itemDeber=ItemDeber(idAlineacion=self.ESTADO_ALINEO,
                                       tamanoLetra=self.TAMANO_LETRA,
                                       texto=textoDeber)

            objeto_itemDeber.senal_deberCumplido.connect(self.borrar_itemDeber)

            # Al crear un 'objeto_itemDeber' este asigna de forma automatica un 'id' unico 
            # e irrepetible, y ese 'id' es el que se almacenara en la lista 'self.listIdsItemsVivos'
            self.listIdsItemsVivos.append(objeto_itemDeber.id)
            
            # Adjuntando el objeto 'itemDeber' dentro del 'QVBoxLayout' para que se pueda visualizar
            self.vbox.addWidget(objeto_itemDeber)

            # Tecnicamente esto no es necesario hacer en windows, pero en linux si no se almacena
            # una lista de las instancias de la clase 'ItemDeber' marca error al querer eliminar
            # un 'itemDeber' de 'QVBoxLayout'
            self.listPunterosItems.append(objeto_itemDeber)
            self.punteroNoItems+=1

        else:
            mensaje="El numero maximo numero de deberes que\n"
            mensaje+=f"puedes registrar es de: {self.MAX_ITEMS} deberes\n"  
            mensaje+=f"y usted ya ha creado {self.MAX_ITEMS} deberes."
            ventanaDialogo = QMessageBox()
            ventanaDialogo.setIcon(QMessageBox.Information)
            ventanaDialogo.setWindowIcon( QIcon(self.ICONO_APLICACION)  )
            ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

            ventanaDialogo.setText(mensaje)
            ventanaDialogo.setStandardButtons(QMessageBox.Ok)
            btn_ok = ventanaDialogo.button(QMessageBox.Ok)
            btn_ok.setText('Entendido')
            ventanaDialogo.exec_()

    def borrar_itemDeber(self,idItemAMatar):
        '''
        Borrara el 'itemDeber' que el usuario ha indicado que ya 
        ha cumplido,  por consuente este 'itemDeber' debera eliminarse
        del 'QVBoxLayout' que muestra todos los 'itemDeber' que el 
        usario ha escrito pero aun no ha cumplido.

        Parámetros:
            idItemAMatar -- representa el valor del 'id' que se va a eliminar
            del 'QVBoxLayout'
        
        Importante: 
            Cuando se manda a eliminar al objeto 'itemDeber' cuyo 'id' es igual al valor
            que tomara el parametro 'idItemAMatar', este objeto no se eliminara de la 
            lista  'self.listPunterosItems' hasta que se manda eliminar otro objeto, es
            decir desaparecera de esa lista hasta que se elimine otro, y el otro objeto
            no se eliminara de esa lista hasta que se mande a eliminar al otroOtro.Esto
            se implemento para que esto funcionara en el sistema operativo 'linux'

            Es importante recordar que la lista 'self.listPunterosItems' almacena las
            direcciones de memoria de los objetos 'itemDeber'

            Debido a lo que se menciono anteriormente es necesario el atributo: 
            'self.siguienteItemEliminar'.
        '''

        logger.debug('Solicitud de eliminar el itemDeber con id={}, recibida'.format(idItemAMatar))

        # La lista 'self.listIdsItemsVivos' almacena todos los 'id' de todos los 'itemDeber' en forma de cola
        # El 'QVBoxLayout' almacena todos los 'itemDeber' como si fuera una lista y en forma de  cola
        # Si se desea eliminar el 'itemDeber' del 'QVBoxLayot' debemos indicarle en que posición del 'QVBoxLayot' 
        # se encuentra dicho 'itemDeber'.
        # Si tenemos el 'id' del 'itemDeber' que se desea eliminar, bastara con encontrar en
        # que posición de la lista 'self.listIdsItemsVivos' se encuentra  dicho 'id' para saber indirectamente en que 
        # posición se encuentra en el 'QVBoxLayout'.
        posObjeto_itemDeber_matar=self.listIdsItemsVivos.index(idItemAMatar)

        logger.debug('Posición del itemDeber obtenida={} '.format(posObjeto_itemDeber_matar))

        objeto_itemDeber_matar = self.vbox.itemAt(posObjeto_itemDeber_matar).widget()
        # Eliminando el objeto 'itemDeber' de la lista layout 
        self.vbox.removeWidget(objeto_itemDeber_matar)
        # Eliminando el objeto 'itemDeber' de la GUI
        objeto_itemDeber_matar.setParent(None)
        # Eliminando el 'id' del objeto 'itemDeber', de la lista de 'id' de los objetos 'itemDeber'
        self.listIdsItemsVivos.pop(posObjeto_itemDeber_matar)

        if self.siguienteItemEliminar!=None:
            #print("Muerte ha*************************************************************",self.siguienteItemEliminar)
            #print("Sentencia para********************************************************",posObjeto_itemDeber_matar)
            self.listPunterosItems.pop(self.siguienteItemEliminar)
            self.siguienteItemEliminar=posObjeto_itemDeber_matar
        else:
            #print("Setencia para**************************************************************",posObjeto_itemDeber_matar)
            self.siguienteItemEliminar=posObjeto_itemDeber_matar

        self.punteroNoItems -= 1


################################################################################################################################
#  RESPALDO  DE   LA    INFORMACIÓN
################################################################################################################################
           
    def cargarDeberes(self):
        '''
        Abrira el archivo  que almacena  los datos  de todos los deberes creados  antes de cerrar por ultima 
        vez el programa.El archivo que se abrira sigue el siguiente formato: 
            tipoAlineacion,tamanoLetra ^ deber_1 ^ deber_2 ^ .... ^ deber_n
                  donde: 
                        1) '^' es el 'SEPARADOR_DEBERES'
                        2) ',' es el separador que separa el 'tipoAlineacion 'del tamaño de letra
                        3) 'tipoAlineacion' representa la posición que tenia el texto de los deberes
                        antes de que el programa fuera cerrado, 'tipoAlineacion' solo puede tener 
                        como valor lo siguientes numeros:
                           '0' si es alineación a la izquierda
                           '1' si es alineación al centro
                           '2' si es alineación a la derecha
                        4) tamanoLetra es un numero entero indica el tamaño de letra que tenian las 
                        deberes antes de que el programa fuera cerrado 
        '''

        logger.debug('Cargando deberes guardados')
        
        datos=""
        try:
            logger.debug( 'Abriendo al archivo: {} para cargar los datos de los deberes guardados la ultima vez'.format(App_Deberes.ARCHIVO_DEBERES) )
            with open(App_Deberes.ARCHIVO_DEBERES,'r') as archivoDeberes:
                datos=archivoDeberes.read()
        except FileNotFoundError:
            logger.warning("Archivo que almacena los deberes no encontrado: {}".format(App_Deberes.ARCHIVO_DEBERES))
        except Exception as e:
            logger.error( "Error al abrir el archivo que almacena los deberes: {}".format(e) )
            sys.exit( "Error al abrir el archivo que almacena los deberes: {}".format(e) ) 
        
        # Guardando los deberes en un lista
        listaDatos_deberes=datos.split(App_Deberes.SEPARADOR_DEBERES)
        confiConArchivo_exitosa=False
        
        logger.debug("Lista de los datos de los deberes cargada: {}".format(listaDatos_deberes))


        # Los elementos de la lista son : [  'tipoAlineacion,tamanoLetra',  'deber_1',  'deber_2', ....'deber_n'  ]
        # por tal motivo se exige que la lista tenga como minimo mas de 1 elemento ya que el primer elemento de esta
        # son los valores de letra y posicion de los deberes
        if len(listaDatos_deberes)>1 and type(listaDatos_deberes)==list:
            try:
                # obteniendo el valor de alineacion y el tamaño de letra los cuales vienen en el primer
                # elemento de la lista, pero como estan separados entre comas y aparte son numeros enteros
                # entonces se prosigue a realizar lo siguiente:
                self.ESTADO_ALINEO,self.TAMANO_LETRA=[ int(x) for x in listaDatos_deberes[0].split(",")  ]
                
                logger.debug("Alineacion obtenida={}  Tamano de letra obtenida={}".format(self.ESTADO_ALINEO,self.TAMANO_LETRA))
    
                # Seleccionando la 'QAction' que corresponde al tipo de alineación cargada
                if self.ESTADO_ALINEO==0: 
                    self.alineacion_izquierda.trigger()
                elif self.ESTADO_ALINEO==1:
                    self.alineacion_centro.trigger()
                elif self.ESTADO_ALINEO==2:
                    self.alineacion_derecha.trigger()

                logger.debug("Deberes obtenidos={}".format(listaDatos_deberes[1:]))

                # el texto de los deberes se encuentra a partir de la posición 1 de la lista, por ende
                # apartir de esa posición se empieza a iterar para obtener el texto de los deberes
                for textoDeber in listaDatos_deberes[1:]:
                    # creando un 'itemDeber' y mostrandolo en el 'QVBoxLayout' donde se ven todos los 
                    # deberes creados por el usuario
                    self.agregarNuevo_itemDeber(textoDeber)
                confiConArchivo_exitosa=True

            except Exception as e:
                logger.error(f"Error al procesar la 'listaDatos_deberes' error={e}")
                sys.exit( f"Error al procesar la 'listaDatos_deberes' error={e}" ) 

        # Si el abrir el archivo y recuperar los datos no ocurrio de manera exitosa
        # entonces se prosegue a cargar los datos default.
        if not(confiConArchivo_exitosa):
            self.alineacion_izquierda.trigger()            
            self.ESTADO_ALINEO=0   #0=IZQUIERDA, 1=CENTRO, 2=DERECHA
            self.TAMANO_LETRA=12

    def respaldarDeberes(self):
        '''
            El archivo que almacena deberes sigue el siguiente formato: 
            tipoAlineacion,tamanoLetra ^ deber_1 ^ deber_2 ^ .... ^ deber_n
                    donde: 
                        1) '^' es el 'SEPARADOR_DEBERES'
                        2) ',' es el separador que separa el 'tipoAlineacion 'del tamaño de letra
                        3) 'tipoAlineacion' representa la posición que tenia el texto de los deberes
                        antes de que el programa fuera cerrado, 'tipoAlineacion' solo puede tener 
                        como valor lo siguientes numeros:
                            '0' si es alineación a la izquierda
                            '1' si es alineación al centro
                            '2' si es alineación a la derecha
                        4) tamanoLetra es un numero entero indica el tamaño de letra que tenian los 
                        deberes antes de que el programa fuera cerrado 
        '''

        logger.debug('Iniciando el proceso de  respaldar los datos de los deberes')
        listaDatos_respaldar=[]
        listaDatos_respaldar.append( str(self.ESTADO_ALINEO)+","+str(self.TAMANO_LETRA)  )

        # Iterando sobre cada  'lineEdit_deber' de cada 'itemDeber' con el fin de obtener el texto de cada deber
        # escrito por el usuario 
        for noItem in range( self.punteroNoItems ):        
            objeto_itemDeber = self.vbox.itemAt(noItem).widget()
            listaDatos_respaldar.append( objeto_itemDeber.lineEdit_deber.text() )        
        
        contenidoArchivo=App_Deberes.SEPARADOR_DEBERES.join(listaDatos_respaldar)

        logger.debug( "Lista de datos a respaldar generada: {}".format(listaDatos_respaldar) )
        logger.debug("Abriendo archivo: {} para guardar los datos de la lista".format(App_Deberes.ARCHIVO_DEBERES) )
        with open(App_Deberes.ARCHIVO_DEBERES,'w') as archivoDeberes:
            archivoDeberes.write(contenidoArchivo)
            logger.debug("Datos guardados con exito en el archivo")
        

def main():
    app = QApplication(sys.argv)
    ex = SeccionDeberes()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()