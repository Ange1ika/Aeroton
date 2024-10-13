// # Editor     : roker
// # Date       : 05.03.2018

// # Product name: URM V5.0 ultrasonic sensor
// # Product SKU : SEN0001
// # Version     : 1.0

// # Description:
// # The Sketch for scanning 180 degree area 2-800cm detecting range
// # The sketch for using the URM37 PWM trigger pin mode from DFRobot
// #   and writes the values to the serialport
// # Connection:
// #       Vcc (Arduino)    -> Pin 1 VCC (URM V5.0)
// #       GND (Arduino)    -> Pin 2 GND (URM V5.0)
// #       Pin 3 (Arduino)  -> Pin 4 ECHO (URM V5.0)
// #       Pin 5 (Arduino)  -> Pin 6 COMP/TRIG (URM V5.0)

// # Working Mode: PWM trigger pin  mode.

int URECHO = 3;         // PWM Output 0-50000US, Every 50US represents 1cm
int URTRIG = 5;         // Trigger pin

unsigned int DistanceMeasured = 0;
unsigned long lastTime = 0;  // Время последней публикации
unsigned long interval = 0;   // Интервал между публикациями
unsigned long count = 0;      // Счетчик публикаций

void setup() {
  // Serial initialization
  Serial.begin(9600);                       // Sets the baud rate to 9600
  pinMode(URTRIG, OUTPUT);                  // A low pull on pin COMP/TRIG
  digitalWrite(URTRIG, HIGH);               // Set to HIGH
  pinMode(URECHO, INPUT);                   // Sending Enable PWM mode command
  delay(5);
  Serial.println("Init the sensor");
}

void loop() {
  Serial.print("Distance=");
  digitalWrite(URTRIG, LOW);
  digitalWrite(URTRIG, HIGH);              

  unsigned long LowLevelTime = pulseIn(URECHO, LOW);
  if (LowLevelTime >= 50000) {              // The reading is invalid.
    Serial.println("Invalid");
  } else {
    DistanceMeasured = LowLevelTime / 50;   // Every 50us low level stands for 1cm
    Serial.print(DistanceMeasured);
    Serial.println(" cm");
  }

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

  delay(10); // Задержка для контроля частоты измерений
}
