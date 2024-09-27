#include <TinyGPS++.h>
#include <SoftwareSerial.h>

int RXPin = 6;
int TXPin = 7;

int GPSBaud = 9600;

TinyGPSPlus gps;

SoftwareSerial gpsSerial(RXPin, TXPin);

int incomingByte; 
char rdata;

#define TINY_GSM_MODEM_SIM800
//Create software serial object to communicate with SIM900
SoftwareSerial SerialAT(8, 9); //SIM900 Tx & Rx is connected to Arduino #7 & #8

#define GSM_AUTOBAUD_MIN 9600
#define GSM_AUTOBAUD_MAX 9600
#include <TinyGsmClient.h>
TinyGsm gsm(SerialAT);
String msg;
void setup()
{
  Serial.begin(9600);
  Serial.println("GPS test");
  gpsSerial.begin(GPSBaud);

  delay(1000);
  
}

void loop()
{
while (gpsSerial.available() > 0)
  {
    if (Serial.available() > 0) {
    // read the oldest byte in the serial buffer:
    incomingByte = Serial.read();
   Serial.println(incomingByte);
    if (incomingByte == 'S')   
    {
      Serial.println("Entered S");
      send();      
      delay(10);
    }

  }
    if (gps.encode(gpsSerial.read()))
      displayInfo();
  
  if (millis() > 5000 && gps.charsProcessed() < 10)
  {
    Serial.println("No GPS detected");
    // while(true);
  }
  
  }
  

  // gps_check();
}

void send()
{
   TinyGsmAutoBaud(SerialAT, GSM_AUTOBAUD_MIN, GSM_AUTOBAUD_MAX);
  Serial.println("Sending message");
  String SMS_TARGET=  "+919740182681";
  if (gps.location.isValid())
  {
    Serial.print("Latitude: ");
    Serial.println(gps.location.lat(), 6);
    Serial.print("Longitude: ");
    Serial.println(gps.location.lng(), 6);
    msg = "Accident location: http://maps.google.com/maps?q=loc:"+String(gps.location.lat(),7)+","+String(gps.location.lng(),7);
    
  }
  else
  {
    Serial.println("Location: Not Available");
    msg =  "Accident location http://maps.google.com/maps?q=loc:13.93672057629985,75.57960836600539";
    msg="Location: Not Available";
  }
  bool res = gsm.sendSMS(SMS_TARGET, String(msg));
  if (res)
  {
    Serial.println("SMS sent");
  }
  else
  {
    Serial.println("SMS: failed");
  }
  
  Serial.println();
  Serial.println();
  delay(1000);
  gpsSerial.begin(GPSBaud);
}

void displayInfo()
{
  if (gps.location.isValid())
  {
    Serial.print("Location Available");
     Serial.print("Latitude: ");
     Serial.println(gps.location.lat(), 6);
     Serial.print("Longitude: ");
     Serial.println(gps.location.lng(), 6);
  }
  else
  {
    Serial.println("Location: Not Available");
  }
  
  Serial.println();
  Serial.println();
  delay(1000);
}