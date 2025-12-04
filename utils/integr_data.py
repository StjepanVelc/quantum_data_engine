import hashlib
import json


def hash_state(state):
    json_state = json.dumps(state, sort_keys=True)
    return hashlib.sha256(json_state.encode()).hexdigest()
