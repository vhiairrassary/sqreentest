from functools import wraps
import hmac
import hashlib
import logging
from typing import Sequence
from flask import abort, request, jsonify
from sqreentest.env import sqreen_webhook_secret
from sqreentest.notifications import Event, Target

# pylint: disable=invalid-name
log = logging.getLogger()


def _check_signature(secret_key: bytes, request_signature: str, request_body: bytes) -> bool:
    hasher = hmac.new(secret_key, request_body, hashlib.sha256)
    dig = hasher.hexdigest()

    return hmac.compare_digest(dig, request_signature)


def validate_signature(func):
    @wraps(func)
    def decorated_route(*args, **kwargs):
        request_body = request.get_data()
        request_signature = request.headers["X-Sqreen-Integrity"]

        if not _check_signature(sqreen_webhook_secret(), request_signature, request_body):
            log.warning("Unauthorized webhook received")
            return jsonify({"status": "unauthorized"}), 401

        return func(*args, **kwargs)

    return decorated_route


def handler(targets: Sequence[Target]):
    for target in targets:

        # TODO: validate JSON schema
        events = []
        for event_json in request.json:
            # Unlike specified "application_id" is **not** present in "test" event send when saving webhook
            event = Event(
                event_json["sqreen_payload_type"],
                event_json["application_name"],
                event_json["environment"],
                event_json["id"],
                event_json["event_category"],
                event_json["event_kind"],
                event_json["risk"],
                event_json["humanized_description"],
                event_json["url"],
            )
            events.append(event)

        target.handle(events)

    return jsonify({"status": "ok"}), 200
