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
    servo_y.value = -0.85
    print("made connection!")
    count = 0
    while True:
        message = await websocket.recv()
        #print("a")
        print(len(message))
        floats = struct.unpack('4f', message)
        print("floats: ", floats)
                    
        value_x = floats[0]
        if value_x > 180:
            value_x -= 360
        value_x /= -90
        if value_x > 0.5:
            value_x = 0.5
        if value_x < -0.5:
            value_x = -0.5
            
        value_y = floats[1]
        if value_y > 180:
            value_y -= 360
        value_y /= -90
        if value_y > 0.5:
            value_y = 0.5
        if value_y < -0.5:
            value_y = -0.5
            
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
