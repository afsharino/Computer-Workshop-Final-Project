# Import Libraries
import uvicorn
from fastapi import FastAPI


app = FastAPI()

@app.get('/')
async def root():
    return {'message' : 'HI Welcome to RestAPI'}