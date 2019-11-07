from mock import Mock, call
from sqreentest.notifications import Event, TwilloTarget


def test_twillo_target():
    events = [
        Event(
            "sqreen_payload_type_1",
            "application_name_1",
            "environment_1",
            "id_1",
            "event_category_1",
            "event_kind_1",
            "risk_1",
            "humanized_description_1",
            "url_1",
        ),
        Event(
            "sqreen_payload_type_2",
            "application_name_2",
            "environment_2",
            "id_2",
            "event_category_2",
            "event_kind_2",
            "risk_2",
            "humanized_description_2",
            "url_2",
        ),
    ]

    target = TwilloTarget()
    target.twillo_client = Mock()
    target.handle(events)

    assert target.twillo_client.messages.create.call_count == 2
    target.twillo_client.messages.create.assert_has_calls(
        calls=[
            call(body="humanized_description_1", from_="twillo_sms_from", to="twillo_sms_to"),
            call(body="humanized_description_2", from_="twillo_sms_from", to="twillo_sms_to"),
        ]
    )
