// author 'Mathieu Bolla'
// copyright 'Copyright 2014, Mathieu Bolla'
// licence 'GPL V3.0'

#include <Adafruit_NeoPixel.h>

Adafruit_NeoPixel strip = Adafruit_NeoPixel(24, 2, NEO_GRB + NEO_KHZ800);
String inputString = "";
boolean stringOk = false;
boolean talking = true;
int stepping = 0;
unsigned int transitions[24][9];
unsigned long lastTime = millis();
#define STEPS 63

void setup() {
  Serial.begin(57600);
  inputString.reserve(20);
  
  strip.begin();
  strip.setBrightness(255); // Half power
  strip.show(); // Initialize all pixels to 'off'
}

void loop() {
  if (talking) {
    if (stringOk) {
      int checksum = 0x0;
      for (int i = 0; i < inputString.length(); i++) {
        int charAtI = inputString.charAt(i);
        checksum ^= charAtI;
      }
      Serial.println(String(checksum, HEX));
      
      int ledId = decodeHex(inputString.substring(0, 2));
      for (int i = 0; i <= 10; i += 2) {
        int value = decodeHex(inputString.substring(i+2, i+4));
        transitions[ledId][i / 2] = value;
      }
      
      stringOk = false;
      inputString = "";
      
      talking = false;
    }
  } else {
    unsigned long currentTime = millis();
    if (currentTime - lastTime > 10 || currentTime - lastTime < 0) {
      lastTime = currentTime;
      showData();
    }
  }
}

void showData() {
  if (stepping < STEPS) {
    showDataAt(0, 3, stepping);
  } else {
    showDataAt(3, 0, stepping - STEPS);
  }
  stepping++;
  if (stepping > 2 * STEPS) {
    stepping = 0;
  }
}

void showDataAt(int k, int k2, int steps) {
      for (int j = 0; j < 24; j++) {
        int red = transitions[j][k];
        int green = transitions[j][k+1];
        int blue = transitions[j][k+2];
        
        int targetRed = transitions[j][k2];
        int targetGreen = transitions[j][k2+1];
        int targetBlue = transitions[j][k2+2];
        
        int deltaRed = targetRed - red;
        int deltaGreen = targetGreen - green;
        int deltaBlue = targetBlue - blue;
        
        strip.setPixelColor(j, strip.Color(red + deltaRed * steps / STEPS, green + deltaGreen * steps / STEPS, blue + deltaBlue * steps / STEPS));
      }
      strip.show();
}

void serialEvent() {
  talking = true;
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n') {
      stringOk = true;
    }
  }
}

int decodeHex(String hex) {
  int results = 0;
  
  char highOrder = hex.charAt(0);
  char lowOrder = hex.charAt(1);
  
  if(highOrder > 58) {
    results += (highOrder - 65 + 10) * 16;
  } else {
    results += (highOrder - 48) * 16;
  }
  
  if(lowOrder > 58) {
    results += lowOrder - 65 + 10;
  } else {
    results += lowOrder - 48;
  }
  
  return results;
}
