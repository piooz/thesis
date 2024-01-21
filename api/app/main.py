from datetime import datetime
import logging
from typing import BinaryIO
from uuid import uuid4
from fastapi import FastAPI, UploadFile
from pandas import DataFrame
from statsmodels.iolib.table import csv
from .. import algorithm as al
from .api_model_lib import *
from motor.motor_asyncio import AsyncIOMotorClient
import statsmodels as sm
from fastapi.middleware.cors import CORSMiddleware
import csv
import codecs

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

mongo_client = AsyncIOMotorClient()


def prepare_data(result, effect: list[float], data: list[float]) -> list[Foo]:
    ls = []
    for i in range(len(data)):

        foo = Foo(
            index=i,
            origin=data[i],
            effect=effect[i],
            result=data[i] - effect[i],
            AO=None,
            LS=None,
            TC=None,
            IO=None,
        )
        if i in result.index:
            type = result.loc[i, 'type']
            match type:
                case 'IO':
                    foo.IO = foo.origin
                case 'AO':
                    foo.AO = foo.origin
                case 'TC':
                    foo.TC = foo.origin
                case 'LS':
                    foo.LS = foo.origin

        ls.append(foo)
    return ls


def prepare_raport(time, fit, stage1stats: DataFrame) -> Raport:
    ls = []
    for i, row in stage1stats.iterrows():
        ls.append(
            Stats(
                index=i,
                IOcoef=row['IOcoef'],
                IOtstat=row['IOtstat'],
                LScoef=row['LScoef'],
                LStstat=row['LStstat'],
                TCcoef=row['TCcoef'],
                TCtstat=row['TCtstat'],
                AOcoef=row['AOcoef'],
                AOtstat=row['AOtstat'],
            )
        )

    f = Fit(type='Arima Model', arparams=fit.arparams, maparams=fit.maparams)
    raport = Raport(executionTime=time, fit=f, stats=ls)
    return raport


def read_first_column_binary(file: BinaryIO):
    csvReader = csv.reader(codecs.iterdecode(file, 'utf-8'))
    data = []
    for row in csvReader:
        logging.debug(row)
        data.append(float(row[0]))
    return data


@app.post('/test/')
async def test(file: UploadFile = None, cval: float = 2) -> AnalyzeResult:
    # data = read_first_column_binary(file.file)
    data = sm.datasets.nile.data.load_pandas().data['volume']

    (result, effect, fit, stage1stats) = al.chen_liu(data, cval)
    logging.debug(stage1stats)
    a = AnalyzeResult(
        id=uuid4(),
        time=datetime.now(),
        data=prepare_data(result, effect.tolist(), data),
        raport=prepare_raport(123, fit, stage1stats),
    )

    return a


@app.post('/upload_file/')
async def upload_file(file: UploadFile):
    return {'Hello': 'World'}
