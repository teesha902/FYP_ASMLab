//Programmed by: Dr. Tirtha Das Banerjee, Department of Biological Sciences and Center for Life Sciences, NUS
//Date: 13th Dec 2024

#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_ST7735.h> // Hardware-specific library for ST7735 - LCD display
#include <Adafruit_ST7789.h> // Hardware-specific library for ST7789
#include <SPI.h>

#include <Fonts/FreeSansBold24pt7b.h>
#include <Fonts/FreeMonoBoldOblique12pt7b.h>
#include <Fonts/FreeMono12pt7b.h>                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
#include <Fonts/FreeSans9pt7b.h>
#include <Fonts/FreeSans12pt7b.h>
#include <Fonts/FreeMonoBold12pt7b.h>

#define TFT_CS 2
#define TFT_DC 3
#define TFT_RST 4
#define TFT_MOSI 5  // Data out
#define TFT_SCLK 6 // Clock out

#define LED 11

// OR for the ST7789-based displays, we will use this call
Adafruit_ST7789 tft = Adafruit_ST7789(TFT_CS, TFT_DC, TFT_MOSI, TFT_SCLK, TFT_RST);

//clock module
#include <wire.h>
#include <DS1307.h>
DS1307 rtc(A4, A5);

#include <Servo.h>
Servo myservo;

//Button 1: 20 mins (1 time)
int F1 = 10;

//Button 2: 20 mins (3 time)
int F2 = 9;

//Button 3: Timed (1)
int F3 = 8;

//Button 4: Timed (2)
int F4 = 7;


void setup(){
  
  Serial.begin(115200);

  // Initialize the rtc object
  rtc.begin();
  
  // Set the clock to run-mode
  rtc.halt(false);

  // The following lines can be uncommented to set the time
  rtc.setDOW(FRIDAY);        // Set Day-of-Week to SUNDAY
  rtc.setTime(11, 30, 0);    // Set the time to 12:00:00 (24hr format)
  rtc.setDate(15, 12, 2024);  // Set the date to October 3th, 2010
   
    // Set SQW/Out rate to 1Hz, and enable SQW
  rtc.setSQWRate(SQW_RATE_1);
  rtc.enableSQW(true);


  pinMode (F1, INPUT_PULLUP);
  pinMode (F2, INPUT_PULLUP);
  pinMode (F3, INPUT_PULLUP);
  pinMode (F4, INPUT_PULLUP);

 pinMode(LED, OUTPUT);

  // OR use this initializer (uncomment) if using a 2.0" 320x240 TFT:
  tft.init(240, 320);           // Init ST7789 320x240
 
 myservo.attach(12);
  myservo.write(135);// move servos to center position -> 90°
  delay(1000);

  tft.setRotation(3);
  tft.fillScreen(ST77XX_BLACK);
  tft.setFont(&FreeSans12pt7b);
  tft.setCursor(20, 60);
  tft.setTextColor(ST77XX_WHITE);
  tft.setTextSize(2);
  tft.println("Danio Feeder");

   tft.setTextSize(2);
   tft.setFont(&FreeSans12pt7b);
   tft.setCursor(40, 160);
  tft.setTextColor(ST77XX_WHITE);  tft.setTextSize(1);
  tft.println("PROGRAMMED BY");
tft.setCursor(100, 190);
  tft.setTextColor(ST77XX_WHITE);  tft.setTextSize(1);
  tft.println("Tirtha");
  delay(100);

  tft.fillScreen(ST77XX_BLACK);
    tft.setTextColor(ST77XX_WHITE);
    tft.setCursor(30, 90);
    tft.setTextSize(2);
  tft.println("Auto Testing");
    delay(100);

for(int i=0; i<4; i++){
    digitalWrite(LED, HIGH);
    delay(500);
    digitalWrite(LED,LOW);
    myservo.write(110);
  delay(200);
  myservo.write(135);
  tft.setCursor(60, 150);
  tft.setTextSize(1);
  tft.println("2 seconds interval");
  delay(1000);
  }
tft.fillScreen(ST77XX_BLACK);
    tft.setTextColor(ST77XX_WHITE);
    tft.setCursor(20, 90);
    tft.setTextSize(2);
  tft.println("Testing Done");
    delay(100);

} 
void loop(){
 
  tft.fillScreen(ST77XX_WHITE);
  tft.setTextColor(ST77XX_BLACK);
  tft.setTextSize(1);
  tft.setCursor(30, 30);
  tft.println("PRESS FOR 5 SECS:");
tft.setCursor(30, 60);
  tft.println("# 20 mins (1X)");
tft.setCursor(30, 90);
  tft.println("# 20 mins (3X)");
tft.setCursor(30, 120);
  tft.println("# Timed (fixed)");
  tft.setCursor(30, 150);
  tft.println("# Timed (input)");

tft.setTextColor(ST77XX_BLUE);
tft.setCursor(20, 200);
  tft.println("Time:");
  tft.setCursor(100, 200);
  tft.println(rtc.getTimeStr());

  tft.setCursor(20, 230);
  tft.println(rtc.getDOWStr(FORMAT_LONG));
  tft.setCursor(100, 230);
  tft.println(rtc.getDateStr());

delay(10000);

if(digitalRead(F1) == LOW)
  {
    tft.fillScreen(ST77XX_BLACK);
    tft.setTextColor(ST77XX_WHITE);
    tft.setCursor(10, 90);
    tft.setTextSize(2);
  tft.println("Program:");
    tft.setCursor(10, 150);
    tft.setTextSize(2);
  tft.println("20 mins (1X)");
    delay(1200000); //wait for 20 mins

    digitalWrite(LED, HIGH);
    delay(5000);
    digitalWrite(LED, LOW);
    myservo.write(110);
  delay(200);
  myservo.write(135);
  }

  if(digitalRead(F2) == LOW)
  {
    for(int i=0; i<3; i++){
    tft.fillScreen(ST77XX_BLACK);
    tft.setTextColor(ST77XX_WHITE);
    tft.setCursor(10, 90);
    tft.setTextSize(2);
  tft.println("Program:");
    tft.setCursor(10, 150);
    tft.setTextSize(2);
  tft.println("20 mins(3X)");
    delay(1200000); //wait for 20 mins

    digitalWrite(LED, HIGH);
    delay(5000);
    digitalWrite(LED, LOW);
    myservo.write(110);
  delay(200);
  myservo.write(135);
    }
  }

  if(digitalRead(F3) == LOW)
  {
    
  }

  if(digitalRead(F4) == LOW)
  {
   
  }
}