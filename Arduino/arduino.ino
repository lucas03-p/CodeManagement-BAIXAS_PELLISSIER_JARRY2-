bool startLoop = false;
bool stopLoop = false;
long startTime = 0

void setup() {
  pinMode(LED_BUILTIN,OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);




  Serial.begin(1000000,SERIAL_8N1);
  while(!startLoop) {
    if(Serial.available() > 0){
      startLoop = Serial.read() == 114;
    }
  }
}


void loop() {
  time = micros() - startTime;
  Serial.println(time);
  delay(1000)

  digitalWrite(LED_BUILTIN, HIGH);
  if (Serial.available() > 0){
    stopLoop = (Serial.read() == 115);
     if(stopLoop) NVIC_SystemReset();
    }


 




}
