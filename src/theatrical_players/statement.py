from dataclasses import dataclass
import math
from abc import ABC, abstractmethod
from typing import Dict, List, Any

PLAY_TYPE = {
    "tragedy": {
        "min_audience": 30,
        "bonus_multiplier": 1000,
        "start_bonus": 0
    },
    "comedy": {
        "min_audience": 20,
        "bonus_multiplier": 500,
        "start_bonus": 10000,
    }
}

class IPlayType(ABC):

    @abstractmethod
    def volume_credits(self, audience) -> int:
        pass

    @abstractmethod
    def bonus(self, audience: int) -> int:
        pass

class PlayType(IPlayType):
    def bonus(self, audience: int) -> int:
        raise NotImplementedError(audience)

    def volume_credits(self, audience: int) -> int:
        return max(audience - 30, 0)
        

class Tragedy(PlayType):
    def bonus(self, audience: int) -> int:
        amount = 40000
        min = 30
        if audience > min:
            amount += 1000 * (audience - min)
        return amount


class Comedy(PlayType):
    def bonus(self, audience: int) -> int:
        amount = 30000
        min = 20
        if audience > min:
            amount += 10000 + 500 * (audience - min)
        amount += 300 * audience
        return amount

    def volume_credits(self, audience: int) -> int:
        v = super().volume_credits(audience)
        v += math.floor(audience / 5)
        return v

PLAY_TYPES = {"comedy": Comedy(), "tragedy": Tragedy()}

@dataclass
class Play(object):
    play_id: str
    name: str
    play_type: PlayType

    @classmethod
    def from_json(cls, play_id: str, play: Dict[str, str]):
        try:
            play_type = PLAY_TYPES[play["type"]]
        except KeyError as e:
            raise ValueError(f"unknown type: {play['type']}") from e
        return cls(play_id=play_id, name=play["name"], play_type=play_type)


@dataclass
class Performance(object):
    play: Play
    audience: int


@dataclass
class Invoice(object):
    customer: str
    performances: List[Performance]


class Statement(object):
    def __init__(self, invoice: Invoice) -> None:
        self.invoice: Invoice = invoice

    @classmethod
    def from_json(cls, invoice: Dict[str, Any], plays: Dict[str, Dict[str, str]]):
        temp_plays: Dict[str, Play] = {}
        for play_id, play in plays.items():
            temp_plays[play_id] = Play.from_json(play_id=play_id, play=play)

        performances: List[Performance] = []
        for performance in invoice["performances"]:
            play_id = performance["playID"]
            play = temp_plays[play_id]
            audience = performance["audience"]
            performances.append(Performance(play=play, audience=audience))

        transformed_invoice = Invoice(customer=invoice["customer"], performances=performances)
        
        return cls(transformed_invoice)

    def calculate(self):
        total_amount: float = 0
        volume_credits: float = 0
        result: str = f'Statement for {self.invoice.customer}\n'
        for perf in self.invoice.performances:
            play = perf.play
            this_amount = play.play_type.bonus(audience=perf.audience)
            volume_credits += play.play_type.volume_credits(audience=perf.audience)
            # print line for this order
            result += f' {play.name}: {self._format_as_dollars(this_amount/100)} ({perf.audience} seats)\n'
            total_amount += this_amount
    
        result += f"Amount owed is {self._format_as_dollars(total_amount/100)}\n"
        result += f"You earned {volume_credits} credits\n"
        return result

    def _format_as_dollars(self, amount: float) -> str:
        return f"${amount:0,.2f}"
