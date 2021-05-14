from typing import List

from dataclasses import dataclass
from theatrical_players.performance import Performance

@dataclass
class Invoice(object):
    customer: str
    performances: List[Performance]
