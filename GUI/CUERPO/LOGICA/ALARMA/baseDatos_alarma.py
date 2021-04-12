import os
import sqlite3

from CUERPO.LOGICA.ALARMA.alarma import Alarma,HoraAlarma


class BaseDatos_alarmas():
    NAME_TABLA = "ALARMAS"

    def __init__(self,NOMBRE_BASE_DATOS):
        self.NOMBRE_BASE_DATOS=NOMBRE_BASE_DATOS
        self.BASE_CREADA = False # variable booleana que nos dira
                                 # si ya existe dicha base


    def crearBaseDatos(self):
        '''
        Esta funcion creara la base de datos con el nombre y las secciones
        requeridas
        return:true si hubo exito/false si ocurrio algun error
        '''
        if self.BASE_CREADA:
            return False  # returna false si ocurrio algun error al crear la base
        else:
            my_path =self.NOMBRE_BASE_DATOS
            if os.path.isfile(my_path):
               return True #ya esta creada la base de datos...
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
                    print("Error a la hora de crear la base de datos, vuelva a intentarlo....")
                    return False

    def iniciarConexion_sql(self):
        try:
            con = sqlite3.connect(self.NOMBRE_BASE_DATOS)
            return con
        except:
            return False

    def addAlarma(self,alarma):
        tuplaDatos=alarma.to_tupla()

        conexion=self.iniciarConexion_sql()
        if conexion:
            cursor = conexion.cursor()
            sqlOrden = "INSERT INTO " + self.NAME_TABLA + " VALUES " + str(tuplaDatos)
            cursor.execute(sqlOrden)
            conexion.commit()
            conexion.close()
            return True
        else:
            print("Error a la hora de agregar al usuario con los datos: ",tuplaDatos)
            return False
    



    def eliminarCancion(self,cancionEliminar,cancionDefault):
        conexion=self.iniciarConexion_sql()
        if conexion==None:
            print("Error a la hora de querer actualizar lo nombres...."
            "de los sonidos de la lista de alarmas")
            return False
        else:
            cancionEliminar="'"+cancionEliminar+"'"
            cancionDefault="'"+cancionDefault+"'"

            cursor = conexion.cursor()
            sqlOrden="UPDATE "+self.NAME_TABLA+" SET SONIDO="+cancionDefault
            sqlOrden+=" WHERE SONIDO="+cancionEliminar

            cursor.execute(sqlOrden)
            #ejecutando y cerrando base de datos..
            conexion.commit()
            conexion.close()
            return True
    
    def actualizarEstadoAlarma(self,nombre,prendida):
        conexion=self.iniciarConexion_sql()
        if conexion==None:
            print("Error a la hora de actualizar los, vuelva a intentarlo....")
            return False
        else:
            cursor = conexion.cursor()
            sql="UPDATE "+self.NAME_TABLA
            sql+="""  SET  PRENDIDA=?  WHERE NOMBRE=?"""
            cursor.execute( sql,(prendida,nombre) )

            #ahora actualizamos la informacion de la base de respuesta..
            conexion.commit()
            conexion.close()
            return True

    def eliminar(self,A):
        A="'"+A+"'"
        conexion=self.iniciarConexion_sql()
        if conexion==None:
            print("Error al eliminar los datos del usuario....")
            return False
        else:
            cursor = conexion.cursor()
            sql="DELETE FROM "+self.NAME_TABLA
            sql+=" WHERE NOMBRE="+A

            print(sql)
            cursor.execute(sql)
            
            #ejecutando y cerrando base de datos..
            conexion.commit()
            conexion.close()
            return True

    def getNombresAlarmasCon(self,cancion):
        conexion=self.iniciarConexion_sql()
        if conexion==None:
            print("Error a la hora de querer cargar los nombres de las alarmas"
            "cuya canción se va a eliminar....")
            return False
        else:
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

            #ejecutando y cerrando base de datos..
            conexion.commit()
            conexion.close()
            return listaNombresAlarmas

    
    def getNombresAlarmas(self):
        conexion=self.iniciarConexion_sql()
        if conexion==None:
            print("Error a la hora de obtener los datos de la alarma:",nombreAlarma)
            return False
        else:
            cursor = conexion.cursor()
            # necesitamos obtener el tipo de respuesta de la pregunta...
            sqlOrden = f"SELECT NOMBRE FROM  "+self.NAME_TABLA
            cursor.execute(sqlOrden)
            listaNombresAlarmas= tuple(cursor.fetchall())  # devuelve una lista con
            #(     ('luis',) ,('')    )


            #Las llaves del diccionario indicaran seran los nombres de la alarma
            #y todos sus values valdran True, hara alusion a dichos nombres ya existen
            resultado={}
            for nombreAlarma in listaNombresAlarmas:
                resultado [ nombreAlarma[0] ]=True

            return resultado




    def getAlarma(self,nombreAlarma):
        conexion=self.iniciarConexion_sql()
        if conexion==None:
            print("Error a la hora de obtener los datos de la alarma:",nombreAlarma)
            return False
        else:
            cursor = conexion.cursor()
            # necesitamos obtener el tipo de respuesta de la pregunta...
            sqlOrden = f"SELECT * FROM  "+self.NAME_TABLA
            nombreAlarma="'"+nombreAlarma+"'"
            sqlOrden+=" WHERE NOMBRE="+nombreAlarma
            cursor.execute(sqlOrden)
            datosAlarma= tuple(cursor.fetchall())[0]  # devuelve una lista con
            #(     ('luis', 'DEFAULT/SIN MUSICA', 0, 7, 0, 1, 0, 0, 0, 0, 0, 1, 1),    )

            alarma=Alarma.tupla_toAlarma(tuplaDatos=datosAlarma)

            return alarma

    def getDictHoraAlarmas(self,noDia,hora,minuto):
        print("Solicitando datos del dia:",noDia)
        DICT_IDS_DIAS=['LUNES','MARTES','MIERCOLES','JUEVES','VIERNES','SABADO','DOMINGO']

        dia=DICT_IDS_DIAS[noDia]
        
        conexion=self.iniciarConexion_sql()

        if conexion==None:
            print("Error a la hora de obtener diccionario de hora de  alarmas que suenan el  dia:",dia)
            return False
        else:
            cursor = conexion.cursor()
            # necesitamos obtener el tipo de respuesta de la pregunta...
            sqlOrden = f"SELECT NOMBRE,HORA,MINUTO  FROM  "+self.NAME_TABLA

            #SELECT NOMBRE,HORA,MINUTO FROM ALARMAS  WHERE LUNES=1 AND (  (HORA>19) OR (HORA==19 AND MINUTO>0) ) ORDER BY HORA,MINUTO
            sqlOrden+= " WHERE "+dia+"=1"+" AND ( (HORA>"+str(hora)+") OR (HORA=="+str(hora)+" AND MINUTO>="+str(minuto)+")  ) ORDER BY HORA ASC, MINUTO ASC"
            cursor.execute(sqlOrden)
            

            listaDatosAlarmas= tuple(cursor.fetchall())  # devuelve una lista con
            #(   ('Julian',9, 30, ), ....   )
            print("PETICION:",sqlOrden)
            print("RESPUESTA:",listaDatosAlarmas)

            dictHorasAlarmas={}
            for nombre,hora,minuto in listaDatosAlarmas:
                dictHorasAlarmas[nombre]=HoraAlarma(hora,minuto)
                
            conexion.commit()
            conexion.close()

            return dictHorasAlarmas


    def getTodas_alarmas(self):
        conexion=self.iniciarConexion_sql()
        if conexion==None:
            print("Error a la hora de obtener los datos de la pregunta....")
            return False
        else:
            cursor = conexion.cursor()
            # necesitamos obtener el tipo de respuesta de la pregunta...
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

    def getSonidoAsunto_alarma(self,nombreAlarma):
        conexion=self.iniciarConexion_sql()
        if conexion==None:
            print("Error a la hora de obtener los datos de la pregunta....")
            return False
        else:
            cursor = conexion.cursor()
            # necesitamos obtener el tipo de respuesta de la pregunta...
            sqlOrden = f"SELECT SONIDO,ASUNTO FROM  "+self.NAME_TABLA+" WHERE NOMBRE="+"'"+nombreAlarma+"'"
            print("INSTRUCCION",sqlOrden)
            cursor.execute(sqlOrden)
            sonidoYasunto= tuple(cursor.fetchall())  # devuelve una lista con
            print(sonidoYasunto)
            #(   ('nombre/123.mp3',asunto),  )
            return sonidoYasunto[0] #(sonido,asunto)

