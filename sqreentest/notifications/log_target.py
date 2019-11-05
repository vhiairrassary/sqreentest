from logging import Logger
from typing import Sequence
from .target import Event, Target


class LogTarget(Target):
    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    def handle(self, events: Sequence[Event]) -> None:
        for event in events:
            event_description = f"{event.humanized_description} for application '${event.application_name}'"
            self.logger.info("Received event: %s", event_description)
