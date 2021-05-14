from theatrical_players.presentation.i_presentation import IPresentation
from theatrical_players.domain.statement import Statement

class Presentation(IPresentation):
    def __init__(self, statement: Statement):
        self.statement = statement

    def __str__(self):
        raise NotImplementedError()
