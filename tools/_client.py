"""Small HTTPS client for the NestDaddy REST API (fixed host, fixed paths)."""
from typing import Any

import requests

BASE_URL = "https://nestdaddy.com"
USER_AGENT = "dify-nestdaddy/0.0.1"
TIMEOUT = 30


class NestDaddyError(Exception):
    """A readable error for the model and the user. Never contains the API key."""


def call(api_key: str, path: str, params: dict[str, Any]) -> dict[str, Any]:
    if not api_key:
        raise NestDaddyError("NestDaddy API key is missing. Get a free key at https://nestdaddy.com/dashboard")
    clean = {k: v for k, v in params.items() if v not in (None, "")}
    try:
        r = requests.get(BASE_URL + path, params=clean, timeout=TIMEOUT,
                         headers={"X-API-Key": api_key, "User-Agent": USER_AGENT, "Accept": "application/json"})
    except requests.Timeout as e:
        raise NestDaddyError("NestDaddy did not answer in time. Try again in a moment.") from e
    except requests.RequestException as e:
        raise NestDaddyError(f"Could not reach NestDaddy: {type(e).__name__}") from e
    try:
        data = r.json()
    except ValueError as e:
        raise NestDaddyError(f"NestDaddy returned an unexpected response (HTTP {r.status_code}).") from e
    if r.status_code != 200:
        msg = data.get("message") or data.get("error") or f"HTTP {r.status_code}"
        if r.status_code == 401:
            msg = "The NestDaddy API key is not valid. Check it at https://nestdaddy.com/dashboard"
        elif r.status_code == 429:
            msg = f"{msg} You may have reached your plan's limit: https://nestdaddy.com/dashboard"
        raise NestDaddyError(str(msg))
    return data


def clamp(value: Any, default: int, low: int, high: int) -> int:
    try:
        n = int(value)
    except (TypeError, ValueError):
        return default
    return max(low, min(high, n))
