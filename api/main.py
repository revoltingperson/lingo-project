from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from settings import DEBUG
from routes import grammar_task
from my_log.log_conf import CONFIG_PROD, DEBUG_CONF
from logging.config import dictConfig

app = FastAPI()

parent_r = APIRouter(prefix='/api')
parent_r.include_router(grammar_task.router)

app.include_router(parent_r)

origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

if not DEBUG:
    dictConfig(CONFIG_PROD)
else:
    dictConfig(DEBUG_CONF)


if DEBUG:
    if __name__ == '__main__':
        uvicorn.run(app, host="0.0.0.0", port=8000)
