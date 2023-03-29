#Include the library files
import websockets
import time
import asyncio
import struct
from gpiozero import Servo
from time import sleep

from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()

async def handler(websocket):
    
    servo_x = Servo(20, min_pulse_width=0.4/1000,   max_pulse_width=2.325/1000, pin_factory=factory)
    servo_y = Servo(21, min_pulse_width=0.4/1000, max_pulse_width=2.325/1000, pin_factory=factory)
    servo_y
    print("made connection!")
    count = 0
    while True:
        message = await websocket.recv()
        #print("a")
        print(len(message))
        floats = struct.unpack('4f', message)
        print("floats: ", floats)
        
        #Moving head right
        if(floats[0] <= 360.0 and floats[0] >= 270.0):
            value_x = ((floats[0]-360) / (270-360))

        #Moving head left
        if(floats[0] >= 0 and floats[1] <= 90):
            value_x = ((floats[1]-0) / (90-0)) * (0-(-1)) + (-1)
        
        #Moving head up
        if(floats[1] <= 360 and floats[0] >= 270):
            value_y = ((floats[0]-360) / (270-360)*-1) * (1-0) + 0

        #Moving head down
        if(floats[1] >= 0 and floats[0] <= 90):
            value_y = ((floats[0]-0) / (90-0)) * (0-(-1)) + (-1)
            
        #marks change
        value_x = floats[0]
        if value_x > 180:
            value_x -= 360
        value_x /= -90
        
        value_y = floats[1]
        if value_y > 180:
            value_y -= 360
        value_y /= -90
            
        print("x",value_x)
        print("y",value_y)
        servo_x.value = value_x
        servo_y.value = value_y
        sleep(0.005)
        
async def main():
    async with websockets.serve(handler, "", PORT):
        await asyncio.Future()

PORT = 5777

asyncio.run(main())
