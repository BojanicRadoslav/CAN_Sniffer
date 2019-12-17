// CAN Receive Example
//

#include <mcp_can.h>
#include <SPI.h>
#include <SoftwareSerial.h>

long unsigned int rxId;
unsigned char len = 0;
unsigned char rxBuf[8];
char msgString[128];                        // Array to store serial string

#define CAN0_INT 2                              // Set INT to pin 2
MCP_CAN CAN0(10);                               // Set CS to pin 10
SoftwareSerial mySerial(4,3);

void setup()
{
  Serial.begin(115200);
  mySerial.begin(9600);
  
  // Initialize MCP2515 running at 16MHz with a baudrate of 500kb/s and the masks and filters disabled.
  if(CAN0.begin(MCP_ANY, CAN_500KBPS, MCP_16MHZ) == CAN_OK)
    Serial.println("MCP2515 Initialized Successfully!");
  else
    Serial.println("Error Initializing MCP2515...");
  
  CAN0.setMode(MCP_NORMAL);                     // Set operation mode to normal so the MCP2515 sends acks to received data.

  pinMode(CAN0_INT, INPUT);                            // Configuring pin for /INT input
  
  Serial.println("MCP2515 Library Receive Example...");
}

void loop()
{
  if(mySerial.available() > 0){
    String s = mySerial.readString();
    setBitrate(s);
  }
  if(!digitalRead(CAN0_INT))                         // If CAN0_INT pin is low, read receive buffer
  {
    CAN0.readMsgBuf(&rxId, &len, rxBuf);      // Read data: len = data length, buf = data byte(s)
    
    if((rxId & 0x40000000) == 0x40000000){    // Determine if message is a remote request frame.
      sprintf(msgString, " REMOTE REQUEST FRAME");
      //Serial.print(msgString);
    } else {
      
      String s = String(rxId, HEX);
      if(s.length() == 2){
        s = "0" + s;
      }
  
      char addr[3];
      addr[0] = s[0];
      addr[1] = s[1];
      addr[2] = s[2];
  
      char data[8];
        for(byte i = 0; i<len; i++){
          data[i] = rxBuf[i];
          //Serial.println(data[i], HEX);
        }
  
  
       char msg[sizeof(addr)+sizeof(data)];
       msg[0] = addr[0];
       msg[1] = addr[1];
       msg[2] = addr[2];
       
       for(byte i = 0; i<len; i++){
          msg[i+3] = data[i];
          //Serial.println(data[i], HEX);
        }
  
        mySerial.write(msg, len+3);
  
      }
  }
}

void setBitrate(String br){
  
  if(br == "5KBPS"){
      if(CAN0.begin(MCP_ANY, CAN_5KBPS, MCP_16MHZ) == CAN_OK)
        Serial.println("MCP2515 Initialized Successfully!");
      else  
        Serial.println("Error Initializing MCP2515...");
  }else if(br == "10KBPS"){
      if(CAN0.begin(MCP_ANY, CAN_10KBPS, MCP_16MHZ) == CAN_OK)
        Serial.println("MCP2515 Initialized Successfully!");
      else  
        Serial.println("Error Initializing MCP2515...");
  }else if(br == "20KBPS"){
      if(CAN0.begin(MCP_ANY, CAN_20KBPS, MCP_16MHZ) == CAN_OK)
        Serial.println("MCP2515 Initialized Successfully!");
      else  
        Serial.println("Error Initializing MCP2515...");
  }else if(br == "31K25BPS"){
      if(CAN0.begin(MCP_ANY, CAN_31K25BPS, MCP_16MHZ) == CAN_OK)
        Serial.println("MCP2515 Initialized Successfully!");
      else  
        Serial.println("Error Initializing MCP2515...");
  }else if(br == "40KBPS"){
      if(CAN0.begin(MCP_ANY, CAN_40KBPS, MCP_16MHZ) == CAN_OK)
        Serial.println("MCP2515 Initialized Successfully!");
      else  
        Serial.println("Error Initializing MCP2515...");
  }else if(br == "50KBPS"){
      if(CAN0.begin(MCP_ANY, CAN_50KBPS, MCP_16MHZ) == CAN_OK)
        Serial.println("MCP2515 Initialized Successfully!");
      else  
        Serial.println("Error Initializing MCP2515...");
  }
  else if(br == "80KBPS"){
      if(CAN0.begin(MCP_ANY, CAN_80KBPS, MCP_16MHZ) == CAN_OK)
        Serial.println("MCP2515 Initialized Successfully!");
      else  
        Serial.println("Error Initializing MCP2515...");
  }else if(br == "100KBPS"){
      if(CAN0.begin(MCP_ANY, CAN_100KBPS, MCP_16MHZ) == CAN_OK)
        Serial.println("MCP2515 Initialized Successfully!");
      else  
        Serial.println("Error Initializing MCP2515...");
  }else if(br == "125KBPS"){
      if(CAN0.begin(MCP_ANY, CAN_125KBPS, MCP_16MHZ) == CAN_OK)
        Serial.println("MCP2515 Initialized Successfully!");
      else  
        Serial.println("Error Initializing MCP2515...");
  }else if(br == "200KBPS"){
      if(CAN0.begin(MCP_ANY, CAN_200KBPS, MCP_16MHZ) == CAN_OK)
        Serial.println("MCP2515 Initialized Successfully!");
      else  
        Serial.println("Error Initializing MCP2515...");
  }else if(br == "250KBPS"){
      if(CAN0.begin(MCP_ANY, CAN_250KBPS, MCP_16MHZ) == CAN_OK)
        Serial.println("MCP2515 Initialized Successfully!");
      else  
        Serial.println("Error Initializing MCP2515...");
  }else if(br == "500KBPS"){
      if(CAN0.begin(MCP_ANY, CAN_500KBPS, MCP_16MHZ) == CAN_OK)
        Serial.println("MCP2515 Initialized Successfully!");
      else  
        Serial.println("Error Initializing MCP2515...");
  }else if(br == "1000KBPS"){
      if(CAN0.begin(MCP_ANY, CAN_1000KBPS, MCP_16MHZ) == CAN_OK)
        Serial.println("MCP2515 Initialized Successfully!");
      else  
        Serial.println("Error Initializing MCP2515...");
  }
} 

/*********************************************************************************************************
  END FILE
*********************************************************************************************************/
