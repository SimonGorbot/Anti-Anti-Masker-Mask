#include <Servo.h>
#include "Arduino.h"
#include "Wire.h"
#include "DFRobot_VL53L0X.h"

DFRobot_VL53L0X sensor;

Servo shootServoRight;  // create servo object to control a servo
Servo shootServoLeft;
Servo pusherMotor;

int RIGHT_SERVO_PIN = 4;
int LEFT_SERVO_PIN = 3;

int SHOOT_SPEED = 100;

void shootStraight(int m_speed) //20 to 160
{
     shootServoLeft.write(m_speed);
     shootServoRight.write(m_speed);
}

void shootStop()
{
    shootServoLeft.write(20);
    shootServoRight.write(20);
}

void shootBullet()
{
  shootStraight(SHOOT_SPEED);
  pusherMotor.write(170); //push
  delay(1500);
  pusherMotor.write(10); //move in
  shootStop();
}

int returnDistance()
{
  Serial.print("Distance: ");
  Serial.println(sensor.getDistance());
  //The delay is added to demonstrate the effect, and if you do not add the delay,
  //it will not affect the measurement accuracy
  return sensor.getDistance();
}


void setup() {
  shootServoRight.attach(RIGHT_SERVO_PIN);  // attaches the servo on pin 9 to the servo object
  shootServoLeft.attach(LEFT_SERVO_PIN);
  shootStop();
  pusherMotor.attach(9);
  
  //initialize serial communication at 9600 bits per second:
  Serial.begin(115200);
  //join i2c bus (address optional for master)
  Wire.begin();
  //Set I2C sub-device address
  sensor.begin(0x50);
  //Set to Back-to-back mode and high precision mode
  sensor.setMode(sensor.eContinuous,sensor.eHigh);
  //Laser rangefinder begins to work
  sensor.start();
}

void loop() {
  Serial.println(returnDistance());
  if(Serial.available() > 0) //means data is 1
  {
    int data = Serial.readString().toInt();
    if(returnDistance() <= 1300)
    {
      shootBullet();
      Serial.println("shot bullet!");
    }
    
  }
}
