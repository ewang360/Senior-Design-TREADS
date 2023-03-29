import websockets
import time
import asyncio
import struct
import RPi.GPIO as GPIO

async def handler(websocket):
    print("made connection!")
    count = 0
    while True:
        message = await websocket.recv()
        print(len(message))
        floats = struct.unpack('4f', message) 
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

print("hi")
asyncio.run(main())
print("there")
    

