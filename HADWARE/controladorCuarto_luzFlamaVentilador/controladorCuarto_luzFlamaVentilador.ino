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
#define FUEGO_DETECTADO 3
#define FUEGO_APAGADO 4


//ID DE LOS SENSORES...
#define VENTILADOR  10
#define FOCO  11

//CONSTANTES...
const char CHAR_SEGURIDAD='_';  
const byte PIN_VENTILADOR=32; //D32
const byte PIN_LED_ALERTA_FLAMA=23; //D23
const byte PIN_SENSOR_FLAMA=15; //D15

//VARIABLES GLOBALES...
BluetoothSerial SerialBT;
Led_sieteColor G_focoDelCuarto(25,26,27,false);
bool SIN_FLAMA=true;
String respuesta="";

void setup() {
  Serial.begin(115200);
  SerialBT.begin("Cuarto_luzFlamaVentilador");

  pinMode(PIN_VENTILADOR,OUTPUT);
  pinMode(PIN_LED_ALERTA_FLAMA,OUTPUT);
  
  pinMode(PIN_SENSOR_FLAMA, INPUT_PULLUP);
  attachInterrupt(PIN_SENSOR_FLAMA,flamaDetectada,RISING);  
}



void loop() {
  char charTerminaMensaje='+'; //le asignamos un char diferente al CHAR_SEGURIDAD
  byte idSensor,idOrdenRealizar; 
  void (*ordenRealizar)(int); //puntero a funcion...
  int param_1=0;
  char charBufer='+'; 

  while( charBufer!=CHAR_SEGURIDAD &&  SIN_FLAMA ){
    charBufer= char( SerialBT.read() );
    //Serial.print(charBufer);
    delay(100);
  }
  
  if(SIN_FLAMA){
        //Serial.println("ENTRAMOS AL PARSEint: ");
        idSensor=SerialBT.parseInt();
        //Serial.println("SALIMOS DEL PARSEint: ");
        //SerialBT.read();//con esto eliminamos al separador(en este caso a la ',' ) del buffer

        //Serial.println("ENTRAMOS AL PARSEint: ");
        idOrdenRealizar=SerialBT.parseInt();//puede ser cero(apagar) o uno(prender)
        //Serial.println("SALIMOS DEL PARSEint: ");

        
        //Serial.print("ID SENSOR: ");Serial.println(idSensor);
        //Serial.print("ID ORDEN: ");Serial.println(idOrdenRealizar);
  
        switch(idSensor){
            case FOCO:
                switch(idOrdenRealizar){
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
                    break;
                 default:
                   break;
               }  
           break;
                   
           case VENTILADOR:
                switch(idOrdenRealizar){
                  case PRENDER:
                    ordenRealizar=&prenderVentilador;
                    break;
                  case APAGAR:
                    ordenRealizar=&apagarVentilador;
                    break;
                  default:
                   break;
               }
            break;
            
           default:
               break;  
  }//fin del swith...
      
  charTerminaMensaje=char(SerialBT.read());
  //Serial.print("FIN MENSAJE: ");Serial.println(charTerminaMensaje);
  if(charTerminaMensaje==CHAR_SEGURIDAD){
      //Serial.println("EJECUTANDO ORDEN: ");
      ordenRealizar(param_1); 
      respuesta=CHAR_SEGURIDAD+String(idSensor)+CHAR_SEGURIDAD+"\n";
      SerialBT.println(respuesta); //le notificamos que ya fue realizado la orden
  }          
 }else{ //SE DETECO FUEGO...
    digitalWrite(PIN_LED_ALERTA_FLAMA,HIGH);
    apagarFoco(10);apagarVentilador(10); //hacemos esto por precaucion...
    
    while(true){
        delay(100);
        //Serial.print("ALERTA ");Serial.println(SIN_FLAMA);
        respuesta=CHAR_SEGURIDAD+String(FUEGO_DETECTADO)+CHAR_SEGURIDAD+"\n";
        SerialBT.println(respuesta);
        SIN_FLAMA =!(digitalRead(PIN_SENSOR_FLAMA));
        if (SIN_FLAMA){
          break;
        }
    }
    digitalWrite(PIN_LED_ALERTA_FLAMA,LOW); 
    SIN_FLAMA=true;
    //ya que se apago el incendio debemos noticarle a la casa que 
    //ya no hay fuego y debemos sercioaranos que ya recibio el mensaje
    //en caso contrario no podremos continuar los labores normales...
    respuesta=CHAR_SEGURIDAD+String(FUEGO_APAGADO)+CHAR_SEGURIDAD+"\n";
    while( !SerialBT.available() ) {
      SerialBT.println(respuesta);
      delay(250);
    }//lo siguiente a esperar sera una instruccion...
 }
 
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

void flamaDetectada(){
  SIN_FLAMA=false;
}
