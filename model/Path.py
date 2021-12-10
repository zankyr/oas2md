from dataclasses import  dataclass, field, make_dataclass
import dataclasses

from model.Method import Method


@dataclass
class Path():
    title: str
    methods: list[Method] = field(init=False, default=None)

            
