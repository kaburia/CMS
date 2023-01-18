
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // OLED display width,  in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

// declare an SSD1306 display object connected to I2C
Adafruit_SSD1306 oled(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
//Encoder pulse per revolution standard value
#define EN_Rev 360
//Arduino's interrrupt pin 3
#define EN_IN 3 //yellow
//PWM to D10
#define PWM 5 //motor speed enabler
//Encoder DIR to D12
#define DIR 12 //motor direction IN1

//initializing encoder pulse count
volatile long encoderValue = 0;

float rpm_oriji;
int en = 5;
int in1 = 6;
int in2 = 7;


//measurement interval in milliseconds
int interval = 1000;

//milliseconds counter during the interval
long previousMillis = 0;
long currentMillis = 0;

//RPM measurement variable
int rpm = 0;

//PWM motor speed output
int motorPwm = 70;



void setup() {
   // For the serial monitor 
  Serial.begin(9600);//baud rate
  pinMode(en, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  //to reduce the noise
  pinMode(EN_IN, INPUT_PULLUP);

  pinMode(PWM, OUTPUT);
  pinMode(DIR, OUTPUT);

  //Attaching interrupt. updateEncoder increments encoder value
  attachInterrupt(digitalPinToInterrupt(EN_IN), updateEncoder, RISING);

  //initializing the timer
  previousMillis = millis();

  // put your setup code here, to run once:
Serial.begin(9600);

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
  
 
  
}

void loop() {
   runmotor();
   oled.println("Speed");
 
  oled.println(rpm_oriji);
  
  oled.display();
  delay(20);
  oled.clearDisplay(); 
   oled.setTextSize(1);          // text size
  oled.setTextColor(WHITE);     // text color
  oled.setCursor(0, 10);        // position to display // text to display
  oled.display();

 
}
void updateEncoder(){
  //incrementing encoder value
  encoderValue++;
}
void runmotor(){
   
  analogWrite(PWM, motorPwm);

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
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(en, 255);
 
  // put your main code here, to run repeatedly:

  
  
  }
