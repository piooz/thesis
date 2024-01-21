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

# import statsmodels as sm
from fastapi.middleware.cors import CORSMiddleware
import csv
import codecs
import time

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


def read_column_binary(file: BinaryIO, have_header: bool, col: int):
    csv_reader = csv.reader(codecs.iterdecode(file, 'utf-8'))
    data = []
    if have_header:
        next(csv_reader)

    for row in csv_reader:
        logging.debug(row)
        if col < len(row):
            data.append(float(row[col]))
        else:
            logging.warning(f'Row {row} does not have column {col}. Skipping.')

    return data


@app.post('/test/')
async def test(
    file: UploadFile = None,
    cval: float = 2,
    have_header: bool = False,
    col: int = 0,
) -> AnalyzeResult:
    data = read_column_binary(file.file, have_header, col)

    start_time = time.time()
    (result, effect, fit, stage1stats) = al.chen_liu(data, cval)
    execution_time = time.time() - start_time
    logging.debug(stage1stats)
    a = AnalyzeResult(
        id=uuid4(),
        time=datetime.now(),
        data=prepare_data(result, effect.tolist(), data),
        raport=prepare_raport(execution_time, fit, stage1stats),
    )

    return a


@app.post('/upload_file/')
async def upload_file(file: UploadFile):
    return {'Hello': 'World'}
