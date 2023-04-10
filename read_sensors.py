import websockets
import time
import smbus2
import asyncio
import struct
import RPi.GPIO as GPIO

async def handler(websocket):
    print("made connection!")
    while True:
        time.sleep(0.5)
       
        data = i2cbus.read_i2c_block_data(address,0x71,1)
        isFound=GPIO.input(29)
        if (data[0] | 0x08) == 0:
           print('Initialization error')
            
        i2cbus.write_i2c_block_data(address,0xac,[0x33,0x00])
        time.sleep(0.1)
            
        data = i2cbus.read_i2c_block_data(address,0x71,7)
            
        Traw = ((data[3] & 0xf) << 16) + (data[4] << 8) + data[5]
        temperature = (200*float(Traw)/2**20 - 50)*(9/5)+ 32
        temp=round(temperature,2)
            
        Hraw = ((data[3] & 0xf0) >> 4) + (data[1] << 12) + (data[2] << 4)
        humidity = 100*float(Hraw)/2**20
        hum=round(humidity,2)
    
        await websocket.send(str(temp)+"+"+str(hum)+"+"+str(isFound))
        
async def main():
    async with websockets.serve(handler, "", PORT):
        await asyncio.Future()

PORT = 5779   
address = 0x38 #Put your device's address here
i2cbus = smbus2.SMBus(1)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(29,GPIO.IN)  

asyncio.run(main())
