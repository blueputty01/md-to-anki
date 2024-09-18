import json
import socket
import urllib.request


class AnkiError(Exception):
    def __init__(self, e, result):
        self.e = e
        self.result = result


def request(action, **params):
    return {"action": action, "params": params, "version": 6}


def invoke(action, **params):
    request_json = json.dumps(request(action, **params)).encode("utf-8")

    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    location = ("localhost", 8765)
    result_of_check = a_socket.connect_ex(location)

    if result_of_check == 0:
        response = json.load(
            urllib.request.urlopen(
                urllib.request.Request("http://localhost:8765", request_json)
            )
        )

        if len(response) != 2:
            raise ValueError("response has an unexpected number of fields")
        if "error" not in response:
            raise ValueError("response is missing required error field")
        if "result" not in response:
            raise ValueError("response is missing required result field")
        if response["error"] is not None:
            raise AnkiError(response["error"], response["result"])

        return response["result"]
    else:
        raise AnkiError(
            "AnkiConnect is not running. Please start Anki and try again.", []
        )


def send_notes(notes) -> None:
    result = invoke("addNotes", notes=notes)

    rejected = []
    for j, note in enumerate(notes):
        if result is None or result[j] is None:
            rejected.append(f'{note["fields"]} under {note["deckName"]}')

    if rejected:
        raise AnkiError("Some notes were rejected by Anki", result)


def send_media(media) -> None:
    invoke("storeMediaFile", **media)
