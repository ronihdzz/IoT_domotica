///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//  INICIO DE CODIGO:
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

//TSerial and Classical Bluetooth (SPP)
//SerialBT 
#include <BluetoothSerial.h>
#include "Led_sieteColor.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

// ESTADOS DE LOS SENSORES...
#define APAGAR 0
#define PRENDER 1
#define CAMBIAR_COLOR_FOCO 2
#define ORDEN_ATENDIDA 5

//ID DE LOS SENSORES...
#define VENTILADOR  10
#define FOCO  11

//CONSTANTES...
const char CHAR_SEGURIDAD='_';  
const char CHAR_NO_SEGURIDAD='+';
const byte PIN_VENTILADOR=32; //D32

// Dato de tipo puntero a funcion que retornaran unas funciones...
typedef void (*ordenUnSensor)(int);


//VARIABLES GLOBALES...
BluetoothSerial SerialBT;
Led_sieteColor G_focoDelCuarto(25,26,27,false);

void setup() {
  Serial.begin(115200);
  SerialBT.begin("Cuarto_luzFlamaVentilador");

  pinMode(PIN_VENTILADOR,OUTPUT); 

}



void loop() {
  char charTerminaMensaje;
  byte idSensor,idOrdenRealizar; 
  //void (*ordenRealizar)(int); //puntero a funcion...
  ordenUnSensor ordenRealizar; //puntero a funcion..
  int param_1;
  char charBufer; 
  String respuesta;

  
  while(true){
      charTerminaMensaje=CHAR_NO_SEGURIDAD; //le asignamos un char diferente al CHAR_SEGURIDAD
      charBufer=CHAR_NO_SEGURIDAD; 
      respuesta="";
      param_1=0;
      
      while( charBufer!=CHAR_SEGURIDAD   ){
        charBufer= char( SerialBT.read() );
        Serial.print(charBufer);
        delay(100);
      }
      Serial.println("ENTRAMOS AL PARSEint: ");
      idSensor=SerialBT.parseInt();
      Serial.println("SALIMOS DEL PARSEint: ");
      SerialBT.read();//con esto eliminamos al separador(en este caso a la ',' ) del buffer
  
      Serial.println("ENTRAMOS AL PARSEint: ");
      idOrdenRealizar=SerialBT.parseInt();//puede ser cero(apagar) o uno(prender)
      Serial.println("SALIMOS DEL PARSEint: ");
      
      Serial.print("ID SENSOR: ");Serial.println(idSensor);
      Serial.print("ID ORDEN: ");Serial.println(idOrdenRealizar);
  
      switch(idSensor){
          case FOCO:
            ordenRealizar=foco_dameOrden(idOrdenRealizar,&param_1);
            break;
                   
         case VENTILADOR:
            ordenRealizar=ventilador_dameOrden(idOrdenRealizar);
          break;
          
         default:
             break;  
    }//fin del swith...
        
    charTerminaMensaje=char(SerialBT.read());
    Serial.print("FIN MENSAJE: ");Serial.println(charTerminaMensaje);
    if(charTerminaMensaje==CHAR_SEGURIDAD){
        Serial.println("EJECUTANDO ORDEN: ");
        ordenRealizar(param_1); 
        respuesta=empaquetarMensaje(String(ORDEN_ATENDIDA));
        SerialBT.println(respuesta); //le notificamos que ya fue realizado la orden
    }
    
  }          
}

  
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// MENUS DE CADA SENSOR...
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

ordenUnSensor foco_dameOrden(int idOrden,int *puntero_param1){
    int param_1;
    //void (*ordenRealizar)(int); //puntero a funcion...
    ordenUnSensor ordenRealizar; //puntero a funcion...
    switch(idOrden){
     case PRENDER:
        ordenRealizar=&prenderFoco;
        break;
     case APAGAR:
        ordenRealizar=&apagarFoco;
        break;
     case CAMBIAR_COLOR_FOCO:
        ordenRealizar=&cambiarColorFoco;
        Serial.read();//con esto eliminamos al separador(en este caso a la ',' ) del buffer
        param_1=SerialBT.parseInt(); //esto representara el color del foco
        *puntero_param1=param_1;
        break;
     default:
       break;
   }
   return ordenRealizar; 
}


ordenUnSensor ventilador_dameOrden(int idOrden){
    //void (*ordenRealizar)(int); //puntero a funcion...
    ordenUnSensor ordenRealizar; //puntero a funcion...
    switch(idOrden){
        case PRENDER:
          ordenRealizar=&prenderVentilador;
          break;
        case APAGAR:
          ordenRealizar=&apagarVentilador;
          break;
        default:
         break;
   }
   return ordenRealizar; 
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//  COMPORTAMIENTOS DE LOS DIFERENTES ESTADOS DE MIS CENSORES...
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void prenderFoco(int _noImporta ){
   G_focoDelCuarto.prender();
}

void apagarFoco(int _noImporta ){
   G_focoDelCuarto.apagar();
}

void cambiarColorFoco(int idColor){
  G_focoDelCuarto.cambiarColor(idColor);
}

void prenderVentilador(int _noImporta ){
  digitalWrite(PIN_VENTILADOR,HIGH);  
}

void apagarVentilador(int _noImporta ){
 digitalWrite(PIN_VENTILADOR,LOW);     
}


String empaquetarMensaje(String mensaje){
  mensaje=CHAR_SEGURIDAD+mensaje+CHAR_SEGURIDAD;
  return mensaje;
}
