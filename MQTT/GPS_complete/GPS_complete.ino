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
const char*   mqttServer = "49.236.136.179";
const int     mqttPort = 1883;
const char*   mqttUser = "yhur";
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
    "<p><input type='submit' value='Submit'></p></form>"
    "<p>This is GPS Setting Page</p></center></body>"
    "<script>function removeSpaces(string) {"
    "   return string.split(' ').join('');"
    "}</script></html>";



void setup() {
    uart_gps.begin(9600);
    Serial.begin(9600);
    EEPROM.begin(EEPROM_LENGTH);
    pinMode(5, INPUT_PULLUP);
    attachInterrupt(5, GPIO5,FALLING);

    ReadString(0, 30);
    if (!strcmp(eRead, "")) {
        setup_captive();
    } else {
        captive = false;
        strcpy(ssid, eRead);
        ReadString(30, 30);
        strcpy(password, eRead);
        setup_runtime();  
        client.setServer(mqttServer, mqttPort);
        while (!client.connected()) 
        {
          Serial.println("Connecting to MQTT...");
          if (client.connect("chan_publisher", mqttUser, mqttPassword )) 
          {
            Serial.println("connected");
            client.publish("status/gps", "success");
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

    if (MDNS.begin("ChanPark")) {
       Serial.println("MDNS responder started");
    }
    

    webServer.onNotFound(handleNotFound);
    webServer.begin();
    Serial.println("HTTP server started");  
}

void setup_captive() {    
    WiFi.mode(WIFI_AP);
    WiFi.softAPConfig(apIP, apIP, IPAddress(255, 255, 255, 0));
    WiFi.softAP("Chan_GPS");
    
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
      if(gps.encode(uart_gps.read()))
      {
        if(gps.location.isValid())
        {
          char mqtt_buf[20];
          sprintf(mqtt_buf, "%f %f", gps.location.lat(), gps.location.lng());
          Serial.print(mqtt_buf);Serial.println("is published!!");
          yield;
          client.publish("hello/world", mqtt_buf);
        }
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

