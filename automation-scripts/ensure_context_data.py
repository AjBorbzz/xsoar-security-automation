"""Handles dict, list, missing keys, and malformed data in the context"""

from typing import Any, Dict, List, Optional 
import traceback


def as_list(value: Any) -> List[Any]:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]

def as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


