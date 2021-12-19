from dataclasses import dataclass

from model.Attribute import Attribute


@dataclass
class Content:
    media_type: str
    attributes: list[Attribute]
