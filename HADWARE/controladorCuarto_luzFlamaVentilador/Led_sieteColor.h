#ifndef RONI_LIBRARY_LED_SIETE_COLOR
#define RONI_LIBRARY_LED_SIETE_COLOR


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//  DEFINICIÓN DE CLASE  'Led_sieteColor':
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class Led_sieteColor{
  private:
    byte pinRojo;
    byte pinVerde;
    byte pinAzul;
    bool estadoRojo;
    bool estadoVerde;
    bool estadoAzul;
    bool anodo;  //true o false
    bool prendido; //true o false
  public:
   static const bool COLORES[8][3];
   static const byte NO_COLORES;
   Led_sieteColor(byte _pinRojo,byte _pinVerde, byte _pinAzul,byte _anodo);
   void cambiarColor(byte idColor);
   void prender();
   void apagar();
};

const bool Led_sieteColor::COLORES[8][3]={ //configuración para leds anodos
                   {0,0,0},  //blanco
                   {0,1,1}, //rojo
                   {1,0,1}, //verde
                   {1,1,0}, //azul
                   {0,0,1}, //amarillo
                   {0,1,0}, //magenta
                   {1,0,0}, //cian
                };
const byte Led_sieteColor::NO_COLORES=7;
Led_sieteColor::Led_sieteColor(byte _pinRojo,byte _pinVerde, byte _pinAzul,byte _anodo){
  this->pinRojo=_pinRojo;
  this->pinVerde=_pinVerde;
  this->pinAzul=_pinAzul;
  this->anodo=_anodo;
  pinMode(this->pinRojo,OUTPUT);
  pinMode(this->pinVerde,OUTPUT);
  pinMode(this->pinAzul,OUTPUT);

  this->apagar(); //estado default, apagado
  this->cambiarColor(0); //color default cargado, blanco
    
}
void Led_sieteColor::cambiarColor(byte idColor){
  if (idColor<NO_COLORES){
      this->estadoRojo=COLORES[idColor][0];
      this->estadoVerde=COLORES[idColor][1];
      this->estadoAzul=COLORES[idColor][2];
      if(this->prendido) this->prender();
  }
}
void Led_sieteColor::prender(){
  this->prendido=true;
  if (this->anodo){
      digitalWrite(this->pinRojo,this->estadoRojo);
      digitalWrite(this->pinVerde,this->estadoVerde );
      digitalWrite(this->pinAzul,this->estadoAzul);
  }else{
      digitalWrite(this->pinRojo, not(this->estadoRojo)  );
      digitalWrite(this->pinVerde,not(this->estadoVerde) );
      digitalWrite(this->pinAzul, not(this->estadoAzul)  );
  }
}

void Led_sieteColor::apagar(){
  //Si es anado para apagarlos no debe de ver diferencial
  //de potencial por tal motivo si en todos son 5-5 [V]
  //estara apagado, pero si es cato su valor sera LOW=0=False
  this->prendido=false;
  digitalWrite(this->pinRojo,this->anodo);
  digitalWrite(this->pinVerde,this->anodo);
  digitalWrite(this->pinAzul,this->anodo);  
}

#endif
