import json
import pathlib
import enum

from theatrical_players.domain.statement import Statement

import typer

from theatrical_players.presentation.html import Html
from theatrical_players.presentation.text import Text

DEFAULT_FILE_OPTIONS = typer.Option(
    ...,
    exists=True,
    file_okay=True,
    dir_okay=True,
    readable=True,
)

class PresentationChoice(str, enum.Enum):
    html = "HTML"
    text = "Text"

app = typer.Typer()

@app.command()
def main(
    invoice: pathlib.Path = DEFAULT_FILE_OPTIONS,
    plays: pathlib.Path = DEFAULT_FILE_OPTIONS,
    presentation: PresentationChoice = PresentationChoice.html,
):
    with invoice.open("r") as invoice_file:
        invoice_json = json.loads(invoice_file.read())

    with plays.open("r") as plays_file:
        plays_json = json.loads(plays_file.read())

    statement = Statement.from_json(invoice=invoice_json, plays=plays_json)
    if presentation == PresentationChoice.html:
        pres = Html(statement)
    else:
        pres = Text(statement)
    typer.echo(str(pres))


if __name__ == "__main__":
    app()
