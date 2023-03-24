import websockets
import cv2
import time
import asyncio

async def handler(websocket):
    print("made connection!")
    count = 0
    while True:
        if count%10 == 0:
            _, img = cap.read()
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Detect the bodies
            bodies = body_cascade.detectMultiScale(gray, 1.1, 4)
        else:
            _, img = cap.read()

        count += 1
        # Draw the rectangle around each body
        for (x, y, w, h) in bodies:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        imgr = cv2.cvtColor(cv2.resize(img, (200,200)),cv2.COLOR_BGR2GRAY)
        success, im_buf_arr = cv2.imencode(".jpg", imgr)
        byte_im = im_buf_arr.tobytes()
        print("send image, size: ", len(byte_im))
        await websocket.send(byte_im)

async def main():
    async with websockets.serve(handler, "", PORT):
        await asyncio.Future()


PORT = 5777

#cv init
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')
cap = cv2.VideoCapture(0)
count = 0
frames = 0
start = time.time()

asyncio.run(main())


