from theatrical_players.presentation.presentation import Presentation

class Html(Presentation):
    def __str__(self):
        customer = self.statement.invoice.customer
        html = self._header(f"Statement | {customer}")
        html += self._style()
        body_text: str = f"<h1>Statement for {customer}</h1>\n"
        body_text += "<table>\n<tr>\n\t<th>Name</th>\n\t<th>Amount ($)</th>\n\t<th>Audience (seats)</th>\n</tr>\n"
        audience_sum: int = 0
        for order in self.statement.orders:
            audience_sum += order.audience
            body_text += "<tr>\n"
            body_text += f"\t<td>{order.name}</td>\n"
            body_text += f"\t<td>{self.statement._format_as_dollars(order.amount/100)}</td>\n"
            body_text += f"\t<td>{order.audience}</td>\n"
            body_text += "</tr>\n"
        body_text += f"<tr>\n\t<td><strong>Total</strong></td>\n\t<td><strong>{self.statement._format_as_dollars(self.statement.total_amount_cents/100)}</strong></td>\n\t<td><strong>{audience_sum}</strong></td>\n</tr>\n"
        body_text += "<table>\n"
        body_text += f"<h3>You earned {self.statement.volume_credits} credits</h3>"
        html += self._body(body_text)
        html += "</html>\n"
        return html

    def _header(self, title: str):
        return f"<!doctype html>\n<html>\n<head>\n\t<title>{title}</title>\n</head>\n"

    def _body(self, text: str):
        return f"<body>\n{text}\n</body>\n"

    def _style(self):
        return "<style>\ntable, th, td {\n\tborder: 1px solid black;\n}\n</style>\n"
