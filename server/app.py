from fastapi import FastAPI , WebSocket , Request , WebSocketDisconnect
from websockets.exceptions import ConnectionClosed
from fastapi.templating import Jinja2Templates
import uvicorn
import asyncio
import cv2
from ultralytics import YOLO

# Install Fastapi, websockets, Jinja2
app = FastAPI()
camera = cv2.VideoCapture(0) #0 for default camera

temp = Jinja2Templates(directory="temp")

@app.get('/')
def index(request: Request):
    return temp.TemplateResponse("dashboard.html", {"request": request})


@app.websocket("/web")
async def get_stream(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:

                model = YOLO("yolov8n.pt")
                result = model.predict(frame , device =[0] )

                frame = result[0].plot()
                cv2.rectangle(frame,(10,5),(40,300),(255,0,0),2)

                ret, buffer = cv2.imencode('.jpg', frame)
                await websocket.send_text("WEB CAM PHAM XUAN KY")
                await websocket.send_bytes(buffer.tobytes())
            await asyncio.sleep(0.03)
    except (WebSocketDisconnect, ConnectionClosed):
        print("Client disconnected")


if __name__ == '__main__':
    
    uvicorn.run(app, host='0.0.0.0', port=8000)