#include "TFLidar.h"
#define USE_3V3_SOFT_SERIAL

#ifdef USE_3V3_SOFT_SERIAL
  SoftwareSerial uart(0, 1); // TX, RX
#else
  SoftwareSerial uart(10, 11);
#endif

TFLuna SeeedTFLuna; // Создаем объект TFLuna
TFLidar SeeedTFLidar(&SeeedTFLuna); // Передаем указатель на SeeedTFLuna

void setup() {
  Serial.begin(9600); // Обратите внимание на правильное использование Serial
  while (!Serial);
#ifdef USE_3V3_SOFT_SERIAL
  SeeedTFLidar.begin(&uart, 9600);
#else
  SeeedTFLidar.begin(&uart, 115200);
#endif
}

void loop() {
  while (!SeeedTFLidar.get_frame_data()) {
#ifdef USE_3V3_SOFT_SERIAL
      delay(20);
  #else
      delay(1);
#endif
  }
  
  Serial.print("dist = ");
  Serial.print(SeeedTFLidar.get_distance()); // выводим измеренное значение расстояния от LiDAR
  Serial.println(" ");
}
