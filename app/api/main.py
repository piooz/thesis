import logging
from typing import BinaryIO, List
from chenLiu import effects
from fastapi import FastAPI, Request, UploadFile
from pandas import DataFrame
from statsmodels.iolib.table import csv
import pickle

from chenLiu.chenLiu import chen_liu, effects_matrix

from .cache import RedisCache
from .api_model_lib import *

from fastapi.middleware.cors import CORSMiddleware
import csv
import codecs
import time

app = FastAPI()
redisService: RedisCache = RedisCache()
logging.basicConfig(level=logging.INFO)


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
        cached_response = cache_service.read(key)
        response_body = pickle.loads(cached_response)
        logging.info(f'Found cached request response key: {key}')
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


def df2Entries(df, fit, n) -> list:
    matrix_df = effects_matrix(fit, df, 0.7, n)
    outliers = []

    for name in list(matrix_df):
        index = int(name)
        values = matrix_df[name].values.tolist()

        outliers.append(
            Effect(
                type=(df['type'][index]),
                omega=df['omega'][index],
                tau=df['tau'][index],
                starts=(int(name)),
                values=values,
            )
        )

    return outliers


def prepare_analyze_report(df, fit, dataset_len, execution_time):
    arima_fit = Fit(type='ARIMA', arparams=fit.arparams, maparams=fit.maparams)
    effects = df2Entries(df, fit, dataset_len)
    return AnalyzeResult(
        outliers=len(df),
        result=effects,
        arimaFit=arima_fit,
        executionTime=execution_time,
    )


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
    cval: float = 2.0,
    have_header: bool = False,
    col: int = 0,
):
    data = read_column_binary(file.file, have_header, col)
    start_time = time.time()
    (report, out_series, effect_series, arima_fit) = chen_liu(data, cval=cval)
    end_time = time.time()
    execution_time = end_time - start_time

    if not isinstance(report, DataFrame):
        return AnalyzeResult(
            outliers=0,
            result=[],
            executionTime=execution_time,
            arimaFit=None,
        )
    else:
        result = prepare_analyze_report(
            report, arima_fit, len(data), execution_time
        )
        return result


@app.get('/ao_effect/')
async def generate_ao(
    len: int, start_point: int, w: float, request: Request
) -> list[float]:
    cache = check_cache(redisService, request)
    if cache is not None:
        logging.info('Found request in cache')
        return list[float](cache)
    else:
        array = effects.ao_effect(len, start_point, w).tolist()
        cache_request(redisService, request, array)
        return array


@app.get('/ls_effect/')
async def generate_ls(
    len: int, start_point: int, w: float, request: Request
) -> list[float]:
    cache = check_cache(redisService, request)
    if cache is not None:
        logging.info('Found request in cache')
        return list[float](cache)
    else:
        logging.info('Not Found request in cache')
        array = effects.ls_effect(len, start_point, w).tolist()
        cache_request(redisService, request, array)
        return array


@app.get('/tc_effect/')
async def generate_tc(
    len: int, start_point: int, w: float, request: Request, delta: float = 0.7
) -> list[float]:
    cache = check_cache(redisService, request)
    if cache is not None:
        logging.info('Found request in cache')
        return list[float](cache)
    else:
        logging.warning('Not Found request in cache')
        array = effects.tc_effect(len, start_point, w, delta).tolist()
        cache_request(redisService, request, array)
    return array


@app.post('/io_effect/')
async def generate_io(
    len: int,
    start_point: int,
    w: float,
    arparams: List[float],
    maparams: List[float],
    request: Request,
) -> list[float]:
    cache = check_cache(redisService, request)
    if cache is not None:
        logging.info('Found request in cache')
        return list[float](cache)
    else:
        array = effects.io_effect(
            len,
            start_point,
            arparams,
            maparams,
            w,
        )
        cache_request(redisService, request, array)
        return array.tolist()


@app.get('/health/')
async def check_health():
    return {'status': redisService.check_healt()}


if __name__ == '__main__':
    print('hello')
