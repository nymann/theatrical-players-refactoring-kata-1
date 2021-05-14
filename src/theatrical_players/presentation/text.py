from theatrical_players.domain.currencies import Usd
from theatrical_players.domain.i_currency import ICurrency
from theatrical_players.presentation.presentation import Presentation

class Text(Presentation):
    def __str__(self, currency: ICurrency = Usd()):
        result: str = f'Statement for {self.statement.invoice.customer}\n'
        for order in self.statement.orders:
            result += f' {order.name}: {currency.format(order.amount)} ({order.audience} seats)\n'
        result += f"Amount owed is {currency.format(self.statement.total_amount_cents)}\n"
        result += f"You earned {self.statement.volume_credits} credits\n"
        return result
