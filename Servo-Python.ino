#include <Servo.h>    //the library which helps us to control the servo motor
//define the servo name

Servo myServo1;
Servo myServo2;

unsigned int data = 0; //data variable
unsigned int data1 = 0; //data variable
unsigned int pos; //position variable
String inputString = "";         // a String to hold incoming data
bool stringComplete = false;  // whether the string is complete
bool feito = false;

void setup(){

  //define the servo input pins
  myServo1.attach(9); //9
  myServo2.attach(10); //10
  Serial.begin(115200);
  // reserve 20 bytes for the inputString:
  inputString.reserve(20);
  }

void loop(){


if (stringComplete) {

 data = inputString.toInt();
 feito = true;
 // Serial.println("primeiro dado");// debugs
 // Serial.println(data);
 
 
// data1 = inputString.toInt();
  feito = false;
  inputString = "";
  stringComplete = false;
 

  
if ((data < 1) || (data > 400)) 
{
    data = 0;
    data1 = 0;
    inputString = "";
    stringComplete = false;
   // Serial.print("segundo dado "); // debugs
   // Serial.println(data);
   // Serial.print("terceiro dado ");
  //  Serial.println(data1);
}
else{

    if ((data > 0) && (data < 201) ) //1 a 200
       {
       pos=map(data, 0, 200, 20, 170);
       myServo1.write(pos);
       delay(1);
      // Serial.print("posicao ");// debugs
      // Serial.println(pos);
       data = 0;
       data1 = 0;
       inputString = "";
       stringComplete = false;
       }
       
    if ((data > 201) && (data < 401) ) //201 a 400
       {
       data = data - 201; 
       pos=map(data, 0, 199, 20, 170);
       myServo2.write(pos);
       delay(1);
      // Serial.print("posicao ");// debugs
      // Serial.println(pos);
       data = 0;
       data1 = 0;
       inputString = "";
       stringComplete = false;
       }

       
}//else
}//string

}//loop


void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
  
}
