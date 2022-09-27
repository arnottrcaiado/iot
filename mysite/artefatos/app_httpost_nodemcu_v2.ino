/**
    Internet das Coisas
    Baseado em exemplo da IDE Arduino (BasicHTTPClient.ino)
    Exemplo 02
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

#define NWIFIS 4
#define NTENTS_WIFI 30
#define TEMP_WIFI 300

struct redes  {
  const char *ssid;
  const char *senha;
};

struct redes redeWifi[NWIFIS]={ "iPhone de Arnott","arbbbe11",
                          "Vivo-Internet-E532", "6EFC366C",
                          "SENAC-Mesh","09080706",
                          "AP1501","ARBBBE11"};

int val_sens=0;
bool conectou = false;
char *redeAtual;


void setup() {

  Serial.begin(115200);

  Serial.println();
  Serial.println();
  Serial.println("Iniciando");
/*
  for (uint8_t t = 4; t > 0; t--) {
    Serial.printf("[SETUP] aguarde %d...\n", t);
    Serial.flush();
    delay(100);
  }
*/
  loopConectaWifi();

}

// ============================================================================
void loopConectaWifi(){
 do{
      conectou = conectaWifi(); // tenta conectar em uma das redes disponiveis
      if ( !conectou )
        Serial.println(".");
  }while(!conectou);

 Serial.println("Setup concluido");
}

//------------------------------------------------------------------------------------
bool conectaWifi()
{
  bool conectou = false;
  int i=0;
  int qtd = 0;

  while ( i < NWIFIS ){ // tenta cada uma das redes disponiveis

      Serial.println ("Conectando: wifi");
      Serial.println( redeWifi[i].ssid );
      WiFi.begin(redeWifi[i].ssid, redeWifi[i].senha);

      qtd = 0;

      while (WiFi.status() != WL_CONNECTED) {
        delay(TEMP_WIFI);
        Serial.print(".");
        qtd++;
        if(qtd > NTENTS_WIFI){
          break;
        }
      }
      if(WiFi.status() == WL_CONNECTED){
        Serial.println("Conectado com sucesso. IP: ");
        Serial.println(WiFi.localIP());
        Serial.println( redeWifi[i].ssid );
        delay( 2000 );
        conectou = true;
        redeAtual = (char *)redeWifi[i].ssid;
        return conectou;
      }
      i++;
    }
  return conectou;
}


void loop() {
  char dados[255];
  char sensor [10], valor[10];

  // aguarde pela conexao wifi
  if ((WiFi.status() == WL_CONNECTED)) {
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