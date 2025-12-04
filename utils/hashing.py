import hashlib
import json


def hash_value(value):
    """Hash jedne vrijednosti (string, broj)."""
    return hashlib.sha256(str(value).encode()).hexdigest()


def hash_state(state: dict):
    """Hash cijelog stanja baze, stabilan i deterministički."""
    json_state = json.dumps(state, sort_keys=True)
    return hashlib.sha256(json_state.encode()).hexdigest()
