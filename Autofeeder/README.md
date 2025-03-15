# **Auto-Feeder System**  

This document provides **detailed instructions** for setting up, using, and customizing the Auto-Feeder System. The system automates feeding schedules using **an Arduino, an OLED display, an RTC module (Real-Time Clock), and servo motors**.  

There are **two versions** of the system:  
✅ **Single Feeder** – Uses **one** servo and **one** LED for dispensing food.  
✅ **Dual Feeder** – Uses **two** servos and **two** LEDs, allowing feeding from **two separate compartments** (Side A, Side B, or Both).  

---

## **1. Button Functions**  

| **Button**  | **Functionality (Single Feeder)** | **Functionality (Dual Feeder)** |
|-------------|----------------------------------|----------------------------------|
| **Button 1** | **Displays the welcome animation again** | **Switches between feeding modes (Side A, Side B, Both)** |
| **Button 2** | **Immediate feeding with countdown** | **Feeds according to selected mode** |
| **Button 3** | **Displays scheduled feeding times** | **Displays scheduled feeding times** |
| **Button 4** | **Triggers a 5-minute feeding event** | **Triggers a 5-minute feeding event for selected mode** |

---

## **2. First-Time Setup & Uploading Code to the Feeder**  

### **📌 Steps for First-Time Setup (New Device)**
1. **Download the code from the `arduino_scripts` folder**.  
2. **Open the Arduino IDE and set up the correct board & port:**  
   - Go to **Tools > Board** and select **Arduino Uno** (or the board you’re using).  
   - Go to **Tools > Port** and select the correct port (e.g., `COM3` on Windows, `/dev/ttyUSB0` on Linux/Mac).  
3. **Enable the Serial Monitor for Debugging:**  
   - Click **Tools > Serial Monitor** (or press `Ctrl + Shift + M`).  
   - Set the baud rate to **9600** (bottom-right corner).  
   - This allows you to check if the RTC and other components are working properly.

### **📌 If This Is the First Upload (Setting the RTC Time)**
1. Locate this line in `setup()`:  
   ```cpp
   rtc.setDateTime(__DATE__, __TIME__);
   ```
2. **Uncomment the line** (remove `//` at the beginning).  
3. **Upload the code** to set the RTC to the current time.  
4. **Comment the line back out** and re-upload the code:  
   ```cpp
   // rtc.setDateTime(__DATE__, __TIME__);
   ```
   ✅ **Why?** If this line is left active, the RTC will reset every time the Arduino restarts.  

5. **Check the Serial Monitor output** to verify the RTC is set correctly:
   ```
   Time now: 2025-02-27 14:35:12
   ```
   If incorrect, repeat the steps above.

### **📌 If Reuploading Code Later**
- If making **changes to feeding times or parameters**, just upload the updated code.
- If the **RTC time is incorrect**, follow the **RTC resetting instructions** above.

---

## **3. Changing the Scheduled Feeding Times**  

The **feeding schedule** is stored in the `feedingTimes` array.  

### **📌 How to Modify Feeding Times**
1. **Open the code in Arduino IDE**.  
2. Locate this section:
   ```cpp
   const int feedingTimes[][3] = {
       {9, 30, 0},    // 9:30 AM
       {10, 07, 0},   // 10:07 AM
       {15, 34, 0},   // 3:34 PM
       {20, 00, 00}   // 8:00 PM
   };
   ```
3. **Edit the times** or **add/remove entries** as needed.  
4. **Upload the modified code to the feeder**.  

### **📌 Time Format**
- **Use 24-hour format** (e.g., `{15, 00, 00}` for **3:00 PM**).  
- Each entry follows `{hour, minute, second}`.  

---

## **4. Adjusting Feeding Amount (Servo Open Time)**  

The **amount of food dispensed** is controlled by **how long the servo stays open**.

### **📌 How to Adjust the Feeding Amount**
1. Locate this line in the code:
   ```cpp
   #define SERVO_OPEN_TIME 100  // Adjust time in milliseconds
   ```
2. **Increase the value** to dispense **more** food.  
3. **Decrease the value** to dispense **less** food.  
4. **Upload the modified code.**  

✅ **Test different values to ensure the correct food portion.**  

---

## **5. Immediate Feeding (Button 2)**  
Button 2 triggers **immediate feeding** after a 5-second countdown.

### **📌 Expected Serial Monitor Output**
```
Button 2 pressed - Immediate Feeding
Feeding in 5 sec
Feeding in 4 sec
Feeding in 3 sec
Feeding in 2 sec
Feeding in 1 sec
Feeding now!
Feeding Complete!
```
If nothing happens, check:  
✅ The **servo wiring**.  
✅ The **Serial Monitor output** for button press detection.  

---

## **6. 5-Minute Feeding Event (Button 4)**  
Button 4 starts a **5-minute feeding event**, consisting of:
1. A **1-minute countdown** before feeding.  
2. A **feeding event** at **1:00**.  
3. A **final countdown** until **5:00**.  

### **📌 Expected Serial Monitor Output**
```
Button 4 pressed - 5-Minute Feeding Event
Feeding in 60 sec
Feeding in 59 sec
...
Feeding in 1 sec
Feeding now!
Feeding Complete!
Time left: 3:59
Time left: 3:58
...
Feeding Event Over!
```

✅ **If feeding doesn’t occur at 1:00, check the servo wiring.**  

---

## **7. Using the Serial Monitor to Debug Issues**  

### **Checking If the RTC Time Is Correct**
If the time displayed on the OLED is incorrect, check the Serial Monitor:
```
Time now: 2025-02-27 14:35:12
```
If incorrect, follow the **RTC Resetting Guide (Section 2)** to fix it.

### **Checking Button Presses**
When a button is pressed, the Serial Monitor will show:
```
Button 1 pressed
Button 2 pressed
Button 3 pressed
Button 4 pressed
```
✅ **If nothing appears**, check the wiring.

### **Checking If the Servo Is Moving**
When the servo operates, the Serial Monitor will print:
```
Triggering Feeding...
```
✅ **If you don’t see this, the servo may not be connected correctly.**

---

## **8. Assembly References**  

- **📂 `CAD_files`** – Includes **3D printable case files** for housing the feeder hardware.  
- **📂 `wiring_diagram`** – Contains **wiring diagrams** for assembling the feeder.  
- **📂 `arduino_scripts`** – Contains the **Arduino programs** for **single and dual feeders**.  

---

## **9. Final Notes**  
✅ **Test the system using the Serial Monitor before deployment.**  
✅ **Ensure the correct time is set before leaving the feeder unattended.**  
✅ **Regularly check the RTC battery and servo connections for accuracy.**  

🚀 **Auto-Feeder System is now ready for use in lab experiments!** 🚀
