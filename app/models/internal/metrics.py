from app.models.commons.values import Event, Source

class Metric:
    __slots__ = ['source', 'event']

    def __init__(self, source: Source, event: Event):
        self.source: set[Source] = {source}
        self.event: set[Event] = {event}
    
    def add_source(self, source: Source) -> None:
        self.source.update({source})
    
    def add_event(self, event: Event) -> None:
        self.event.update({event})

    def update_metric(self, source: Source, event: Event) -> None:
        self.add_source(source)
        self.add_event(event)
    
    def merge_metrics(self, other: "Metric") -> None:
        self.source.update(other.source)
        self.event.update(other.event)

    def is_bounced(self) -> bool:
        pass