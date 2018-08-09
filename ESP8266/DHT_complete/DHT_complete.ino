#include <ESP8266WiFi.h>
#include <DNSServer.h>
#include <ESP8266WebServer.h>
#include <EEPROM.h>
#include <ESP8266mDNS.h>
#include <PubSubClient.h>
#include <DHT11.h>
#define   EEPROM_LENGTH 1024

const char*   mqttServer = "49.236.136.179";
const int     mqttPort = 1883;
const char*   mqttUser = "chan";
const char*   mqttPassword = "chan";


char eRead[30];
byte len;
char ssid[30];
char password[30];
char id[30];
char topic[100];

char topic_temp[100];
char topic_humi[100];

bool captive = true;

DHT11 dht11(2);
WiFiClient espClient;
PubSubClient client(espClient);
const byte DNS_PORT = 53;
IPAddress apIP(192, 168, 1, 1);
DNSServer dnsServer;
ESP8266WebServer webServer(80);

String responseHTML = ""
    "<!DOCTYPE html><html><head><title>DHT Setting Page</title></head><body><center>"
    "<p>DHT Setting Page</p>"
    "<form action='/button'>"
    "<p><input type='text' name='ssid' placeholder='SSID' onblur='this.value=removeSpaces(this.value);'></p>"
    "<p><input type='text' name='password' placeholder='WLAN Password'></p>"
    "<p><input type='text' name='id' placeholder='Car ID'></p>"
    "<p><input type='submit' value='Submit'></p></form>"
    "<p>This is DHT Setting Page</p></center></body>"
    "<script>function removeSpaces(string) {"
    "   return string.split(' ').join('');"
    "}</script></html>";


void setup() 
{
  Serial.begin(9600);
  EEPROM.begin(EEPROM_LENGTH);
  pinMode(5, INPUT_PULLUP);
  attachInterrupt(5, initDevice, FALLING);

  ReadString(0, 30);
  if (!strcmp(eRead, ""))
    setup_captive();
  else 
  {
    captive = false;
    strcpy(ssid, eRead);
    ReadString(30, 30);
    strcpy(password, eRead);
    ReadString(60, 30);
    strcpy(id, eRead);
    // make topic
    strcat(topic, id);
    strcpy(topic_temp, topic);
    strcpy(topic_humi, topic);
    strcat(topic_temp, "/temperature");
    strcat(topic_humi, "/humidity");
    Serial.println(topic);
    // -------------
    setup_runtime();  
    client.setServer(mqttServer, mqttPort);
    while (!client.connected()) 
    {
      Serial.println("Connecting to MQTT...");
      if (client.connect("Chan_DHT", mqttUser, mqttPassword )) 
      {
        Serial.println("connected");
        client.publish("DHT/status", topic);
      } 
      else 
      {
        Serial.print("failed with state "); Serial.println(client.state());
        ESP.restart();
      }
    }
  }
}

void loop() {
  if (captive)
  {
    dnsServer.processNextRequest();
    webServer.handleClient();
  }
  else
  {
    yield;
    delay(5000);
    int err;
    float temp, humi;
    if((err=dht11.read(humi, temp))==0)
    {
      char temp_buf[10];
      char humi_buf[10];
      Serial.print("temperature:");Serial.println(temp);
      Serial.print("humidity:");Serial.println(humi);
      sprintf(temp_buf, "%.2f", temp);
      sprintf(humi_buf, "%.2f", humi);
      client.publish(topic_humi, humi_buf);
      client.publish(topic_temp, temp_buf);
    }
  }
  
  client.loop();
}


void setup_runtime() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");

  // Wait for connection
  int i = 0;
  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(500);
    Serial.print(".");
    yield;
    if(i++ > 30) 
    {
      ESP.restart();
      return; 
    }
  }
  Serial.println("");
  Serial.print("Connected to "); Serial.println(ssid);
  Serial.print("IP address: "); Serial.println(WiFi.localIP());

  if (MDNS.begin("Chan_DHT")) {
   Serial.println("MDNS responder started");
  }
  

  webServer.onNotFound(handleNotFound);
  webServer.begin();
  Serial.println("HTTP server started");  
}

void setup_captive() {    
  WiFi.mode(WIFI_AP);
  WiFi.softAPConfig(apIP, apIP, IPAddress(255, 255, 255, 0));
  WiFi.softAP("Chan_DHT");
  
  dnsServer.start(DNS_PORT, "*", apIP);

  webServer.on("/button", button);

  webServer.onNotFound([]() {
    webServer.send(200, "text/html", responseHTML);
  });
  webServer.begin();
  Serial.println("Captive Portal Started");
}

void button()
{
  Serial.println("button pressed");
  Serial.println(webServer.arg("ssid"));
  SaveString( 0, (webServer.arg("ssid")).c_str());
  SaveString(30, (webServer.arg("password")).c_str());
  SaveString(60, (webServer.arg("id")).c_str());
  webServer.send(200, "text/plain", "OK");
  ESP.restart();
}

void SaveString(int startAt, const char* id) 
{ 
  for (byte i = 0; i <= strlen(id); i++)
    EEPROM.write(i + startAt, (uint8_t) id[i]);
  EEPROM.commit();
}

void ReadString(byte startAt, byte bufor) 
{
  for (byte i = 0; i <= bufor; i++) {
    eRead[i] = (char)EEPROM.read(i + startAt);
  }
  len = bufor;
}

void handleNotFound()
{
  String message = "File Not Found\n";
  webServer.send(404, "text/plain", message);
}

void initDevice() {
    Serial.println("Flushing EEPROM....");
    SaveString(0, "");
    ESP.restart();
}




