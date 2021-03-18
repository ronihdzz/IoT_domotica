const int pinMicrophone = A5;
 
void setup ()
{
  pinMode (pinMicrophone, INPUT);
  Serial.begin(9600);
}
 
void loop ()
{
  bool soundDetected = digitalRead(pinMicrophone);
  if (soundDetected)
  {
    Serial.println("DECTECTADO");
    delay(1000);
  }
  else
  {
    delay(10);
  }
}
