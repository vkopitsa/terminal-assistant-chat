import json


def is_json(myjson: str) -> bool:
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True
