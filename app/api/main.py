from datetime import datetime
import logging
from typing import BinaryIO, List
from uuid import uuid4
from chenLiu import effects
from fastapi import FastAPI, Request, Response, UploadFile
from pandas import DataFrame
from statsmodels.iolib.table import csv
import pickle

# from .. import algorithm as al
from chenLiu.chenLiu import chen_liu as cl

from .cache import RedisCache
from .api_model_lib import *

from fastapi.middleware.cors import CORSMiddleware
import csv
import codecs
import time

app = FastAPI()
redisService: RedisCache = RedisCache()


def calc_request_hash(request: Request):
    path_params = tuple(sorted(request.path_params.items()))
    query_params = tuple(sorted(request.query_params.items()))
    key = hash((request.url._url, path_params, query_params))
    return key


def cache_request(cache_service: RedisCache, request: Request, response_body):
    key = calc_request_hash(request)
    try:
        cache_service.push(str(key), pickle.dumps(response_body))
    except Exception as e:
        logging.warning(f'Failed to push key {key} to cache database')
        logging.warning(e)


def check_cache(cache_service: RedisCache, request: Request):
    key = calc_request_hash(request)
    try:
        response_body = pickle.loads(cache_service.read(key))
        logging.info(response_body)
        return response_body
    except Exception as e:
        logging.warning(f'Failed to read key: {key} from cache service')
        logging.warning(e)
        return None


# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


def prepare_data(
    result, effect: list[float], data: list[float]
) -> list[Entry]:
    ls = []
    for i in range(len(data)):

        foo = Entry(
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


def prepare_raport(time, fit) -> Raport:
    f = Fit(type='Arima Model', arparams=fit.arparams, maparams=fit.maparams)
    raport = Raport(executionTime=time, fit=f)
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


@app.post('/analyze/')
async def analyze_file(
    file: UploadFile,
    cval: float = 2,
    have_header: bool = False,
    col: int = 0,
):
    data = read_column_binary(file.file, have_header, col)
    return file


@app.get('/ao_effect/')
async def generate_ao(
    len: int, start_point: int, w: float, request: Request
) -> list[float]:

    cache = check_cache(redisService, request)
    if cache is not None:
        return list[float](cache)
    else:
        logging.info('dupa')
        array = effects.ao_effect(len, start_point, w).tolist()
        cache_request(redisService, request, array)
        return array


@app.get('/ls_effect/')
async def generate_ls(len: int, start_point: int, w: float) -> list[float]:
    array = effects.ls_effect(len, start_point, w)
    return array.tolist()


@app.get('/tc_effect/')
async def generate_tc(
    len: int, start_point: int, w: float, delta: float = 0.7
) -> list[float]:
    array = effects.tc_effect(len, start_point, w, delta)
    return array.tolist()


@app.post('/io_effect/')
async def generate_io(
    len: int,
    start_point: int,
    w: float,
    arparams: List[float],
    maparams: List[float],
) -> list[float]:
    logging.debug(arparams)
    array = effects.io_effect(
        len,
        start_point,
        arparams,
        maparams,
        w,
    )
    return array.tolist()


@app.get('/health/')
async def check_health():
    return {'status': redisService.check_healt()}


if __name__ == '__main__':
    print('hello')
