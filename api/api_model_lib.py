from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class Result_entry(BaseModel):
    type: str
    coefhat: float
    tstatic: float
    ind: int


class Fit(BaseModel):
    type: str
    arparams: list[float]
    maparams: list[float]


class AnalyzeResult(BaseModel):
    id: UUID
    time: datetime
    data: list[float]
    effect: list[float]
    result: list[Result_entry]
    fit: Fit
