/* Primer Prototipo de Cinta Clasificadora 
 *  Pagina de interes > http://www.schwindt.org/posts/arduino-al-rescate-de-una-balanza
 *  https://github.com/bogde/HX711/blob/master/examples/HX711SerialBegin/HX711SerialBegin.ino
 *  https://articulo.mercadolibre.com.co/MCO-455673917-celda-de-carga-50kg-sensor-de-fuerza-peso-mas-modulo-hx711-_JM
*/
//Librerias
#include <Servo.h>


//Detector de Color

Servo servoAmarillo;
//Pin7
Servo servoAmarillo90;
//Pin 8 for ServoVerde
Servo servoVerde;
//pin 9
Servo servoVerde90;

void setup() {
  Serial.begin(9600);
  //Configuraciones para el Detector de Metales
  initSensorColor();
}

void loop() {
  //Pasando por el Detector de Metal
  //Serial.println("Inicio");
  if(Serial.available() > 0){
    char val = Serial.read();
    if(val == 'v'){
      tratarVerdeOn();
    }
    if(val =='a'){
      tratarAmarilloOn();
    }
  }
}
void tratarVerdeOn(){
  Serial.println("Se Detecto Lima Verde ...");
  servoVerde.write(85);
  servoVerde90.write(100);
  delay(2000);
  tratarVerdeOff();
}
void tratarVerdeOff(){
  servoVerde.write(21);
  servoVerde90.write(46);
  delay(150);
}
void tratarAmarilloOn(){
  Serial.println("Se Detecto Lima Amarilla ...");
  servoAmarillo.write(110);
  servoAmarillo90.write(90);//TODO: Falta configurar!!!
  delay(2000);
  tratarAmarilloOff();
}
void tratarAmarilloOff(){
  servoAmarillo.write(164);
  servoAmarillo90.write(0);//TODO: Falta configurar!!!
   delay(150);
}
void initSensorColor(){
  servoAmarillo.attach(6); // Iniciamos el 6 para ServoAmarillo
  servoAmarillo.write(164); // Desplazamos a la posición 0º
  servoAmarillo90.attach(7); // Iniciamos el 7 para ServoAmarillo90 TODO:Falta Configurar!!!
  servoAmarillo90.write(0); // Desplazamos a la posición 0ºServoAmarillo90 TODO:Falta Configurar!!!
  servoVerde.attach(8); // Iniciamos el 8 para servoVerde
  servoVerde.write(21); // Desplazamos a la posición 21º
  servoVerde90.attach(9); // Iniciamos el 9 para servoVerde
  servoVerde90.write(46); // Desplazamos a la posición 46º
  }

