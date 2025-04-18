from pydantic import BaseModel
from datetime import date

class EventCalendarSchema(BaseModel):
    month:int
    year:int

class ParticularEventSchema(BaseModel):
    date:date