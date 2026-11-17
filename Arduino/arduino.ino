#include "HX711.h"




bool startLoop = false;
unsigned long startTime;
char buffer[64];




const int HX711_DOUT = 13;
const int HX711_SCK = 12;




// À remplir après la calibration (phase 1 : laisser 0.0 et 1.0)
const float OFFSET = 0.0;   // valeur brute à vide
const float SCALE = 1.0;    // unités brutes par gramme




HX711 jauge;




void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);




  Serial.begin(115200, SERIAL_8N1);
  jauge.begin(HX711_DOUT, HX711_SCK);




  // Attendre la commande 'r' (114) envoyée par Python
  while (!startLoop) {
    if (Serial.available() > 0) {
      startLoop = (Serial.read() == 114);
    }
  }




  digitalWrite(LED_BUILTIN, HIGH);
  startTime = micros();
}




void loop() {
  // Commande d'arrêt 's' (115)
  if (Serial.available() > 0) {
    if (Serial.read() == 115) NVIC_SystemReset();
  }




  if (jauge.is_ready()) {
    // 1) Lire la valeur brute
    long brute = jauge.read();




    // 2) Calculer la valeur calibrée (en milligrammes)
    long masse_mg = (long)(1000.0 * (brute - OFFSET) / SCALE);




    unsigned long t_ms = (micros() - startTime) / 1000;




    // 3) Transmettre : temps(ms) ; brute ; masse(mg)
    sprintf(buffer, "%lu;%ld;%ld", t_ms, brute, masse_mg);
    Serial.println(buffer);
  }
}



