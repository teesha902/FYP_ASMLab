#include <Servo.h>
#include <ESP8266WiFi.h> // to connect to WIFI - also: check connection status, get local IP address
#include <WiFiUdp.h> //handling UDP communication (NTP operates over UDP)
#include <NTPClient.h> //simplifies time synchronization with NTP server

const int LED_Pin = D5;
const int SERVO_Pin = D4;

const int servo_angle_on = 50;
const int servo_angle_off = 180;

Servo myServo;

// Replace with your university email and password
#define EAP_IDENTITY "e0758814@u.nus.edu" 
#define EAP_PASSWORD  
const char *ssid = "NUS_STU";  

const long utcOffsetInSeconds = 28800; //define constant - represents offset from Coordinated Universal Time (UTC) in sec
//adjusts time retrieved from NTP server to match local time zone.
//SINGAPORE: UTC Offset: +8 hours --> 8 hr * 60 min * 60 sec

WiFiUDP ntpUDP; //creates instance of WiFiUDP class, named ntpUDP
NTPClient timeClient(ntpUDP, "pool.ntp.org", utcOffsetInSeconds); //creates instance of NTPClient class, named timeClient


void setup() {
  pinMode(LED_Pin, OUTPUT); //set LED pin
  myServo.attach(SERVO_Pin); //set servo pin

  Serial.begin(115200); //initializes serial communication (@ baud rate 115200 bps) - allows sending messages to Serial Monitor for debugging
  WiFi.begin(ssid, EAP_PASSWORD); //starts the process of connecting to a Wi-Fi network

  //continuously checks status of Wi-Fi connection
  //waits until device is connected 
  while (WiFi.status() != WL_CONNECTED) { 
    //might need to check if ^ successful
    delay(500);
    Serial.print(".");
  }

  Serial.println("Connected to WiFi");
  //Serial.print("IP address: ");
  //Serial.println(WiFi.localIP()); // Print the IP address assigned to the device
  
  timeClient.begin(); //initializes NTP client - start fetching time from NTP server
}

void loop() {
    timeClient.update(); //updates time from NTP server - sends req to configured NTP server ("pool.ntp.org")
    //might need to check if ^ successful
    Serial.println(timeClient.getFormattedTime()); //prints current time in string format: "HH:MM:SS".
    delay(1000); //wait 1 sec before repeat

  // Turn the LED on - when feeding tunnel is open
  digitalWrite(LED_Pin, HIGH);
  myServo.write(servo_angle_on);
  delay(1000);

  // Turn the LED off - when feeding tunnel is closed
  digitalWrite(LED_Pin, LOW);
  myServo.write(servo_angle_off);
  delay(3000);
}


void activateServoAndLED() {
  digitalWrite(LED_Pin, HIGH); 
  myServo.write(servo_angle_on); 
    
  delay(5000); // Wait (open) for 5 seconds 
    
  digitalWrite(LED_Pin, LOW); 
  myServo.write(servo_angle_off); 
}
