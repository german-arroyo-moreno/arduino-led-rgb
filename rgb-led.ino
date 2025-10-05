/*  Automatización para Todos
 *  www.automatizacionparatodos.com
 *  
 *  Como controlar un LED RGB
 *  
 *  EJEMPLO 01
 *  
 *  Ejemplo donde encendemos y apagamos un LED RGB.
 */
 
int pinR = 9;
int pinG = 10;
int pinB = 11;
 
void setup() {
  Serial.begin(9600);
  pinMode(pinR,OUTPUT);
  pinMode(pinG,OUTPUT);
  pinMode(pinB,OUTPUT);
}
 
void loop() {
  while (Serial.available() > 0) {
    int red = Serial.parseInt();
    int green = Serial.parseInt();
    int blue = Serial.parseInt();
    if (Serial.read() == '\n') {
      red = constrain(red, 0, 255);
      green = constrain(green, 0, 255);
      blue = constrain(blue, 0, 255);
      analogWrite(pinR, red);
      analogWrite(pinG, green);
      analogWrite(pinB, blue);
    }
  }
}

//arduino, ejemplo_rgbled
