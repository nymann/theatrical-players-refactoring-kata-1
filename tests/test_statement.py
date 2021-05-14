import json

from approvaltests.utils import get_adjacent_file
from approvaltests import verify
import pytest

from theatrical_players.domain.statement import Statement
from theatrical_players.presentation.text import Text

def test_example_statement():
    with open(get_adjacent_file("invoice.json")) as f:
        invoice = json.loads(f.read())
    with open(get_adjacent_file("plays.json")) as f:
        plays = json.loads(f.read())
    statement = Statement.from_json(invoice=invoice, plays=plays)
    presentation = Text(statement)
    verify(str(presentation))


def test_statement_with_new_play_types():
    with open(get_adjacent_file("invoice_new_plays.json")) as f:
        invoice = json.loads(f.read())
    with open(get_adjacent_file("new_plays.json")) as f:
        plays = json.loads(f.read())
    statement = Statement.from_json(invoice=invoice, plays=plays)
    presentation = Text(statement)
    verify(str(presentation))
