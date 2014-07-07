#include <Adafruit_NeoPixel.h>

Adafruit_NeoPixel strips[] = {Adafruit_NeoPixel(8, 2, NEO_GRB + NEO_KHZ800), Adafruit_NeoPixel(8, 3, NEO_GRB + NEO_KHZ800)};

String inputString = "";
boolean stringOk = false;
boolean talking = true;
int stepping = 0;
unsigned int transitions[2][8][9];
unsigned long lastTime = millis();
#define STEPS 63

void setup() {
  Serial.begin(57600);
  inputString.reserve(20);
  
  strips[0].begin();
  strips[0].setBrightness(255); // Half power
  strips[0].show(); // Initialize all pixels to 'off'
  
  strips[1].begin();
  strips[1].setBrightness(255); // Half power
  strips[1].show(); // Initialize all pixels to 'off'
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
      
      int stripId = (int)(inputString.charAt(0) - 48);
      int ledId = (int)(inputString.charAt(1) - 48);

      for (int i = 0; i <= 10; i += 2) {
        int value = decodeHex(inputString.substring(i+2, i+4));
        transitions[stripId][ledId][i / 2] = value;
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
  for (int i = 0; i < 2; i++) {
      for (int j = 0; j < 8; j++) {
        int red = transitions[i][j][k];
        int green = transitions[i][j][k+1];
        int blue = transitions[i][j][k+2];
        
        int targetRed = transitions[i][j][k2];
        int targetGreen = transitions[i][j][k2+1];
        int targetBlue = transitions[i][j][k2+2];
        
        int deltaRed = targetRed - red;
        int deltaGreen = targetGreen - green;
        int deltaBlue = targetBlue - blue;
        
        strips[i].setPixelColor(j, strips[i].Color(red + deltaRed * steps / STEPS, green + deltaGreen * steps / STEPS, blue + deltaBlue * steps / STEPS));
      }
      strips[i].show();
    }
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
