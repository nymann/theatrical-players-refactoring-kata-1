from dataclasses import dataclass

@dataclass
class Order(object):
    name: str
    audience: int
    amount: float
