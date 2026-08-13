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
        <canvas id="chart"></canvas>

        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script>
          const ctx = document.getElementById("chart");
          const chart = new Chart(ctx, {
            type: 'line',
            data: {
              labels: [],
              datasets: [{ label: 'coolant', data: [] }]
            }
          });

          const ws = new WebSocket("ws://127.0.0.1:8000/ws");
          ws.onmessage = (event) => {
            const value = Number(event.data);

            chart.data.labels.push(new Date().toLocaleTimeString());
            chart.data.datasets[0].data.push(value);
            chart.update();

              if (value > 95) {
                  document.body.style.background = 'red';
              } else {
                  document.body.style.background = 'white';
              }
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
            value = rows[-1][2]          
            await websocket.send_text(str(value))
        await asyncio.sleep(1)

    