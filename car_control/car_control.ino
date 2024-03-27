// This example code is in the Public Domain (or CC0 licensed, at your option.)
// By Evandro Copercini - 2018
//
// This example creates a bridge between Serial and Classical Bluetooth (SPP)
// and also demonstrate that SerialBT have the same functionalities of a normal Serial

#include "BluetoothSerial.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif
#define VELOCIDADE_DO_SOM 0.034 // definir a velocidade do som em cm/uS
#define CM_PARA_POLEGADA 0.393701
#define DIST_LIM 40
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

long duracao;
float distancCm;

void setup()
{
  Serial.begin(9600);
  SerialBT.begin("ESP32test"); // Bluetooth device name
  Serial.println("The device started, now you can pair it with bluetooth!");

  pinMode(pin_ena, OUTPUT);
  pinMode(pin_in1, OUTPUT);
  pinMode(pin_in3, OUTPUT);

  pinMode(pin_enb, OUTPUT);
  pinMode(pin_in2, OUTPUT);
  pinMode(pin_in4, OUTPUT);

  pinMode(trigPin, OUTPUT); // Define o trigPin como uma saída
  pinMode(echoPin, INPUT);  // Define o echoPin como uma entrada
}

void loop()
{
  char control = 'N';
  float distancia = distance_sensor();
  Serial.println(last_control);
  if (SerialBT.available())
  {
    control = SerialBT.read();
  }

  if (distancia >= DIST_LIM)
  {
    switch (control)
    {
    case '1':
      startEngine();
      controleVelocidade(15, 15);
      break;
    case '2':
      startEngine();
      controleVelocidade(16.5, 17);
      break;
    case '3':
      startEngine();
      controleVelocidade(18, 19);
      break;
    case '4':
      startEngine();
      controleVelocidade(20.5, 22);
      break;
    case '5':
      startEngine();
      controleVelocidade(25, 25);
      break;
    case 'P':
      stop();
      break;
    case 'D':
      controleDirecao(1);
      break;
    case 'L':
      controleDirecao(2);
      break;
    }
  }
  else if (distancia <= DIST_LIM)
  {
    stop();
    if (last_control != 'N' && last_control != 'P')
    {
      while (distancia <= DIST_LIM)
      {
        delay(500);
        control = (char)SerialBT.read();
        if(SerialBT.read() != -1){
          break;
        }
        else if (control == 'P')
        {
          stop();
          break;
        }
        else
        {
          rotate();
          distancia = distance_sensor();
          if (distancia >= DIST_LIM)
          {
            startEngine();
            controleVelocidade(speedMa, speedMb);
            break;
          }
        }
      }
    }
  }

  if (SerialBT.read() != -1 && control != 'N')
  {
    last_control = (char)control;
  }
}

float distance_sensor()
{ // Limpa o trigPin

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2); // Define o trigPin no estado ALTO por 10 microssegundos
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Lê o echoPin, retorna o tempo de viagem da onda sonora em microssegundos
  duracao = pulseIn(echoPin, HIGH);
  // Calcule a distância
  distancCm = duracao * VELOCIDADE_DO_SOM / 2; // Converter para centimetros
  delay(200);
  return distancCm;
}

void startEngine()
{
  analogWrite(pin_enb, 50);
  analogWrite(pin_ena, 50);
  digitalWrite(pin_in1, HIGH);
  digitalWrite(pin_in2, LOW);
  digitalWrite(pin_in3, HIGH);
  digitalWrite(pin_in4, LOW);
  delay(50);
}

void controleVelocidade(float Ma, float Mb)
{
  Serial.println("Moving Forward");
  speedMa = Ma;
  speedMb = Mb;
  analogWrite(pin_enb, speedMb);
  analogWrite(pin_ena, speedMa);
  digitalWrite(pin_in1, HIGH);
  digitalWrite(pin_in2, LOW);
  digitalWrite(pin_in3, HIGH);
  digitalWrite(pin_in4, LOW);
}

void controleDirecao(int direcao)
{
  startEngine();
  analogWrite(pin_ena, 16.5);
  analogWrite(pin_enb, 17);
  if (direcao == 1)
  {
    digitalWrite(pin_in1, HIGH);
    digitalWrite(pin_in2, LOW);
    digitalWrite(pin_in3, LOW);
    digitalWrite(pin_in4, LOW);
  }
  if (direcao == 2)
  {
    digitalWrite(pin_in1, LOW);
    digitalWrite(pin_in2, LOW);
    digitalWrite(pin_in3, HIGH);
    digitalWrite(pin_in4, LOW);
  }
  delay(1000);
  startEngine();
  analogWrite(pin_ena, speedMa);
  analogWrite(pin_enb, speedMb);
  digitalWrite(pin_in1, HIGH);
  digitalWrite(pin_in2, LOW);
  digitalWrite(pin_in3, HIGH);
  digitalWrite(pin_in4, LOW);
}

void stop()
{
  // Stop the DC motor
  Serial.println("Motor stopped");
  digitalWrite(pin_in1, LOW);
  digitalWrite(pin_in2, LOW);
  digitalWrite(pin_in3, LOW);
  digitalWrite(pin_in4, LOW);
}

void rotate()
{
  startEngine();
  digitalWrite(pin_in1, HIGH);
  digitalWrite(pin_in2, LOW);
  digitalWrite(pin_in3, LOW);
  digitalWrite(pin_in4, LOW);
  analogWrite(pin_ena, 13);
  delay(500);
}