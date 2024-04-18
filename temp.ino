#include "OneWire.h"
#include "DallasTemperature.h"
// Pin D2 for OneWire
#define ONE_WIRE_BUS 2
int sec = 1000;
int min = 60 * sec;
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

void setup() {
  Serial.begin(9600);
  sensors.begin();
}

void loop() {
  sensors.requestTemperatures();
  float tempC = sensors.getTempCByIndex(0);
  // Outputs data on Arduino TX pin which is connected to PIN 16 on Pycom SiPy
  Serial.println(tempC, 2);
  // Change to adjust temperature read frequency
  delay(15*sec);
}
