# Python Spyware

## Overview

A simple client-server RAT (Remote Access Tool) written in Python. The client connects to the server, executes remote shell commands, and can stream live webcam video.

## Structure

```
.
├── client.py   # Runs on the target: executes commands, streams webcam
├── server.py   # Operator side: sends commands, receives and displays video
```

## Requirements

- Python 3.6+
- opencv-python
- numpy

```bash
pip install opencv-python numpy
```

## Usage

Start the server first:

```bash
python server.py
```

Then run the client on the target machine:

```bash
python client.py
```

The client connects to `127.0.0.1:4000` and sends its OS and working directory.

## Commands

| Command | Description |
|---------|-------------|
| `start` | Starts webcam stream, saves to `output.mp4` |
| `exit`  | Terminates the client |
| anything else | Executes as a shell command, returns output |

Press `Ctrl+C` on the server to stop and save the video file.

## Notes

- All data is transmitted unencrypted over TCP.
- Single client only — no multi-connection support.
- Video is streamed as JPEG frames.
