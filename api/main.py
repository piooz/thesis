from datetime import datetime
import logging
from uuid import uuid4
from fastapi import FastAPI, UploadFile
import algorithm as al
from .api_model_lib import *
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

mongo_client = AsyncIOMotorClient()


@app.get('/test/')
async def test() -> AnalyzeResult:
    data = [1.0, 1, 1, 1, 1, 1, 1]
    (result, effect, fit, stage1stats) = al.chen_liu(data, 3.5)
    logging.debug(result)
    output = AnalyzeResult(
        id=uuid4(),
        data=data,
        time=datetime.now(),
        effect=effect.tolist(),
        result=[],
        fit=Fit(type='test', arparams=[], maparams=[]),
    )

    return output


@app.post('/upload_file/')
async def upload_file(file: UploadFile):
    return {'Hello': 'World'}


@app.get('/upload_file/')
async def get_effect(file: UploadFile):
    return {'Hello': 'World'}
