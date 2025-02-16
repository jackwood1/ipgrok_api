import logging
import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import file_details, benefits_compare, ip_tools

log_file_path = os.getenv("LOG_FILE_PATH", "app.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_file_path)
    ]
)
logger = logging.getLogger(os.getenv("SERVICE_NAME", "FileCompareService"))

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("File Compare Service application started")
    yield
    logger.info("File Compare Service application shutting down")

app = FastAPI(lifespan=lifespan, title="Customer Service")

app.include_router(file_details.router)
app.include_router(benefits_compare.router)

app.include_router(ip_tools.router)

@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {"message": "You found me"}

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "localhost")
    port = int(os.getenv("PORT", 5008))
    logger.info(f"Starting server at {host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=True)