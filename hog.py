import cv2
import time
from threading import Thread
from cps import CountsPerSec

# declare global variables
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
stream = cv2.VideoCapture(0)
            
def main():
    cps = CountsPerSec().start()

    while True:
        (grabbed, image) = stream.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Detect the bodies
        rects, weights = hog.detectMultiScale(gray, padding=(4, 4), scale=1.02)
        # Draw the rectangle around each body
        for i, (x, y, w, h) in enumerate(rects):
            if weights[i] < 0.13:
                continue
            elif weights[i] < 0.3 and weights[i] > 0.13:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
            if weights[i] < 0.7 and weights[i] > 0.3:
                cv2.rectangle(image, (x, y), (x+w, y+h), (50, 122, 255), 2)
            if weights[i] > 0.7:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.putText(image, 'High confidence', (10, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(image, 'Moderate confidence', (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (50, 122, 255), 2)
        cv2.putText(image, 'Low confidence', (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        if image is not None:
            cv2.putText(image, "{:.0f} iterations/sec".format(cps.countsPerSec()), (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
            cv2.imshow("img",image)
            cps.increment()
        if cv2.waitKey(1) == ord("q") or not grabbed:
            break

main()
stream.release()