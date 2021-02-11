import enum
import json

from pathlib import Path


class Request(enum.Enum):
    """ Reads in the request body's from the specification examples """
    CONSENT_PUT = 'updateConsent.json'
    CONSENT_POST = 'createConsent.json'
    REMOVE_RA_RECORD_POST = 'removerarecord.json'
    FLAG_PUT = 'updateFlag.json'
    FLAG_POST = 'createFlag.json'
    LIST_POST = 'createList.json'
    LIST_PUT = 'updateList.json'


def get_body(request_method: enum):
    return __read_spec(request_method.value)


def __read_spec(filename: str):
    base_path = Path(__file__).parent
    file_location = '../../specification/components/examples/' + filename
    file_path = (base_path.joinpath(file_location)).resolve()

    f = open(file_path, "r")
    if f.mode == 'r':
        return json.loads(f.read())
