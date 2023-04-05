import cv2
from threading import Thread
from cps import CountsPerSec

# declare global variables
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
stream = cv2.VideoCapture(0)

# cv
cv_stopped = False
frame = None
rectangles = None
weights = None

# getter
getter_stopped = False
grabbed = True

# sender functionss
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
            # print(grabbed)

def cv():
    global rectangles
    global grabbed
    global frame
    global weights

    while not cv_stopped:
        if grabbed and frame is not None:
            # Computer Vision Section
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.rotate(gray, cv2.ROTATE_90_COUNTERCLOCKWISE)
            # Detect the bodies
            rectangles, weights = hog.detectMultiScale(gray, padding=(4, 4), scale=1.02)

def handler():
    global grabbed
    global frame
    global stream
    global getter_stopped
    global cv_stopped
    global rectangles

    cps = CountsPerSec().start()

    while not cv_stopped:
        # Draw rectangles around detected bodies
        conf = weights
        rects = rectangles
        if rects is not None:
            for i, (x, y, w, h) in enumerate(rects):
                if conf[i] > 0.7:
                    #cv2.rectangle(frame, (frame.shape[1]-y, x), (frame.shape[1]-y-h, x+w), (0, 255, 0), 2)
                    img = frame
                    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(img, str(round(conf[i],2)), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
                    frame = img
        #img = cv2.resize(frame, (200,200))
        if frame is not None:
            cv2.putText(frame, "{:.0f} iterations/sec".format(cps.countsPerSec()), (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
            cv2.imshow("img",frame)
            cps.increment()
        if cv2.waitKey(1) == ord("q"):
            cv_stop()
            getter_stop()

getter_start()
cv_start()

handler()

stream.release()
get_thread.join()
cv_thread.join()
