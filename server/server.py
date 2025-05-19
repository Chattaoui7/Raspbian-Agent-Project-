from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from websockets.exceptions import ConnectionClosed
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import asyncio
import cv2
from threading import Thread

from detection_model import Detection_RGB_model, Detection_Termel_model  # Your custom class

#src = "http://192.168.1.102:8160"
# ---------- Threaded Video Stream for Lower Latency ----------
class CameraStream:
    def __init__(self, src):
        self.cap = cv2.VideoCapture(src)
        if not self.cap.isOpened():
            raise Exception("Failed to open video stream.")
        self.ret, self.frame = self.cap.read()
        self.running = True
        self.thread = Thread(target=self.update, daemon=True)
        self.thread.start()

    def update(self):
        while self.running:
            self.ret, self.frame = self.cap.read()

    def read(self):
        return self.ret, self.frame

    def release(self):
        self.running = False
        self.thread.join()
        self.cap.release()

# ------------------------------------------------------------

app = FastAPI()
model_RGB= Detection_RGB_model()
model_Thermal = Detection_Termel_model()

camera = CameraStream("http://192.168.1.102:8160")  # Or 0 for local webcam
cap = CameraStream(r"./videoThermal.mp4") #video thermal

templates = Jinja2Templates(directory="./temp")

@app.websocket("/web")
async def get_stream(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            success, frame = camera.read()
            if not success:
                continue

            # Resize frame to reduce latency
            frame = cv2.resize(frame, (840, 580))

            # Run detection
            frame = model_RGB.run(frame)

            # Optional: draw overlay
            #cv2.rectangle(frame, (10, 5), (40, 300), (255, 0, 0), 2)

            # Encode as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue

            # Send frame to frontend
            #await websocket.send_text("Live detection stream")
            await websocket.send_bytes(buffer.tobytes())

            # Small sleep to avoid overloading
            await asyncio.sleep(0.01)
    except (WebSocketDisconnect, ConnectionClosed):
        print("Client disconnected")

@app.websocket("/web1")
async def get_stream(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            success, frame = cap.read()
            if not success:
                continue

            # Resize frame to reduce latency
            frame = cv2.resize(frame, (840, 580))

            # Run detection
            frame = model_Thermal.run(frame)

            # Optional: draw overlay
            #cv2.rectangle(frame, (10, 5), (40, 300), (255, 0, 0), 2)

            # Encode as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue

            # Send frame to frontend
            #await websocket.send_text("Live detection stream")
            await websocket.send_bytes(buffer.tobytes())

            # Small sleep to avoid overloading
            await asyncio.sleep(0.01)
    except (WebSocketDisconnect, ConnectionClosed):
        print("Client disconnected")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
