import cv2
import time

# ------------------------------------------------------------------------------
# automaticdai
# YF Robotics Labrotary
# Instagram: yfrobotics
# Twitter: @yfrobotics
# Website: https://www.yfrl.org
# ------------------------------------------------------------------------------
# Reference: 
# - https://towardsdatascience.com/face-detection-in-2-minutes-using-opencv-python-90f89d7c0f81
# ------------------------------------------------------------------------------

# Load the cascade
#face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')

# To capture video from webcam. 
cap = cv2.VideoCapture(0)
# To use a video file as input 
# cap = cv2.VideoCapture('filename.mp4')

count = 0
frames = 0

start = time.time()

while True:
    # Read the frame
    _, img = cap.read()
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect the bodies
    bodies = body_cascade.detectMultiScale(gray, 1.1, 4)
    # Draw the rectangle around each body
    for (x, y, w, h) in bodies:
        path = "output/img" + str(count) + ".jpg"
        cv2.imwrite(path, img[y:y+h,x:x+w])
        count += 1
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    # Display
    cv2.imshow('img', img)
    frames += 1
    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break

end = time.time()
seconds = end - start
print(frames)
print("fps: ", str(frames/seconds))

# Release the VideoCapture object
cap.release()
