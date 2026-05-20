from app.models.commons.values import Event, Source

class Metric:
    __slots__ = ['source', 'event']

    def __init__(self, source: Source, event: Event):
        self.source: set[Source] = {source}
        self.event: set[Event] = {event}