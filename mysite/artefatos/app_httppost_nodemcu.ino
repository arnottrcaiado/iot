/**
    Internet das Coisas
    Baseado em exemplo da IDE Arduino (BasicHTTPClient.ino)

    Setembro de 2022
*/

#include <Arduino.h>

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ArduinoJson.h>

#include <ESP8266HTTPClient.h>

#include <WiFiClient.h>

/* Variaveis Globais , objetos e classes */

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
    Serial.printf("[SETUP] aguarde %d...\n", t);
    Serial.flush();
    delay(1000);
  }

  WiFi.mode(WIFI_STA);
  WiFiMulti.addAP("iPhone de Arnott", "arbbbe11");
}

void loop() {
  char dados[255];
  char sensor [10], valor[10];

  // aguarde pela conexao wifi
  if ((WiFiMulti.run() == WL_CONNECTED)) {
    Serial.print("[HTTP] iniciando ...\n");
    if (http.begin(client, "http://apiot.pythonanywhere.com/postJson")){
      Serial.print("[HTTP] POST...\n");
      // inicia conexao e envia HTTP header
      http.addHeader("Content-Type","application/json");
      http.addHeader("Authorization-Token", "chave de header" );

      sprintf( sensor, "%02d", 1 );
      sprintf( valor, "%03d", val_sens++ );

      doc["sensor"] = sensor;
      doc["valor"] = valor;

      serializeJson(doc, dados);
      Serial.println( dados );

      int httpCode = http.POST( dados );

      // httpCode retorna numero negativo em caso de erro
      if (httpCode > 0) {
        // HTTP enviou header e informaç~ões
        Serial.printf("[HTTP] POST... codigo: %d\n", httpCode);

        // requisiç~ão bem sucedida
        if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) {
          String payload = http.getString();
          Serial.println(payload);
        }
      } else {
        Serial.printf("[HTTP] POST... falhou, erro n.: %s\n", http.errorToString(httpCode).c_str());
      }

      http.end();
    } else {
      Serial.printf("[HTTP} Nao foi ppssivel conectar\n");
    }
  }

  delay(1000);
}