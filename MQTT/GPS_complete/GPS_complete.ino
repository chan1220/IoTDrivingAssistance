#include <ESP8266WiFi.h>
#include <DNSServer.h>
#include <ESP8266WebServer.h>
#include <EEPROM.h>
#include <ESP8266mDNS.h>
#include <PubSubClient.h>
// GPS
#include <SoftwareSerial.h>
#include <TinyGPS.h>
TinyGPS gps;
SoftwareSerial uart_gps(12, 13);
void getgps(TinyGPS &gps);

//
const char*   mqttServer = "49.236.136.179";
const int     mqttPort = 1883;
const char*   mqttUser = "yhur";
const char*   mqttPassword = "hi";

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
    SaveString(0, ""); // blank out the SSID field in EEPROM
}

String responseHTML = ""
    "<!DOCTYPE html><html><head><title>CaptivePortal</title></head><body><center>"
    "<p>Captive Sample Server App</p>"
    "<form action='/button'>"
    "<p><input type='text' name='ssid' placeholder='SSID' onblur='this.value=removeSpaces(this.value);'></p>"
    "<p><input type='text' name='password' placeholder='WLAN Password'></p>"
    "<p><input type='submit' value='Submit'></p></form>"
    "<p>This is a captive portal example</p></center></body>"
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

    if(uart_gps.available())     // While there is data on the RX pin...
    {
        int c = uart_gps.read();    // load the data into a variable...
        if(gps.encode(c))      // if there is a new valid sentence...
        {
          getgps(gps);         // then grab the data.
        }
        else
        {
          Serial.write(c);
        }
    }

    client.loop();
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


void getgps(TinyGPS &gps)
{
  float latitude, longitude;
  gps.f_get_position(&latitude, &longitude);
  Serial.print("Lat/Long: "); 
  Serial.print(latitude,5); 
  Serial.print(", "); 

  gps.crack_datetime(&year,&month,&day,&hour,&minute,&second,&hundredths);
  // Print data and time
  Serial.print("Date: "); Serial.print(month, DEC); Serial.print("/"); 
  Serial.print(day, DEC); Serial.print("/"); Serial.print(year);
  Serial.print("  Time: "); Serial.print(hour, DEC); Serial.print(":"); 
  Serial.print(minute, DEC); Serial.print(":"); Serial.print(second, DEC); 
  Serial.print("."); Serial.println(hundredths, DEC);
  //Since month, day, hour, minute, second, and hundr
  
  // Here you can print the altitude and course values directly since 
  // there is only one value for the function
  Serial.print("Altitude (meters): "); Serial.println(gps.f_altitude());  
  // Same goes for course
  Serial.print("Course (degrees): "); Serial.println(gps.f_course()); 
  // And same goes for speed
  Serial.print("Speed(kmph): "); Serial.println(gps.f_speed_kmph());
  Serial.println();
  
  unsigned long chars;
  unsigned short sentences, failed_checksum;
  gps.stats(&chars, &sentences, &failed_checksum);
  char pub_str[30];
  sprintf(pub_str, "(%f, %f)", latitude, longitude);
  client.publish("hello/world", pub_str);
}



