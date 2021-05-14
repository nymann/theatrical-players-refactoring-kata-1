from abc import ABC, abstractmethod

class IPlayType(ABC):

    @abstractmethod
    def volume_credits(self, audience) -> int:
        pass

    @abstractmethod
    def bonus(self, audience: int) -> int:
        pass

class PlayType(IPlayType):
    def bonus(self, audience: int) -> int:
        raise NotImplementedError(audience)

    def volume_credits(self, audience: int) -> int:
        return max(audience - 30, 0)

    @classmethod
    def from_str(cls, name_type: str):
        try:
            return PLAY_TYPES[name_type]
        except KeyError as e:
            raise ValueError(f"unknown type: {name_type}") from e

class Tragedy(PlayType):
    def bonus(self, audience: int) -> int:
        amount = 40000
        min = 30
        if audience > min:
            amount += 1000 * (audience - min)
        return amount


class Comedy(PlayType):
    def bonus(self, audience: int) -> int:
        amount = 30000
        min = 20
        if audience > min:
            amount += 10000 + 500 * (audience - min)
        amount += 300 * audience
        return amount

    def volume_credits(self, audience: int) -> int:
        v = super().volume_credits(audience)
        v += audience // 5
        return v

PLAY_TYPES = {"comedy": Comedy(), "tragedy": Tragedy()}
