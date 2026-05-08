### XSOAR Context Safety Helpers

A small CommonServerUserPython helper set that prevents common XSOAR automation failures when context data changes shape between dict, list, None, or nested list-of-dicts.

Core Value: 
Prevents:
- 'NoneType' object has no attribute 'get'
- list indices must be integers
- unsafe nested context access
- broken iteration over dict/list context values
- repeated boilerplate normalization code across automations


### Usage:
1. as_list()

    Solves the the most common XSOAR context problem:

    ```for item in context.get("RecordedFuture"):```

    This fails when RecordedFuture is a dict, None, or missing.

    Use:
    ```for item in as_list(context.get("RecordedFuture)):```

2. as_dict()

    Solves this failure:

    ```context.get("DomainDNSDetails").get("A")```

    Use:

    ```a_records = xs_dict(context.get("DomainDNSDetails")).get("A")```

3. flatten_list() 

    XSOAR context often becomes nested like:
    ```
    [
    [{"name": "1.1.1.1"}],
    [{"name": "8.8.8.8"}]
    ]
    ```

    Use:
    
    ```flat_items = xs_flatten(items)```