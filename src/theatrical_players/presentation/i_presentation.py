from abc import ABC, abstractmethod
from theatrical_players.domain.statement import Statement

class IPresentation(ABC):
    @abstractmethod
    def __init__(self, statement: Statement):
        pass

    @abstractmethod
    def __str__(self):
        pass
