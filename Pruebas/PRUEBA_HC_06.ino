// PRUEBA 4: BLUETOOTH
#include <SoftwareSerial.h>

// RX en 10, TX en 11
SoftwareSerial BT(10, 11); 

void setup() {
  Serial.begin(9600); // Comunicación con PC
  BT.begin(9600);     // Comunicación con HC-06
  Serial.println("Modo CHAT: Escribe en la PC o en el Celular");
}

void loop() {
  // Si el Bluetooth manda algo, mostrarlo en PC
  if (BT.available()) {
    Serial.write(BT.read());
  }

  // Si la PC manda algo, enviarlo al Bluetooth
  if (Serial.available()) {
    BT.write(Serial.read());
  }
}