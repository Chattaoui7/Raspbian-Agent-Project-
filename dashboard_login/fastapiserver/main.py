from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosed
import uvicorn
import asyncio
import cv2
from threading import Thread
import time

from detection_model import Detection_RGB_model, Detection_Termel_model

# ---------- Threaded Video Stream ----------
class CameraStream:
    def __init__(self, src):
        self.src = src
        self.cap = None
        self.ret = False
        self.frame = None
        self.running = True
        self.thread = Thread(target=self._update, daemon=True)
        self.thread.start()

    def _connect(self):
        while self.running:
            self.cap = cv2.VideoCapture(self.src)
            if self.cap.isOpened():
                print(f"Connected to {self.src}")
                return
            print(f"Failed to open {self.src}, retrying in 1s...")
            time.sleep(1)

    def _update(self):
        self._connect()
        while self.running:
            if not self.cap or not self.cap.isOpened():
                self._connect()
            self.ret, self.frame = self.cap.read()
            if not self.ret:
                print(f"Frame failed from {self.src}, reconnecting...")
                if self.cap:
                    self.cap.release()
                self._connect()
            time.sleep(0.01)

    def read(self):
        return self.ret, self.frame

    def release(self):
        self.running = False
        self.thread.join()
        if self.cap:
            self.cap.release()

# ------------------------------------------------------------

app = FastAPI()

model_RGB = Detection_RGB_model()
model_Thermal = Detection_Termel_model()

# Shared camera streams
rgb_stream = CameraStream("http://192.168.1.102:8160")
thermal_stream = CameraStream("./videoThermal.mp4")

# ------------------- WebSocket Routes -----------------------

@app.websocket("/web")  # RGB stream
async def stream_rgb(websocket: WebSocket):
    await websocket.accept()
    print("RGB client connected")
    try:
        while True:
            success, frame = rgb_stream.read()
            if not success or frame is None:
                await asyncio.sleep(1)
                continue

            frame = cv2.resize(frame, (840, 580))
            frame = model_RGB.run(frame)

            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                await asyncio.sleep(0.01)
                continue

            await websocket.send_bytes(buffer.tobytes())
            await asyncio.sleep(0.01)

    except (WebSocketDisconnect, ConnectionClosed):
        print("RGB client disconnected")

@app.websocket("/web1")  # Thermal stream
async def stream_thermal(websocket: WebSocket):
    await websocket.accept()
    print("Thermal client connected")
    try:
        while True:
            success, frame = thermal_stream.read()
            if not success or frame is None:
                await asyncio.sleep(1)
                continue

            frame = cv2.resize(frame, (840, 580))
            frame = model_Thermal.run(frame)

            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                await asyncio.sleep(0.01)
                continue

            await websocket.send_bytes(buffer.tobytes())
            await asyncio.sleep(0.01)

    except (WebSocketDisconnect, ConnectionClosed):
        print("Thermal client disconnected")

# ------------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

