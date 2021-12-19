from dataclasses import dataclass

from model.ResponseAttribute import ResponseAttribute

@dataclass
class ResponseBody():
    media_type: str
    attributes: list[ResponseAttribute]