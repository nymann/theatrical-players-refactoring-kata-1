import math
import pydantic
from typing import Dict, List, Any

class Play(pydantic.BaseModel):
    play_id: str
    name: str
    play_type: str

    @classmethod
    def from_json(cls, play_id: str, play: Dict[str, str]):
        return cls(play_id=play_id, name=play["name"], play_type=play["type"])


class Performance(pydantic.BaseModel):
    play: Play
    audience: int

class Invoice(pydantic.BaseModel):
    customer: str
    performances: List[Performance]

class Statement(object):
    def __init__(self, invoice: Invoice) -> None:
        self.invoice = invoice

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
            if play.play_type == "tragedy":
                this_amount = 40000
                if perf.audience > 30:
                    this_amount += 1000 * (perf.audience - 30)
            elif play.play_type == "comedy":
                this_amount = 30000
                if perf.audience > 20:
                    this_amount += 10000 + 500 * (perf.audience - 20)
    
                this_amount += 300 * perf.audience
    
            else:
                raise ValueError(f'unknown type: {play.play_type}')
    
            # add volume credits
            volume_credits += max(perf.audience - 30, 0)
            # add extra credit for every ten comedy attendees
            if "comedy" == play.play_type:
                volume_credits += math.floor(perf.audience / 5)
            # print line for this order
            result += f' {play.name}: {self._format_as_dollars(this_amount/100)} ({perf.audience} seats)\n'
            total_amount += this_amount
    
        result += f"Amount owed is {self._format_as_dollars(total_amount/100)}\n"
        result += f"You earned {volume_credits} credits\n"
        return result

    def _format_as_dollars(self, amount: float) -> str:
        return f"${amount:0,.2f}"
