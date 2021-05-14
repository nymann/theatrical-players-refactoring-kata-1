from theatrical_players.presentation.presentation import Presentation

class Text(Presentation):
    def __str__(self):
        result: str = f'Statement for {self.statement.invoice.customer}\n'
        for order in self.statement.orders:
            result += f' {order.name}: {self.statement._format_as_dollars(order.amount/100)} ({order.audience} seats)\n'
        result += f"Amount owed is {self.statement._format_as_dollars(self.statement.total_amount_cents/100)}\n"
        result += f"You earned {self.statement.volume_credits} credits\n"
        return result
