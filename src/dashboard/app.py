from fastapi import FastAPI, WebSocket
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

          // BACKFILL: fetch history first, fill chart, then go live
          fetch("/history?channel=coolant_temp&last=300")
            .then(response => response.json())
            .then(rows => {
              console.log('history rows:', rows.length);
              for (const row of rows) {
                chart.data.labels.push('');
                chart.data.datasets[0].data.push(row[2]);
              }
              chart.update();
            });

          // LIVE: WebSocket takes over
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

    