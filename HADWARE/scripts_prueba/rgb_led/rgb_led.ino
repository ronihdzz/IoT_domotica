///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//  DEFINICIÓN DE CLASE:
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
   Led_sieteColor(byte _pinRojo,byte _pinVerde, byte _pinAzul,byte _anodo);
   void cambiarColor(byte idColor);
   void prender();
   void apagar();
};

const bool Led_sieteColor::COLORES[8][3]={ 
                   {1,1,1},  //blanco
                   {1,0,0}, //rojo
                   {0,1,0}, //verde
                   {0,0,1}, //azul
                   {1,1,0}, //amarillo
                   {1,0,1}, //magenta
                   {0,1,1}, //cian
                };
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
  this->estadoRojo=COLORES[idColor][0];
  this->estadoVerde=COLORES[idColor][1];
  this->estadoAzul=COLORES[idColor][2];
  if(this->prendido) this->prender();
}
void Led_sieteColor::prender(){
  this->prendido=true;
  digitalWrite(this->pinRojo,this->estadoRojo);
  digitalWrite(this->pinVerde,this->estadoVerde );
  digitalWrite(this->pinAzul,this->estadoAzul);
}
void Led_sieteColor::apagar(){
  this->prendido=false;
  digitalWrite(this->pinRojo,this->anodo);
  digitalWrite(this->pinVerde,this->anodo);
  digitalWrite(this->pinAzul,this->anodo);  
}


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//  INICIO DE CODIGO:
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

Led_sieteColor foco_miCuarto(25,26,27,false);

void setup() {
  
  
}
void loop() {
  for(int i=0; i<7;i++){
    foco_miCuarto.cambiarColor(i);
    delay(500);
  }
  foco_miCuarto.apagar();
  delay(2000);
  foco_miCuarto.prender();
}
