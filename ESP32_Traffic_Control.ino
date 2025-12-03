#include <WiFi.h>


const char* ssid = "YOUR_SSID";         
const char* password = "YOUR_PASSWORD"; 
const char* host = "IP_ADDRESS_OF_SYSTEM_ON_WHICH_PYTHON_SERVER_IS_RUNNING";     
const int port = 8080;                       

WiFiClient client;


const int N_R = 23; const int N_Y = 22; const int N_G = 21; 
const int S_R = 19; const int S_Y =18; const int S_G = 5;
const int E_R = 13; const int E_Y = 12; const int E_G = 14;
const int W_R = 4; const int W_Y = 2; const int W_G = 15;


struct LightPins {
    int R, Y, G;
};


const int YELLOW_TIME = 3;


LightPins getPins(char dir) {
    if (dir == 'N') return {N_R, N_Y, N_G};
    if (dir == 'S') return {S_R, S_Y, S_G};
    if (dir == 'E') return {E_R, E_Y, E_G};
    if (dir == 'W') return {W_R, W_Y, W_G};
    return {N_R, N_Y, N_G};
}


void setAllLights(char active_dir, int active_R, int active_Y, int active_G) {
    char dirs[] = {'N', 'S', 'E', 'W'};
    for (char dir : dirs) {
        LightPins pins = getPins(dir);
        if (dir == active_dir) {
            digitalWrite(pins.R, active_R);
            digitalWrite(pins.Y, active_Y);
            digitalWrite(pins.G, active_G);
        } else {
            digitalWrite(pins.R, HIGH);
            digitalWrite(pins.Y, LOW);
            digitalWrite(pins.G, LOW);
        }
    }
}


void setAllRed() {
    setAllLights(' ', HIGH, LOW, LOW); 
}


void transitionToRed(char active_dir) {
    LightPins pins = getPins(active_dir);
    
    Serial.print("Street "); Serial.print(active_dir); 
    Serial.println(" transition: GREEN -> YELLOW -> RED");
    
  
    digitalWrite(pins.G, LOW);
    digitalWrite(pins.Y, HIGH);
    delay(YELLOW_TIME * 1000); 
    
    
    digitalWrite(pins.Y, LOW);
    digitalWrite(pins.R, HIGH);
    
    Serial.println("Transition complete. Waiting for next command.");
}

void connectToWiFi() {
    Serial.print("Connecting to WiFi: ");
    Serial.println(ssid);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println();
    Serial.println("WiFi connected.");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
}

void connectToServer() {
    Serial.print("Connecting to Server: ");
    Serial.print(host);
    Serial.print(":");
    Serial.println(port);

    while (!client.connected()) {
        if (client.connect(host, port)) {
            Serial.println("Connected to server successfully!");
        } else {
            Serial.println("Connection failed! Retrying in 5 seconds...");
            delay(5000);
        }
    }
}

void setup() {
    Serial.begin(115200); 

   
    pinMode(N_R, OUTPUT); pinMode(N_Y, OUTPUT); pinMode(N_G, OUTPUT);
    pinMode(S_R, OUTPUT); pinMode(S_Y, OUTPUT); pinMode(S_G, OUTPUT);
    pinMode(E_R, OUTPUT); pinMode(E_Y, OUTPUT); pinMode(E_G, OUTPUT);
    pinMode(W_R, OUTPUT); pinMode(W_Y, OUTPUT); pinMode(W_G, OUTPUT);
    
    connectToWiFi();
    
    
    setAllRed(); 
    Serial.println("System starting with mandatory 5s All-Red safety gap.");
    delay(5000); 
    setAllRed(); 

    connectToServer();

    Serial.println("ESP32 ready. Waiting for traffic data from Python (Wi-Fi)...");
}

void loop() {
    
    if (!client.connected()) {
        Serial.println("Server disconnected. Reconnecting...");
        connectToServer();
        return;
    }

    if (client.available()) {
        
        String dataStr = client.readStringUntil('\n');
        dataStr.trim();
        
        if (dataStr.length() > 0) {
            int firstComma = dataStr.indexOf(',');
            int secondComma = dataStr.indexOf(',', firstComma + 1);
            
            if (firstComma > 0 && secondComma > 0) {
                char direction = dataStr.charAt(0); 
                int greenTime = dataStr.substring(firstComma + 1, secondComma).toInt(); 
                
                if ((direction == 'N' || direction == 'S' || direction == 'E' || direction == 'W') && greenTime > 0) {
                    
             
                    setAllLights(direction, LOW, LOW, HIGH);
                    Serial.print("Direction "); Serial.print(direction); 
                    Serial.print(" GREEN for "); Serial.print(greenTime); Serial.println("s");
                    delay(greenTime * 1000); 

                    
                    transitionToRed(direction);
                    
                }
            }
        }
    }
}
