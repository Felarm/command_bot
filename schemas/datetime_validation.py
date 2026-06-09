from datetime import datetime

from pydantic import BaseModel


class DatetimeValidator(BaseModel):
    input_dt: datetime