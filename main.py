from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import logging
import dspy
from core import modules, framework, data

# Setup logger
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Prepare data, setup DSPy and initiate RAG
docs, ids = data.prepare_data()
framework.setup(docs, ids)
rag = modules.RAG()

# Setup FastAPI
app = FastAPI()
app.mount("/public", StaticFiles(directory="public"), name="public")

# Setup websocket
@app.websocket("/bot")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            raw_query = await websocket.receive_text()
            response = rag(raw_query)
            await websocket.send_text(response.answer)
    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error("An unexpected exception occurred", exc_info=True)
        await websocket.send_text("Some error occurred on the server, try reloading")
        await websocket.close()

# Setup web app
@app.get("/")
async def main():
    return FileResponse('public/app.html')
