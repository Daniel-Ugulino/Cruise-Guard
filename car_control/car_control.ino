#include "BluetoothSerial.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif
#define SOUND_SPEED 0.034
#define DIST_LIM 50

BluetoothSerial SerialBT;

const int pin_ena = 4;
const int pin_in1 = 16;
const int pin_in2 = 17;

const int pin_enb = 26;
const int pin_in3 = 33;
const int pin_in4 = 25;

const int trigPin = 22;
const int echoPin = 23;

float speedMa = 0;
float speedMb = 0;

char last_control = 'N';

void setup()
{
  Serial.begin(9600);
  SerialBT.begin("ESP32test");
  Serial.println("The device started, now you can pair it with bluetooth!");

  pinMode(pin_ena, OUTPUT);
  pinMode(pin_in1, OUTPUT);
  pinMode(pin_in3, OUTPUT);

  pinMode(pin_enb, OUTPUT);
  pinMode(pin_in2, OUTPUT);
  pinMode(pin_in4, OUTPUT);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop()
{
  char control = 'N';
  float distance = distance_sensor();

  if (SerialBT.available())
  {
    control = SerialBT.read();
  }

  if (distance >= DIST_LIM)
  {
    switch ((char)control)
    {
    case '1':
      startEngine(3);
      speedControl(14.5, 15);
      break;
    case '2':
      startEngine(3);
      speedControl(16.5, 17);
      break;
    case '3':
      startEngine(3);
      speedControl(18.5, 19);
      break;
    case '4':
      startEngine(3);
      speedControl(20.5, 22);
      break;
    case '5':
      startEngine(3);
      speedControl(25, 25);
      break;
    case 'S':
      stop();
      break;
    case 'R':
      directionControl(1);
      break;
    case 'L':
      directionControl(2);
      break;
    }
  }
  else if (distance <= DIST_LIM)
  {
    stop();
    if (last_control != 'N' && last_control != 'S')
    {
      while (distance <= DIST_LIM)
      {
        delay(500);
        control = (char)SerialBT.read();
        if(SerialBT.read() != -1){
          break;
        }
        else if (control == 'S')
        {
          stop();
          break;
        }
        else
        {
          rotate();
          distance = distance_sensor();
          if (distance >= DIST_LIM)
          {
            startEngine(3);
            speedControl(speedMa, speedMb);
            break;
          }
        }
      }
    }
  }

  if (control != 'N')
  {
    last_control = (char)control;
  }
}

float distance_sensor()
{ 
  long length;
  float distanceCM;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  length = pulseIn(echoPin, HIGH);
  distanceCM = length * SOUND_SPEED / 2;
  delay(200);
  return distanceCM;
}

void startEngine(int engine)
{
  if(engine == 1){
    analogWrite(pin_ena, 45);
    digitalWrite(pin_in1, HIGH);
    digitalWrite(pin_in2, LOW);
    digitalWrite(pin_in3, LOW);
    digitalWrite(pin_in4, LOW);
  }
  if(engine == 2){
    analogWrite(pin_enb, 50);
    digitalWrite(pin_in1, LOW);
    digitalWrite(pin_in2, LOW);
    digitalWrite(pin_in3, HIGH);
    digitalWrite(pin_in4, LOW);
  }
  else if (engine == 3){
    analogWrite(pin_ena, 45);
    analogWrite(pin_enb, 50);
    digitalWrite(pin_in1, HIGH);
    digitalWrite(pin_in2, LOW);
    digitalWrite(pin_in3, HIGH);
    digitalWrite(pin_in4, LOW);
  }
  delay(50);
}

void speedControl(float Ma, float Mb)
{
  speedMa = Ma;
  speedMb = Mb;
  analogWrite(pin_enb, speedMb);
  analogWrite(pin_ena, speedMa);
  digitalWrite(pin_in1, HIGH);
  digitalWrite(pin_in2, LOW);
  digitalWrite(pin_in3, HIGH);
  digitalWrite(pin_in4, LOW);
}

void directionControl(int direcao)
{
  if (direcao == 1) // right
  {
    startEngine(1);
    analogWrite(pin_ena, 16.5);
    digitalWrite(pin_in1, HIGH);
    digitalWrite(pin_in2, LOW);
    digitalWrite(pin_in3, LOW);
    digitalWrite(pin_in4, LOW);
  }
  if (direcao == 2) // left
  {
    startEngine(2);
    analogWrite(pin_enb, 17);
    digitalWrite(pin_in1, LOW);
    digitalWrite(pin_in2, LOW);
    digitalWrite(pin_in3, HIGH);
    digitalWrite(pin_in4, LOW);
  }
  delay(1000);
  startEngine(3);
  analogWrite(pin_ena, speedMa);
  analogWrite(pin_enb, speedMb);
  digitalWrite(pin_in1, HIGH);
  digitalWrite(pin_in2, LOW);
  digitalWrite(pin_in3, HIGH);
  digitalWrite(pin_in4, LOW);
}

void stop()
{
  digitalWrite(pin_in1, LOW);
  digitalWrite(pin_in2, LOW);
  digitalWrite(pin_in3, LOW);
  digitalWrite(pin_in4, LOW);
}

void rotate()
{
  startEngine(1);
  digitalWrite(pin_in1, HIGH);
  digitalWrite(pin_in2, LOW);
  digitalWrite(pin_in3, LOW);
  digitalWrite(pin_in4, LOW);
  analogWrite(pin_ena, 13);
  delay(500);
}
