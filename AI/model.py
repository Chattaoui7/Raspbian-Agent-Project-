from ultralytics import YOLO
import cv2

# Load the trained model

trained_model_path = r"C:\Users\admin\Desktop\Raspbian-Agent-Project-\AI\detect\yolov8n_v8_50e\weights\best.pt"
# Load the model

model = YOLO(trained_model_path)

# Perform inference on an image   

# Initialize webcam (0 = default camera)
#cap = cv2.VideoCapture(0)

image = cv2.imread(r"C:\Users\admin\Desktop\Raspbian-Agent-Project-\AI\data\input\istockphoto-1955739359-612x612.jpg")

while True:
#    ret, frame = cap.read()
#    if not ret:
#        break

    # Inference
    #results = model(frame)
    results = model(image)

    # Plot results
    annotated_frame = results[0].plot()

    # Show frame
    cv2.imshow("YOLOv8 Real-Time Detection", annotated_frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#cap.release()
cv2.destroyAllWindows()