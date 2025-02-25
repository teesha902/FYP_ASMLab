#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <NTPClient.h>
#include <Servo.h>

const char *ssid = "rpi_hotspot";
const char *password = "rpi_hotspot";

const int LED_Pin = D5;
const int SERVO_Pin = D4;

const int servo_angle_on = 50;
const int servo_angle_off = 180;

WiFiUDP ntpUDP; 
NTPClient timeClient(ntpUDP, "10.42.0.1", 0, 60000);
Servo myServo;

unsigned long lastPrintTime = 0; 
unsigned long lastNTPUpdate = 0;
//const int timeOpen = 1000; //NEED TO MEASURE HOW LONG TO OPEN FOR (in milisec)

const int servoOpenTime = 1000; //in miliseconds
const int startTimeHrs = 17; //24hr time
const int startTimeMin = 33; 

void setup() {
  Serial.begin(115200); 
  WiFi.begin(ssid, password); 
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  
  Serial.println("Connected to WiFi");
  timeClient.begin(); 
  timeClient.setTimeOffset(8 * 3600);

  pinMode(LED_Pin, OUTPUT); 
  myServo.attach(SERVO_Pin); 
  myServo.write(servo_angle_off); // Initialize the servo to the 'off' position

}

void activateSystem(int timeOpened) {
  // Turn LED on
  digitalWrite(LED_Pin, HIGH); 
  Serial.println("LED ON");

  //wait 3 seconds
  delay(3000);

  // Activate the servo for measured time
  myServo.write(servo_angle_on);
  Serial.println("Servo ON");
  delay(timeOpened);

  // Return the servo to the 'off' position
  myServo.write(servo_angle_off);
  Serial.println("Servo OFF");

  // Wait for the remaining 2 seconds
  delay(2000);

  // Turn the LED off
  digitalWrite(LED_Pin, LOW);
  Serial.println("LED OFF");
}


void loop() {
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
  //int currentSecond = timeClient.getSeconds();

  // Print the current time every 30 seconds
  if (millis() - lastPrintTime >= 30000) {
    Serial.print("Current time: ");
    Serial.print(currentHour);
    Serial.print(":");
    Serial.print(currentMinute);
    //Serial.print(":");
    //Serial.println(currentSecond);
    lastPrintTime = millis(); // Update the last print time
    
    if ((currentHour == startTimeHrs && currentMinute == startTimeMin)) {
      activateSystem(servoOpenTime);
    }
  }
  delay(15000); // Check every 15 sec
}

