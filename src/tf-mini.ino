#include "TFLidar.h"
#include <SoftwareSerial.h>

SoftwareSerial mySerial(10, 11);
#define LIDAR_SERIAL mySerial

TFLidar lidar;
int dist;

unsigned long previousMillis = 0;
unsigned long lastTime = 0;  // Время последней публикации
unsigned long interval = 0;   // Интервал между публикациями
unsigned long count = 0;      // Счетчик публикаций

void setup() {
  Serial.begin(9600);
  while (!Serial);
  
  Serial.println("Serial init OK\r\n");
  LIDAR_SERIAL.begin(115200);
  lidar.begin(&LIDAR_SERIAL);
}

void loop() {
  unsigned long startTime = millis();
  lidar.getData(dist);
  unsigned long endTime = millis();
  Serial.print("Dist: ");
  Serial.print(dist);
  Serial.print(" cm");
  Serial.print(" (");
  Serial.print(endTime - startTime);
  Serial.println(" ms)");
  

  // Вычисление и публикация частоты
  unsigned long currentTime = millis(); // Текущее время в миллисекундах
  interval = currentTime - lastTime;     // Интервал между публикациями
  count++;                                // Увеличиваем счетчик

  if (interval >= 1000) { // Если прошло более 1 секунды
    Serial.print("Frequency = ");
    Serial.print(count);          // Публикация количества сообщений
    Serial.println(" messages/second");
    
    // Сбрасываем счетчик и время
    count = 0; 
    lastTime = currentTime;
  }
  
  delay(2);
}
