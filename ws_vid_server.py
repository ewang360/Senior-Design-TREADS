import cv2
import time
import asyncio
from threading import Thread
import websockets

# declare global variables
# CV
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')
stream = cv2.VideoCapture(0)
count = 0
frames = 0
start = time.time()

# sender
sender_stopped = False
PORT = 5777
frame = None
rectangles = None

# getter
getter_stopped = False
grabbed = True

# sender functions
def sender_start():
    global send_thread
    send_thread = Thread(target=send, args=())
    send_thread.start()

def sender_stop():
    global sender_stopped
    sender_stopped = True

async def send(websocket):
    global frame
    global sender_stopped

    while not sender_stopped:
        # Draw the rectangle around each body
        if rectangles:
            for (x, y, w, h) in rectangles:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            img = cv2.resize(frame, (200,200))
            success, im_buf_arr = cv2.imencode(".jpg", img)
            byte_im = im_buf_arr.tobytes()
            await websocket.send(byte_im)
        if cv2.waitKey(1) == ord("q"):
            sender_stopped = True

async def async_init():
    async with websockets.serve(send(), "", PORT):
        await asyncio.Future()

# getter functions
def getter_start(): 
    global get_thread   
    get_thread = Thread(target=get, args=())
    get_thread.start()

def get():
    global grabbed
    global frame
    global getter_stopped

    while not getter_stopped:
        if not grabbed:
            getter_stop()
        else:
            (grabbed, frame) = stream.read()

def getter_stop():
    global getter_stopped
    getter_stopped = True

def handler():
    global grabbed
    global frame
    global stream
    global getter_stopped
    global sender_stopped
    global rectangles

    print("starting")
    (grabbed, frame) = stream.read()

    getter_start()
    sender_start()

    while True:
        # Computer Vision Section
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detect the bodies
        bodies = body_cascade.detectMultiScale(gray, 1.1, 4)

        rectangles = bodies

        if sender_stopped or getter_stopped:
            print("stopped")
            sender_stop()
            getter_stop()
            break

    stream.release()
    get_thread.join()
    send_thread.join()

async def main():
    async with websockets.serve(handler, "", PORT):
        await asyncio.Future()

asyncio.run(main())