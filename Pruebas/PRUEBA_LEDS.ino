// PRUEBA 2: LUCES
int gui_izq = A0;
int gui_der = A1;
int faroles = A2;

void setup() {
  pinMode(gui_izq, OUTPUT);
  pinMode(gui_der, OUTPUT);
  pinMode(faroles, OUTPUT);
}

void loop() {
  // 1. Guiñador Izquierdo (A0)
  digitalWrite(gui_izq, HIGH);
  delay(500);
  digitalWrite(gui_izq, LOW);
  
  // 2. Guiñador Derecho (A1)
  digitalWrite(gui_der, HIGH);
  delay(500);
  digitalWrite(gui_der, LOW);

  // 3. Faroles Blancos (A2)
  digitalWrite(faroles, HIGH);
  delay(1000);
  digitalWrite(faroles, LOW);
  
  delay(500);
}