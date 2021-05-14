from typing import Dict, List, Any
from theatrical_players.data.order import Order
from theatrical_players.data.invoice import Invoice
from theatrical_players.data.play import Play
from theatrical_players.data.performance import Performance

class Statement(object):
    def __init__(self, invoice: Invoice) -> None:
        self.invoice: Invoice = invoice
        self.volume_credits: float = 0
        self.total_amount: float = 0
        self.orders: List[Order] = []
        for performance in self.invoice.performances:
            play = performance.play
            play_type = play.play_type
            this_amount = play_type.bonus(audience=performance.audience)
            self.volume_credits += play_type.volume_credits(audience=performance.audience)
            order = Order(name=play.name, audience=performance.audience, amount=this_amount)
            self.orders.append(order)
            self.total_amount += this_amount


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

    def __str__(self):
        result: str = f'Statement for {self.invoice.customer}\n'
        for order in self.orders:
            result += f' {order.name}: {self._format_as_dollars(order.amount/100)} ({order.audience} seats)\n'
        result += f"Amount owed is {self._format_as_dollars(self.total_amount/100)}\n"
        result += f"You earned {self.volume_credits} credits\n"
        return result

    def _format_as_dollars(self, amount: float) -> str:
        return f"${amount:0,.2f}"
