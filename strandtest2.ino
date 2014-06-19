#include <Adafruit_NeoPixel.h>

Adafruit_NeoPixel strips[] = {Adafruit_NeoPixel(8, 2, NEO_GRB + NEO_KHZ800), Adafruit_NeoPixel(8, 3, NEO_GRB + NEO_KHZ800)};

String inputString = "";
boolean stringComplete = false;

void setup() {
  Serial.begin(57600);
  inputString.reserve(200);
  
  strips[0].begin();
  strips[0].setBrightness(255); // Half power
  strips[0].show(); // Initialize all pixels to 'off'
  
  strips[1].begin();
  strips[1].setBrightness(255); // Half power
  strips[1].show(); // Initialize all pixels to 'off'
}

void loop() {
  if(stringComplete) {
    int stripId = (int)(inputString.charAt(0) - 48);
    int ledId = (int)(inputString.charAt(1) - 48);
    
    int colors[] = {decodeHex(inputString.substring(2, 4)), decodeHex(inputString.substring(4, 6)), decodeHex(inputString.substring(6, 8))};
    
    strips[stripId].setPixelColor(ledId, strips[stripId].Color(colors[0], colors[1], colors[2]));
    strips[stripId].show();

    stringComplete = false;
    inputString = "";
  }
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}

int decodeHex(String hex) {
  int results = 0;
  char highOrder = hex.charAt(0);
  char lowOrder = hex.charAt(0);
  
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
