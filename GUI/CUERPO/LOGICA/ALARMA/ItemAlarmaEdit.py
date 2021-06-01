from PyQt5.QtWidgets import QMenu,QCompleter
from PyQt5.QtCore import Qt,QEvent,pyqtSignal,QTime,QRegExp
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import  QRegExpValidator,QIcon
import textwrap
from PyQt5 import QtWidgets
import os
###############################################################
#  IMPORTACION DEL DISEÑO...
##############################################################
from CUERPO.DISENO.ALARMA.itemAlarmaEdit_dise import Ui_Dialog

###############################################################
#  MIS LIBRERIAS...
##############################################################
from CUERPO.LOGICA.ALARMA.alarma import Alarma
from CUERPO.LOGICA.ALARMA.baseDatos_alarma import BaseDatos_alarmas
from CUERPO.LOGICA.ALARMA.reproductorSonidosAlarmas import ReproductorSonidosAlarmas
from  recursos import App_Alarmas,HuellaAplicacion


class ItemAlarmaEdit(QtWidgets.QDialog,Ui_Dialog,HuellaAplicacion):
    '''
    Esta clase sirve para editar o crear alarmas, si:
        A)Se crea una alarma se emitira la senal cuyo nombre es: 'senal_alarmaCreada'
        B)Se edita una alarma emitira la senal cuyo nombre es: 'senal_alarmaEditada'  
    '''

    senal_alarmaCreada=pyqtSignal(list)  # una lista con un solo elemento el cual sera una 
    #instancia de la clase 'Alarma' la cual contendra  los datos de la alarma creada

    senal_alarmaEditada=pyqtSignal(list) # una lista con un solo elemento el cual sera una 
    # instancia de la clase 'Alarma' la cual contendra  los datos de la alarma editada

    senal_editorCreador_cerrado=pyqtSignal(bool) # dicha señal se emitiara cuando este cuadro de dialogo
    # este por cerrarse.

    LISTA_REPRODUCCION_USUARIO=1
    LISTA_REPRODUCCION_DEFAULT=0

    def __init__(self):
        Ui_Dialog.__init__(self)
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.ApplicationModal)
        HuellaAplicacion.__init__(self)
        

        self.baseDatosAlarmas=BaseDatos_alarmas(App_Alarmas.NOMBRE_BASE_DATOS_ALARMAS)
        self.reproductor=ReproductorSonidosAlarmas(
            self,direccionCarpetas=App_Alarmas.CARPETA_MUSICA,
            listasNombresCarpetas=(App_Alarmas.CARPETA_MUSICA_DEFAULT,App_Alarmas.CARPETA_MUSICA_MIA)
        )

        self.restringirLasEntradas()


        self.tuplaDias_rb=(self.cB_1, self.cB_2, self.cB_3, self.cB_4,
        self.cB_5, self.cB_6, self.cB_7  )

        self.btn_finalizar.clicked.connect(self.terminar)
    
        self.listWid_soniMio.currentRowChanged.connect(self.reproducirSonidoAlarma)
        self.listWid_soniDef.currentRowChanged.connect(self.reproducirSonidoAlarma)
   
     
        # estableciendo opciones a partir del clic derecho a los items de la lista
        # de las canciones de la lista de reproduccion del usuario
        self.listWid_soniMio.installEventFilter(self)
 

        #self.btn_addCancion.clicked.connect(self.agregarUnaCancion)
        #Parece ser que el usuario QUIERE agregar una cancion, por ende
        #se le notifica al reproductor para que el inicie el proceso. 
        self.btn_addCancion.clicked.connect(lambda : self.reproductor.agregarUnaCancion(idListaAlmacenara=self.LISTA_REPRODUCCION_USUARIO) )
        
        #Este metodo agregara el nombre de la cancion que se agrego de manera
        #oficial, es decir la cancion que el usuario escogio y que el 'reproductor' 
        #la copio con exito en la carpeta respectiva 
        self.reproductor.senal_cancionAgregada.connect(lambda nombreSonido : self.listWid_soniMio.addItem(nombreSonido))
       

        # Cuando cambiemos a la otra lista de reproduccion los valores
        # de la otra se inicializaran a cero...
        self.tabWid_sonidosAlarmas.currentChanged.connect(self.cambioDeListaReproduccion)


    def modoTrabajo(self,modoEdicion=False,idAlarma=None):
        """
        Actualiza la lista de alarmas del reproductor de musica por si hay alguna alarma eliminada 
        u agregada,  
        En funcion del valor que puede tomar el parametro 'modoEdicion' tiene
        un comportamiento diferente, es decir si el parametro 'modoEdicion' toma:
            A)El valor de 'True', carga el contenido de la alarma cuyo 'id' es igual al valor que
            tome el parametro 'idAlarma' el cual representa el 'id' de la alarma que se desea editar
            B)El valor de 'False', muestra todos los apartados de la widget con los valores default 
            de una alarma 
        Parámetros:
            modoEdicion -- dato de tipo 'bool' en donde si:
                    A) modoEdicion=True, significa que se desea editar una alarma
                    B) modoEdicion=False, significa que se desea crear una alarma
            idAlarma -- dato de tipo 'int' que representa el 'id' de la alarma que se desea editar.
        """

        self.reproductor.cargarNombresCanciones()

        # borrando el contenido de las: 'listWidget' para posteriormente ser actualizados
        self.listWid_soniMio.clear()
        self.listWid_soniDef.clear()
        
        self.cargarSonidosEnListas()

        # el atributo de instancia 'self.dictNombresAlarmasYaCreaas' es un diccionario donde 
        # los 'keys' son los nombres de todas las alarmas, y sus 'values' son siempre 'True' 
        # en todos los casos
        #   Ejemplo:
        #       {"nombre_1":True, "nombre_2":True ... "nombre_n":True} , con esto la busqueda de la
        #       existencia de una alarma sera mas rapida
        self.dictNombresAlarmasYaCreadas=dict( [ (nombre,True)  for nombre in self.baseDatosAlarmas.getNombresAlarmas() ] )
    
        self.modoEdicion=modoEdicion
        self.mostrarNombresAlarmas()
        
        # Si se quiere editar una alarma
        if modoEdicion:
            if idAlarma:
                self.idAlarmaEditara=idAlarma

                # consultamos todos los datos de la alarma que se quiere editar
                alarma=self.baseDatosAlarmas.getAlarma(idAlarma=idAlarma)

                self.nombreAlarmaEditar=alarma.nombre # el nombre es el id de cada alarma registrada

                self.mostrarAlarmaEditar(alarma) # se cargan los datos de la alarma a editar en la widget

                self.selecSonidoAlarma(nombreCancionAlarma=alarma.sonido )# se seleccionada la cancion
                # de la alarma que se desea editar

                # eliminando del diccionario de alarmas el nombre de esta alarma
                del self.dictNombresAlarmasYaCreadas[alarma.nombre]
        
        #Si se quiere crear una nueva alarma
        else:
            self.idAlarmaEditara=None

            #el sonido default de la alarma es no tener sonido, por eso cargamos esa opcion
            self.mostrarAlarmaBlanco()
            
            #print("Mostrando cancion NULA PORQUE SE DECIDIO CREAR UNA ALARMA")
            self.selecSonidoAlarma(nombreCancionAlarma=None) 
        

###############################################################################################################
# SONIDO DE LA ALARMA
###############################################################################################################

    def cargarSonidosEnListas(self): 
        """
        Carga en las 'listWidget' el nombre de las canciones, es decir:
            1)La 'listWidget' que muestra las canciones por defecto atraves de este metodo
            cargara todos los nombres de  las canciones por defecto.
            2)La 'listWidget' que muestra las canciones agregadas por el usuario a traves 
            de este metodo cargara todos  los nombres de las  canciones descargadas
        """

        # cargando los nombres de las canciones default:
        listaCanciones=self.reproductor.getNombresCanciones(idListaReproduccion=self.LISTA_REPRODUCCION_DEFAULT)
        # el primer item de la lista sera la opccion: 'cancionNula'
        self.listWid_soniDef.addItem(App_Alarmas.NOMBRE_SONIDO_NULL)
        for cancion in listaCanciones:
            self.listWid_soniDef.addItem(cancion)

        # cargando los nombres de las canciones del usuario:
        listaCanciones=self.reproductor.getNombresCanciones(idListaReproduccion=self.LISTA_REPRODUCCION_USUARIO)
         # el primer item de la lista sera la opccion: 'cancionNula'
        self.listWid_soniMio.addItem(App_Alarmas.NOMBRE_SONIDO_NULL)
        for cancion in listaCanciones:
            self.listWid_soniMio.addItem(cancion)
  

    def selecSonidoAlarma(self,nombreCancionAlarma=None):
        """
        Mostrara la pestaña del 'TabWidget' que contiene la lista de reproduccion que contiene
        el: 'nombreCancionAlarma' posteriormente seleccionara el item cuyo nombre es igual a: 
        'nombreCancionAlarma', si 'nombreCancionAlarma'=None, significara que  se desea seleccionar
        la opción 'App_Alarmas.NOMBRE_SONIDO_NULL'.o en otras palabras la que dice: 'SIN CANCION' si el 'nombreCancionAlarma' 
        no existe en la lista de reproduccion, se notificara con un mensaje emergente
        """

    
        idLista_estaCancion=None

        # se desconecta la señal ya que a la hora de seleccionar la pestaña de la
        # lista de reproduccion, no queremos que haga el comportamiento predeterminado
        self.tabWid_sonidosAlarmas.currentChanged.disconnect(self.cambioDeListaReproduccion)

        if nombreCancionAlarma:    
            nombreCancionPartes=os.path.normpath(nombreCancionAlarma).split(os.sep)
            nombreCancionAlarma = nombreCancionPartes[-1]
            print("Cancion que se desea seleccionar:",nombreCancionAlarma)
            #rutaCancion=os.sep.join( nombreCancionPartes[:-1] )
        
        # Carga la canción y retorna el 'id' de la lista de reproduccion en la cual se encuentra
        # en caso de no existir dicha canción retornara el valor igual a -1.
        idLista_estaCancion=self.reproductor.cargarCancion(nombreCancion=nombreCancionAlarma)

        if idLista_estaCancion==None:
            self.tabWid_sonidosAlarmas.setCurrentIndex(0)
            self.listWid_soniDef.setCurrentRow(0)
        
        elif idLista_estaCancion>=0:
             # En la pestaña 0  se encunetra la 'listWiget' de canciones default
             # En la pestaña 1  se encunetra la 'listWiget' de canciones del usuario
            self.tabWid_sonidosAlarmas.setCurrentIndex(idLista_estaCancion)
        
            # Buscando en la list widget cual es la sonido de alarma elegido por el usuario
            # y posteriormente se selecciona
            if idLista_estaCancion==self.LISTA_REPRODUCCION_DEFAULT:
                listaWidget=self.listWid_soniDef
            elif idLista_estaCancion==self.LISTA_REPRODUCCION_USUARIO:
                listaWidget=self.listWid_soniMio
            try:    
                items=listaWidget.findItems(nombreCancionAlarma,QtCore.Qt.MatchCaseSensitive)
                items[0].setSelected(True)
                self.reproductor.tocar()
            except:
                self.mostrarCancionNoEncontrada(nombreCancionAlarma)

        else: # si no se encontro la cancion
            self.tabWid_sonidosAlarmas.setCurrentIndex(0)
            self.listWid_soniDef.setCurrentRow(0)
            self.mostrarCancionNoEncontrada(nombreCancionAlarma)

        self.tabWid_sonidosAlarmas.currentChanged.connect(self.cambioDeListaReproduccion)


    def cambioDeListaReproduccion(self,indice):
        """
        Cada vez que la GUI detecte que hay un cambio de vista entre las pestañas del 'TabWidget' 
        significara que el usuario cambio de lista  de reproduccion, asi que esto significa que 
        si hay una cancion sonando antes de cambiar a la otra lista de reproduccion, hay que
        pausarla.
        La lista de reproduccion que dejara de mostrarse para mostrarse la otra tomara el valor 
        de: 'App_Alarmas.NOMBRE_SONIDO_NULL'.
        """

        # pausando cualquier cancion que se este escuchando y poniendo como valor de
        # sonido de alarma, la opcion de 'App_Alarmas.NOMBRE_SONIDO_NULL'
        self.reproductor.pausar()
        self.reproductor.cargarCancion(nombreCancion=None)
        

        #El 'tabWidget' solo contiene dos ventanas
        #indice: 0 = la ventana donde viene la lista que muestra el nombre de las canciones defecto
        #indice: 1 = la ventana donde viene la lista que muestra el nombre de las canciones elegida por el usuario
        if indice==self.LISTA_REPRODUCCION_DEFAULT:
            self.listWid_soniDef.setCurrentRow(0)
        else:
            self.listWid_soniMio.setCurrentRow(0)


    def reproducirSonidoAlarma(self,indice):
        """
        Proseguira a reproducir la cancion u sonido seleccionado
        """
 
        #0 =carpeta de canciones defecto...
        #1 =carpeta de cancion mias...

        # Cuando se usa el metodo 'clean()'  en las 'listWidget' se activa
        # este metodo con un 'indice'=-1, por ende se hace esa validación
        # ya que en caso contrario colapsaria el programa.
        if indice>=0:
            nombreCancion=None
            idListaReproduccion=None
            if indice>0:
                idListaReproduccion= self.tabWid_sonidosAlarmas.currentIndex()

                if idListaReproduccion==self.LISTA_REPRODUCCION_USUARIO:
                    nombreCancion=self.listWid_soniMio.item(indice).text()
                elif idListaReproduccion==self.LISTA_REPRODUCCION_DEFAULT:
                    nombreCancion=self.listWid_soniDef.item(indice).text()
                    
            self.reproductor.cargarCancion( nombreCancion=nombreCancion,
                                            idListaAlmacenaCancion=idListaReproduccion)
            self.reproductor.tocar()


    def eventFilter(self, source, event):
        """
        Cada vez que alguien haga click derecho sobre algun item de la 
        'listWid_soniMio' significara que probablemente quiera borrar 
        esa canción asi que debe  mostrar la opcion de borrar, y en caso 
        de ser seleccionada dicha opcion se mandara a borrar a dicha cancion
        """

        if event.type() == QEvent.ContextMenu and source is  self.listWid_soniMio:
            menu = QMenu()
            menu.addAction("eliminar")  # menu.addAction("eliminar",metodoA_llamar)
            
            #print("Clic derecho")
            #item = source.itemAt(event.pos())
            #indice=self.listWid_soniMio.currentIndex().row()
            #cancionEliminar=self.listWid_soniMio.item(indice).text()
            #print(f"Indice {indice} indice{event.pos()}  cancionEliminar{cancionEliminar}")
               
            if menu.exec_(event.globalPos()):                
                self.eliminarCancion()

            return True
        return super().eventFilter(source, event)
    
    def eliminarCancion(self):
        """
        Comprobara cual es el item que se quiere eliminar de la 'listWid_soniMio', si es el 
        item 0(App_Alarmas.NOMBRE_SONIDO_NULL), mostrara un cuadro de dialogo explicando que 
        dicho item no se puede borrar, pero si es otro item diferente el que se quiere borrar 
        lo primero que hara es hacer un consulta a la base de datos de las alarmas con la 
        finalidad de obtener el nombre de las alarmas que utilizan esa cancion como sonido
        de alarma, posteriormente mostrara un cuadro de dialogo explicando cuales son las 
        alarmas que se verian afectadas si se decide eliminar dicha canción y como las afectaria,
        si el usuario procede a querer eliminar la cancion, se borrara la cancion de la carpeta,
        tambien de la 'listWid_soniMio' y las alarmas que tenian esa cancion como sonido de alarma
        ahora tendran como sonido de alarma a: App_Alarmas.NOMBRE_SONIDO_NULL
        """

        indice=self.listWid_soniMio.currentIndex().row()
        cancionEliminar=self.listWid_soniMio.item(indice).text()

        # quiere eliminar la opccion default
        if indice==0:
            self.mostrarAlerta_noSeEliminaPrimera()

        # quiere eliminar una cancion que un dia el subio
        else:
            # hacemos esto:  'self.reproductor.carpetaMusicaMia+cancionEliminar', por que en la base de datos
            # los nombres de los sonidos de alarmas le antece el nombre de la carpeta en la cual estan almacenados  
            alarmasAfectadas=self.baseDatosAlarmas.getNombresAlarmasCon(cancion=App_Alarmas.CARPETA_MUSICA_MIA+cancionEliminar)
            desicionEliminarCancion=self.mostrarAlertaEliminarCancion(cancionEliminar,alarmasAfectadas)
            if desicionEliminarCancion:

                #  eliminando la cancion del reproductor(elimina la cancion de la carpeta y tambien
                #  de la lista en la que tiene almacenado el nombre)
                self.reproductor.eliminarMiCancion(nombreCancion=cancionEliminar,
                                                  idListaAlmacenaCancion=self.tabWid_sonidosAlarmas.currentIndex())

                # eliminamos la cancion de la list widget
                self.listWid_soniMio.takeItem(indice)

                # actualizando la base de datos, por si habia una alarma que usara como 
                # sonido de alarma la cancion que se elimino
                self.baseDatosAlarmas.eliminarCancion(
                    cancionEliminar=App_Alarmas.CARPETA_MUSICA_MIA+cancionEliminar,
                    cancionDefault=None)

                # cuando se elimine la cancion, la que ahora se seleccionara sera la opcion:
                # App_Alarmas.NOMBRE_SONIDO_NULL
                self.listWid_soniMio.setCurrentRow(0)

                self.reproductor.cargarCancion()
                self.reproductor.tocar()
                
                
###############################################################################################################
# SONIDO DE LA ALARMA
###############################################################################################################

    def mostrarNombresAlarmas(self):
        '''
        Este metodo cargara los nombres de alarmas ya existentes en el line edit donde se pone 
        el nombre de alarma, con el fin de que el usuario pueda darse cuenta que nombres de alarmas 
        ya existen y por lo tanto ya no estan disponibles.
        '''

        acompletador=QCompleter(list(self.dictNombresAlarmasYaCreadas) )
        self.lineEdit_nombre.setCompleter(acompletador)

    def restringirLasEntradas(self):
        '''
        Este metodo restrgira  ciertos caracteres en el lineEdit el cual es el elemento
        en donde se pone el  nombre de la alarma,las restricciones son las siguientes:
            A)El nombre de alarma no puede contener espacios en blanco
            B)El nombre de alarma no puede tener mas de 15 caracteres
            C)El nombre de alarma solo puede usar letras(minusculas y mayusculas)
            y solo numeros naturales
        '''

        # validacion del nombre de usuario...
        validator = QRegExpValidator(QRegExp("[0-9a-zA-Z]{1,15}"))  # maximo solo 15 caracteres
        self.lineEdit_nombre.setValidator(validator)

    def comprobarSiDatosCorrectos(self):
        ''' 
        Este metodo comprobara que todos los datos de la alarma ingresados
        por el usuario esten correctos, en caso de que no, le explicara al
        usuario las razones y retornara False, en caso de que esten correctos
        todos los datos retornara True.

        Returns(devoluciones):
            dato de tipo 'bool' igual a True en caso de que los datos esten correctos
            dato de tipo 'bool' igual a False en caso de que los datos esten incorrectos
        '''

        mensajeError=""
        datosCorrectos=True
        nombreAlarma=self.lineEdit_nombre.text()
        if nombreAlarma=="" or nombreAlarma==None:
            mensajeError="Debes asignar un nombre a la alarma"
            datosCorrectos=False
        #si ya existe el nombre de la alarma
        elif self.dictNombresAlarmasYaCreadas.get(nombreAlarma,False):
            nombreAlarmasExistentes= ",".join( list(self.dictNombresAlarmasYaCreadas.keys())  )
            mensajeError="Ya existe una alarma con el nombre de :{}".format(nombreAlarma)
            mensajeError+=", los nombres  de alarmas existentes son:{}".format(nombreAlarmasExistentes)
            mensajeError+=" y no puede elegir ninguno de ellos como nombre de alarma."
            mensajeError=textwrap.fill(mensajeError,len("mi longitud deseada es la siguiente para"))
            datosCorrectos=False
        
        if mensajeError:
            ventanaDialogo = QMessageBox()
            ventanaDialogo.setIcon(QMessageBox.Critical)
            ventanaDialogo.setWindowIcon( QIcon(self.ICONO_APLICACION)  )
            ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)


            ventanaDialogo.setText(mensajeError)
            ventanaDialogo.setStandardButtons(QMessageBox.Ok)
            btn_ok = ventanaDialogo.button(QMessageBox.Ok)
            btn_ok.setText('Entendido')
            ventanaDialogo.exec_()
            return datosCorrectos
        return datosCorrectos


    def mostrarAlarmaBlanco(self):
        """
        Cargara los datos default de un objeto de tipo alarma en la widget 
        """

        self.mostrarAlarmaEditar( Alarma() )
        
 
    def mostrarAlarmaEditar(self,alarma):
        """
        Cargara los datos de un objeto de tipo 'Alarma'  en la widget
        
        Parámetros:
            alarma -- una instancia de la clase 'Alarma' que contendran
            los datos de la alarma que la widget mostrara
        """

        #cargando el nombre de la alarma
        self.lineEdit_nombre.setText(alarma.nombre)

        #cargando los dias de la alarma
        for c,diaRequerido in enumerate(alarma.diasActiva):
            if diaRequerido:
                self.tuplaDias_rb[c].setChecked(True)
            else:
                self.tuplaDias_rb[c].setChecked(False)

        #seleccionando el asunto de la alarma
        self.comBox_asunto.setCurrentIndex(alarma.asunto)

        #mostrando la hora a la cual sonara la alarma
        horaAlarma=QTime()
        horaAlarma.setHMS(alarma.horaAlarma.hora,alarma.horaAlarma.minuto,0)
        self.timeEdit_hora.setTime( horaAlarma )


    def terminar(self):
        """
        Carga todos los datos ingresados por el usuario en la widget, posteriormente dichos datos 
        los utiliza  para crear un objeto de tipo 'Alarma', despues  procede a  emitir la señal cuyo
        nombre es: 'senal_alarmaEditada' la cual mandara la instancia de alarma creada
        pero contenida en una lista.
        Si hay algun dato erroneo se le avisara al usuario.
        """

        if self.comprobarSiDatosCorrectos():
            #obteniendo el nombre de la alarma
            nombre=self.lineEdit_nombre.text()

            #obteniendo el nombre de la cancion con ruta completa...
            sonido=self.reproductor.getNom_cancionSelec_guardaBase()


            #Guardando los dias que son...
            diasActiva=[0,0,0,0,0,0,0] 
            for c,rb_dia in enumerate(self.tuplaDias_rb):
                if rb_dia.isChecked():
                    diasActiva[c]=1

            #Guardando el asunto:
            asunto=self.comBox_asunto.currentIndex()

            #obteniendo la hora a la cual se ejecutara la alarma
            hora=self.timeEdit_hora.time().hour()
            minuto=self.timeEdit_hora.time().minute()

            alarma=Alarma(nombre=nombre,sonido=sonido,asunto=asunto,hora=hora,minuto=minuto,diasActiva=diasActiva)
        
            #si no estabamos en modo de edicion, significa que estamos
            #creando una alarma mas 
            if not(self.modoEdicion):
                #registrar los datos de la nueva alarma en la base de datos

                id_asignadoAlarma=self.baseDatosAlarmas.addAlarma(alarma)
                alarma.id=id_asignadoAlarma

                #informando acerca de la nueva alarma creada
                self.senal_alarmaCreada.emit([alarma])

            else:
                #informado acerca de la alarma ya editada
                alarma.id=self.idAlarmaEditara
                self.baseDatosAlarmas.actualizarAlarma(alarma)
                self.senal_alarmaEditada.emit([alarma])
                
            self.close()

    def closeEvent(self,event):
        '''
        Antes de cerra la widget, pausara la reproduccion de una posible cancion que
        se este ejecutando. 
        '''

        self.reproductor.detener()
        self.senal_editorCreador_cerrado.emit(True)



###############################################################################################################
# VENTANAS DE DIALOGO 
###############################################################################################################

    def mostrarCancionNoEncontrada(self,nombreCancion):
        '''
        Mostrara un cuadro de dialogo informando que la canción no fue encontrada, 
        dicha canción es el valor que tomara el  parametro 'nombreCancion'

        Parámetros:
            nombreCancion -- dato de tipo 'str' que almacenara el nombre de 
            la canción que no fue encontrada.
        '''

        mensaje="""La cancion cuyo nombre es:'{}' 
que escogiste como tu sonido de alarma 
ha sido eliminada, por tal motivo deberias
escoger otra cancion como sonido de alarma""".format(nombreCancion)

        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Information)
        ventanaDialogo.setWindowIcon( QIcon(self.ICONO_APLICACION)  )
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Ok)
        btn_ok = ventanaDialogo.button(QMessageBox.Ok)
        btn_ok.setText('Entendido')
        ventanaDialogo.exec_()
    
    def mostrarAlertaEliminarCancion(self,cancionEliminar,nombresAlarmasAfectadas):
        '''
        Le mostrara a las alarmas que se verian afectadas si elimina la cancion: 'cancionEliminar' 
        y que es lo que pasaria con ellas

        Returns(devoluciones):
            Dato de tipo 'bool'=True  si el usuario sigue queriendo eliminar la canción
            Dato de tipo 'bool'=False si el usuario ya no desea eliminar la canción
        '''

        #si no hay ninguna alarma afectada
        if nombresAlarmasAfectadas==[]:
            mensajeAdvertencia="¿Estas seguro de querer eliminar la cancion:\n'{}' ?".format(cancionEliminar)
        
        # si hay almeos una alarma afectada
        else:
            alarmasAfectadas=",".join( nombresAlarmasAfectadas ) 
            mensajeAdvertencia="""Las alarmas:{} 
tienen la cancion:' {} ' 
como sonido de alarma, si eliminas esta cancion
el sonido de alarma de dichas alarmas cambiara  
a ser igual a 'NULL', es decir 'sin musica'
¿Estas seguro de eliminar la cancion?""".format(alarmasAfectadas,cancionEliminar)


        #Cuadro de dialogo de advertencia si elimina esa alarma
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Warning)
        ventanaDialogo.setWindowIcon( QIcon(self.ICONO_APLICACION)  )
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        ventanaDialogo.setText(mensajeAdvertencia)
        ventanaDialogo.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        btn_yes = ventanaDialogo.button(QMessageBox.Yes)
        btn_yes.setText('Si')
        btn_no = ventanaDialogo.button(QMessageBox.No)
        btn_no.setText('No')
        ventanaDialogo.exec_()
        if ventanaDialogo.clickedButton()  ==  btn_yes:
            return True
        else:
            return False

    def mostrarAlerta_noSeEliminaPrimera(self):
        '''
        Mostrara un cuadro de dialogo con la intencia de informarle
        al usuario que no se puede eliminar el item: 'App_Alarmas.NOMBRE_SONIDO_NULL'
        '''

        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Information)
        ventanaDialogo.setWindowIcon( QIcon(self.ICONO_APLICACION)  )
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        ventanaDialogo.setText("No puedes eliminar la opcion default")
        ventanaDialogo.setStandardButtons(QMessageBox.Ok)
        btn_ok = ventanaDialogo.button(QMessageBox.Ok)
        btn_ok.setText('Entendido')
        ventanaDialogo.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = ItemAlarmaEdit()
    application.show()
    app.exec()
    #sys.exit(app.exec())