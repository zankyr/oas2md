from dataclasses import dataclass, field

from model.Operation import Operation


@dataclass
class Path:
    name: str
    operations: list[Operation] = field(init=False, default=None)
