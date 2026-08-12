from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import asyncio

app = FastAPI()

@app.get("/")
def home():
    return HTMLResponse("""
    <html>
      <body>
        <h1>Telemetry</h1>
        <div id="output"></div>
        <script>
          const ws = new WebSocket("ws://127.0.0.1:8000/ws");
          ws.onmessage = (event) => {
            document.getElementById("output").innerText = event.data;
          };
        </script>
      </body>
    </html>
    """)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    n = 0
    while True:
        await websocket.send_text(f"reading {n}")
        n += 1
        await asyncio.sleep(1)