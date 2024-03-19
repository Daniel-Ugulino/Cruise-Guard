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

BluetoothSerial SerialBT;

const int pin_ena = 4;
const int pin_in1 = 16;
const int pin_in2 = 17;

const int pin_enb = 26;
const int pin_in3 = 33;
const int pin_in4 = 25;

const int trigPin = 22;
const int echoPin = 23;

int speedMa = 0;
int speedMb = 0;

char last_control;

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
  Serial.println(distancia);

  if (distancia >= 45)
  {
    if (SerialBT.available())
    {
      control = (char)SerialBT.read();
      Serial.write(control);
    }

    if (control == '1')
    {
      speedMa = 10;
      speedMb = 32;
      controleVelocidade();
    }
    else if (control == '2')
    {
      speedMa = 36;
      speedMb = 42;
      controleVelocidade();
    }
    else if (control == '3')
    {
      speedMa = 46;
      speedMb = 52;
      controleVelocidade();
    }
    else if (control == '4')
    {
      speedMa = 56;
      speedMb = 62;
      controleVelocidade();
    }
    else if (control == '5')
    {
      speedMa = 66;
      speedMb = 72;
      controleVelocidade();
    }
    else if (control == 'P')
    {
      speedMa = 0;
      speedMb = 0;
      stop();
    }
    else if (control == 'D')
    {
      controleDirecao(1);
    }
    else if (control == 'L')
    {
      controleDirecao(2);
    }
  }
  else if (distancia <= 45)
  {
    stop();
  }

  delay(20);
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

void controleVelocidade()
{
  Serial.println("Moving Forward");
  analogWrite(pin_enb, speedMb);
  analogWrite(pin_ena, speedMa);
  digitalWrite(pin_in1, HIGH);
  digitalWrite(pin_in2, LOW);
  digitalWrite(pin_in3, HIGH);
  digitalWrite(pin_in4, LOW);
}

void controleDirecao(int direcao)
{
  if (direcao == 1)
  {
    Serial.println("Direita");
    digitalWrite(pin_in1, HIGH);
    digitalWrite(pin_in2, LOW);
    digitalWrite(pin_in3, LOW);
    digitalWrite(pin_in4, LOW);
  }
  if (direcao == 2)
  {
    Serial.println("Esquerda");
    digitalWrite(pin_in1, LOW);
    digitalWrite(pin_in2, LOW);
    digitalWrite(pin_in3, HIGH);
    digitalWrite(pin_in4, LOW);
  }
  delay(1000);
  digitalWrite(pin_in1, HIGH);
  digitalWrite(pin_in2, LOW);
  digitalWrite(pin_in3, HIGH);
  digitalWrite(pin_in4, LOW);
  delay(2000);
}

void stop()
{
  // Stop the DC motor
  Serial.println("Motor stopped");

  analogWrite(pin_enb, speedMb);
  analogWrite(pin_ena, speedMa);
  digitalWrite(pin_in1, LOW);
  digitalWrite(pin_in2, LOW);
  digitalWrite(pin_in3, LOW);
  digitalWrite(pin_in4, LOW);
}