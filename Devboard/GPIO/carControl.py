import RPi.GPIO as GPIO #In order to us RPi.GPIO throughout the rest of the Python script
from time import sleep
import time

GPIO.setmode(GPIO.BOARD) #determine  pin-numbering schemes BOARD= pin numbers follow the pin numbers on header OR BCM=pin numbers follow the lower-level numbering system defined by the Raspberry Pi's Broadcom-chip brain.
GPIO.setwarnings(False)

#...................................ULTRASONIC SENSOR SETUP....................................................


#......................................SERVO SETUP............................................................
PWM_PIN=33 #use GPIO12(BCM) pin 32(*BOARD)
GPIO.setup(PWM_PIN,GPIO.OUT)
Servo = GPIO.PWM(PWM_PIN,50)  #50hz pwm frequency to get a period of 20ms that a servo needs
Servo.start(0)

#....................................MOTOR DRIVER............................................................
class Drive(): #to call the objects functions  moveF ,moveB,STOP,LEFT,RIGHT
    def __init__(self,Ena,In1,In2,Enb,In3,In4):
        self.Ena = Ena
        self.In1 = In1
        self.In2 = In2
        self.Enb = Enb
        self.In3 = In3
        self.In4 = In4
        GPIO.setup(self.Ena,GPIO.OUT)
        GPIO.setup(self.In1,GPIO.OUT)
        GPIO.setup(self.In2,GPIO.OUT)
        GPIO.setup(self.Enb,GPIO.OUT)
        GPIO.setup(self.In3,GPIO.OUT)
        GPIO.setup(self.In4,GPIO.OUT)
        self.pwma = GPIO.PWM(self.Ena,1000) #set pwm pin and a frequency of 1kHz
        self.pwmb = GPIO.PWM(self.Enb,1000)
        self.pwma.start(0)
        self.pwmb.start(0)


    def moveF(self,speed=80,Time =5): #move Forward motors rotate in the same direction  to call it........... Drive1.moveF(Duty Cycle ,Time to move forward).........
        GPIO.output(self.In1,GPIO.HIGH)
        GPIO.output(self.In2,GPIO.LOW)
        GPIO.output(self.In3,GPIO.HIGH)
        GPIO.output(self.In4,GPIO.LOW)
        self.pwma.ChangeDutyCycle(speed)
        self.pwmb.ChangeDutyCycle(speed)
        sleep(Time)
    def moveB(self,speed=80,Time =5): #move ackward motors rotate in the oposite direction to call it........... Drive1.move(Duty Cycle ,Time to reverse).........
        GPIO.output(self.In1,GPIO.LOW)
        GPIO.output(self.In2,GPIO.HIGH)
        GPIO.output(self.In3,GPIO.LOW)
        GPIO.output(self.In4,GPIO.HIGH)
        self.pwma.ChangeDutyCycle(speed)
        self.pwmb.ChangeDutyCycle(speed)
        sleep(Time)
    def STOP(self,Time =2):  #stop motors puling in pins low stops the lm298 to call it........... Drive1.STOP(STOP time else it will stop for 2 sec).........
        GPIO.output(self.In1,GPIO.LOW) #selt in1 high
        GPIO.output(self.In2,GPIO.LOW)
        GPIO.output(self.In3,GPIO.LOW)
        GPIO.output(self.In4,GPIO.LOW)
        self.pwm.ChangeDutyCycle(0) #0% pwm duty cycle
        sleep(Time) 
    def LEFT(self,Time=0.5): #move left to call it........... Drive1.LEFT(Time for this left movement ).........
        GPIO.output(self.In1,GPIO.HIGH)
        GPIO.output(self.In2,GPIO.LOW)
        GPIO.output(self.In3,GPIO.HIGH)
        GPIO.output(self.In4,GPIO.LOW)
        self.pwmb.ChangeDutyCycle(50)
        self.pwma.ChangeDutyCycle(100)
        
        sleep(Time)
    def RIGHT(self,Time =0.5): #move left to call it........... Drive1.RIGHT(Time for this left movement ).........
        GPIO.output(self.In1,GPIO.HIGH)
        GPIO.output(self.In2,GPIO.LOW)
        GPIO.output(self.In3,GPIO.HIGH)
        GPIO.output(self.In4,GPIO.LOW)
        self.pwma.ChangeDutyCycle(50)
        self.pwmb.ChangeDutyCycle(100)
        # self.pwma.ChangeDutyCycle(speed)
        sleep(Time)  


#....................................GET DISTANCE ULTRASONIC..........................................................
def Distance():
    GPIO_TRIGGER = 29 #USE GPIO_5 AS trigger
    GPIO_ECHO = 31 #USE GPIO_6 AS Echo 
    GPIO.setup(GPIO_TRIGGER,GPIO.OUT) # set trigger pin as output
    GPIO.setup(GPIO_ECHO,GPIO.IN) #set echo pin as input
   # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
   # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
#................................Estimated time based on car speed in order to stop on time...................................
def Estimate_Time(D):
  t=D/40 #Distance divided by estimated robot speed since no encoder data of 40cm/sec
  return t

#...........................................SERVO MOTOR CONTROL..............................................................
def SERVO(Angle):
    
    Servo.ChangeDutyCycle(Angle)
    time.sleep(3)
  



