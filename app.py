from flask import Flask
import sqreen  # type: ignore

from sqreentest.webhook import validate_signature, handler
from sqreentest.notifications import LogTarget

sqreen.start()

# pylint: disable=invalid-name
app = Flask(__name__)


NOTIFICATION_TARGETS = [
    LogTarget(app.logger),
    # TwilloTarget()
]


@app.route("/")
def root():
    return "Hello, World!"


@app.route("/webhook", methods=["POST"])
@validate_signature
def webhook():
    return handler(NOTIFICATION_TARGETS)
