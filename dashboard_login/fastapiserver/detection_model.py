# Detection_model.py
import cv2
from ultralytics import YOLO
from threading import Thread

class CameraStream:
    def __init__(self, src):
        self.cap = cv2.VideoCapture(src)
        if not self.cap.isOpened():
            raise Exception("Failed to open stream.")
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

class Detection_RGB_model:
    def __init__(self, model_path='./yolov8n.pt'):
        # Load YOLO model (change path if needed)
        self.model = YOLO(model_path)
        # Load the model
    def run(self, frame):
        results = self.model.predict(frame, imgsz=640, conf=0.5)
        annotated_frame = results[0].plot()  # Draw detections on the frame
        return annotated_frame

class Detection_Termel_model : 

    def __init__(self, model_path=r'./best.pt'):
        # Load YOLO model (change path if needed)
        self.model = YOLO(model_path)
        # Load the model
    def run(self, frame):
        results = self.model.predict(frame, imgsz=640, conf=0.5)
        annotated_frame = results[0].plot()  # Draw detections on the frame
        return annotated_frame
