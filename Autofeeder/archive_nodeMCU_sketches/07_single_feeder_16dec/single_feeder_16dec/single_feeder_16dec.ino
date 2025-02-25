#include <Wire.h>          // I2C communication for RTC module
#include <RTClib.h>        // Library for DS1307 RTC module
#include <Servo.h>         // Library for controlling servo motor
#include <Adafruit_GFX.h>  // Graphics library for TFT display - fonts etc
//#include <Adafruit_TFTLCD.h>  // For older/large TFT screens (parallel).
//#include <Adafruit_ST7735.h>  // For lower-resolution (128x160) TFT screens.
#include <Adafruit_ST7789.h>  //Lbrary for controlling LCD screen 
#include <SPI.h>              //core library - facilitates communication between Arduino (master) & SPI-compatible devices (slaves) - screen 

//Colors and Fonts
#define BLACK 0x0000
#define WHITE 0xFFFF
//#include <Fonts/FreeSans9pt7b.h>
#include <Fonts/FreeSansBold9pt7b.h>  //from Adafruit GFX library - 9 pixel height
//#include <Fonts/FreeSans12pt7b.h>
//#include <Fonts/FreeSansBold12pt7b.h>


// Pin definitions
const int SERVO_PIN = 12;  // Single Servo control pin (corrected per diagram)
const int LED_PIN = 11;    // Single LED control pin (corrected per diagram)
const int BUTTON1 = 10;    // Button 1 (Event Mode) - Corrected
const int BUTTON2 = 9;     // Button 2 (Test Servo/LED) - Corrected
const int BUTTON3 = 8;     // Button 3 (Return to Default Mode) - Corrected
const int BUTTON4 = 7;     // Button 4 (Show Menu) - Corrected
const int TFT_CS = 2;      // TFT Chip Select pin
const int TFT_DC = 3;      // TFT Data/Command pin
const int TFT_RST = 4;     // TFT Reset pin
const int TFT_MOSI = 5;    //(Master Out Slave In) - send DATA OUT (color/commands) from Arduino (master) to display (slave)
const int TFT_SCLK = 6;    // Clock out (Serial Clock) - like metronome - tells display when to read data from MOSI


// Feeding schedule constants [EXAMPLE]
const int FEED_HOUR_1 = 9;  // First feeding time: 9:00 AM
const int FEED_MINUTE_1 = 0;
const int FEED_HOUR_2 = 18;  // Second feeding time: 6:00 PM
const int FEED_MINUTE_2 = 0;

// Servo angle constants
const int SERVO_OPEN_ANGLE = 110;   // Open position (110 degrees)
const int SERVO_CLOSE_ANGLE = 135;  // Close position (135 degrees)

// Objects
Adafruit_ST7789 tft = Adafruit_ST7789(TFT_CS, TFT_DC, TFT_MOSI, TFT_SCLK, TFT_RST);  // TFT display object
RTC_DS1307 rtc;                                                                      // RTC module object
Servo myServo;                                                                       // Servo motor object

// State variables
//unsigned long lastInteractionTime = 0;  // Tracks last user interaction
//const int idleTime = 15000;             // Auto sleep after 15 seconds

void setup() {
  Serial.begin(9600);
  Serial.println("Starting System...");

  // Initialize RTC
  if (!rtc.begin()) {
    Serial.println("ERROR: Couldn't find RTC");
    while (1)
      ;  // Stops program if RTC not found
  }

  if (!rtc.isrunning()) {
    Serial.println("RTC not running. Setting time...");
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));  // Set to compile time
  } else {
    // Check the current time on the RTC
    DateTime now = rtc.now();
    Serial.print("RTC is running. Current time: ");
    Serial.print(now.year());
    Serial.print('/');
    Serial.print(now.month());
    Serial.print('/');
    Serial.print(now.day());
    Serial.print(" ");
    Serial.print(now.hour());
    Serial.print(':');
    Serial.print(now.minute());
    Serial.print(':');
    Serial.println(now.second());
  }
  Serial.println("RTC Initialized.");

  // Initialize TFT Display
  Serial.println("Initializing TFT display...");
  tft.init(240, 320);  // Set dimensions for ST7789
  tft.setRotation(1);
  tft.fillScreen(BLACK);
  tft.setTextColor(WHITE);
  //starting message
  //tft.setRotation(3); //upside down
  tft.setFont(&FreeSansBold9pt7b);
  tft.setCursor(20, 60);
  //tft.setTextSize(1); ??
  tft.setCursor(20, 60);
  tft.println("Starting up AutoFeeder...");  //can be bigger and lower
  Serial.println("TFT Display Initialized.");

  // Initialize Servo
  Serial.println("Initializing Servo...");
  myServo.attach(SERVO_PIN);
  myServo.write(SERVO_CLOSE_ANGLE);  // Set servo to closed position
  Serial.println("Servo Initialized. Moved to close position.");

  // Initialize LED
  pinMode(LED_PIN, OUTPUT);
  Serial.println("LED Initialized.");

  // Initialize Buttons
  pinMode(BUTTON1, INPUT_PULLUP);
  pinMode(BUTTON2, INPUT_PULLUP);
  pinMode(BUTTON3, INPUT_PULLUP);
  pinMode(BUTTON4, INPUT_PULLUP);
  Serial.println("Buttons Initialized.");

  tft.setCursor(20, 120);
  showStatus("Default Mode Active");  //can be bigger and lower
  Serial.println("Default Mode Active.");
  //lastInteractionTime = millis();  //?? for what
}

void loop() {
  // Event Handling - Check button presses -- check if button == LOW (inactive-enabled) 
  //NEED TO PRESS FIRMLY AND HOLD FOR 3-5 SECONDS
  //(top most)
  if (!digitalRead(BUTTON1)) {
    Serial.println("Button 1 pressed: Activating Event Mode.");
    activateEventMode();
  } else if (!digitalRead(BUTTON2)) {
    Serial.println("Button 2 pressed: Testing Servo and LED.");
    testServoAndLED();
  } else if (!digitalRead(BUTTON3)) {
    Serial.println("Button 3 pressed: Returning to Default Mode."); // No need - does this after every event anyway 
    returnToDefaultMode();
  //(bottom most)
  } else if (!digitalRead(BUTTON4)) {
    Serial.println("Button 4 pressed: Showing Menu."); // Show on welcome page? 
    showMenu();
  }

  runDefaultMode();
}

void runDefaultMode() {
  DateTime now = rtc.now();

  tft.fillScreen(BLACK);
  //tft.setCursor(20, 60);
  //tft.println("DEFAULT FEEDING TIMES:");
  tft.setCursor(30, 90);
  tft.println("Scheduled Feeding Times:");
  tft.setCursor(30, 120);
  tft.print("1. ");
  tft.print(FEED_HOUR_1);
  tft.print(":");
  tft.print(FEED_MINUTE_1 < 10 ? "0" : "");
  tft.print(FEED_MINUTE_1);
  tft.println(" hrs");
  tft.setCursor(30, 150);
  tft.print("2. ");
  tft.print(FEED_HOUR_2);
  tft.print(":");
  tft.print(FEED_MINUTE_2 < 10 ? "0" : "");
  tft.print(FEED_MINUTE_2);
  tft.println(" hrs");

  delay(1000);
  if ((now.hour() == FEED_HOUR_1 && now.minute() == FEED_MINUTE_1) || (now.hour() == FEED_HOUR_2 && now.minute() == FEED_MINUTE_2)) {
    tft.setCursor(20, 60);
    tft.println("Feeding Time!");
    Serial.println("Feeding time reached.");
    feed();
  }
}

void activateEventMode() {
  showStatus("Event mode starting...");
  Serial.println("Entering Event Mode...");

  int countdown = 5;                  // Countdown starts from 5  
  // Countdown loop
  while (countdown > 0) {
    countdown("LED", countdown); // Update the display
    Serial.print("Countdown: ");
    Serial.println(countdown);
    countdown--; // Decrease the countdown
  }
  /*
  //updated code to be accurate to 5 seconds 
  unsigned long startTime = millis(); // Record the start time
  int countdown = 5;                  // Countdown starts from 5 seconds

  while (countdown > 0) {
    unsigned long currentTime = millis();
    
    // Check if 1 second has passed
    if (currentTime - startTime >= 1000) {
      startTime = currentTime; // Update the start time for the next interval
      //bigger font - split message on 2 lines - bring down lower 
      countdown("Get ready to turn on LED", countdown); // Update the display
      Serial.print("Countdown: ");
      Serial.println(countdown);
      countdown--; // Decrease the countdown
    }
  }
  */

  // Trigger LED+Servo mechanism
  //light on 5 seconds before, then feed 3 seconds in
  digitalWrite(LED_PIN, HIGH);
  Serial.println("LED turned ON.");
  unsigned long startTime2 = millis(); // Record the start time
  while (millis() - startTime2 < 5000) { // Keep LED on for 5 seconds
    if (millis() - startTime2 == 3000) { // Check if 3 seconds have passed
      Serial.println("Performing feed() at 3 seconds.");
      feed(); // Call feed function
    }
  }
  // Turn off the LED after 5 seconds
  digitalWrite(LED_PIN, LOW);
  Serial.println("LED turned OFF.");

  //feed();
  //message lower and bigger
  showStatus("Event Complete");
  Serial.println("Event Mode complete.");

  /*
  for (int i = 5; i > 0; i--) {
    countdown("Get ready to feed", i);
    //each feels longer than 1 second
    delay(1000);
  }

  feed();
  showStatus("Event Complete");
  Serial.println("Event Mode complete.");
  */
}

void testServoAndLED() {
  //not really immediate 
      //all messages biggers and bring down to center more
  showStatus("Testing Servo and LED...");
  Serial.println("Testing LED and Servo.");

  digitalWrite(LED_PIN, HIGH);
  delay(1000);
  digitalWrite(LED_PIN, LOW);

  feed();
  showStatus("Test Complete");
  Serial.println("Test Complete.");
}

void returnToDefaultMode() {
  //lower in screen 
  showStatus("Returning to Default Mode...");
  Serial.println("Returning to Default Mode.");
}

void showMenu() {
  tft.fillScreen(BLACK);
  tft.setCursor(20, 60);
  tft.println("Menu:");
  tft.println("1. Event Mode");
  tft.println("2. Test Servo/LED");
  tft.println("3. Default Mode");
  tft.println("4. Show Menu");
  Serial.println("Menu displayed on screen.");
}

void feed() {
  //Message on screen? 
  Serial.println("Feeding: Moving servo.");
  myServo.write(SERVO_OPEN_ANGLE);
  delay(150);
  myServo.write(SERVO_CLOSE_ANGLE);
  Serial.println("Feeding Complete: Servo returned to close position.");
}

void showStatus(const char* message) {
  tft.fillScreen(BLACK);
  tft.setCursor(20, 60);
  tft.println(message);
  Serial.print("Status: ");
  Serial.println(message);
}

void countdown(const char* message, int time) {
  tft.fillScreen(BLACK);
  tft.setCursor(20, 60);
  tft.print(message);
  tft.print(" in ");
  tft.println(time);
  //tft.println("seconds");
  Serial.print(message);
  Serial.print(" in ");
  Serial.println(time);
}

/*
// Function to center text horizontally and vertically
void centerText(const char* text, int yPosition) {
  int16_t x1, y1; // Variables to hold text bounds
  uint16_t textWidth, textHeight;
  
  // Get text dimensions using getTextBounds
  tft.setFont(&FreeSans12pt7b); // Set the desired font
  tft.getTextBounds(text, 0, 0, &x1, &y1, &textWidth, &textHeight);
  
  // Calculate the X position to center the text
  int16_t xCenter = (tft.width() - textWidth) / 2;
  
  // Set the cursor position to center the text
  tft.setCursor(xCenter, yPosition);
  tft.println(text);
}
*/