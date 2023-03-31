import cv2
import time
import asyncio
from threading import Thread
import websockets

# declare global variables
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')
stream = cv2.VideoCapture(0)
count = 0
frames = 0
start = time.time()

# cv
cv_stopped = False
PORT = 5787
frame = None
rectangles = None

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
    
    print("starting")
    (grabbed, frame) = stream.read()

    while True:
        if grabbed:
            # Computer Vision Section
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Detect the bodies
            rectangles = body_cascade.detectMultiScale(gray, 1.1, 4)
            
async def handler(websocket):
    global grabbed
    global frame
    global stream
    global getter_stopped
    global cv_stopped
    global rectangles

    while not cv_stopped:
        # Draw the rectangle around each body
        for (x, y, w, h) in rectangles:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        #img = cv2.resize(frame, (200,200))
        img = frame
        success, im_buf_arr = cv2.imencode(".jpg", img)
        byte_im = im_buf_arr.tobytes()
        await websocket.send(byte_im)
        if cv2.waitKey(1) == ord("q"):
            cv_stopped = True

async def main():
    async with websockets.serve(handler, "", PORT):
        await asyncio.Future()

getter_start()
cv_start()
asyncio.run(main())

stream.release()
get_thread.join()
send_thread.join()
