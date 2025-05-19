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

# Load YOLOv8 model
model = YOLO(r'C:\Users\admin\Desktop\Raspbian-Agent-Project-\server\yolov8n.pt')

# Threaded camera stream
camera = CameraStream("http://192.168.42.132:8160")

while True:
    success, frame = camera.read()
    if not success:
        continue

    # Resize for faster inference (optional)
    frame = cv2.resize(frame, (640, 480))

    # Run YOLO detection
    results = model.predict(frame, imgsz=480, conf=0.5, verbose=False)

    # Draw results
    annotated = results[0].plot()

    # Display frame
    cv2.imshow("YOLO Stream", annotated)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
