void setup() {
  // mettre le port LED_BUILTIN en output
  pinMode(LED_BUILTIN,OUTPUT);
  //mettre le port à low (éteindre la led)
  digitalWrite(LED_BUILTIN, LOW);
  // Demarre/configurer le port série : serial
  Serial.begin(1000000,SERIAL_8N1);
  //attendre réception caractére spéciale du port série (boucle whyle)
  while(!startLoop)) {
    if(Serial.available() > 0){ // tant qu’il n’y a pas de donnée envoyé ( dans le port serie)
      int value = Serial.read(); // on affecte la fonction serial.read au mots value
      if(value == 114) startLoop = true; // ici on précise que l'on attent la lettre r minisucule pour allumer la lumière
    }
  }
}
// une foix qu'il n'y a plus rien à faire passe automatiquement dans le loop

}

void loop() {
  // put your main code here, to run repeatedly:

}
