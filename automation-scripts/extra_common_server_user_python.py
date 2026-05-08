"""XSOAR engineers commonly struggle with parsing context JSON, 
list-of-dict outputs, nested keys, and returning manipulated arrays back into context. 
"""

from typing import Any, Dict, List, Optional 
import traceback


def as_list(value: Any) -> List[Any]:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]

def as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}

def flatten_list(value: Any) -> List[Any]:
    items: List[Any] = []
    def walk(v: Any):
        if isinstance(v, list):
            for i in v:
                walk(i)

        elif v is not None:
            items.append(v)

    walk(value)
    return items
