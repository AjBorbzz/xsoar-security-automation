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
    """Flatten nested lists and remove None values."""
    items: List[Any] = []
    def walk(v: Any):
        if isinstance(v, list):
            for i in v:
                walk(i)

        elif v is not None:
            items.append(v)

    walk(value)
    return items

def get_nested_values(data: Any, path: str, default: Any = None) -> Any:
    """
    Safely get nested values from dict/list context.

    example :
     get_nested_values(context, "RecordedFuture.IP.name")
     get_nested_values(context, "Triage.sample-summaries.score")
    """
    current = [data]

    for key in path.split("."):
        found = []

        for item in flatten_list(current):
            if isinstance(item, dict) and key in item:
                found.append(item.get(key))

        current = flatten_list(found)
        if not current:
            return default 
        
    return current[0] if len(current) == 1 else current

def get_dict_records(data: Any, path: str = "") -> List[Dict[str, Any]]:
    """
    Return only dict records from any context path.

    Example:
        xs_records(context, "RecordedFuture.IP")
        xs_records(context, "Domain")
    """

    value = get_nested_values(data, path, []) if path else data 
    return [item for item in flatten_list(as_list(value)) if isinstance(item, dict)]

def get_subplaybook_context(res: Dict[str, Any], ctx_key: str) -> Optional[Any]:
    """
    Get context from a subplaybook.
    """

    if not isinstance(res, dict):
        return None 
    
    context = res.get("context")
    if not isinstance(context, dict):
        return None 
    
    context_key = context.get(ctx_key)
    if context_key:
        return context_key 
    
    for key, val in context.items():
        if "subplaybook" not in str(key).lower():
            continue 

        if isinstance(val, dict):
            desired_ky = val.get(ctx_key)
            if desired_ky:
                return desired_ky 
            
        elif isinstance(val, list):
            for item in reversed(val):
                if isinstance(item, dict):
                    desired_ky = item.get(ctx_key)
                    if desired_ky:
                        return desired_ky
                    
    return None
