///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//  INICIO DE CODIGO:
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#include <BluetoothSerial.h>
#include "Led_sieteColor.h"

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
uint8_t address1[6] = {0x98, 0xD3, 0x36, 0x81, 0x13, 0x70}; // HC-05
String name = "blutu_roni";
char *pin = "1234"; 
bool connected;
Led_sieteColor G_focoDelCuarto(27,26,25,false);

void setup() {
  Serial.begin(115200);
  SerialBT.begin("Cuarto_luzFlamaVentilador", true);
  SerialBT.setPin(pin);
  Serial.println("The device started in master mode, make sure remote BT device is on!");
  // connect(address) is fast (upto 10 secs max), connect(name) is slow (upto 30 secs max) as it needs
  // to resolve name to address first, but it allows to connect to different devices with the same name.
  // Set CoreDebugLevel to Info to view devices bluetooth address and device names
  connected = SerialBT.connect(name);
  //connected = SerialBT.connect(address1);
  
  if(connected) {
    Serial.println("Connected Succesfully!");
  } else {
    while(!SerialBT.connected(10000)) {
    Serial.println("Failed to connect. Make sure remote device is available and in range, then restart app.");
    }
  }
  
  // disconnect() may take upto 10 secs max
  //if (SerialBT.disconnect()) {
  //  Serial.println("Disconnected Succesfully!");
  //}
  
  // this would reconnect to the name(will use address, if resolved) or address used with connect(name/address).
  //SerialBT.connect();


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
