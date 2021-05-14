from theatrical_players.domain.i_currency import ICurrency


class Usd(ICurrency):
    def format(self, amount: float) -> str:
        return f"${amount/100:0,.2f}"
