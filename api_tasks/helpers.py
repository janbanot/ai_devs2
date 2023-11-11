import time
import requests  # type: ignore
from requests import Response
from typing import Any, Optional, Dict
from enum import Enum


class ErrorCodes(Enum):
    BOT_DETECTED = (403, "bot detected!")
    SERVER_ERROR = (500, "server error X_X")


def handle_request(method: str, url: str, **kwargs) -> Response:
    try:
        response: Response = requests.request(method, url, **kwargs)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return err.response.status_code, err.response.text
    except requests.exceptions.RequestException as err:
        raise err
    else:
        return response


def send_request(
    method: str,
    url: str,
    max_delay: int = 32,
    base_kwargs: Optional[Dict[str, Any]] = None,
    **kwargs: Any
) -> str:
    if base_kwargs is None:
        base_kwargs = {}
    delay: int = 1
    while delay <= max_delay:
        response = handle_request(method, url, **base_kwargs, **kwargs)
        if response == ErrorCodes.BOT_DETECTED.value:
            print(f"HTTP error occurred: {response[0]}, {response[1]}")
            print("Retrying after 1 second...")
            time.sleep(1)
            headers = (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            )
            base_kwargs["headers"] = {"User-Agent": headers}
        elif response == ErrorCodes.SERVER_ERROR.value:
            print(f"HTTP error occurred: {response[0]}, {response[1]}")
            print(f"Retrying after {delay} seconds...")
            time.sleep(delay)
            delay *= 2
        else:
            print("Success!")
            return response.text
    return ""
