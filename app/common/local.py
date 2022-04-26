import os

from flask import request


def check_if_local() -> bool:
    """
    A helper function to check whether a request is being made from a local connection or on the
    live website.
    """
    local = False

    if os.environ.get("IS_LOCAL"):
        local = (
            request.remote_addr == "127.0.0.1"
            or os.environ.get("VPN")
            or request.host == "localhost"
        )

    return local
