#include <Wire.h>
#include <Adafruit_BMP280.h>
#include "DHT.h"

#define DHTPIN A1
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);
Adafruit_BMP280 bmp; // usa I2C (A4 SDA / A5 SCL)

void setup() {
    Serial.begin(9600);
    dht.begin();

    // Inicializa BMP280
    if (!bmp.begin(0x76)) {  
        Serial.println("Erro: BMP280 não encontrado!");
        while (1); // trava se não encontrar
    }
}

void loop() {
    float temp = dht.readTemperature();
    float umid = dht.readHumidity();
    float pressao = bmp.readPressure() / 100.0; // hPa

    if (!isnan(temp) && !isnan(umid)) {
        Serial.print("{");
        Serial.print("\"temperatura\":"); Serial.print(temp);
        Serial.print(",\"umidade\":"); Serial.print(umid);
        Serial.print(",\"pressao\":"); Serial.print(pressao);
        Serial.println("}");
    }

    delay(5000);
}