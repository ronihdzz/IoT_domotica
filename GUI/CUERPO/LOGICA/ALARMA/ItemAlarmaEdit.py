from PyQt5.QtWidgets import QMenu,QCompleter
from PyQt5.QtCore import Qt,QEvent,pyqtSignal,QTime,QRegExp
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import  QRegExpValidator,QIcon
import textwrap
from PyQt5 import QtWidgets

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
    '''Esta clase sirve para editar o crear alarmas, si:
        A)Se crea una alarma se emitira la senal cuyo
        nombre es: 'senal_alarma'
        B)Se edita una alarma emitira la senal cuyo
        nombre es: 'senal_alarmaEditada'  '''

    senal_alarmaCreada=pyqtSignal(list) #una lista con un solo elemento el cual sera  'unaInstanciaAlarma'
    #la cual contendra  los datos de la alarma creada

    senal_alarmaEditada=pyqtSignal(list)#una lista con un solo elemento el cual sera 'unaInstanciaAlarma'
    #la cual contendra los datos de la alarma creada

    senal_editorCreador_cerrado=pyqtSignal(bool)#dicha senal se emitiara cuando este cuadro de dialogo
    #este por cerrarse.

    def __init__(self):
        Ui_Dialog.__init__(self)
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.ApplicationModal)
        HuellaAplicacion.__init__(self)
        
        self.baseDatosAlarmas=BaseDatos_alarmas(App_Alarmas.NOMBRE_BASE_DATOS_ALARMAS)
        self.reproductor=ReproductorSonidosAlarmas(self,direccionCarpetas=App_Alarmas.CARPETA_MUSICA,
        carpetaMusicaDefault=App_Alarmas.CARPETA_MUSICA_DEFAULT,
        carpetaMusicaMia=App_Alarmas.CARPETA_MUSICA_MIA,
        cancionDefault=App_Alarmas.NOMBRE_SONIDO_NULL)

        self.restringirLasEntradas()

        self.reproductor.senal_cancionAgregada.connect(self.sonidoAlarmaAgregado)
            


        self.tuplaDias_rb=(self.cB_1, self.cB_2, self.cB_3, self.cB_4,
        self.cB_5, self.cB_6, self.cB_7  )

        self.btn_finalizar.clicked.connect(self.terminar)

        #reproducir una cancion cada vez que hagan click sobre la lista de reproduccion default
        self.listWid_soniDef.clicked.connect(self.reproducirSonidoAlarma)
        self.listWid_soniMio.clicked.connect(self.reproducirSonidoAlarma)

        #estableciendo opciones a partir del clic derecho a los items de la lista
        #de reproduccion del usuario
        self.listWid_soniMio.installEventFilter(self)

        #vinculando el boton de cargar cancion...
        self.btn_addCancion.clicked.connect(self.agregarUnaCancion)
        
        #Cuando cambiemos a la otra lista de reproduccion los valores
        #de la otra se inicializaran a cero...
        self.tabWid_sonidosAlarmas.currentChanged.connect(self.cambioDeListaReproduccion)


    def modoTrabajo(self,modoEdicion=False,nombreAlarma=None):
        """Actualiza la lista de alarmas del reproductor de musica
        por si hay alguna alarma eliminada u agregada.
        En funcion del valor que puede tomar el parametro 'modoEdicion' tiene
        un comportamiento diferente, es decir si el parametro 'modoEdicion' toma:
            A)El valor de 'True', carga el contenido de la alarma que se quiere editar
            B)El valor de 'False', muestra todos los apartados de la widget con los
            valores default de una alarma """

        self.reproductor.refrescarListaMisAlarmas()
        #borrando el contenido de las: 'listWidget'
        self.listWid_soniMio.clear()
        self.listWid_soniDef.clear()

        #los 'keys' son los nombres de todas las alarmas, y sus 'values' son siempre 'True' en todos los casos
        #   Ejemplo:
        #       {"nombre_1":True, "nombre_2":True ... "nombre_n":True} ,con esto la busqueda de la
        #       existencia de una alarma sera mas rapida
        self.dictNombresAlarmasYaCreadas=dict( [ (nombre,True)  for nombre in self.baseDatosAlarmas.getNombresAlarmas() ] )
    
        #Si se quiere editar una alarma
        if modoEdicion:
            if nombreAlarma:

                #consultamos todos los datos de la alarma que se quiere editar
                alarma=self.baseDatosAlarmas.getAlarma(nombreAlarma=nombreAlarma)

                self.nombreAlarmaEditar=alarma.nombre #el nombre es el id de cada alarma registrada

                self.mostrarAlarmaEditar(alarma)#cargamos los datos de la alarma en la widget

                self.mostrarSonidosParaAlarma(  alarma.sonido   )#mostramos la lista de sonidos
                #disponibles para elegir asi como seleccionamos el sonido que fue escogido previamente

                #eliminando del diccionario de alarmas el nombre de esta alarma
                del self.dictNombresAlarmasYaCreadas[alarma.nombre]
        
        #Si se quiere crear una nueva alarma
        else:
            #el sonido default de la alarma es no tener sonido, por eso cargamos esa opcion
            self.mostrarAlarmaBlanco()
            self.mostrarSonidosParaAlarma() 
        
        self.modoEdicion=modoEdicion
        self.mostrarNombresAlarmas()


###############################################################################################################
# SONIDO DE LA ALARMA
###############################################################################################################

    def mostrarSonidosParaAlarma(self,nombreSonidoAlarma=None): 
        """Carga en las 'listWidget' el nombre de las canciones, es decir
        la 'listWidget':
            1)Que muestra las canciones por defecto atraves de este metodo
            cargara todos los nombres de  las canciones por defecto.
            2)Que muestra las canciones agregadas por el usuario a traves de 
            este metodo cargara todos  los nombres de las  canciones descargadas
        """

        #cargando los nombres de las canciones default:
        listaCanciones=self.reproductor.listaCancionesDefault
        self.listWid_soniDef.addItem(App_Alarmas.NOMBRE_SONIDO_NULL)
        for cancion in listaCanciones:
            self.listWid_soniDef.addItem(cancion)

        #cargando los nombres de las canciones del usuario:
        listaCanciones=self.reproductor.listaCancionesMias
        self.listWid_soniMio.addItem(App_Alarmas.NOMBRE_SONIDO_NULL)
        for cancion in listaCanciones:
            self.listWid_soniMio.addItem(cancion)

        self.selecSonidoAlarma(nombreCancionAlarma=nombreSonidoAlarma)

        
        
    def selecSonidoAlarma(self,nombreCancionAlarma=None):
        """Seleccionara el item cuyo nombre es: 'nombreCancionAlarma', y mostrara
        la pestaña del 'TabWidget' que contiene la lista de reproduccion que contiene
        el: 'nombreCancionAlarma'.Si 'nombreCancionAlarma'=None, significara que 
        se seleccione la 'cancionNull' es decir la opcion de silencio.
        """

        #desconectamo es señal ya que a la hora de seleccionar la pestaña de la
        #lista de reproduccion, no queremos que haga el comportamiento predeterminado
        self.tabWid_sonidosAlarmas.currentChanged.disconnect(self.cambioDeListaReproduccion)
        if nombreCancionAlarma==None:
            nombreCancionAlarma=self.reproductor.getNombre_cancionDefault_guardaBase()

        if nombreCancionAlarma.startswith(self.reproductor.carpetaMusicaDefault):
            listaWidget=self.listWid_soniDef
            dirCarpeta=self.reproductor.carpetaMusicaDefault
            #En la pestaña 0  se encunetra la 'listWiget' de canciones default
            self.tabWid_sonidosAlarmas.setCurrentIndex(0)
            estaEnListaDefault=True 
        else:
            listaWidget=self.listWid_soniMio
            dirCarpeta=self.reproductor.carpetaMusicaMia
            #En la pestaña 1  se encunetra la 'listWiget' de canciones del usuario
            self.tabWid_sonidosAlarmas.setCurrentIndex(1)
            estaEnListaDefault=False
  
        #quitamos el nombre de la carpeta en el cual se encuentra la pestaña
        nombreCancionAlarma=nombreCancionAlarma.replace(dirCarpeta,"")
        
        #buscamos en la list widget cual es la sonido de alarma elegido por el usuario
        #y lo seleccionamos
        #listaWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        try:
            items=listaWidget.findItems(nombreCancionAlarma,QtCore.Qt.MatchCaseSensitive)
            items[0].setSelected(True)
            self.reproductor.cargarCancion(nombreCancion=nombreCancionAlarma,musicaDefault=estaEnListaDefault)
            self.reproductor.tocar()
        except:
            mensaje="""La cancion cuyo nombre es:'{}' 
que escogiste como tu sonido de alarma 
ha sido eliminada, por tal motivo deberias
escoger otra cancion como sonido de alarma""".format(nombreCancionAlarma)

            ventanaDialogo = QMessageBox()
            ventanaDialogo.setIcon(QMessageBox.Information)
            ventanaDialogo.setWindowIcon( QIcon(self.ICONO_APLICACION)  )
            ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

            ventanaDialogo.setText(mensaje)
            ventanaDialogo.setStandardButtons(QMessageBox.Ok)
            btn_ok = ventanaDialogo.button(QMessageBox.Ok)
            btn_ok.setText('Entendido')
            ventanaDialogo.exec_()
            self.reproductor.cargarCancion() #cargamos la cancion sin sonido 
            self.reproductor.tocar()

        #hacemos esto  para que no se sombree un item, almenos que sea con un click
        #self.listWid_soniDef.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        #self.listWid_soniMio.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

        #volvemos a ligar la señal que desconectamos...
        self.tabWid_sonidosAlarmas.currentChanged.connect(self.cambioDeListaReproduccion)

    def cambioDeListaReproduccion(self,indice):
        """Cada vez que la GUI detecte que hay un cambio de vista entre
        las pestañas del 'TabWidget' significara que el usuario cambio de lista 
        de reproduccion, asi que esto significa que si hay una cancion
        sonando antes de cambiar a la otra lista de reproduccion, hay que
        pausarla.La lista de reproduccion que dejara de mostrarse para mostrarse la otra
        tomara el valor de cancion por defecto.
        """
        
        #pausando cualquier cancion que se este escuchando y poniendo como valor de
        #sonido de alarma, la opcion de 'SIN MUSICA'
        self.reproductor.cargarCancion()
        self.reproductor.tocar() 


        #El 'tabWidget' solo contiene dos ventanas
        #indice: 0 = la ventana donde viene la lista que muestra el nombre de las canciones defecto
        #indice: 1 = la ventana donde viene la lista que muestra el nombre de las canciones elegida por el usuario
        estaEnListaDefault=not( indice )
        if estaEnListaDefault:
            listWidget=self.listWid_soniDef
        else:
            listWidget=self.listWid_soniMio

        #seleccionando el sonido defecto en la lista de reproduccion que 
        #dejara de mostrarse
        #listWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        listWidget.setCurrentRow(0)
        #listWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)


    def sonidoAlarmaAgregado(self,nombreSonido):
        """Este metodo agregara el nombre de la cancion que se agrego de manera
        oficial, es decir la cancion que el usuario escogio y que el 'reproductor' 
        la copio con exito en la carpeta respectiva """

        self.listWid_soniMio.addItem(nombreSonido)

    def agregarUnaCancion(self):
        """Parece ser que el usuario QUIERE agregar una cancion, por ende
        se le notifica al reproductor para que el inicie el proceso. 
        """
        self.reproductor.agregarUnaCancion()

    def reproducirSonidoAlarma(self,row):
        """Al hacer click sobre cualquier item de cualquier 'listWidget', este
        metodo lo seleccionara y despues proseguira a sonar la cancion u sonido
        corrrespodiente
        """

        #obteniendo el indice del item que recibio el click izquierdo
        indice=row.row()
        #0 =carpeta de canciones defecto...
        #1 =carpeta de cancion mias...
        estaEnListaDefault=not( self.tabWid_sonidosAlarmas.currentIndex()  )
        if estaEnListaDefault:
            listWidget=self.listWid_soniDef
        else:
            listWidget=self.listWid_soniMio

        #listWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        listWidget.setCurrentRow(indice)
        #listWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

        if indice>0:
            nombreCancion=listWidget.item(indice).text()#obtenemos el texto de la cancion
            #tocamo la cancion por medio del reproductor
            self.reproductor.cargarCancion(nombreCancion=nombreCancion,musicaDefault=estaEnListaDefault)
            self.reproductor.tocar()
        else:
            #si se selecciono el indice cero, significa que tomar el valor default
             #si no ponemos nada se se cargara la cancion default
            self.reproductor.cargarCancion()
            self.reproductor.tocar()

    def eventFilter(self, source, event):
        """Cada vez que alguien haga click derecho sobre algun
        item de la 'listWid_soniMio' significara que probablemente
        quiera borrar esa canción asi que le demos mostrar dicha
        opcion, y en caso de ser seleccionada ligarla con el metodo
        que permite borrar a la cancion
        """
        if event.type() == QEvent.ContextMenu and source is  self.listWid_soniMio:
            menu = QMenu()
            menu.addAction("eliminar",self.eliminarCancion)
            if menu.exec_(event.globalPos()):
                pass
                #item = source.itemAt(event.pos())
                #print(item.text())
            return True
        return super().eventFilter(source, event)
    
    def eliminarCancion(self):
        """Comprobara cual es el item que se quiere eliminar de la 'listWid_soniMio', si
        es el item 0(cancion por defecto), mostrara un cuadro de dialogo explicando
        que dicho item no se puede borrar, pero si es otro item diferente al que se quiere
        borrar los primero que hara es hacer un consulta a la base de datos de las alarmas con la 
        finalidad de obtener el nombre de las alarmas que utilizan esa cancion como sonido
        de alarma, posteriormente mostrara un cuadro de dialogo explicando cuales son las 
        alarmas que se verian afectadas si se decide eliminar dicha canción y como las afectaria,
        si el usuario procede a querer eliminar la cancion, se borrara la cancion de la carpeta,
        tambien de la 'listWid_soniMio' y las alarmas que tenian esa cancion como sonido de alarma
        ahora tendran como sonido de alarma el 'sonido_default'
        """

        print("Cancion eliminada...")
        indice=self.listWid_soniMio.currentIndex().row()
        cancionEliminar=self.listWid_soniMio.item(indice).text()

        #quiere eliminar la opccion default
        if indice==0:
            ventanaDialogo = QMessageBox()
            ventanaDialogo.setIcon(QMessageBox.Information)
            ventanaDialogo.setWindowIcon( QIcon(self.ICONO_APLICACION)  )
            ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

            ventanaDialogo.setText("No puedes eliminar la opcion default")
            ventanaDialogo.setStandardButtons(QMessageBox.Ok)
            btn_ok = ventanaDialogo.button(QMessageBox.Ok)
            btn_ok.setText('Entendido')
            ventanaDialogo.exec_()

        #quiere eliminar una cancion que un dia el subio
        else:
            #hacemos esto:  'self.reproductor.carpetaMusicaMia+cancionEliminar', por que en la base de datos
            #los nombres de los sonidos de alarmas le antece el nombre de la carpeta en la cual estan almacenados  
            alarmasAfectadas=self.baseDatosAlarmas.getNombresAlarmasCon(cancion=self.reproductor.carpetaMusicaMia+cancionEliminar)

            #si no hay ninguna alarma afectada
            if alarmasAfectadas==[]:
                mensajeAdvertencia="¿Estas seguro de querer eliminar la cancion:\n'{}' ?".format(cancionEliminar)
            #si hay almeos una alarma afectada
            else:
                alarmasAfectadas=",".join( alarmasAfectadas ) 
                mensajeAdvertencia="""Las alarmas:{} 
tienen la cancion:' {} ' 
como sonido de alarma, si eliminas esta cancion
el sonido de alarma de dichas alarmas cambiara  
a ser el sonido default.
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

                #eliminando la cancion del reproductor(elimina la cancion de la carpeta y tambien
                # de la lista en la que tiene almacenado el nombre)
                self.reproductor.eliminarMiCancion(nombreCancion=cancionEliminar)

                #eliminamos la cancion de la list widget
                self.listWid_soniMio.takeItem(indice)

                #actualizando la base de datos, por si habia una alarma que usara como 
                #sonido de alarma la cancion que se elimino
                self.baseDatosAlarmas.eliminarCancion(cancionEliminar=self.reproductor.carpetaMusicaMia+cancionEliminar,
                cancionDefault=self.reproductor.carpetaMusicaDefault+App_Alarmas.NOMBRE_SONIDO_NULL)

                #cuando eliminemos la cancion que se escogera  la defualt...
                #self.listWid_soniMio.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
                self.listWid_soniMio.setCurrentRow(0)
                #self.listWid_soniMio.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)


                self.reproductor.cargarCancion()
                self.reproductor.tocar()
                
                

###############################################################################################################
# SONIDO DE LA ALARMA
###############################################################################################################

    def mostrarNombresAlarmas(self):
        '''Este metodo cargara los nombres de alarmas ya existentes en el
        line edit donde colocamos el nombre de alarma, con el fin de
        que el usuario pueda darse cuenta que nombres ya no estan disponibles.'''

        acompletador=QCompleter(list(self.dictNombresAlarmasYaCreadas) )
        self.lineEdit_nombre.setCompleter(acompletador)

    def restringirLasEntradas(self):
        '''Este metodo restrgira a ciertos caracteres el nombre de la alarma,
        las restricciones son las siguientes:
            A)El nombre de alarma no puede contener espacios en blanco
            B)El nombre de alarma no puede tener mas de 15 caracteres
            C)El nombre de alarma solo puede usar letras(minusculas y mayusculas)
            y solo numeros naturales'''

        # validacion del nombre de usuario...
        validator = QRegExpValidator(QRegExp("[0-9a-zA-Z]{1,15}"))  # maximo solo 15 caracteres
        self.lineEdit_nombre.setValidator(validator)

    def comprobarSiDatosCorrectos(self):
        ''' Este metodo comprobara que todos los datos de la alarma ingresados
        por el usuario esten correctos, en caso de que no, le explicara al
        usuario las razones y retornara False, en caso de que esten correctos
        todos los datos retornara True '''

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
        """Cargara los datos default de un objeto de tipo alarma en la widget """

        self.mostrarAlarmaEditar( Alarma() )
        
 
    def mostrarAlarmaEditar(self,alarma):
        """Cargara los datos de un objeto de tipo 'Alarma'  en la widget"""

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
        """Carga todos los datos ingresados por el usuario en la widget, no importando
        posteriormente dichos datos los utiliza  para crear un objeto de tipo 'Alarma'
        con dichos datos, despues de hacer lo anterior procede a  emitir la señal cuyo
        nombre es: 'senal_alarmaEditada' la cual mandara la instancia de alarma creada
        contenida en una lista.
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
                #informando acerca de la nueva alarma creada
                self.senal_alarmaCreada.emit([alarma])
                #registrar los datos de la nueva alarma en la base de datos
                self.baseDatosAlarmas.addAlarma(alarma)
            else:
                #informado acerca de la alarma ya editada
                self.senal_alarmaEditada.emit([alarma])
                #eliminando la alarma previa
                self.baseDatosAlarmas.eliminar(nombreAlarma=self.nombreAlarmaEditar)
                #agregando la alarma editada a la base de datos
                self.baseDatosAlarmas.addAlarma(alarma)

            self.close()

    def closeEvent(self,event):
        ''' Antes de cerra la widget, pausara la reproduccion de una posible cancion que
         se este ejecutando. '''

        self.reproductor.detener()
        self.senal_editorCreador_cerrado.emit(True)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = ItemAlarmaEdit()
    application.show()
    app.exec()
    #sys.exit(app.exec())