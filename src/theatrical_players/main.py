import json
import pathlib

from theatrical_players.statement import statement

import typer

DEFAULT_FILE_OPTIONS = typer.Option(..., exists=True, file_okay=True, dir_okay=True, readable=True)

app = typer.Typer()

@app.command()
def main(
    invoice: pathlib.Path = DEFAULT_FILE_OPTIONS,
    plays: pathlib.Path = DEFAULT_FILE_OPTIONS,
):
    with invoice.open("r") as invoice_file:
        invoice_json = json.loads(invoice_file.read())

    with plays.open("r") as plays_file:
        plays_json = json.loads(plays_file.read())
    
    result = statement(invoice=invoice_json, plays=plays_json)
    typer.echo(result)

if __name__ == "__main__":
    app()
