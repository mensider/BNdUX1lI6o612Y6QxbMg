#define ENA   14          // Enable/speed motors Right        GPIO14(D5)
#define ENB   12          // Enable/speed motors Left         GPIO12(D6)
#define IN_1  15          // L298N in1 motors Right           GPIO15(D8)
#define IN_2  13          // L298N in2 motors Right           GPIO13(D7)
#define IN_3  2           // L298N in3 motors Left           GPIO2(D4) -> D0 GPIO16
#define IN_4  0           // L298N in4 motors Left            GPIO0(D3) -> D2 GPIO4
#define servo_pin 5
#define parcel_speed 10


#include <ESP8266WiFi.h>
#include <Servo.h>

String command;
int speedCar = 800;
int speed_Coeff = 3;
Servo servo;
int angle;
char myVal;
#define SendKey 0  //Button to send data Flash BTN on NodeMCU

int port = 5000;  //Port number
WiFiServer server(port);

//Server connect to WiFi Network
const char *ssid = "flipkart";  //Enter your wifi SSID
const char *password = "flipkart";  //Enter your wifi Password

int count=0;
//=======================================================================
//                    Power on setup
//=======================================================================
void setup() 
{
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);  
  pinMode(IN_1, OUTPUT);
  pinMode(IN_2, OUTPUT);
  pinMode(IN_3, OUTPUT);
  pinMode(IN_4, OUTPUT); 
  servo.attach(servo_pin);

  
  Serial.begin(9600);
  pinMode(SendKey,INPUT_PULLUP);  //Btn to send data
  Serial.println();

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password); //Connect to wifi
 
  // Wait for connection  
  Serial.println("Connecting to Wifi");
  while (WiFi.status() != WL_CONNECTED) {   
    delay(500);
    Serial.print(".");
    delay(500);
  }

  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);

  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());  
  server.begin();
  Serial.print("Open Telnet and connect to IP:");
  Serial.print(WiFi.localIP());
  Serial.print(" on port ");
  Serial.println(port);
}

void goAhead(){ 
      Serial.println("Go ahead code activated");
      digitalWrite(IN_1, LOW);
      digitalWrite(IN_2, HIGH);
      analogWrite(ENA, speedCar);

      digitalWrite(IN_3, LOW);
      digitalWrite(IN_4, HIGH);
      analogWrite(ENB, speedCar);
      delay(1500);

  }

void goBack(){
//       Serial.println("Go Back code activated");
//       digitalWrite(IN_1, HIGH);
//       digitalWrite(IN_2, LOW);
//       analogWrite(ENA, speedCar);
//
//       digitalWrite(IN_3, HIGH);
//       digitalWrite(IN_4, LOW);
//       analogWrite(ENB, speedCar);

      digitalWrite(IN_1, HIGH);
      digitalWrite(IN_2, LOW);
      analogWrite(ENA, speedCar);

      digitalWrite(IN_3, LOW);
      digitalWrite(IN_4, HIGH);
      analogWrite(ENB, speedCar);
      delay(2000);
  }

void goRight(){ 

      digitalWrite(IN_1, HIGH);
      digitalWrite(IN_2, LOW);
      analogWrite(ENA, speedCar);

      digitalWrite(IN_3, LOW);
      digitalWrite(IN_4, HIGH);
      analogWrite(ENB, speedCar);
      delay(1000);
  }

void goLeft(){

      digitalWrite(IN_1, LOW);
      digitalWrite(IN_2, HIGH);
      analogWrite(ENA, speedCar);

      digitalWrite(IN_3, HIGH);
      digitalWrite(IN_4, LOW);
      analogWrite(ENB, speedCar);
      delay(1000);
  }

void goAheadRight(){
      
      digitalWrite(IN_1, LOW);
      digitalWrite(IN_2, HIGH);
      //analogWrite(ENA, speedCar/speed_Coeff);
 
      digitalWrite(IN_3, LOW);
      digitalWrite(IN_4, HIGH);
      //analogWrite(ENB, speedCar);
   }

void goAheadLeft(){
      
      digitalWrite(IN_1, LOW);
      digitalWrite(IN_2, HIGH);
      //analogWrite(ENA, speedCar);

      digitalWrite(IN_3, LOW);
      digitalWrite(IN_4, HIGH);
      //analogWrite(ENB, speedCar/speed_Coeff);
  }

void goBackRight(){ 

      digitalWrite(IN_1, HIGH);
      digitalWrite(IN_2, LOW);
      //analogWrite(ENA, speedCar/speed_Coeff);

      digitalWrite(IN_3, HIGH);
      digitalWrite(IN_4, LOW);
      //analogWrite(ENB, speedCar);
  }

void goBackLeft(){ 

      digitalWrite(IN_1, HIGH);
      digitalWrite(IN_2, LOW);
      //analogWrite(ENA, speedCar);

      digitalWrite(IN_3, HIGH);
      digitalWrite(IN_4, LOW);
      //analogWrite(ENB, speedCar/speed_Coeff);
  }
  
void drop_parcel() {
  Serial.println("Droping");
for(angle = 90; angle >= 0; angle--) {
    servo.write(angle);
    delay(parcel_speed);
  
  }

  delay(1000);
for(angle = 0; angle <= 90; angle++) {
    servo.write(angle);
    delay(parcel_speed);
  
  }
}
void stopRobot(){  

      digitalWrite(IN_1, LOW);
      digitalWrite(IN_2, LOW);
      analogWrite(ENA, speedCar);
      
      
      digitalWrite(IN_3, LOW);
      digitalWrite(IN_4, LOW);
      analogWrite(ENB, speedCar);
     
      //drop_parcel();
      //bool state = false;
      
 }
//=======================================================================
//                    Loop
//=======================================================================

void loop() 
{
  WiFiClient client = server.available();
  
  if (client) {
    if(client.connected())
    {
      Serial.println("Client Connected");
    }
    
    while(client.connected()){      
      while(client.available()>0){
        // read data from the connected client
        //Serial.write(client.read());
        command =client.read();
        Serial.println(command);
        Serial.println(myVal);
        if (command == "F") goAhead();
        else if (command == "B") goBack();
        else if (command == "L") goLeft();
        else if (command == "R") goRight();
        else if (command == "I") goAheadRight();
        else if (command == "G") drop_parcel();
        else if (command == "J") goBackRight();
        else if (command == "H") goBackLeft();
        else if (command == "0") speedCar = 400;
        else if (command == "1") speedCar = 470;
        else if (command == "2") speedCar = 540;
        else if (command == "3") speedCar = 610;
        else if (command == "4") speedCar = 680;
        else if (command == "5") speedCar = 750;
        else if (command == "6") speedCar = 820;
        else if (command == "7") speedCar = 890;
        else if (command == "8") speedCar = 960;
        else if (command == "9") speedCar = 1023;
        else if (command == "S") stopRobot();
        command = "e";
        stopRobot();
        client.write("OK");
      }
      //Send Data to connected client
      while(Serial.available()>0)
      {
        //client.write(Serial.read());
        client.write("OK");
        Serial.println("OK");
      }
    }
    client.stop();
    Serial.println("Client disconnected");    
  }
}
