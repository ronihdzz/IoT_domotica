import os
import sqlite3

from CUERPO.LOGICA.ALARMA.alarma import Alarma


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

    def actualizarEstadoAlarma(self,nombre,prendida):
        conexion=self.iniciarConexion_sql()
        if conexion==None:
            print("Error a la hora de actualizar los, vuelva a intentarlo....")
            return False
        else:
            cursor = conexion.cursor()
            sql="UPDATE "+self.NAME_TABLA
            sql+="""  SET  PRENDIDA=?  WHERE NOMBRE=?"""
            d=listaDias
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

    def getTodas_alarmas(self):
        conexion=self.iniciarConexion_sql()
        if conexion==None:
            print("Error a la hora de obtener los datos de la pregunta....")
            return False
        else:
            cursor = conexion.cursor()
            # necesitamos obtener el tipo de respuesta de la pregunta...
            sqlOrden = f"SELECT * FROM  "+self.NAME_TABLA
            cursor.execute(sqlOrden)
            listaDatosAlarmas= tuple(cursor.fetchall())  # devuelve una lista con
            #(   ('Julian', 1, 9, 30, 1, 1, 1, 0, 0, 0, 0, 0), ....   )

            listaAlarmas=[]
            for datosAlarmas in listaDatosAlarmas:
                nombre=datosAlarmas[0]
                asunto=datosAlarmas[1]
                hora=datosAlarmas[2]
                minuto=datosAlarmas[3]
                diasActiva=datosAlarmas[4:-1]
                prendida=datosAlarmas[-1]
                
                alarma=Alarma(nombre=nombre, asunto=asunto,hora=hora,minuto=minuto,
                diasActiva=diasActiva,prendida=prendida)

                listaAlarmas.append(alarma)

            conexion.commit()
            conexion.close()

            return listaAlarmas