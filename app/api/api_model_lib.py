from datetime import time
from pydantic import BaseModel


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


class Effect(BaseModel):
    type: str
    omega: float
    tau: float
    starts: int
    values: list[float]


class AnalyzeResult(BaseModel):
    outliers: int
    executionTime: float
    result: list[Effect]
    arimaFit: Fit | None
