import os


def sqreen_webhook_secret() -> bytes:
    return bytes(os.environ["SQREEN_WEBHOOK_SECRET"], "utf-8")


def twillo_account_sid() -> str:
    return os.environ["TWILLO_ACCOUNT_SID"]


def twillo_auth_token() -> str:
    return os.environ["TWILLO_AUTH_TOKEN"]


def twillo_sms_from() -> str:
    return os.environ["TWILLO_SMS_FROM"]


def twillo_sms_to() -> str:
    return os.environ["TWILLO_SMS_TO"]
