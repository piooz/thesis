from pydantic import BaseModel
from datetime import datetime, time
from uuid import UUID


class Stats(BaseModel):
    index: int
    IOcoef: float
    IOtstat: float
    AOcoef: float
    AOtstat: float
    TCcoef: float
    TCtstat: float
    LScoef: float
    LStstat: float


class Fit(BaseModel):
    type: str
    arparams: list[float]
    maparams: list[float]


class Foo(BaseModel):
    index: float
    origin: float
    effect: float
    result: float
    AO: float | None
    IO: float | None
    TC: float | None
    LS: float | None


class Raport(BaseModel):
    executionTime: time
    fit: Fit
    stats: list[Stats]


class AnalyzeResult(BaseModel):
    id: UUID
    time: datetime
    data: list[Foo]
    raport: Raport
