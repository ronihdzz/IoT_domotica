import os
import sqlite3
from CUERPO.LOGICA.ALARMA.alarma import Alarma,HoraAlarma


class BaseDatos_alarmas():
    NAME_TABLA = "ALARMAS" #nombre de la tabla que almacenara los datos de la alarma
    LISTA_DIAS=['LUNES','MARTES','MIERCOLES','JUEVES','VIERNES','SABADO','DOMINGO']

    def __init__(self,NOMBRE_BASE_DATOS):
        """Necesita el nombre completo de la base de datos que almacenara los datos
        de las alarmas, el nombre completo es aquel que contiene la ruta completa de
        donde se ubica la base de datos.Es importante que el nombre incluya la extension
        del archivo es decir una extension '.sqlite3' o '.db'
        """
        self.NOMBRE_BASE_DATOS=NOMBRE_BASE_DATOS
        self.BASE_CREADA = False # variable booleana que nos dira
                                 # si ya existe dicha base

    def crearBaseDatos(self):
        '''Esta funcion creara la base de datos con el nombre y las secciones
        requeridas,retornara: True si hubo exito o False si ocurrio algun error'''
        if self.BASE_CREADA:
            return True  #retorno True por que la base ya ha sido creada
        else:
            my_path =self.NOMBRE_BASE_DATOS
            if os.path.isfile(my_path):# si la base de datos ya existe ya no la creamos
               self.BASE_CREADA=True
               return True 
            else:
                conexion = self.iniciarConexion_sql()
                if conexion:
                    cursor = conexion.cursor()
                    cursor.execute('''
                            CREATE TABLE ALARMAS(
                            NOMBRE VARCHAR(150) PRIMARY KEY,
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

                    conexion.commit()
                    conexion.close()
                    return True
                else:
                    print("Error a la hora de crear la base de datos")
                    return False

    def iniciarConexion_sql(self):
        """Hara una conexión con la base de datos, si todo sale bien
        retornara un objeto que nos permitira interactuar con la base
        de datos, en caso contrario retornara False si llegase a ocurrir
        algun error"""
        try:
            con = sqlite3.connect(self.NOMBRE_BASE_DATOS)
            return con
        except:
            return False

    def addAlarma(self,alarma):
        """Almacenara  los datos de una alarma en la base de datos.Este metodo
        necesita una instancia de la clase 'Alarma', y a partir de ella guardara
        sus datos, retornara: True si hubo exito o False si ocurrio algun error """

        tuplaDatos=alarma.to_tupla() #converitmos todos los datos de la instancia de la
                                     #Clase 'Alarma' en una tupla que contiene dichos datos
                                     #de forma ordenada.

        conexion=self.iniciarConexion_sql()
        if conexion:
            cursor = conexion.cursor()
            sqlOrden = "INSERT INTO " + self.NAME_TABLA + " VALUES " + str(tuplaDatos)
            cursor.execute(sqlOrden)
            conexion.commit()
            conexion.close()
            return True
        else:
            print("Error a la hora de almacenar los datos de la alarma: ",tuplaDatos)
            return False
     
    def eliminarCancion(self,cancionEliminar,cancionDefault):
        """Buscara en la base de datos todos los sonidos de alarma cuyo valor
        se igual a: 'cancionEliminar' y los remplazara por 'cancionDefault' 
        retornara: True si hubo exito  o False si ocurrio algun error """

        conexion=self.iniciarConexion_sql()
        if conexion:
            #Las consutas de los strings en sqlite deben ir entre comillas
            cancionEliminar="'"+cancionEliminar+"'"
            cancionDefault="'"+cancionDefault+"'"

            cursor = conexion.cursor()
            sqlOrden="UPDATE "+self.NAME_TABLA+" SET SONIDO="+cancionDefault
            sqlOrden+=" WHERE SONIDO="+cancionEliminar

            cursor.execute(sqlOrden)
            conexion.commit()
            conexion.close()
            return True
        else:
            print("Error a la hora de querer actualizar lo nombres...."
            "de los sonidos de la lista de alarmas")
            return False

    
    def actualizarEstadoAlarma(self,nombreAlarma,prendida):
        """Modificara en la base de datos el estado de alarma,
        ya sea a prendida u apagada, retornara: True si hubo exito  
        o False si ocurrio algun error.
            * El parametro 'nombreAlarma' es un dato de tipo 'str' que representara
              el nombre de la alarma que deseas actualizar su estado
            * El parametro 'nombre' es un dato de tipo 'bool' que si vale:
                A) 'True'  significa que la alarma esta prendida
                B) 'False' significa que la alarma esta apagada """

        conexion=self.iniciarConexion_sql()
        if conexion:
            cursor = conexion.cursor()
            sql="UPDATE "+self.NAME_TABLA
            sql+="""  SET  PRENDIDA=?  WHERE NOMBRE=?"""
            cursor.execute( sql,(prendida,nombreAlarma) )
            conexion.commit()
            conexion.close()
            return True   
        else:
            print("Error a la hora de actualizar el prendido y apagado de la alarma {}".format(nombreAlarma))
            return False


    def eliminar(self,nombreAlarma):
        """Eliminara  de la base de datos todos los datos de la alarma 
        cuyo nombre es: 'nombreAlarma'  retornara: True si hubo exito  
        o False si ocurrio algun error """

        nombreAlarma="'"+nombreAlarma+"'"
        conexion=self.iniciarConexion_sql()
        if conexion:
            cursor = conexion.cursor()
            sql="DELETE FROM "+self.NAME_TABLA
            sql+=" WHERE NOMBRE="+nombreAlarma
            cursor.execute(sql)
            conexion.commit()
            conexion.close()
            return True
        else:
            print("Error al eliminar los datos de la alarma",nombreAlarma)
            return False

    def getNombresAlarmasCon(self,cancion):
        """Retorna una lista con los nombres  de las alarmas cuyo sonido de alarma
        sea igual a: 'cancion', si no hay ninguna se retornara una lista vacia,y si
        ocurre un error al hacer la consulta retornara False """

        conexion=self.iniciarConexion_sql()
        if conexion:
            cursor = conexion.cursor()
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

            conexion.commit()
            conexion.close()
            return listaNombresAlarmas
        else:
            print("Error a la hora de querer cargar los nombres de las alarmas"
            "cuya canción={}".format(cancion) )
            return False
    
    def getNombresAlarmas(self):
        """Retorna una lista con todos los nombres de las alarmas, si no hay
        alarmas retornara una lista vacia y su ocurre un error al hacer la 
        consulta retornara False"""

        conexion=self.iniciarConexion_sql()
        if conexion:
            cursor = conexion.cursor()
            sqlOrden = f"SELECT NOMBRE FROM  "+self.NAME_TABLA
            cursor.execute(sqlOrden)
            datosRecuperados= tuple(cursor.fetchall())  # devuelve una lista como:
            #(     ('luis',), ('pedro',), ('julian',), ('Isra',)    )

            #Creamos una lista con solo los nombres de todas las alarmas registradas
            listaNombresAlarmas=[ renglonDatos[0]  for renglonDatos in datosRecuperados ]
            return listaNombresAlarmas
        else:
            print("Error de obtener una lista con todos los nombres de las alarmas")
            return False


    def getAlarma(self,nombreAlarma):
        """Retornara una instancia de la clase 'Alarma' que contenga todos los
        datos  de la alarma cuyo nombre es: 'nombreAlarma', si ocurre un error
        en la consulta retornara False """

        conexion=self.iniciarConexion_sql()
        if conexion:
            cursor = conexion.cursor()
            sqlOrden = f"SELECT * FROM  "+self.NAME_TABLA
            nombreAlarma="'"+nombreAlarma+"'"
            sqlOrden+=" WHERE NOMBRE="+nombreAlarma
            cursor.execute(sqlOrden)
            datosAlarma= tuple(cursor.fetchall())[0]  # devuelve una lista con
            #(     ('luis', 'DEFAULT/SIN MUSICA', 0, 7, 0, 1, 0, 0, 0, 0, 0, 1, 1),    )
            alarma=Alarma.tupla_toAlarma(tuplaDatos=datosAlarma)
            return alarma
        else:
            print("Error al querer obtener todos los datos de la alarma: ",nombreAlarma)
            return False

    def getDictHoraAlarmas(self,noDia,hora,minuto):
        """Retornara un diccionario donde las las 'keys' sean los nombres de las
        alarmas, y lo 'values' sean instancias la clase 'HoraAlarma'  las cuales
        indicara a que hora dicha alarma debe sonar.
        Ejemplo:
            { 'nombreAlarma_1': HoraAlarma(hora=10,minuto=15),
              'nombreAlarma_2': HoraAlarma(hora=7,minuto=15),
              'nombreAlarma_3': HoraAlarma(hora=19,minuto=30),
               }
        
        Es importante mencionar que solo retornara las alarmas que cumplan con las
        siguientes restricciones :
            A) Las Alarmas deben estar programadas para sonar en el dia indicado por 
            el atributo 'noDia' donde si:
                noDia=0 significa que es el dia lunes
                noDia=1 significa que es el dia martes
                noDia=2 significa que es el dia miercoles
                .
                .
                .
            B) Las 'HoraAlarma' a la que suenan las alarmas debe ser mayor a la instancia
            formada por los parametros 'hora' y 'minuto', es decir la 'HoraAlarma'>HoraAlarma(hora,minuto)
        
        Por ultimo es importante mencionar los datos se retornaran en orden ascendente en funcion del
        valor 'HoraAlarma' que tiene cada alarma, en caso de error retornara False.
        """  

        dia=self.LISTA_DIAS[noDia]
        conexion=self.iniciarConexion_sql()
        if conexion:
            cursor = conexion.cursor()
            sqlOrden = f"SELECT NOMBRE,HORA,MINUTO  FROM  "+self.NAME_TABLA
            #ejemplo:
            #SELECT NOMBRE,HORA,MINUTO FROM ALARMAS  WHERE LUNES=1 AND (  (HORA>19) OR (HORA==19 AND MINUTO>0) ) ORDER BY HORA,MINUTO
            sqlOrden+= " WHERE "+dia+"=1"+" AND ( (HORA>"+str(hora)+") OR (HORA=="+str(hora)+" AND MINUTO>="+str(minuto)+")  ) ORDER BY HORA ASC, MINUTO ASC"
            cursor.execute(sqlOrden)
            listaDatosAlarmas= tuple(cursor.fetchall())  # devuelve una lista con
            #(   ('Julian',9, 30, ), ....   )
            dictHorasAlarmas={}
            for nombre,hora,minuto in listaDatosAlarmas:
                dictHorasAlarmas[nombre]=HoraAlarma(hora,minuto)
            conexion.commit()
            conexion.close()
            return dictHorasAlarmas
        else:
            print("Error a la hora de obtener diccionario de hora de  alarmas que suenan en el  dia:",dia)
            return False

    def getTodas_alarmas(self):
        """Retornara una lista de instancias de la clase 'Alarma' donde cada
        instancia contendra todos los datos de cada alarma que se encuentra 
        almacenada en la base de datos, en caso de error retornara False """

        conexion=self.iniciarConexion_sql()
        if conexion:
            cursor = conexion.cursor()
            sqlOrden = f"SELECT * FROM  "+self.NAME_TABLA+" ORDER BY HORA ASC, MINUTO ASC"
            cursor.execute(sqlOrden)
            listaDatosAlarmas= tuple(cursor.fetchall())  # devuelve una lista con
            #(   ('Julian', 1, 9, 30, 1, 1, 1, 0, 0, 0, 0, 0), ....   )
            listaAlarmas=[]
            for datosAlarmas in listaDatosAlarmas:
                alarma=Alarma.tupla_toAlarma(tuplaDatos=datosAlarmas)
                listaAlarmas.append(alarma)
            conexion.commit()
            conexion.close()
            return listaAlarmas
        else:
            print("Error a la hora de obtener la lista de todas las instancias de todas"
            "las alarmas registradas en la base de datos")
            return False

    def getSonidoAsunto_alarma(self,nombreAlarma):
        """Retornara una tupla que contenga el nombre del sonido y el asunto, de la alarma 
        cuyo nombre es igual al valor contenido en el parametro 'nombreAlarma', en caso de
        error retornara False """
        conexion=self.iniciarConexion_sql()
        if conexion:
            cursor = conexion.cursor()
            sqlOrden = f"SELECT SONIDO,ASUNTO FROM  "+self.NAME_TABLA+" WHERE NOMBRE="+"'"+nombreAlarma+"'"
            print("INSTRUCCION",sqlOrden)
            cursor.execute(sqlOrden)
            sonidoYasunto= tuple(cursor.fetchall())  # devuelve una lista con
            print(sonidoYasunto)
            #(   ('nombre/123.mp3',asunto),  )
            return sonidoYasunto[0] #(sonido,asunto)
        else:
            print("Error a la hora de obtener el nombre del sonido y el asunto, de la alarma"
            "cuyo nombre es: {}".format(nombreAlarma) )
            return False