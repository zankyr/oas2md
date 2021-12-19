
from dataclasses import dataclass

from model.Header import Header
from model.ResponseBody import ResponseBody


@dataclass
class ResponseResult():
    code: int
    description: str
    headers: list[Header]
    bodies: list[ResponseBody]
