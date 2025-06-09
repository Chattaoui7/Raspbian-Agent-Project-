import asyncio
import json
import websockets
import os

HOST = 'localhost'
PORT = 8765
SEND_INTERVAL = 2  
TEMP_PATH = "/sys/class/thermal/thermal_zone0/temp"

def read_cpu_temp():
    try:
        with open(TEMP_PATH, "r") as f:
            raw = f.read().strip()
            # Convert to Celsius
            temp_c = int(raw) / 1000.0
            return {"temperature_c": temp_c}
    except FileNotFoundError:
        return {"error": f"Temperature file not found at {TEMP_PATH}"}
    except Exception as e:
        return {"error": str(e)}

async def send_cpu_temperature(websocket, path):
    while True:
        temp_data = read_cpu_temp()
        await websocket.send(json.dumps(temp_data))
        await asyncio.sleep(SEND_INTERVAL)

async def main():
    async with websockets.serve(send_cpu_temperature, HOST, PORT):
        print(f"WebSocket server started at ws://{HOST}:{PORT}")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())

