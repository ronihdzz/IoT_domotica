import os
import sqlite3
from typing import Tuple
from CUERPO.LOGICA.ALARMA.alarma import Alarma,HoraAlarma
import sys
from logger import logger


#############################################################################################################################
# ACCIONES COMUNES 
############################################################################################################################


class Conexion:
    '''
    Permite crear objetos que sean utiles para relizar conexiones sqlite3 a una base de datos 
    especifica, dichas conexiones tienen como proposito ser sencillas y seguras.
    '''

    def __init__(self,baseDatos):
        '''
        Parámetros:
            baseDatos -- nombre de la base de datos de la cual se desea hacer
            conexion
        '''

        self.__BASE_DATOS = baseDatos
        self.__conexion = None
        self.__cursor = None

    def obtenerConexion(self):
        """
        Creara un objeto  de tipo 'conexion' el cual sirve para conectarse 
        con la base de datos cuyo nombre  es igual a: 'self.__BASE_DATOS'

        Returns(devoluciones):
            objeto de tipo 'conexion' si hubo exito.
            Si no hubo exito en la operación se ocasionara el cierre inmediato del programa
        """

        if self.__cursor is None:
            try:
                self.__conexion = sqlite3.connect(self.__BASE_DATOS)
                logger.debug(f'Conexión exitosa: {self.__conexion}')
                return self.__conexion

            except Exception as e:
                logger.error(f'Error al conectar a la BD: {e}')
                sys.exit()
        else:
            return self.__conexion


    def obtenerCursor(self):
        """
        Apartir del atributo de instancia: 'self.__cursor' creara un objeto  de tipo 'cursor' 
        el cual sirve para ejecutar sentencias de tipo Query a la base de datos cuyo nombre 
        es igual a: 'self.__BASE_DATOS'

        Returns(devoluciones):
            objeto de tipo 'conexion' si hubo exito.
            Si no hubo exito en la operación se ocasionara el cierre inmediato del programa
        """

        if self.__cursor is None:
            try:
                self.__cursor = self.obtenerConexion().cursor()
                logger.debug(f'Se abrio el cursor con éxito: {self.__cursor}')
                return self.__cursor
            except Exception as e:
                logger.error(f'Error al obtener cursor:{e}')
                sys.exit()
        else:
            return self.__cursor

    def cerrar(self):
        '''
        Cerrara a los objetos almacenados por los atributos de instancia: 'self.__cursor'
        y 'self.__conexion' y despues los igualara a valores None

        Si no hubo exito en la operación se ocasionara el cierre inmediato del programa
        '''

        if self.__cursor is not None:
            try:
                self.__cursor.close()
            except Exception as e:
                logger.error(f'Error al cerrar cursor: {e}')
                
        if self.__conexion is not None:
            try:
                self.__conexion.close()
            except Exception as e:
                logger.error(f'Error al cerrar conexión: {e}')
            
        self.__conexion=None
        self.__cursor=None                
        logger.debug('Se han cerrado los objetos de conexión y cursor')


class Cursor:
    '''
    Clase cuyo objetivo es que sus instancias permitan omitir las lineas de codigo:   
        a) 'conexion=sqlite3.connect()'
        b) 'cursor=conexion.cursor()'
        c) 'conexion.commit() '
        b) 'cursor.close()' 
        c) 'conexion.close()'
    Para cada setencia Query que se desea ejecutar con la base de datos por ende
    esta clase define a los metodos especiales '__enter__', '__exit__' los cuales
    permiten utilizar el 'with as' y que este hago las lineas de codigo mencionadas
    anteriormente.
    '''

    def __init__(self,nombreBase):
        '''
        Parámetros:
            nombreBase -- dato de tipo 'str' que representa el nombre de la base 
            de dato que se desea abrir, obtener una conexion, despues un cursor
            para posteriormente ejecutar una sentencia query, y finalmente
            guardar los cambios realizador y cerrar la conexion y el cursor.
        '''

        self.nombreBase=nombreBase
        self.__objetoConector=Conexion(nombreBase)


    # inicio de with
    def __enter__(self):
        '''
        Lo que returne este metodo es lo que almacenara la variable que le procede a:
        'as' del 'with open() as', es decir si setiene que: 
            'with open(nombreBase) as variableX'
            la variable cuyo nombre es 'variableX' almacenara lo que
            retorne este metodo

        Returns(devoluciones):
            Objeto de tipo cursor que permitira ejecutar sentencias
            Query a la base de datos cuyo nombre es igual a:'self.nombreBase'
        '''

        logger.debug('Inicio de with método __enter__') 
        return self.__objetoConector.obtenerCursor()
    
    # fin del bloque with
    def __exit__(self, exception_type, exception_value, exception_traceback):
        '''
        Este metodo definira lo que se haga una vez que se termine de ejecutar
        la ultima linea de codigo que este definida dentro del 'with() as'
        ejemplo:
            with(nombreArchivo) as:
                linea de codigo 1 que definide el usuario dentro del 'with as'
                linea de codigo 2 que definide el usuario dentro del 'with as'
                linea de codigo 3 que definide el usuario dentro del 'with as'
                linea de codigo 4 que definide el usuario dentro del 'with as'
                .
                .
                ultima linea de codigo  que definide el usuario dentro del 'with as'
                ACCION DEFINIDA EN ESTE METODO SE EJECUTARA AQUI  
        '''

        logger.debug('Se ejecuta método __exit__()')

        #if exception_value is not None:
        if exception_value:
            #self.__conn.rollback()  
            logger.debug(f'Ocurrió una excepción: {exception_value}') 
            sys.exit() 

        else:
            self.__objetoConector.obtenerConexion().commit() 
            logger.debug('Commit de la transacción') 

        #Cerramos las conexiones
        self.__objetoConector.cerrar() 
             

#############################################################################################################################
# A L A R M A 
############################################################################################################################

class BaseDatos_alarmas():
    '''
    Clase que servira para crear bases de datos que permitan registrar los datos
    de las alarmas, asi como que permitan que se consulten de la manera mas
    sencilla los datos de las alarmas almacenadas
    '''

    NAME_TABLA = "ALARMAS" #nombre de la tabla que almacenara los datos de la alarma
    LISTA_DIAS=['LUNES','MARTES','MIERCOLES','JUEVES','VIERNES','SABADO','DOMINGO']


    def __init__(self,NOMBRE_BASE_DATOS):
        """

        Parámetros:
            NOMBRE_BASE_DATOS -- Necesita el nombre completo de la base de datos que
            almacenara los datos de las alarmas, el nombre completo es aquel que 
            contiene la ruta completa de donde se ubica la base de datos.Es importante 
            que el nombre incluya la extension del archivo es decir una extension 
            '.sqlite3' o '.db'
        """

        self.NOMBRE_BASE_DATOS=NOMBRE_BASE_DATOS

    def crearBaseDatos(self):
        '''
        Creara la base de datos con el nombre y las secciones requeridas
        
        Returns (Devoluciones):
            dato de tipo 'bool' igual a 'True' si hubo exito.
            Si no hubo exito en la operación se ocasionara el cierra inmediato del programa
        '''

        if not( os.path.isfile(self.NOMBRE_BASE_DATOS)  ): # si la base de datos no existe
            with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
                cursor.execute('''
                            CREATE TABLE ALARMAS(
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            NOMBRE VARCHAR(150),
                            SONIDO VARCHAR(400),
                            ASUNTO INTEGER,
                            HORA INTEGER,
                            MINUTO INTEGER,
                            LUNES  INTEGER,
                            MARTES INTEGER,
                            MIERCOLES INTEGER,
                            JUEVES INTEGER,
                            VIERNES INTEGER,
                            SABADO INTEGER,
                            DOMINGO INTEGER,
                            PRENDIDA INTEGER
                            )        
                ''')
            
            return True


    def addAlarma(self,alarma):
        """
        Almacenara  los datos de una alarma los cuales vienen inmersos en el parametro
        cuyo nombre es 'alarma'

        Parámetros:
            alarma -- Una instancia de la clase 'Alarma' que contiene los datos de la alarma
            que se desea agregar 
        
        Returns(devoluciones):        
            Si los datos de la alarma fueron registrados correctamente retornara el 'id' que
            le asigno la base de datos a esa alarma.
            Si los datos de la alarma NO fueron registrados correctamente el programa se cerrara

        """

        tuplaDatos=alarma.to_tupla(conId=False) #converitmos todos los datos de la instancia de la
                                     #Clase 'Alarma' en una tupla que contiene dichos datos
                                     #de forma ordenada.
        
        idAsignado=None

        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            # Como la base de datos asignara automaticamente un 'id' a la alarma,
            # significa que en el apartado de 'id' se le debe colocar 'NULL'
            sqlOrden="INSERT INTO "+self.NAME_TABLA+" VALUES(NULL,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            cursor.execute(sqlOrden,tuplaDatos)
            # recuperando el 'id' que la base de datos le asigno a la alarma que almmaceno
            idAsignado=cursor.lastrowid
        return idAsignado



    def eliminarCancion(self,cancionEliminar,cancionDefault):
        """
        Buscara en la base de datos todos los sonidos de alarma cuyo valor
        se igual al parametro: 'cancionEliminar' y los remplazara por el valor
        que almacene el parametro: 'cancionDefault' 

        Parámetros:
            cancionEliminar -- dato de tipo 'string' que representa al nombre de la 
            canción que se desea eliminar de todas las alarmas que tengan dicho 
            nombre de canción como sonido de alarma.
            cancionDefault -- dato de tipo 'string' que representa el nombre de la 
            canción que sera  el nuevo sonido de alarma de las alarmas que tenian
            como canciónsonido de alarma a la cancion: 'cancionEliminar'

        Returns(devoluciones):
            dato de tipo 'bool' igual a 'True' si hubo exito.
            Si no hubo exito en la operación se ocasionara el cierra inmediato del programa
        """

        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            sqlOrden="UPDATE "+self.NAME_TABLA+" SET SONIDO=? WHERE SONIDO=?"
            cursor.execute(sqlOrden, (cancionDefault,cancionEliminar)  )
            
        return True
    
        #    print("Error a la hora de querer actualizar lo nombres...."
        #    "de los sonidos de la lista de alarmas")
        #    return False
    
    def actualizarAlarma(self,alarma):
        '''
        Actualizara en la base de datos todos la alarma cuyo 'id'='alarma.id', es importante
        mencionar que el valor que no se editara es el 'id', pues este es unico entre todas
        las alarmas creadas.

        Parámetros:
            alarma -- Un instancia de la clase 'Alarma', dicha instancia los nuevo de datos
            de la alarma cuyo 'id'= 'alarma.id'

        Returns(devoluciones):
            dato de tipo 'bool' igual a 'True' si hubo exito.
            Si no hubo exito en la operación se ocasionara el cierra inmediato del programa     
        '''

        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            sql="UPDATE "+self.NAME_TABLA
            sql+=""" SET NOMBRE=?,SONIDO=?,ASUNTO=?,HORA=?,MINUTO=?,
            LUNES=?,MARTES=?,MIERCOLES=?,JUEVES=?,VIERNES=?,SABADO=?,DOMINGO=? WHERE ID=?
            """

            tuplaDatos=list(alarma.to_tupla(conId=False)) #converitmos todos los datos de la instancia de la
                                # Clase 'Alarma' en una tupla que contiene dichos datos
                                # de forma ordenada

            tuplaDatos[-1]=alarma.id # quitando el estado de alarma y remplazandolo por el id
            
            print(f"actualizar: {sql}  {tuplaDatos}")
            cursor.execute( sql,tuplaDatos)
        return True   
        

        #    print("Error a la hora de actualizar el prendido y apagado de la alarma {}".format(alarma.nombre))
    
    def actualizarEstadoAlarma(self,tupla_idsYestados_alarmas):
        """
        Modificara en la base de datos el valor de la columna 'PRENDIDA' de  las alarmas cuyos 
        'id' estan contenidos dentro del parametro 'tupla_idsYestados_alarmas' 

        Parámetros:
            tupla_idsYestados_alarmas -- Es una tupla con 'N' tuplas dentro, donde cada tupla
            que almacena tiene las siguientes caracteristicas:
                A) Cada tupla tiene 2 elementos dentro:
                    a) El primer elemento es numero entero que representa el 'id' de la alarma
                    cuyo valor de la columna 'PRENDIDA' quiere ser modificado
                    a) El segundo parametro es un dato de tipo booleano, el cual representa
                    el valor de la columna 'PRENDIDA' que tomara la alarma con dicho 'id'
                    Ejemplo:
                    [ (alarma1_id,alarma1_estado),(alarma2_id,alarma2_estado),...
                        (alarmaN_id,alarmaN_estado), ]

        Returns(devoluciones): 
            dato de tipo 'bool' igual a 'True' si hubo exito.
            Si no hubo exito en la operación se ocasionara el cierra inmediato del programa
        """

        #lista de tuplas  [ (alarma1_id,alarma1_estado), ]


        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            sql="UPDATE "+self.NAME_TABLA
            sql+="""  SET  PRENDIDA=?  WHERE ID=?"""
            cursor.executemany( sql, tupla_idsYestados_alarmas )
        return True   

        # print("Error a la hora de actualizar el prendido y apagado de las alarmas")

    def eliminar(self,id_alarmaEliminar):
        """
        Eliminara  de la base de datos todos los datos de la alarma cuyo 'id' es igual a:
        'id_alarmaEliminar'
        
        Parámetros:
            id_alarmaEliminar -- Dato de tipo 'int' que representara el 'id' de la
            alarma que se desea eliminar
        
        Returns(devoluciones):
            dato de tipo 'bool' igual a 'True' si hubo exito.
            Si no hubo exito en la operación se ocasionara el cierra inmediato del programa
        """

        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            sql="DELETE FROM "+self.NAME_TABLA
            sql+=" WHERE ID="+str(id_alarmaEliminar)
            cursor.execute(sql)
        return True

        #print("Error al eliminar los datos de la alarma con id=",id_alarmaEliminar)
         
    def getNombresAlarmasCon(self,cancion):
        """
        Crea una lista con los nombres  de las alarmas cuyo sonido de alarma sea igual al valor
        que almacena el parametro 'cancion', posteriormente retorna esa lista

        Parámetros:
            cancion -- Dato de tipo 'str' que representara el nombre de la canción que se desea
            saber que alarma la tienen definida como sonido de alarma
            
        Returns(devoluciones):
            a) lista con los nombres de las alarmas que contienen como sonido de alarma al nombre
            de la canción que contiene el parametro 'cancion'
            b) lista vacia en caso de no existir alarma con sonido de alarma igual al nombre
            de la canción que contiene el parametro 'cancion'
            Si no hubo exito en la operación se ocasionara el cierra inmediato del programa
        """

        listaNombresAlarmas=None
        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            sqlOrden = "SELECT NOMBRE FROM  "+self.NAME_TABLA
            cancion="'"+cancion+"'"
            sqlOrden+= " WHERE SONIDO="+cancion

            cursor.execute(sqlOrden)
            listaDatosAlarmas= tuple(cursor.fetchall())  # devuelve una lista con
            #((nombreAlarma_1,), (nombreAlarma_2,), (nombreAlarma_3,), (nombreAlarma_4,))

            listaNombresAlarmas=[]
            for datosAlarma in listaDatosAlarmas:
                nombre=datosAlarma[0]
                listaNombresAlarmas.append(nombre)
        return listaNombresAlarmas
        
       #     print("Error a la hora de querer cargar los nombres de las alarmas"
       #     "cuya canción={}".format(cancion) )

    
    def getNombresAlarmas(self):
        """
        Crea una lista con todos los nombres de las alarmas y posteriormente la retorna.
            
        Returns(devoluciones):
            a) lista con los nombres de las alarmas 
            b) lista vacia en caso de no existir ninguna alarma registrada
            Si no hubo exito en la operación se ocasionara el cierra inmediato del programa     
        """
        
        listaNombresAlarmas=None
        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            sqlOrden = f"SELECT NOMBRE FROM  "+self.NAME_TABLA
            cursor.execute(sqlOrden)
            datosRecuperados= tuple(cursor.fetchall())  # devuelve una lista como:
            #(     ('luis',), ('pedro',), ('julian',), ('Isra',)    )

            #Creamos una lista con solo los nombres de todas las alarmas registradas
            listaNombresAlarmas=[ renglonDatos[0]  for renglonDatos in datosRecuperados ]
        return listaNombresAlarmas
        
        #    print("Error de obtener una lista con todos los nombres de las alarmas")


    def getAlarma(self,idAlarma):
        """
        Creara una instancia de la clase 'Alarma' que contenga todos los datos  de la alarma 
        cuyo 'id' es igual al valor que almacena el parametro: 'idAlarma', posteriormente 
        retornara dicha instancia creada.
        
        Parámetros:
            idAlarma -- Dato de tipo 'int' que representara el id de la alarma de la que se
            quieren obtener todos sus datos
            
        Returns(devoluciones):
            a) Una instancia de la clase 'Alarma' con todos los datos de la alarma con 'id' es 
            igual al valor que almacena el parametro: 'idAlarma'
            Si no hubo exito en la operación se ocasionara el cierra inmediato del programa
        """
        
        alarma=None
        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            sqlOrden = f"SELECT * FROM  "+self.NAME_TABLA
            sqlOrden+=" WHERE ID="+str(idAlarma)
            cursor.execute(sqlOrden)
            datosAlarma= tuple(cursor.fetchall())[0]  # devuelve una lista con
            #(     (1,'luis', 'DEFAULT/SIN MUSICA', 0, 7, 0, 1, 0, 0, 0, 0, 0, 1, 1),    )
            alarma=Alarma.tupla_toAlarma(tuplaDatos=datosAlarma)
        
        return alarma
        
        #    print("Error al querer obtener todos los datos de la alarma con id=",idAlarma)


    def getDatosNecesariosParaSonarAlarma(self,listaIds):
        """
        Creara una tupla de dos elementos, donde:
            a) El primer elemento de dicha tupla sera una lista con los nombres de las alarmas 
            cuyos 'ids' son iguales a los que tiene el parametro 'listaIds'
            b) El segundo elemento sera una tupla de 3 elementos, donde:
                1) El primer elemento sera una instancia de la clase 'HoraAlarma' formada
                por la 'hora' y 'minuto' en la que suena la alarma  cuyo 'id' es igual al 
                primer 'id' del parametro 'listaIds'. 
                2) El segundo elemento sera un dato de tipo 'str' el cual sera el nombre
                de la canción del sonido de alarma de la alarma  uyo 'id' es igual al 
                primer 'id' del parametro 'listaIds'. 
                3) El segundo elemento sera un dato de tipo 'int' el cual sera el asunto
                de la  alarma cuyo 'id' es igual al  primer 'id' del parametro 'listaIds'. 
        Una vez creada la tupla descrita anteriormente la retornara.

        Parámetros:
            listaIds -- Dato de tipo 'list' que contendra almacenados 'id' de alarmas
            
        Returns(devoluciones):
            a) Si el parametro 'listaIds' por lo menos contiene una 'id', se retornara
            la tupla antes mencionada
            b) Si el parametro 'listaIds' no contiene ningun 'id' este metodo ocacionara
            un error
            Si no hubo exito en la operación se ocasionara el cierra inmediato del programa
        """  
        
        listaNombres=None;horaSuena=None;sonido=None;asunto=None
        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            listaIds_str=" OR ID=".join( [ str(id) for id in listaIds ] )
            sqlOrden_paraObtenerNombres='SELECT NOMBRE FROM ' +self.NAME_TABLA+' WHERE ID='+listaIds_str
            cursor.execute(sqlOrden_paraObtenerNombres)
            datosRetornados= tuple(cursor.fetchall())  # devuelve una lista con
            #(   ('Nombre1' ), ('Nombre2'), ....   )

            listaNombres=[]
            for dato  in  datosRetornados:
                listaNombres.append(dato[0])    

            id_alarma1=listaIds[0]
            sqlOrden = f"SELECT HORA,MINUTO,SONIDO,ASUNTO FROM  "+self.NAME_TABLA+" WHERE ID="+str(id_alarma1)
            cursor.execute(sqlOrden)
            sonidoYasunto= tuple(cursor.fetchall())  # devuelve una lista con
            #(   ('nombre/123.mp3',asunto),  )
            hora,minuto,sonido,asunto=sonidoYasunto[0]
            horaSuena=HoraAlarma(hora,minuto)
        return (listaNombres, (horaSuena,sonido,asunto)  )  
        
        #print("Error a la hora de obtener diccionario de hora de  alarmas que suenan en el  dia:",dia)
        #    return False


    def getDictHoraAlarmas(self,noDia,hora,minuto):
        """
        Creara un diccionario donde las las 'keys' sean los 'id' de las alarmas y los 
        'values' sean instancias la clase 'HoraAlarma'  las cuales indicara a que hora 
        dicha alarma debe sonar.
        Ejemplo:
            { 'idAlarma_1': HoraAlarma(horaAlarma_1,minutoAlarma_1),
              'idAlarma_2': HoraAlarma(horaAlarma_2,minutoAlarma_2),
              'idAlarma_3': HoraAlarma(horaAlarma_3,minutoAlarma_3),
               }
        Es importante mencionar que el diccionario solo almacenara esos datos solo de las
        las alarmas que cumplan con lassiguientes restricciones:

            A) Las Alarmas deben estar programadas para sonar en el dia indicado por 
            el atributo 'noDia'

            B) Las 'HoraAlarma' a la que suenan las alarmas deben ser mayor a la instancia
            formada por los parametros 'hora' y 'minuto', es decir la 'HoraAlarma'>HoraAlarma(hora,minuto)
        Una vez creado el diccionario descrito anteriormente se retornara
        
        Parámetros:
            noDia -- dato de tipo 'int' cuyos valores equivalen a los dias de la semana,
            es decir:
                noDia=0 significa que es el dia lunes
                noDia=1 significa que es el dia martes
                noDia=2 significa que es el dia miercoles
                .
                .
                noDia=6 significa que es el dia domingo
            hora -- dato de tipo 'int' que equivale a un valor de hora 
            minuto -- dato de tipo 'int' que equivale a un valor de minuto
            
        Returns(devoluciones):
            a) El diccionario antes descrito
            b) Si no hay ninguna alarma que cumpla con las restricciones antes mencionadas
            entonces se retornara un diccionario vacio.
        Si no hubo exito en la operación se ocasionara el cierra inmediato del programa
        """  

        dictHorasAlarmas=None
        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            dia=self.LISTA_DIAS[noDia]
            sqlOrden = f"SELECT ID,HORA,MINUTO  FROM  "+self.NAME_TABLA
            #ejemplo:
            #SELECT NOMBRE,HORA,MINUTO FROM ALARMAS  WHERE LUNES=1 AND (  (HORA>19) OR (HORA==19 AND MINUTO>0) ) ORDER BY HORA,MINUTO
            sqlOrden+= " WHERE "+dia+"=1"+" AND ( (HORA>"+str(hora)+") OR (HORA=="+str(hora)+" AND MINUTO>="+str(minuto)+")  ) ORDER BY HORA ASC, MINUTO ASC"
            cursor.execute(sqlOrden)
            listaDatosAlarmas= tuple(cursor.fetchall())  # devuelve una lista con
            #(   ('Julian',9, 30, ), ....   )
            dictHorasAlarmas={}
            for id,hora,minuto in listaDatosAlarmas:
                dictHorasAlarmas[id]=HoraAlarma(hora,minuto)
        return dictHorasAlarmas
        
        #    print("Error a la hora de obtener diccionario de hora de  alarmas que suenan en el  dia:",dia)


    def getTodas_alarmas(self):
        """
        Creara una lista de instancias de la clase 'Alarma' donde cada instancia contendra 
        todos los datos de cada alarma que se encuentra almacenada en la base de datos.
        Una vez creada la lista descrita anteriormente, se procede a retornarse.

        Returns(devoluciones):
            a) En caso de existir almenos alguna alarma registrada en la base de datos,
            se retornara la lista antes descrita.
            b) Si no hay ninguna alarma registrada se retornara una lista vacia.
        Si no hubo exito en la operación se ocasionara el cierra inmediato del programa
        """

        listaAlarmas=None
        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            sqlOrden = f"SELECT * FROM  "+self.NAME_TABLA+" ORDER BY HORA ASC, MINUTO ASC"
            cursor.execute(sqlOrden)
            listaDatosAlarmas= tuple(cursor.fetchall())  # devuelve una lista con
            #(   (0,'Julian', 1, 9, 30, 1, 1, 1, 0, 0, 0, 0, 0), ....   )
            listaAlarmas=[]
            for datosAlarmas in listaDatosAlarmas:
                alarma=Alarma.tupla_toAlarma(tuplaDatos=datosAlarmas)
                listaAlarmas.append(alarma)
        return listaAlarmas
        
        #    print("Error a la hora de obtener la lista de todas las instancias de todas"
        #    "las alarmas registradas en la base de datos")
         