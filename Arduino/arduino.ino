#include "HX711.h"


bool startLoop = false;
char buffer[64];


const int HX711_DOUT = 13;
const int HX711_SCK = 12;


HX711 jauge;


unsigned long startTime;


void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);


  // Même vitesse que Python
  Serial.begin(115200, SERIAL_8N1);


  // Initialisation du HX711
  jauge.begin(HX711_DOUT, HX711_SCK);


  // Attendre la commande 'r'
  while (!startLoop) {
    if (Serial.available() > 0) {
      startLoop = (Serial.read() == 114);
    }
  }


  startTime = micros();
}


void loop() {


  // Vérifier la commande d'arrêt
  if (Serial.available() > 0) {
    if (Serial.read() == 115) {
      NVIC_SystemReset();
    }
  }


  // Vérifier si le HX711 est prêt
  if (jauge.is_ready()) {


    long valeurBrute = jauge.read();


    float temps = (micros() - startTime) / 1000000.0;


    // Formater les données
    sprintf(buffer, "%.3f;%ld", temps, valeurBrute);


    // Transmettre au PC
    Serial.println(buffer);
  }


  digitalWrite(LED_BUILTIN, HIGH);
}








