#include <math.h>

//Variables globales:
bool G_sonidoDetectado=false;
bool G_flamaDetectada=false;
long G_tiempo=500;

//Estados de los sensores:
#define TEMPERATURA "1"
#define SONIDO_DETECTADO "2"
#define FUEGO_DETECTADO "3"
#define FUEGO_APAGADO "4"
//Constantes...
const String CHAR_SEGURIDAD="_";
const String SEP_ENTRE_DATOS=",";

//Pines...
#define PIN_MICROFONO 2
#define PIN_SENSOR_FLAMA 3
#define PIN_SENSOR_TEMPERATURA A7

void setup() {
 Serial.begin(9600);
 attachInterrupt(digitalPinToInterrupt(PIN_MICROFONO),sonidoDetectado,RISING);
 attachInterrupt(digitalPinToInterrupt(PIN_SENSOR_FLAMA),flamaDetectada,RISING); 
  
}
void loop() {
  char respuesta;
  String mensaje;

  while(true){
    if (!G_sonidoDetectado && !G_flamaDetectada ){
       mensaje= (TEMPERATURA+SEP_ENTRE_DATOS);
       mensaje+= String(Thermister(analogRead(PIN_SENSOR_TEMPERATURA)));  
       mensaje=empaquetarMensaje( mensaje ); 
            
    }else if(G_sonidoDetectado){
      G_sonidoDetectado=false;
      G_tiempo=750;
      mensaje=empaquetarMensaje( SONIDO_DETECTADO );
    }else{
      actuar_fuegoDetectado();
      continue;
    }
   Serial.println(mensaje);
   delay(G_tiempo); 
 }

}


double Thermister(int RawADC) {
 double Temp;
 Temp = log(((10240000/RawADC) - 10000));
 Temp = 1 / (0.001129148 + (0.000234125 + (0.0000000876741 * Temp * Temp ))* Temp );
 Temp = Temp - 273.15; // Convert Kelvin to Celcius
 return Temp;
}

void sonidoDetectado(){
  G_sonidoDetectado=true;
  G_tiempo=0;
}

void flamaDetectada(){
  G_flamaDetectada= true;
}


String empaquetarMensaje(String mensaje){
  mensaje=CHAR_SEGURIDAD+mensaje+CHAR_SEGURIDAD;
  return mensaje;
}


// DESACTIVAR Y ACTIVAR INTERRUPCCIONES...
//https://community.particle.io/t/nointerrupts/47264
void actuar_fuegoDetectado(){
  String mensaje;
  int MAX_ESPERA=10;
  int c=0; //contador de esperas
  //desactivamos la interrupccion del micronfono
  detachInterrupt(digitalPinToInterrupt(PIN_MICROFONO)) ;
  //vaciamos todo nuestro buffer
  while(Serial.available()){  Serial.read();  } 
  //medimos mientras dure el fuego cada 500 [ms]
  while(true){       
    delay(500);
    //Serial.print(" FUEGO... ");
    G_flamaDetectada =digitalRead(PIN_SENSOR_FLAMA);
    if (!G_flamaDetectada){ //la flama ya no es detectada...
      mensaje=empaquetarMensaje( FUEGO_APAGADO );
      Serial.println(mensaje) ;
      delay(250);
      c+=1;
      if( Serial.available() || c >MAX_ESPERA){//recibimos alguna respuesta...
        G_flamaDetectada=false;
        break;
      }
   }else{//la flama sigue siendo detectada...
      mensaje=empaquetarMensaje( FUEGO_DETECTADO );
      Serial.println(mensaje);
    }
    
 }
 attachInterrupt(digitalPinToInterrupt(PIN_MICROFONO),sonidoDetectado,RISING);
}
