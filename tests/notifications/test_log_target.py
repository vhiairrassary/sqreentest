from mock import Mock, call
from sqreentest.notifications import Event, LogTarget


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

    logger = Mock()

    target = LogTarget(logger)
    target.handle(events)

    assert logger.info.call_count == 2
    logger.info.assert_has_calls(
        calls=[
            call("Received event: %s", "humanized_description_1 for application 'application_name_1'"),
            call("Received event: %s", "humanized_description_2 for application 'application_name_2'"),
        ]
    )
