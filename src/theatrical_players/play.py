from typing import Dict

from dataclasses import dataclass
from theatrical_players.play_types import PlayType, get_play_type_from_name

@dataclass
class Play(object):
    play_id: str
    name: str
    play_type: PlayType

    @classmethod
    def from_json(cls, play_id: str, play: Dict[str, str]):
        try:
            play_type = get_play_type_from_name(play["type"])
        except ValueError as e:
            raise e
        return cls(play_id=play_id, name=play["name"], play_type=play_type)
