/**
    Internet das Coisas
    Baseado em exemplo da IDE Arduino
    BasicHTTPClient.ino
    Created on: 24.05.2015

    Exemplo POST

    Setembro de 2022
*/

#include <Arduino.h>

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ArduinoJson.h>
#include <ESP8266HTTPClient.h>

#include <WiFiClient.h>

/* Variaveis Globais */


ESP8266WiFiMulti WiFiMulti;
WiFiClient client;
HTTPClient http;
DynamicJsonDocument doc(1024);

int val_sens=0;


void setup() {

  Serial.begin(115200);

  Serial.println();
  Serial.println();
  Serial.println();

  for (uint8_t t = 4; t > 0; t--) {
    Serial.printf("[SETUP] WAIT %d...\n", t);
    Serial.flush();
    delay(1000);
  }

  WiFi.mode(WIFI_STA);
  WiFiMulti.addAP("ssid", "senha");
}

void loop() {
  char dados[255];
  char sensor [10], valor[10];

  // wait for WiFi connection
  if ((WiFiMulti.run() == WL_CONNECTED)) {

    Serial.print("[HTTP] begin...\n");
    if (http.begin(client, "http://apiot.pythonanywhere.com/postJson")){

      Serial.print("[HTTP] POST...\n");
      // start connection and send HTTP header
      http.addHeader("Content-Type","application/json");
      http.addHeader("Authorization-Token", "chave de header" );

      sprintf( sensor, "%02d", 1 );
      sprintf( valor, "%03d", val_sens++ );

      doc["sensor"] = sensor;
      doc["valor"] = valor;

      serializeJson(doc, dados);
      Serial.println( dados );

      int httpCode = http.POST( dados );

      // httpCode will be negative on error
      if (httpCode > 0) {
        // HTTP header has been send and Server response header has been handled
        Serial.printf("[HTTP] POST... code: %d\n", httpCode);

        // file found at server
        if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) {
          String payload = http.getString();
          Serial.println(payload);
        }
      } else {
        Serial.printf("[HTTP] POST... failed, error: %s\n", http.errorToString(httpCode).c_str());
      }

      http.end();
    } else {
      Serial.printf("[HTTP} Unable to connect\n");
    }
  }

  delay(1000);
}