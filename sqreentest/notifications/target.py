from dataclasses import dataclass
from typing import Sequence


@dataclass
class Event:
    sqreen_payload_type: str
    application_id: str
    application_name: str
    environment: str
    id: str
    event_category: str
    event_kind: str
    risk: str
    humanized_description: str
    url: str


class Target:
    def handle(self, events: Sequence[Event]) -> None:
        pass
