#include <Wire.h>               // I2C communication for RTC module
#include <RTClib.h>             // Library for DS1307 RTC module
#include <Servo.h>              // Library for controlling servo motor
#include <Adafruit_GFX.h>       // Graphics library for TFT display
#include <Adafruit_TFTLCD.h>    // TFT display control library

// Pin definitions
const int SERVO_PIN = 9;
const int LED_PIN = 7;
const int BUTTON1 = 2; // Button 1 (Event Mode)
const int BUTTON2 = 3; // Button 2 (Sleep/Wake Mode)
const int BUTTON3 = 4; // Button 3 (Return to Default Mode)
const int BUTTON4 = 5; // Button 4 (Show Menu)
const int TFT_CS = 10; // TFT Chip Select pin
const int TFT_DC = 9;  // TFT Data/Command pin
const int TFT_RST = 8; // TFT Reset pin

// Feeding schedule constants [EXAMPLE]
const int FEED_HOUR_1 = 9;   // First feeding time: 9:00 AM
const int FEED_MINUTE_1 = 0;
const int FEED_HOUR_2 = 18;  // Second feeding time: 6:00 PM
const int FEED_MINUTE_2 = 0;
//to adjust time duration servo is open --> feed() function

// TFT and RTC objects
Adafruit_TFTLCD tft(TFT_CS, TFT_DC, TFT_RST); // TFT display object
RTC_DS1307 rtc; // RTC module object
Servo myServo; // Servo motor object

// State variables
bool isSleeping = false; // Power-saving mode status
unsigned long lastInteractionTime = 0; // Tracks last user interaction
const int idleTime = 15000; // Auto sleep after 15 seconds - for power saving

void setup() {
  Serial.begin(9600);
  
  // Initialize RTC
  if (!rtc.begin()) {
    Serial.println("Couldn't find RTC");
    while (1); // Stops program if RTC not found
  }

  //set correct date, time 
  if (!rtc.isrunning()) {
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__))); 
  }
  
  // Initialize TFT Display
  tft.begin();
  tft.setRotation(1); // Rotate display to landscape
  tft.fillScreen(BLACK); // Clear the screen
  tft.setTextColor(WHITE); // White text color
   
  // Initialize Servo
  myServo.attach(SERVO_PIN);
  myServo.write(0); // Set servo to default position
  
  // Initialize LED
  pinMode(LED_PIN, OUTPUT);
  
  // Initialize Buttons
  pinMode(BUTTON1, INPUT_PULLUP);
  pinMode(BUTTON2, INPUT_PULLUP);
  pinMode(BUTTON3, INPUT_PULLUP);
  pinMode(BUTTON4, INPUT_PULLUP);
  
  showWelcomeScreen(); //Display welcome message upon starting
  lastInteractionTime = millis();
}

void loop() {
  // Event Handling - Check which button pressed -- activates corresponding mode
  if (!digitalRead(BUTTON1)) activateEventMode();
  else if (!digitalRead(BUTTON2)) testServoAndLED();
  else if (!digitalRead(BUTTON3)) returnToDefaultMode();
  else if (!digitalRead(BUTTON4)) showMenu();

  // Run Default Mode (Servo open/close at set times)
  runDefaultMode();
}

void runDefaultMode() {
  DateTime now = rtc.now();

  // Display the scheduled feeding times
  tft.fillScreen(BLACK);
  tft.setCursor(0, 0);
  tft.println("Default Mode:");
  tft.println("Scheduled Feeding:");
  tft.print("1. ");
  tft.print(FEED_HOUR_1);
  tft.print(":");
  tft.print(FEED_MINUTE_1 < 10 ? "0" : "");
  tft.print(FEED_MINUTE_1);
  tft.println(" AM");
  tft.print("2. ");
  tft.print(FEED_HOUR_2 % 12);
  tft.print(":");
  tft.print(FEED_MINUTE_2 < 10 ? "0" : "");
  tft.print(FEED_MINUTE_2);
  tft.println(" PM");

  if ((now.hour() == FEED_HOUR_1 && now.minute() == FEED_MINUTE_1) ||
      (now.hour() == FEED_HOUR_2 && now.minute() == FEED_MINUTE_2)) {
    feed();
  }
}

//BUTTON 1 
void activateEventMode() {
  lastInteractionTime = millis();
  showStatus("Event mode starting...");

  // Pre-event countdown
  for (int i = 5; i > 0; i--) {
    showCountdown("Get ready to film ", i);
    delay(1000);
  }

  // 3-minute countdown
  showCountdown("Event running [3 min]", 180);

  // Countdown before LED activation
  for (int i = 120; i > 0; i--) {
    if (i == 60) {
      digitalWrite(LED_PIN, HIGH);
      showCountdown("LED On for 5s", 5);
      delay(5000);
      digitalWrite(LED_PIN, LOW);
    }
    showCountdown("Time till LED activation", i);
    delay(1000);
  }

  // Servo activation countdown
  for (int i = 5; i > 0; i--) {
    showCountdown("Time till feeding", i);
    delay(1000);
  }
  feed();

  // Timer for 2 minutes after servo opening
  showCountdown("Post-event timer [2 min]", 120);
  delay(120000);

  showStatus("Event complete!");
}

//BUTTON 2
void testServoAndLED() {
  lastInteractionTime = millis();
  showStatus("Testing Servo and LED...");

  // Test LED
  digitalWrite(LED_PIN, HIGH);
  delay(1000); // LED on for 1 second
  digitalWrite(LED_PIN, LOW);

  // Test Servo
  feed();
  showStatus("Test complete");
}

//BUTTON 3
void returnToDefaultMode() {
  lastInteractionTime = millis();
  showStatus("Returning to default mode...");
}

//BUTTON 4
void showMenu() {
  lastInteractionTime = millis();
  tft.fillScreen(BLACK);
  tft.setCursor(0, 0);
  tft.println("Menu:");
  tft.println("1. Event Mode");
  tft.println("2. Test Servo/LED");
  tft.println("3. Default Mode");
  tft.println("4. Show Menu");
}

//HELPER FUNCTIONS

//open and close servo 
void feed() {
  myServo.write(90); // Open position
  delay(150);        // Stay open for 150 ms
  myServo.write(0);  // Close position
}

//Display startup message.
void showWelcomeScreen() {
  tft.fillScreen(BLACK);
  tft.setCursor(0, 0);
  tft.println("Dual Channel Feeder");
  tft.println("Initializing...");
  delay(2000);
  tft.fillScreen(BLACK);
  showStatus("Default mode active");
}

// Updates the display with a status message
void showStatus(const char* message) {
  tft.fillScreen(BLACK);
  tft.setCursor(0, 0);
  tft.println(message);
}

void showCountdown(const char* message, int seconds) {
  tft.fillScreen(BLACK);
  tft.setCursor(0, 0);
  tft.print(message);
  tft.print(" - ");
  tft.print(seconds);
  tft.println("s remaining");
}
