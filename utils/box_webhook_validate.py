import dateutil.parser
import pytz
import datetime
import hmac
import hashlib
import base64
from typing import Optional


def validate_webhook_signature(
    key_a,
    key_b,
    timestamp_header,
    signature1,
    signature2,
    payload,
    box_signature_version,
    box_signature_algorithm,
) -> bool:
    is_expired = validate_timestamp(timestamp_header)

    is_correct_version = validate_signature_version(box_signature_version)
    is_correct_algorithm = validate_signature_algorithm(
        box_signature_algorithm
    )

    digest_key_a = sign_payload(key_a, payload, timestamp_header)
    digest_key_b = sign_payload(key_b, payload, timestamp_header)

    is_signature1_valid = digest_key_a == signature1
    is_signature2_valid = digest_key_b == signature2

    if not is_signature1_valid:
        print(f"Invalid signature 1: {digest_key_a} != {signature1}")

    if not is_signature2_valid:
        print(f"Invalid signature 2: {digest_key_b} != {signature2}")

    return (
        not is_expired
        and is_correct_version
        and is_correct_algorithm
        and (is_signature1_valid or is_signature2_valid)
    )


def validate_signature_version(signature_version) -> bool:
    is_correct_version = signature_version == "1"
    if not is_correct_version:
        print(f"Invalid signature version: {signature_version}")
    return is_correct_version


def validate_signature_algorithm(signature_algorithm) -> bool:
    is_correct_algorithm = signature_algorithm == "HmacSHA256"
    if not is_correct_algorithm:
        print(f"Invalid signature algorithm: {signature_algorithm}")
    return is_correct_algorithm


def validate_timestamp(timestamp_header) -> bool:
    # the timestamp must be within 10 minutes

    date = dateutil.parser.parse(timestamp_header).astimezone(pytz.utc)

    now = datetime.datetime.now(pytz.utc)
    deltaMinutes = datetime.timedelta(minutes=10)
    expiry_date = now + deltaMinutes
    is_expired = date >= expiry_date
    if is_expired:
        print(
            f"Webhook is expired: Timestamp: {date} : Now: {now} : Expiry: {expiry_date}"
        )

    return is_expired


def sign_payload(key: str, payload: bytes, timestamp: str) -> Optional[str]:

    if key is None:
        return None

    encoded_signature_key = key.encode("utf-8")
    encoded_delivery_time_stamp = timestamp.encode("utf-8")
    new_hmac = hmac.new(encoded_signature_key, digestmod=hashlib.sha256)
    new_hmac.update(payload + encoded_delivery_time_stamp)
    signature = base64.b64encode(new_hmac.digest()).decode()
    return signature
