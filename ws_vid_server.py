import cv2
import time
import asyncio
from threading import Thread
import websockets
import RPi.GPIO as GPIO

# declare global variables
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
stream = cv2.VideoCapture(0)

# cv
cv_stopped = False
PORT = 5788
frame = None
rectangles = None
weights = None

# getter
getter_stopped = False
grabbed = True

# sender functions
def cv_start():
    global cv_thread
    cv_thread = Thread(target=cv, args=())
    cv_thread.start()

def cv_stop():
    global cv_stopped
    cv_stopped = True

# getter functions
def getter_start(): 
    global get_thread   
    get_thread = Thread(target=get, args=())
    get_thread.start()

def getter_stop():
    global getter_stopped
    getter_stopped = True
    
def get():
    global grabbed
    global frame
    global getter_stopped

    while not getter_stopped:
        if not grabbed:
            getter_stop()
        else:
            (grabbed, frame) = stream.read()

def cv():
    global rectangles
    global grabbed
    global frame
    global weights
    
    print("starting")
    (grabbed, frame) = stream.read()

    while True:
        if grabbed:
            # Computer Vision Section
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.rotate(gray, cv2.ROTATE_90_COUNTERCLOCKWISE)
            # Detect the bodies
            rectangles, weights = hog.detectMultiScale(gray, padding=(4, 4), scale=1.02)
            
async def handler(websocket):
    global grabbed
    global frame
    global stream
    global getter_stopped
    global cv_stopped
    global rectangles

    while not cv_stopped:
        # Draw rectangles around detected bodies
        conf = weights
        rects = rectangles
        found = False
        if rects is not None:
            for i, (x, y, w, h) in enumerate(rects):
                if conf[i] > 0.7:
                    img = frame
                    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(img, str(round(conf[i],2)), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
                    frame = img
                    found = True
                    
        GPIO.output(29,found)
                    
        # transmit image
        img = cv2.resize(frame, (200,200))
        success, im_buf_arr = cv2.imencode(".jpg", frame)
        byte_im = im_buf_arr.tobytes()
        await websocket.send(byte_im)
        time.sleep(0.05)
        
async def main():
    async with websockets.serve(handler, "", PORT):
        await asyncio.Future()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(29,GPIO.OUT)

getter_start()
cv_start()
asyncio.run(main())

stream.release()
get_thread.join()
cv_thread.join()
