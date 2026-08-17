from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import asyncio
from src.ingest.db import get_recent

app = FastAPI()

@app.get("/history")
def history(channel: str, last: int):
    return get_recent(channel, last)

@app.get("/")
def home():
    return HTMLResponse("""
    <html>
      <body>
        <h1>Telemetry</h1>
        <canvas id="coolant_temp"></canvas>
        <canvas id="rpm"></canvas>
        <canvas id="throttle_pos"></canvas>

        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script>
          function makeChannel(channel) {
            const chart = new Chart(document.getElementById(channel), {
              type: 'line',
              data: {
                labels: [],
                datasets: [{ label: channel, data: [] }]
              }
            });

            // BACKFILL: fetch history first
            fetch("/history?channel=" + channel + "&last=300")
              .then(response => response.json())
              .then(rows => {
                for (const row of rows) {
                  chart.data.labels.push('');
                  chart.data.datasets[0].data.push(row[2]);
                }
                chart.update();
              });

            // LIVE: WebSocket takes over
            const ws = new WebSocket("ws://127.0.0.1:8000/ws/" + channel);
            ws.onmessage = (event) => {
              const value = Number(event.data);
              chart.data.labels.push(new Date().toLocaleTimeString());
              chart.data.datasets[0].data.push(value);
              chart.update();
            };
          }

          makeChannel('coolant_temp');
          makeChannel('rpm');
          makeChannel('throttle_pos');
        </script>
      </body>
    </html>
    """)

@app.websocket("/ws/{channel}")
async def websocket_endpoint(websocket: WebSocket, channel: str):
    await websocket.accept()
    try:
        while True:
            rows = get_recent(channel, 5)
            if rows:
                value = rows[-1][2]
                await websocket.send_text(str(value))
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        pass