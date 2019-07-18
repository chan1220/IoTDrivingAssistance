#include <ESP8266WiFi.h>
#include <DNSServer.h>
#include <ESP8266WebServer.h>
#include <EEPROM.h>
#include <ESP8266mDNS.h>
#include <PubSubClient.h>
#include <Wire.h>
#define   EEPROM_LENGTH 1024

const int MPU = 0x68;  //MPU 6050 의 I2C 기본 주소

const char*   mqttServer = "15.164.149.11";
const int     mqttPort = 1883;
const char*   mqttUser = "chan";
const char*   mqttPassword = "chan";


char eRead[30];
byte len;
char ssid[30];
char password[30];
char id[30];
char topic[100];

bool captive = true;

WiFiClient espClient;
PubSubClient client(espClient);
const byte DNS_PORT = 53;
IPAddress apIP(192, 168, 1, 1);
DNSServer dnsServer;
ESP8266WebServer webServer(80);

String responseHTML = ""
    "<!DOCTYPE html><html><head><title>Gyro Sensor Setting Page</title></head><body><center>"
    "<p>Gyro Sensor Setting Page</p>"
    "<form action='/button'>"
    "<p><input type='text' name='ssid' placeholder='SSID' onblur='this.value=removeSpaces(this.value);'></p>"
    "<p><input type='text' name='password' placeholder='WLAN Password'></p>"
    "<p><input type='text' name='id' placeholder='Car ID'></p>"
    "<p><input type='submit' value='Submit'></p></form>"
    "<p>This is Gyro Sensor Setting Page</p></center></body>"
    "<script>function removeSpaces(string) {"
    "   return string.split(' ').join('');"
    "}</script></html>";


void setup() 
{
  Serial.begin(9600);
  EEPROM.begin(EEPROM_LENGTH);
  pinMode(0, INPUT_PULLUP);
  attachInterrupt(0, initDevice, FALLING);

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
    strcat(topic, "/gyro");
    Serial.println(topic);
    // -------------
    setup_runtime();  
    client.setServer(mqttServer, mqttPort);
    while (!client.connected()) 
    {
      Serial.println("Connecting to MQTT...");
      if (client.connect("Doraemon_Gyro", mqttUser, mqttPassword )) 
      {
        Serial.println("connected");
        client.publish("Gyro/status", topic);
      } 
      else 
      {
        Serial.print("failed with state "); Serial.println(client.state());
        ESP.restart();
      }
    }
    // Gyro
    Wire.begin();      //Wire 라이브러리 초기화
    Wire.beginTransmission(MPU); //MPU로 데이터 전송 시작
    Wire.write(0x6B);  // PWR_MGMT_1 register
    Wire.write(0);     //MPU-6050 시작 모드로
    Wire.endTransmission(true);
    // -----
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
    char buf[10];
    sprintf(buf, "%.2lf", getGyro());
    client.publish(topic, buf);
    Serial.println(buf);
    delay(1000);
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

  if (MDNS.begin("Doraemon_Gyro")) {
   Serial.println("MDNS responder started");
  }
  

  webServer.onNotFound(handleNotFound);
  webServer.begin();
  Serial.println("HTTP server started");  
}

void setup_captive() {    
  WiFi.mode(WIFI_AP);
  WiFi.softAPConfig(apIP, apIP, IPAddress(255, 255, 255, 0));
  WiFi.softAP("Doraemon_Gyro");
  
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


float getGyro()
{
  int16_t AcX, AcY, AcZ;
  Wire.beginTransmission(MPU);    //데이터 전송시작
  Wire.write(0x3B);               // register 0x3B (ACCEL_XOUT_H), 큐에 데이터 기록
  Wire.endTransmission(false);    //연결유지
  Wire.requestFrom(MPU, 6, true); //MPU에 데이터 요청

  AcX = Wire.read() << 8 | Wire.read();  // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)
  AcY = Wire.read() << 8 | Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  AcZ = Wire.read() << 8 | Wire.read();  // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)

  float RADIAN_TO_DEGREES = 180 / 3.141592;
  float val_y = atan(AcX / sqrt(pow(AcY, 2) + pow(AcZ, 2))) * RADIAN_TO_DEGREES;
  float val_x = atan(AcY / sqrt(pow(AcX, 2) + pow(AcZ, 2))) * RADIAN_TO_DEGREES;

//  Serial.println(val_y);

  //  delay(10);
  return val_x;
}




