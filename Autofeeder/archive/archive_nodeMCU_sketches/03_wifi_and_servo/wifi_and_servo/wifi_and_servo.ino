// to connect to WIFI - also: check connection status, get local IP address
#include <ESP8266WiFi.h>

//handling UDP communication (NTP operates over UDP)
#include <WiFiUdp.h>

//simplifies time synchronization with NTP server
#include <NTPClient.h>

#include <Servo.h>

const char *ssid = "rpi_hotspot";
const char *password = "rpi_hotspot";


const int LED_Pin = D5;
const int SERVO_Pin = D4;

const int servo_angle_on = 50;
const int servo_angle_off = 180;

WiFiUDP ntpUDP; //creates instance of WiFiUDP class, named ntpUDP

//creates instance of NTPClient class, named timeClient
//NTPClient timeClient(ntpUDP, "time.google.com"); 
//NTPClient timeClient(ntpUDP, "raspberrypi.local", 0, 60000);
NTPClient timeClient(ntpUDP, "10.42.0.1", 0, 60000);
Servo myServo;

unsigned long lastPrintTime = 0; // Store the last print time
/// DELETE LATER
unsigned long lastNTPUpdate = 0;
const int timeOpen = 1000; //NEED TO MEASURE HOW LONG TO OPEN FOR (in milisec)

void setup() {
  Serial.begin(115200); //initializes serial communication (@ baud rate 115200 bps) - allows sending messages to Serial Monitor for debugging
  WiFi.begin(ssid, password); //starts the process of connecting to a Wi-Fi network
  
  //continuously checks status of Wi-Fi connection
  //waits until device is connected 
  while (WiFi.status() != WL_CONNECTED) {
    //might need to check if ^ successful
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  
  Serial.println("Connected to WiFi");
      //Serial.print("IP address: ");
      //Serial.println(WiFi.localIP()); // Print the IP address assigned to the device
  timeClient.begin(); //initializes NTP client - start fetching time from NTP server
  timeClient.setTimeOffset(8 * 3600);

  pinMode(LED_Pin, OUTPUT); //set LED pin
  myServo.attach(SERVO_Pin); //set servo pin
}

void activateServoAndLED(int timeOpened) {
  // Turn LED on and move servo to 'on' position (feeding tunnel open)
  digitalWrite(LED_Pin, HIGH); 
  myServo.write(servo_angle_on); 
    
  delay(timeOpened); // NEED TO MEASURE HOW LONG TO OPEN FOR (in milisec)
  
  // Turn LED off and move servo to 'off' position (feeding tunnel closed)
  digitalWrite(LED_Pin, LOW); 
  myServo.write(servo_angle_off); 
}


void loop() {
  // Set the UTC offset to Singapore time before each update (8 * 3600 seconds)
  //timeClient.setTimeOffset(8 * 3600);
  //timeClient.update();// continous updates time from NTP server - sends req to configured NTP server ("pool.ntp.org")
  
  // Attempt to update NTP time
  if (millis() - lastNTPUpdate >= 60000 && WiFi.status() == WL_CONNECTED) {
  Serial.println("Attempting NTP time update...");
  bool updated = timeClient.update();

    if (updated) {
      Serial.println("Time updated successfully.");
      Serial.print("Epoch Time: ");
      Serial.println(timeClient.getEpochTime());
    } else {
      Serial.println("Failed to update time. Check NTP server connection.");
    }
    lastNTPUpdate = millis();
  }

  int currentHour = timeClient.getHours();
  int currentMinute = timeClient.getMinutes();
  int currentSecond = timeClient.getSeconds();

  // Print the current time every 30 seconds
  if (millis() - lastPrintTime >= 30000) {
    Serial.print("Current time: ");
    Serial.print(currentHour);
    Serial.print(":");
    Serial.print(currentMinute);
    Serial.print(":");
    Serial.println(currentSecond);
    lastPrintTime = millis(); // Update the last print time
    activateServoAndLED(timeOpen);
  }
  
  /*
  // Specify the times when you want the servo and LED to activate
  if ((currentHour == 14 && currentMinute == ) || (currentHour == 18 && currentMinute == 0)) {
    activateServoAndLED();
  }
  */

  delay(15000); // Check every 15 sec
}

//At given time: 
//LED ON for 3 Seconds
//LED off
//Food 
