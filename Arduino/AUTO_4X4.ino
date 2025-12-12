

#include <SoftwareSerial.h>

// Configuración Bluetooth: RX en 10 (conecta al TX del HC-06), TX en 11 (conecta al RX del HC-06)
SoftwareSerial BT(10, 11);

// CLASE: SENSOR ULTRASÓNICO
class SensorUltrasonico {
  private:
    int pinTrig, pinEcho;
  public:
    SensorUltrasonico(int t, int e) {
      pinTrig = t; pinEcho = e;
      pinMode(pinTrig, OUTPUT);
      pinMode(pinEcho, INPUT);
    }
    float obtenerDistancia() {
      digitalWrite(pinTrig, LOW); delayMicroseconds(2);
      digitalWrite(pinTrig, HIGH); delayMicroseconds(10);
      digitalWrite(pinTrig, LOW);
      long duration = pulseIn(pinEcho, HIGH, 25000); // Timeout corto
      return (duration == 0) ? 999 : duration * 0.034 / 2;
    }
};

// CLASE: LUCES (Con Toggle para Faroles)
class ControladorLuces {
  private:
    int pIzq, pDer, pFarol;
    unsigned long lastBlink;
    bool ledState;     // Estado para parpadeo
    bool gIzq, gDer;   // Estados guiñadores
    bool farolesOn;    // Estado de faroles

  public:
    ControladorLuces(int i, int d, int f) {
      pIzq = i; pDer = d; pFarol = f;
      pinMode(pIzq, OUTPUT); pinMode(pDer, OUTPUT); pinMode(pFarol, OUTPUT);
      gIzq = false; gDer = false; 
      farolesOn = false; // Empiezan apagados
      ledState = LOW; lastBlink = 0;
      
      digitalWrite(pFarol, LOW); // Asegurar apagado inicial
    }
    
    // Acción para la tecla 'R'
    void toggleFaroles() { 
      farolesOn = !farolesOn; // Invierte el estado
      digitalWrite(pFarol, farolesOn ? HIGH : LOW);
    }
    
    void toggleIzq() { gIzq = !gIzq; gDer = false; if(!gIzq) digitalWrite(pIzq, LOW); }
    void toggleDer() { gDer = !gDer; gIzq = false; if(!gDer) digitalWrite(pDer, LOW); }
    
    void actualizar() {
      if ((gIzq || gDer) && (millis() - lastBlink >= 500)) {
        lastBlink = millis();
        ledState = !ledState;
        if(gIzq) digitalWrite(pIzq, ledState);
        if(gDer) digitalWrite(pDer, ledState);
      }
    }
};


class TrenMotriz {
  private:
    int in1, in2, in3, in4;
  public:
    TrenMotriz(int p1, int p2, int p3, int p4) {
      in1 = p1; in2 = p2; in3 = p3; in4 = p4;
      pinMode(in1, OUTPUT); pinMode(in2, OUTPUT);
      pinMode(in3, OUTPUT); pinMode(in4, OUTPUT);
    }
    void adelante() { digitalWrite(in1, HIGH); digitalWrite(in2, LOW); digitalWrite(in3, HIGH); digitalWrite(in4, LOW); }
    void atras()    { digitalWrite(in1, LOW); digitalWrite(in2, HIGH); digitalWrite(in3, LOW); digitalWrite(in4, HIGH); }
    void izquierda(){ digitalWrite(in1, LOW); digitalWrite(in2, HIGH); digitalWrite(in3, HIGH); digitalWrite(in4, LOW); }
    void derecha()  { digitalWrite(in1, HIGH); digitalWrite(in2, LOW); digitalWrite(in3, LOW); digitalWrite(in4, HIGH); }
    void detener()  { digitalWrite(in1, LOW); digitalWrite(in2, LOW); digitalWrite(in3, LOW); digitalWrite(in4, LOW); }
};

// --- INSTANCIAS GLOBALES ---
TrenMotriz auto(4, 5, 6, 7);      
ControladorLuces luces(A0, A1, A2); 
SensorUltrasonico sensor(2, 3);   

int modoOperacion = 0; // 0=Espera, 1=USB, 2=Bluetooth
bool obstaculoDetectado = false;

void setup() {
  Serial.begin(9600);
  BT.begin(9600);
  // luces.toggleFaroles(); // Descomentar si quieres que inicien PRENDIDOS
  Serial.println("SISTEMA INICIADO. Esperando comando 'T' (USB) o 'Y' (BT)");
}

void loop() {
  luces.actualizar(); 
  verificarSeguridad(); 

  char comando = 0;

  // 1. LEER USB
  if (Serial.available() > 0) {
    char c = toupper(Serial.read());
    if (c == 'T') { modoOperacion = 1; Serial.println("MODO USB ACTIVADO"); }
    else if (c == 'Y') { modoOperacion = 2; Serial.println("MODO BT ACTIVADO"); }
    else if (modoOperacion == 1) comando = c;
  }

  // 2. LEER BLUETOOTH (Solo si modo es 2)
  if (modoOperacion == 2 && BT.available() > 0) {
    char c = toupper(BT.read());
    if (c == 'Y') { Serial.println("Re-confirmado BT"); }
    else comando = c;
  }

  // 3. EJECUTAR
  if (comando != 0 && !obstaculoDetectado) {
    ejecutarMovimiento(comando);
  }
}

void verificarSeguridad() {
  float dist = sensor.obtenerDistancia();
  if (dist > 1 && dist <= 8) {
    if (!obstaculoDetectado) {
      obstaculoDetectado = true;
      maniobraEvasiva();
    }
  } else {
    obstaculoDetectado = false;
  }
}

void maniobraEvasiva() {
  auto.detener(); delay(300);
  auto.atras();   delay(600);
  auto.derecha(); delay(500);
  auto.detener();
  obstaculoDetectado = false; 
}

void ejecutarMovimiento(char cmd) {
  switch (cmd) {
    case 'W': auto.adelante(); break;
    case 'S': auto.atras(); break;
    case 'A': auto.izquierda(); break;
    case 'D': auto.derecha(); break;
    case ' ': auto.detener(); break; 
    
    // --- LUCES ---
    case 'Q': luces.toggleDer(); break;     // Guiñador Derecho
    case 'E': luces.toggleIzq(); break;     // Guiñador Izquierdo
    case 'R': luces.toggleFaroles(); break; // NUEVO: Faroles Blancos ON/OFF
  }
}