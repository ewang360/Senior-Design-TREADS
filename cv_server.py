import cv2
import time
import socket

body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')
cap = cv2.VideoCapture(0)
count = 0
frames = 0
start = time.time()
HOST = "192.168.2.3"
PORT = 5778  # Port to listen on (non-privileged ports are > 1023)

hexstring = bytearray(bytes.fromhex("F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0"))
step = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("connecting...")
    conn, addr = s.accept()
    with conn:
        while True:
            # Read the frame
            _, img = cap.read()
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Detect the bodies
            bodies = body_cascade.detectMultiScale(gray, 1.1, 4)
            # Draw the rectangle around each body
            for (x, y, w, h) in bodies:
                #path = "output/img" + str(count) + ".jpg"
                #cv2.imwrite(path, img[y:y+h,x:x+w])
                count += 1
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            imgr = cv2.cvtColor(cv2.resize(img, (100,100)),cv2.COLOR_BGR2GRAY)
            success, im_buf_arr = cv2.imencode(".jpg", imgr)
            byte_im = im_buf_arr.tobytes()
            size = len(byte_im)
            size_message = size.to_bytes(4, "little")
            print("send: ", size_message, size)
            #conn.send(hexstring)
            conn.send(size_message)
            curr = 0
            size_remaining = size
            while size_remaining > 0:
                step_target = min(size, curr + step)
                #print(curr, step_target, size, size_remaining)
                conn.send(byte_im[curr:step_target])
                size_remaining -= step
                curr += step
            frames += 1
            # # Stop if escape key is pressed
            k = cv2.waitKey(30) & 0xff
            if k==27:
                break

end = time.time()
seconds = end - start
print(frames)
print("fps: ", str(frames/seconds))

# Release the VideoCapture object
cap.release()
