from typing import Sequence
from twilio.rest import Client  # type: ignore
from sqreentest.env import twillo_account_sid, twillo_auth_token, twillo_sms_from, twillo_sms_to
from .target import Event, Target


class TwilloTarget(Target):
    def __init__(self) -> None:
        self.twillo_client = Client(twillo_account_sid(), twillo_auth_token())

    def handle(self, events: Sequence[Event]) -> None:
        for event in events:
            sms_content = event.humanized_description

            self.twillo_client.messages.create(body=sms_content, from_=twillo_sms_from(), to=twillo_sms_to())
