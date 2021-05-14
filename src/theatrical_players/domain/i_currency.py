from abc import ABC, abstractmethod

class ICurrency(ABC):
    @abstractmethod
    def format(self, amount: float) -> str:
        pass
