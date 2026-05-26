from dataclasses import dataclass

from app.models.commons.values import Event, Source

@dataclass
class Interaction:
    __slots__ = ['user_ids', 'source', 'event']
    user_ids: set[str]
    source: Source
    event: Event
