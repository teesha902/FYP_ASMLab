#include <ESP8266WiFi.h>

const char* ssid = "Feeder_AP";
const char* password = "12345678";

WiFiServer server(80);

void setup() {
  Serial.begin(115200);
  WiFi.softAP(ssid, password);
  server.begin();
  Serial.println("Access Point Started");
  Serial.println(WiFi.softAPIP());
}

void loop() {
  WiFiClient client = server.available();
  if (!client) return;

  while(!client.available()){ delay(1); }

  String request = client.readStringUntil('\r');
  client.flush();

  String response = "<html><body><h2>Feeder Ready</h2></body></html>";
  client.print("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n");
  client.print(response);
  delay(1);
  client.stop();
}
