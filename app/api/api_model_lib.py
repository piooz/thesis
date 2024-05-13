from pydantic import BaseModel
from datetime import datetime, time
from uuid import UUID


class Fit(BaseModel):
    type: str
    arparams: list[float]
    maparams: list[float]


class Entry(BaseModel):
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


class AnalyzeResult(BaseModel):
    id: UUID
    time: datetime
    data: list[Entry]
    raport: Raport
