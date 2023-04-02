import cv2
import time
from threading import Thread
from cps import CountsPerSec

# declare global variables
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')
stream = cv2.VideoCapture(0)
            
def main():
    cps = CountsPerSec().start()

    while True:
        (grabbed, frame) = stream.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detect the bodies
        rectangles = body_cascade.detectMultiScale(gray, 1.1, 4)
        # Draw the rectangle around each body
        if rectangles is not None:
            for (x, y, w, h) in rectangles:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        if frame is not None:
            cv2.putText(frame, "{:.0f} iterations/sec".format(cps.countsPerSec()), (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
            cv2.imshow("img",frame)
            cps.increment()
        if cv2.waitKey(1) == ord("q") or not grabbed:
            break

main()
stream.release()