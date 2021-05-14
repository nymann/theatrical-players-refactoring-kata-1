from dataclasses import dataclass
from theatrical_players.domain.play_types import PlayType

@dataclass
class Play(object):
    play_id: str
    name: str
    play_type: PlayType
