import re

from flask import abort, request

_CLIENT_ID = re.compile(r"^[A-Za-z0-9-]{16,64}$")


def get_client_id():
    """Anonymous cart owner, sent by the browser in the X-Client-Id header.

    Each browser generates a random ID once, so visitors no longer share one cart.
    There are no user accounts in this project; a real shop would add authentication.
    """
    client_id = request.headers.get("X-Client-Id", "")
    if not _CLIENT_ID.match(client_id):
        abort(400, description="Missing or invalid X-Client-Id header")
    return client_id
