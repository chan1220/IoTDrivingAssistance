#include <ESP8266WiFi.h>
#include <DNSServer.h>
#include <ESP8266WebServer.h>
#include <EEPROM.h>
#include <ESP8266mDNS.h>
#include <PubSubClient.h>
// GPS
#include <SoftwareSerial.h>
#include <TinyGPS++.h>
TinyGPSPlus gps;
SoftwareSerial uart_gps(12, 13);
void getgps(TinyGPSPlus &gps);

//
const char*   mqttServer = "15.164.149.11";
const int     mqttPort = 1883;
const char*   mqttUser = "chan";
const char*   mqttPassword = "hi";
bool          isReset = false;
WiFiClient espClient;
PubSubClient client(espClient);

#define   EEPROM_LENGTH 1024

char eRead[30];
byte len;
int relay_status = 0;
char ssid[30];
char password[30];
char id[30];
char topic[100];
bool captive = true;

const byte DNS_PORT = 53;
IPAddress apIP(192, 168, 1, 1);
DNSServer dnsServer;
ESP8266WebServer webServer(80);

void GPIO5() {
    Serial.println("Flushing EEPROM....");
    SaveString(0, ""); // blank out the SSID field in EEPROM
    isReset = true;
}

String responseHTML = ""
    "<!DOCTYPE html><html><head><title>GPS Setting Page</title></head><body><center>"
    "<p>GPS Setting Page</p>"
    "<form action='/button'>"
    "<p><input type='text' name='ssid' placeholder='SSID' onblur='this.value=removeSpaces(this.value);'></p>"
    "<p><input type='text' name='password' placeholder='WLAN Password'></p>"
    "<p><input type='text' name='id' placeholder='Car ID'></p>"
    "<p><input type='submit' value='Submit'></p></form>"
    "<p>This is GPS Setting Page</p></center></body>"
    "<script>function removeSpaces(string) {"
    "   return string.split(' ').join('');"
    "}</script></html>";



void setup() {
    uart_gps.begin(9600);
    Serial.begin(9600);
    EEPROM.begin(EEPROM_LENGTH);
    pinMode(0, INPUT_PULLUP);
    attachInterrupt(0, GPIO5,FALLING);

    ReadString(0, 30);
    if (!strcmp(eRead, "")) {
        setup_captive();
    } else {
        captive = false;
        strcpy(ssid, eRead);
        ReadString(30, 30);
        strcpy(password, eRead);
        ReadString(60, 30);
        strcpy(id, eRead);
        // make topic
        strcat(topic, id);
        strcat(topic, "/gps");
        Serial.println(topic);
        // -------------
        setup_runtime();  
        client.setServer(mqttServer, mqttPort);
        while (!client.connected()) 
        {
          Serial.println("Connecting to MQTT...");
          if (client.connect("Doraemon_GPS", mqttUser, mqttPassword )) 
          {
            Serial.println("connected");
            client.publish("gps/status", topic);
          } 
          else 
          {
            Serial.print("failed with state "); Serial.println(client.state());
            delay(2000);
          }
        }
    }
}

void setup_runtime() {
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    Serial.println("");

    // Wait for connection
    int i = 0;
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
        yield;
        if(i++ > 30) {
            captive = true;
            setup_captive();
            return; 
        }
    }
    Serial.println("");
    Serial.print("Connected to "); Serial.println(ssid);
    Serial.print("IP address: "); Serial.println(WiFi.localIP());

    if (MDNS.begin("Doraemon_GPS")) {
       Serial.println("MDNS responder started");
    }
    

    webServer.onNotFound(handleNotFound);
    webServer.begin();
    Serial.println("HTTP server started");  
}

void setup_captive() {    
    WiFi.mode(WIFI_AP);
    WiFi.softAPConfig(apIP, apIP, IPAddress(255, 255, 255, 0));
    WiFi.softAP("Doraemon_GPS");
    
    dnsServer.start(DNS_PORT, "*", apIP);

    webServer.on("/button", button);

    webServer.onNotFound([]() {
        webServer.send(200, "text/html", responseHTML);
    });
    webServer.begin();
    Serial.println("Captive Portal Started");
}

void loop() {
    if (captive) { 
        dnsServer.processNextRequest();
    }

    webServer.handleClient();

    if(uart_gps.available())
    {
      yield;
      if(gps.encode(uart_gps.read()))
      {
        yield;
        char mqtt_buf[20];
        float gps_lat = gps.location.lat();
        float gps_lon = gps.location.lng();
        if(gps_lat && gps_lon)
        {
          sprintf(mqtt_buf, "%f %f", gps.location.lat(), gps.location.lng());
          yield;
          Serial.print(mqtt_buf);Serial.println("is published!!");
          yield;
          client.publish(topic, mqtt_buf);
          yield;
        }
        else
          Serial.print("GPS is empty!");
        delay(1000);
      }

    }
    client.loop();

    if(isReset)
      ESP.restart();
}

void button(){
    Serial.println("button pressed");
    Serial.println(webServer.arg("ssid"));
    SaveString( 0, (webServer.arg("ssid")).c_str());
    SaveString(30, (webServer.arg("password")).c_str());
    SaveString(60, (webServer.arg("id")).c_str());
    webServer.send(200, "text/plain", "OK");
    ESP.restart();
}

// Saves string to EEPROM
void SaveString(int startAt, const char* id) { 
    for (byte i = 0; i <= strlen(id); i++) {
        EEPROM.write(i + startAt, (uint8_t) id[i]);
    }
    EEPROM.commit();
}

// Reads string from EEPROM
void ReadString(byte startAt, byte bufor) {
    for (byte i = 0; i <= bufor; i++) {
        eRead[i] = (char)EEPROM.read(i + startAt);
    }
    len = bufor;
}

void handleNotFound(){
    String message = "File Not Found\n\n";
    webServer.send(404, "text/plain", message);
}

