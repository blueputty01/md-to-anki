import json
import socket
import urllib.request
import os


def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}


def invoke(action, **params):
    request_json = json.dumps(request(action, **params)).encode('utf-8')
    # print(request_json)

    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    location = ("localhost", 8765)
    result_of_check = a_socket.connect_ex(location)

    if result_of_check == 0:
        # print("Port is open")
        response = json.load(urllib.request.urlopen(
            urllib.request.Request('http://localhost:8765', request_json)))

        if len(response) != 2:
            raise Exception('response has an unexpected number of fields')
        if 'error' not in response:
            raise Exception('response is missing required error field')
        if 'result' not in response:
            raise Exception('response is missing required result field')
        if response['error'] is not None:
            raise Exception(response['error'])
        return response['result']
    else:
        print("Port is closed")
        return


def send_notes(notes):
    print("Sending notes")
    result = invoke('addNotes', notes=notes)
    rejected = []

    total = len(notes)
    for j, note in enumerate(notes):
        if result is None or result[j] is None:
            rejected.append(f'{note["fields"]} under {note["deckName"]}')

    rej_count = len(rejected)
    print(f'{total - rej_count} / {total} notes were successfully added to Anki.')
    if rej_count > 0:
        print("The following notes were rejected by Anki:")
        print(*rejected, sep='\n')
    # print("Action complete")


def send_media(media):
    print("Sending media")
    invoke('storeMediaFile', **media)
    # print("Action complete")
