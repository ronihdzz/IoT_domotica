#include <math.h>
#define SENSOR_TEMP A4;
#define SENSOR_MICRO A5;


String charSeguridad="_";
String mensaje="";
long tiempo=500;
bool sonido=false;

double Thermister(int RawADC) {
 double Temp;
 Temp = log(((10240000/RawADC) - 10000));
 Temp = 1 / (0.001129148 + (0.000234125 + (0.0000000876741 * Temp * Temp ))* Temp );
 Temp = Temp - 273.15; // Convert Kelvin to Celcius
 return Temp;
}

void sonidoDetectado(){
  sonido=true;
  tiempo=0;
}

void setup() {
 Serial.begin(9600);
 attachInterrupt(digitalPinToInterrupt(2),sonidoDetectado,RISING);
}
void loop() {
    if (!sonido){
       mensaje=charSeguridad + "0," + String(Thermister(analogRead(A4))) +charSeguridad+"\n";          
    }else{
      sonido=false;
      tiempo=750;
      mensaje=charSeguridad+ "1" + charSeguridad+"\n";
    }
    Serial.print(mensaje);
    delay(tiempo);
}
