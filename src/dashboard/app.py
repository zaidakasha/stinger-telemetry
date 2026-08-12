from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import asyncio
from src.ingest.db import get_recent

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

    while True:
        rows = get_recent('coolant_temp', 5)
        if rows:
            value = rows[-1][2]          # last row's value (index 2)
            await websocket.send_text(str(value))
        await asyncio.sleep(1)

    