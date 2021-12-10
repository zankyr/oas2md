
from dataclasses import dataclass

from model.ResponseResult import ResponseResult


@dataclass
class Response():
    results: list[ResponseResult]