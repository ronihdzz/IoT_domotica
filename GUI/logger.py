import logging
from recursos import App_Principal

'''
Niveles:

    1) DEBUG-.Información detallada, por lo general de interés solo cuando se diagnostican problemas.

    2) INFO-.Confirmación de que las cosas están funcionando como se esperaba.
    
    3) WARNING-.Una indicación de que sucedió algo inesperado, o indicativo de 
    algún problema en el futuro cercano (por ejemplo, 'espacio en disco bajo').
    El software sigue funcionando como se esperaba.
    
    4) ERROR-. Debido a un problema más grave, el software no ha podido realizar 
    alguna función.
    
    5) CRITICAL-. Un error grave que indica que es posible que el programa en sí no pueda seguir ejecutándose.

Formatos:

    A) Tiempo= '%(asctime)s '
    B) Nivel del mensaje= '%(levelname)s'
    C) Nombre del archivo que envia la informacion= '%(filename)s'
    D) Numero de linea= '%(lineo)s'
    E) Contenido del mensaje= '%(message)s'
'''


logger = logging

print(App_Principal.NOMBRE_ARCHIVO_LOG)

# CARACTERISTICAS DEL REPORTE: 
logger.basicConfig( level=logging.DEBUG, # remplazar por 'DEBUG' para un reporte mas amplio
                    format='%(asctime)s: %(levelname)s [%(filename)s:%(lineno)s] %(message)s',
                    handlers=[
                                logging.FileHandler(App_Principal.NOMBRE_ARCHIVO_LOG),  # indicando el nombre del archivo donde se escribiran los mensajes
                                logging.StreamHandler()   # esta función ocacione que los mensajes se muestren en consola
                            ])






