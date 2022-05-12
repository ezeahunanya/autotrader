import pickle
import json
from typing import Any, Dict

def save_as_pickle(obj: Any, filepath: str) -> None:
    with open(filepath, 'wb') as handle:
        pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)

def save_as_json(obj: Dict, filepath: str) -> None:
    with open(filepath, 'w') as fp:
        json.dump(obj, fp)