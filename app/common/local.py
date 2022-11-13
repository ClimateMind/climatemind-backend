import os

from flask import request


def check_if_local() -> bool:
    """
    A helper function to check whether a request is being made from a local connection or on the
    live website.
    """
    local = False

    if os.environ.get("IS_LOCAL"):
        request_hostname = request.host.split(":")[0]
        local = (
            request.remote_addr == "127.0.0.1"
            or request_hostname == "127.0.0.1"
            or request_hostname == "localhost"
            or os.environ.get("VPN")
        )

    return local
