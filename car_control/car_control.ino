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
  Serial.println(distancia);

  if (distancia >= DIST_LIM)
  {
    if (SerialBT.available())
    {
      control = (char)SerialBT.read();
      if(control != ' '){
        last_control = control;
      }
    }

    if (control == '1')
    {
      startEngine();
      speedMa = 13.5;
      speedMb = 14;
      controleVelocidade();
    }
    else if (control == '2')
    {
      startEngine();
      speedMa = 15.5;
      speedMb = 16;
      controleVelocidade();
    }
    else if (control == '3')
    {
      startEngine();
      speedMa = 17.5;
      speedMb = 18;
      controleVelocidade();
    }
    else if (control == '4')
    {
      startEngine();
      speedMa = 19.5;
      speedMb = 21;
      controleVelocidade();
    }
    else if (control == '5')
    {
      startEngine();
      speedMa = 23;
      speedMb = 23;
      controleVelocidade();
    }
    else if (control == 'P')
    {
      startEngine();
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
  else if (distancia <= DIST_LIM)
  {
    stop();
    if(last_control != ' ' && last_control != 'N' && last_control != 'P' && last_control != 'D'  && last_control != 'L')
    {
      while (distancia <= DIST_LIM){
        control = (char)SerialBT.read();
        if(control == 'P'){
          stop();
          break;
        }
        else{
          rotate();
          distancia = distance_sensor();
          delay(1000);
          if(distancia >= DIST_LIM){
            startEngine();
            speedMa = 14.5;
            speedMb = 15;
            controleVelocidade();
            break;
          }
        }
      }
    }
  }
  delay(200);
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

void startEngine(){
    analogWrite(pin_enb, 50);
    analogWrite(pin_ena, 50);
    digitalWrite(pin_in1, HIGH);
    digitalWrite(pin_in2, LOW);
    digitalWrite(pin_in3, HIGH);
    digitalWrite(pin_in4, LOW);
    delay(50);
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
  analogWrite(pin_ena, speedMa);
  analogWrite(pin_enb, speedMb);
  digitalWrite(pin_in1, HIGH);
  digitalWrite(pin_in2, LOW);
  digitalWrite(pin_in3, HIGH);
  digitalWrite(pin_in4, LOW);
  delay(1000);
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

void rotate(){
  startEngine();
  digitalWrite(pin_in1, HIGH);
  digitalWrite(pin_in2, LOW);
  digitalWrite(pin_in3, LOW);
  digitalWrite(pin_in4, LOW);
  analogWrite(pin_ena, 13);

  delay(500);
}
