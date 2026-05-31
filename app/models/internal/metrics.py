from app.models.commons.values import Event, Source

class Metric:
    __slots__ = ['source', 'display', 'buy']

    def __init__(self, source: Source, event: Event):
        self.source: set[Source] = {source}
        self.display: int = 1 if Event(event) == Event.DISPLAY else 0
        self.buy: int = 1 if Event(event) == Event.BUY else 0
    
    def add_source(self, source: Source) -> None:
        self.source.update({source})
    
    def add_event(self, event: Event) -> None:
        self.display += 1 if Event(event) == Event.DISPLAY else 0
        self.buy += 1 if Event(event) == Event.BUY else 0

    def update_metric(self, source: Source, event: Event) -> None:
        self.add_source(source)
        self.add_event(event)
    
    def merge_metrics(self, other: "Metric") -> None:
        self.source.update(other.source)
        self.display += other.display
        self.buy += other.buy

    def is_bounced(self) -> bool:
        return self.display == 1 and self.buy == 0
    
    def is_crossed(self) -> bool:
        return len(self.source) == 2