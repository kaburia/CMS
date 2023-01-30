#include <Servo.h>
#include <Wire.h>
#include<SPI.h>  
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>


//.......................................SPI with Coral Dev Board Master................................................



//...................... declare an SSD1306 display object connected to I2C.................................
#define SCREEN_WIDTH 128 // OLED display width,  in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels
Adafruit_SSD1306 oled(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);


//...............Encoder interupt and time counter declaration................................................
                                       //Arduino's interrrupt pin 3 and 2
#define EN_IN1 3 // Encoder Interupt 3
#define EN_IN2 2 //Encoder Interupt 2
//measurement interval in milliseconds
int interval = 1000;
//milliseconds counter during the interval
long previousMillis = 0;
long currentMillis = 0;


//...................RPM measurement variable..................................................................
#define EN_Rev 360
int rpm = 0;
float rpm_oriji;
//initializing encoder pulse count
volatile long encoderValue = 0;


//..................................  L298 MOTOR DRIVER CONTROL..................................................
int enA = 5; //enable motors A pwm
int enB = 6;//enable motors B pwm

int in1 = A0; //i motors A Direction
int in2 = A1;
int in3 = A2; // motors B Direction
int in4 = A3;

//.............................ULTRASONIC SENSOR.................................................................
// defines pins numbers
const int trigPin = 8;
const int echoPin = 4;
// defines variables
long duration;
int distance;



//............................Servo...........................................................

Servo myservo; 
int Degree;


//..............................................................................................................................................................................................
void setup() {
   // For the serial monitor 
  Serial.begin(9600);//baud rate

  //....................L298 MOTOR CONTROL............................
  pinMode(enA, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);

  pinMode(enB, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  

//.......................ULTRASONIC SENSOR...............................
   pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  
  
//.........................INTERUPTS.......................................
  pinMode(EN_IN1, INPUT_PULLUP);//Internal pull up to rduce noise
  pinMode(EN_IN2, INPUT_PULLUP);
        //Attaching interrupt. updateEncoder increments encoder value
  attachInterrupt(digitalPinToInterrupt(EN_IN1), updateEncoder, RISING);
  attachInterrupt(digitalPinToInterrupt(EN_IN2), updateEncoder, RISING);
        //initializing the timer
  previousMillis = millis();


//.....................SPI COMMUNICATION WITH DEV BOARD.......................
pinMode(MISO,OUTPUT); 
SPCR |= _BV(SPE);
SPI.attachInterrupt(); 

 
//...........................OLED.............................................
        // initialize OLED display with address 0x3C for 128x64
  if (!oled.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    while (true);
  }
  delay(2000);         // wait for initializing
  oled.clearDisplay(); // clear display
  oled.setTextSize(1);          // text size
  oled.setTextColor(WHITE);     // text color
  oled.setCursor(0, 10);        // position to display // text to display
  oled.display();
//...........................SERVO.............................................
  
   myservo.attach(9,600,2300);  // (pin 9, min 0, max 180 deg =2300 uSec, if 90deg =1450 uSec)
  
  }

  
//................................................................................................................
//................................................................................................................
void loop() {
 
  
  byte Slavesend=Degree;                             
  SPDR = Slavesend;
            
  
  
/*oled.println("Speed");
oled.println(rpm_oriji);
int CentiMetres = Get_Distance();
oled.println(CentiMetres);
oled.println("Meteres");
oled.display();
delay(20);
oled.clearDisplay(); 
oled.setTextSize(1);          // text size
oled.setTextColor(WHITE);     // text color
oled.setCursor(5, 10);        // position to display // text to display
oled.display();*/

Rotate_servo(0);
Left(250);
delay(1000);
Right(250);
delay(1000);
forward(250);
delay(1000);
Rotate_servo(90);




 
}
//..............................................................................................................................................................................

void updateEncoder(){
  //incrementing encoder value
  encoderValue++;
}
ISR (SPI_STC_vect)
{
  byte Slavereceived = SPDR;                  
  bool received = true; 
  /*if (Slavereceived ==DegreeRead ){
    SPDR = Degree;
    }
    if (Slavereceived ==DistanceRead ){
    SPDR = Distance;
    }  
    if (Slavereceived ==forward ){
    
    } 
    if (Slavereceived == Back ){
    
    }
    if (Slavereceived == Left ){
    
    }
    if (Slavereceived == Right ){
    
    }
    if (Slavereceived == Stop ){
    
    }
    if (Slavereceived ==Degree  ){
    
    }*/
    
    
   
     
                        
}

void  forward(int speed){
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);

  analogWrite(enA, speed);
  analogWrite(enB, speed);

  //to update milliseconds every second
  currentMillis = millis();
  
  if (currentMillis - previousMillis > interval){
    previousMillis = currentMillis;
  
//calculating RPM. encoderValue is pulses/sec EN_REV is pulses/rev
  rpm = (float)(encoderValue * 60 / EN_Rev);
  rpm_oriji = rpm/3;

//Resetting the encoderValue
  encoderValue= 0;
  }
}

  
  void  Left(int speed){
  
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  
  analogWrite(enA, speed);
  analogWrite(enB, speed);

  //to update milliseconds every second
  currentMillis = millis();
  
  if (currentMillis - previousMillis > interval){
    previousMillis = currentMillis;
  
//calculating RPM. encoderValue is pulses/sec EN_REV is pulses/rev
  rpm = (float)(encoderValue * 60 / EN_Rev);
  rpm_oriji = rpm/3;

//Resetting the encoderValue
  encoderValue= 0;
  }
  }

  
  void  Right(int speed){
  
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  
  analogWrite(enA, speed);
  analogWrite(enB, speed);

  //to update milliseconds every second
  currentMillis = millis();
  
  if (currentMillis - previousMillis > interval){
    previousMillis = currentMillis;
  
//calculating RPM. encoderValue is pulses/sec EN_REV is pulses/rev
  rpm = (float)(encoderValue * 60 / EN_Rev);
  rpm_oriji = rpm/3;

//Resetting the encoderValue
  encoderValue= 0;
  }
 }


int Get_Distance(){
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance 340m/s * Time(microseconds)=0.034*Time(seconds)
  distance = duration * 0.034 / 2;
  // Prints the distance on the Serial Monitor
  return distance;
 }


 
void Rotate_servo(int Angle){
   myservo.write(Angle);                  // sets the servo position according to the scaled value
  delay(500);   
  }
