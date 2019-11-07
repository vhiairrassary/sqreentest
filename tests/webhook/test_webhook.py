import json
from mock import Mock
from flask import Flask
from sqreentest.notifications import Event
from sqreentest.webhook import validate_signature, handler


def test_webhook_invalid():
    app = Flask(__name__)

    @app.route("/test-webhook", methods=["POST"])
    @validate_signature
    def public():
        return "data-public-route"

    client = app.test_client()

    rv = client.post("/test-webhook", headers={"X_SQREEN_INTEGRITY": "coucou"}, data="coucou")
    assert 401 == rv.status_code
    assert b'{"status":"unauthorized"}\n' == rv.data


def test_webhook_valid():
    app = Flask(__name__)

    @app.route("/test-webhook", methods=["POST"])
    @validate_signature
    def public():
        return "ok"

    client = app.test_client()

    rv = client.post(
        "/test-webhook",
        headers={"X_SQREEN_INTEGRITY": "1c45f2709acf5de270f7a957bac667163379f28908260d9ed13937aea90237f0"},
        data="coucou",
    )
    assert 200 == rv.status_code
    assert b"ok" == rv.data


def test_webhook_handler():
    app = Flask(__name__)

    target_1 = Mock()
    target_2 = Mock()

    @app.route("/test", methods=["POST"])
    def test():
        return handler([target_1, target_2])

    data = [
        {
            "sqreen_payload_type": "sqreen_payload_type_1",
            "application_name": "application_name_1",
            "environment": "environment_1",
            "id": "id_1",
            "event_category": "event_category_1",
            "event_kind": "event_kind_1",
            "risk": "risk_1",
            "humanized_description": "humanized_description_1",
            "url": "url_1",
        },
        {
            "sqreen_payload_type": "sqreen_payload_type_2",
            "application_name": "application_name_2",
            "environment": "environment_2",
            "id": "id_2",
            "event_category": "event_category_2",
            "event_kind": "event_kind_2",
            "risk": "risk_2",
            "humanized_description": "humanized_description_2",
            "url": "url_2",
        },
    ]

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

    app.test_client().post("/test", content_type="application/json", data=json.dumps(data))

    target_1.handle.assert_called_once_with(events)
    target_2.handle.assert_called_once_with(events)
