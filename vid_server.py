import socket
import cv2
import time

print("vidcap..")
vidcap = cv2.VideoCapture(0)
print("capture on")

#HOST = "192.168.0.239"  # Standard loopback interface address (localhost)
#HOST = "192.168.0.240"  # Standard loopback interface address (localhost)
HOST = "192.168.2.3"
PORT = 5777  # Port to listen on (non-privileged ports are > 1023)

hexstring = bytearray(bytes.fromhex("F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0"))
step = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("connecting...")
    conn, addr = s.accept()
    with conn:
        while True:
            success,image_ = vidcap.read()
            image = cv2.resize(image_, (100,100), interpolation = cv2.INTER_AREA)
            print(image.shape)
            success, im_buf_arr = cv2.imencode(".jpg", image)
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
