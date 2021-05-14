from dataclasses import dataclass
from theatrical_players.play import Play

@dataclass
class Performance(object):
    play: Play
    audience: int
