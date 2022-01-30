
// ESTE CODIGO FUE OBTENIDO DE: https://github.com/espressif/arduino-esp32/issues/3916

#include "BluetoothSerial.h"
BluetoothSerial SerialBT;
uint8_t address1[6] = {0x98, 0xD3, 0x36, 0x81, 0x13, 0x70}; // HC-05
String name = "blutu_roni";
char *pin = "1234"; //<- standard pin would be provided by default
bool connected;

void setup() {
Serial.begin(115200);
SerialBT.begin("ESP32test", true);
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
if (SerialBT.disconnect()) {
Serial.println("Disconnected Succesfully!");
}
// this would reconnect to the name(will use address, if resolved) or address used with connect(name/address).
SerialBT.connect();


}



void loop() {




}
