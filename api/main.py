from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from routes import grammar_task

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

# if __name__ == '__main__':
#     uvicorn.run(app, host="0.0.0.0", port=8000)
