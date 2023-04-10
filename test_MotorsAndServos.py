import websockets
import time
import asyncio
import struct
import RPi.GPIO as GPIO
from gpiozero import Servo
from time import sleep

from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()

async def handler(websocket):
    print("made connection!")
    
    servo_x = Servo(20, min_pulse_width=0.4/1000,   max_pulse_width=2.325/1000, pin_factory=factory)
    servo_y = Servo(21, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)
    servo_y.value = -0.25
    
    while True:
        message = await websocket.recv()
        #print(len(message))
        floats = struct.unpack('4f', message) 
        #print("floats: ", floats)
        
        ### Servos Controls ###
        value_x = floats[0]
        if value_x > 180:
            value_x -= 360
        value_x /= -90
        if value_x > 0.5:
            value_x = 0.5
        if value_x < -0.3:
            value_x = -0.3
            
        value_y = floats[1]
        if value_y > 180:
            value_y -= 360
        value_y /= -90
        if value_y > 1:
            value_y = 1
        if value_y < -1:
            value_y = -1
            
        #print("x",value_x)
        #print("y",value_y)
        servo_x.value = value_x-.5
        servo_y.value = value_y
        sleep(0.005)
        
        
            ######Motor Controls ##########
            
        # both motors backwards (forwards)
        if (floats[2]>=-0.25 and floats[2]<=0.25) and (floats[3]>=0.75):
            GPIO.output(7,False) # M1
            GPIO.output(11,True) # E1

            GPIO.output(13,False) # M2
            GPIO.output(15,True) # E2
            # both motors forwards (backwards)
        elif (floats[2]>=-0.25 and floats[2]<=0.25) and (floats[3]<=-0.75):
                GPIO.output(7,True)
                GPIO.output(11,True)

                GPIO.output(13,True)
                GPIO.output(15,True)
        # right forwards, left backwards (turning left)
        elif (floats[2]<=-0.75) and (floats[3]>=-0.25 and floats[3]<=0.25):
            GPIO.output(7,False)
            GPIO.output(11,True)

            GPIO.output(13,True)
            GPIO.output(15,False)
        # right backwards, left forwards (turning right)
        elif (floats[2]>=0.75) and (floats[3]>=-0.25 and floats[3]<=0.25):
            GPIO.output(7,True)
            GPIO.output(11,False)

            GPIO.output(13,False)
            GPIO.output(15,True)
        # stop motors
        elif floats[2]==0 and floats[3]==0:
            GPIO.output(7,False)
            GPIO.output(11,False)

            GPIO.output(13,False)
            GPIO.output(15,False)


async def main():
    async with websockets.serve(handler, "", PORT):
        await asyncio.Future()


PORT = 5777
# set GPIO numbering mode and define output pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)      # motor A (right)    -> forwards    (M1)
GPIO.setup(11,GPIO.OUT)     # motor A (left)     -> backwards   (E1)
GPIO.setup(13,GPIO.OUT)     # motor B  (right)   -> forwards    (M2)
GPIO.setup(15,GPIO.OUT)     # motor B  (left)    -> backwards   (E2)

asyncio.run(main())

    

