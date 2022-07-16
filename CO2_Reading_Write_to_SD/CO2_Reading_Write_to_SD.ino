//Measure CO2, temperature, relative humidty, light and display on 16x2 I2C LCD
#include "SD.h"
#include <Adafruit_SCD30.h>              
#include <LiquidCrystal_I2C.h>
#define LED D0
#define CHIP_SELECT D8
//initialize the liquid crystal library
//the first parameter is the I2C address
//the second parameter is how many rows are on your screen
//the third parameter is how many columns are on your screen
LiquidCrystal_I2C lcd(0x27, 16, 2);
  
Adafruit_SCD30  scd30;


const int buttonPin = 2;
int buttonState = 0; 
String filename = "output.txt";


void setup() {

  Serial.begin(9600);
  while (!Serial);

  Serial.println("Adafruit SCD30 test!");

  // Try to initialize!
  while (!scd30.begin()) {
    Serial.println("Failed to find SCD30 chip");
    delay(10);
  }
  Serial.println("SCD30 Found!");

  Serial.print("Measurement Interval: "); 
  Serial.print(scd30.getMeasurementInterval()); 
  Serial.println(" seconds");

  SD.begin(CHIP_SELECT); 
  if(!SD.begin(CHIP_SELECT)) {
    Serial.println("Card Mount Failed");
    return;
  }

//  while (!SD.begin(CHIP_SELECT)) {
//    Serial.println("Initialization failed!");
//  }

  // write headers to output file
  write_to_sd_card("Temp, Relative Humidity, CO2");

  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(LED, OUTPUT);

  lcd.init();                 
  lcd.display();
  lcd.clear();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("HELLO");
  lcd.setCursor(0, 1);
  lcd.print("INITIALIZING");
}


void button() {
  
  if(buttonState == LOW){
     // Turn on the display:
     lcd.display();
     lcd.backlight();
  } else {
     // Turn off the display:
     lcd.noDisplay();
     lcd.noBacklight();
  }
}

void write_to_sd_card(String data) {
    File dataFile = SD.open(filename, FILE_WRITE);
    digitalWrite(LED, LOW);
    Serial.println(data);
    if (dataFile) {
      dataFile.println(data);
      dataFile.close();
      delay(1000);
      digitalWrite(LED, HIGH);
    } else {
      Serial.println("error opening " + filename);
    }
}

void loop() {

    /* Initial checks */
    if (scd30.dataReady()){
      Serial.println("Data available!");
    } else {
      Serial.println("No new data available");  
    }

    if (!scd30.read()){ 
      Serial.println("Error reading sensor data");
      delay(1000);
      return; 
    }

    /* Data collection */
    String co2_reading = String(scd30.CO2, 0);
    String temp_reading = String(scd30.temperature);
    String relative_humidity_reading = String(scd30.relative_humidity);

    /* Serial output for debugging */
    Serial.println("Temperature: " + temp_reading + "degC");
    Serial.println("Relative Humidity: " + relative_humidity_reading + "%");    
    Serial.println("CO2: " + co2_reading + " ppm");

    /* SD card output */
    write_to_sd_card(temp_reading + "," + relative_humidity_reading + "," + co2_reading);

    /* LCD output */
    lcd.setCursor(0, 0);
    lcd.print("CO2:" + co2_reading + "ppm   ");
    
    lcd.setCursor(13, 0);
    lcd.print(temp_reading + "C");  
          
    lcd.setCursor(8, 1);
    lcd.print("RH:" + relative_humidity_reading + "% ");

    /* Run button logic */
    buttonState = digitalRead(buttonPin);
    Serial.print("Button State: ");
    Serial.println(buttonState);
    button();

    delay(2000);
}
