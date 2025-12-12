============================================================
DOCUMENTACIÓN TÉCNICA: AUTO ROBOT ARDUINO (POO + MODULAR)
============================================================

------------------------------------------------------------
1. LISTA DE MATERIALES (HARDWARE)
------------------------------------------------------------
A) CEREBRO Y COMUNICACIÓN:
   - 1x Arduino Uno (con cable USB).
   - 1x Módulo Bluetooth HC-06 (o HC-05 en modo esclavo).

B) POTENCIA Y MOTORES:
   - 4x Motores DC con caja reductora (ruedas amarillas estándar).
   - 2x Drivers L298N (Puentes H).
     * Nota: Cada L298N controla 2 motores (uno para el lado izquierdo, otro para el derecho).
   - Fuente de energía: 2x Baterías Li-ion 18650 (7.4V) o Pack de 6-8 pilas AA.
   - 1x Interruptor ON/OFF (opcional pero recomendado para las baterías).

C) SENSORES E ILUMINACIÓN:
   - 1x Sensor Ultrasónico HC-SR04.
   - 2x LEDs Blancos (Faroles delanteros).
   - 2x LEDs Amarillos/Naranjas (Guiñadores delanteros).
   - 2x LEDs Rojos/Amarillos (Guiñadores traseros).
   - 6x Resistencias de 220 ohm o 330 ohm (una para cada LED o par de LEDs).

D) VARIOS:
   - Cables Jumper (Macho-Macho, Macho-Hembra).
   - Protoboard pequeña (para distribuir voltaje y conectar LEDs).
   - Chasis del auto.

------------------------------------------------------------
2. INSTALACIÓN DE LIBRERÍAS Y SOFTWARE
------------------------------------------------------------
A) EN EL ARDUINO (IDE):
   - No necesitas descargar nada extra.
   - La librería "SoftwareSerial.h" ya viene instalada por defecto en el IDE de Arduino.

B) EN LA COMPUTADORA (PYTHON):
   - Necesitas tener Python instalado.
   - Abre la terminal (CMD o PowerShell) y ejecuta el siguiente comando para instalar la librería de comunicación serial:
   
     pip install pyserial

   - La librería "tkinter" ya viene instalada por defecto con Python.

------------------------------------------------------------
3. DIAGRAMA DE CONEXIONES (CABLEADO)
------------------------------------------------------------
¡IMPORTANTE!: Todas las tierras (GND) de las baterías, los drivers L298N y el Arduino deben estar conectadas entre sí.

A) CONEXIÓN BLUETOOTH (Módulo HC-06):
   - HC-06 VCC  -> Arduino 5V
   - HC-06 GND  -> Arduino GND
   - HC-06 TX   -> Arduino Pin 10  (RX Virtual)
   - HC-06 RX   -> Arduino Pin 11  (TX Virtual)

B) CONEXIÓN MOTORES (Drivers L298N):
   * Pines de Control en Arduino:
   - Arduino Pin 4 -> Driver IN1 (Lado Izquierdo)
   - Arduino Pin 5 -> Driver IN2 (Lado Izquierdo)
   - Arduino Pin 6 -> Driver IN3 (Lado Derecho)
   - Arduino Pin 7 -> Driver IN4 (Lado Derecho)

   * Energía de Motores:
   - Batería (+) -> 12V de los L298N.
   - Batería (-) -> GND de los L298N y GND de Arduino.

C) CONEXIÓN SENSOR ULTRASÓNICO (HC-SR04):
   - Sensor VCC  -> Arduino 5V
   - Sensor GND  -> Arduino GND
   - Sensor Trig -> Arduino Pin 2
   - Sensor Echo -> Arduino Pin 3

D) CONEXIÓN DE LUCES (LEDS):
   * Nota: Conecta la pata larga del LED (+) al pin del Arduino y la corta (-) a GND con una resistencia.
   
   - Guiñadores IZQUIERDA (Delantero y Trasero) -> Arduino Pin A0
   - Guiñadores DERECHA (Delantero y Trasero)   -> Arduino Pin A1
   - Faroles BLANCOS (Delanteros)               -> Arduino Pin A2

------------------------------------------------------------
4. RESUMEN DE COMANDOS (PROTOCOLOS)
------------------------------------------------------------
El sistema funciona enviando caracteres individuales (bytes):

   [MOVIMIENTO]
   'W' -> Ir Adelante
   'S' -> Ir Atrás
   'A' -> Girar Izquierda
   'D' -> Girar Derecha
   ' ' -> (Espacio) Frenar / Detener

   [LUCES]
   'Q' -> Guiñador Derecho (Toggle)
   'E' -> Guiñador Izquierdo (Toggle)
   'R' -> Faroles Blancos (Toggle ON/OFF)

   [CONFIGURACIÓN DE MODO]
   'T' -> Activa modo Serial (USB).
   'Y' -> Activa modo Inalámbrico (Bluetooth).

------------------------------------------------------------
5. PASOS PARA INICIAR
------------------------------------------------------------
1. Cargar el código "Auto_Final_v2.ino" al Arduino mediante cable USB.
2. Abrir la interfaz "control_auto_v2.py" en la computadora.
3. Conectar el puerto COM en la interfaz y pulsar "Conectar".
4. Elegir modo:
   - Si es prueba USB: Click en "MODO CABLEADO (T)".
   - Si es Bluetooth: Click en "MODO BLUETOOTH (Y)", luego desconectar USB, conectar baterías y reconectar la App al puerto Bluetooth de la PC.