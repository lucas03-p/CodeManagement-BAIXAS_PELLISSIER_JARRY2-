bool startLoop = false;
bool stopLoop = false;
unsigned long startTime;
char buffer[64];


void setup() {
  pinMode(LED_BUILTIN,OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  Serial.begin(1000000,SERIAL_8N1);
  while(!startLoop) {
    if(Serial.available() > 0){
      startLoop = Serial.read() == 114;
    }
  }
  startTime = micros();
}


void loop() {

  float Time = (micros() - startTime) / 1000000.0;
  sprintf(buffer, "%.2f", Time);
  Serial.println(buffer);
  Serial.flush();
 


  digitalWrite(LED_BUILTIN, HIGH);
  if (Serial.available() > 0){
    stopLoop = (Serial.read() == 115);
     if(stopLoop) NVIC_SystemReset();
    }
}


