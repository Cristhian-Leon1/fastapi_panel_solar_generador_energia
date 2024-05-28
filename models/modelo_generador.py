from pydantic import BaseModel
from datetime import datetime


class GeneradorDataModel(BaseModel):
    voltaje: float = None
    corriente: float = None
    potencia: float = None
    energiaAcumulada: float = None
    timestamp: datetime = None
