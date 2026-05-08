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

4. get_nested_values()

    Instead of writing unsafe code:

    ```score = context.get("Triage").get("sample-summaries").get("score")```

    Use:

    ```score = get_nested_values(context, "Triage.sample-summaries.score")```

    It works whether Triage or sample-summaries is a dict, list, missing, or None.

5. get_dict_records()

    This is useful when you expect a list of dictionaries but XSOAR may return one dictionary, many dictionaries, or nothing.

    Example:
    ```
    rf_ips = xs_records(context, "RecordedFuture.IP")

    for ip_obj in rf_ips:
        ip_name = xs_get(ip_obj, "name")
        evidence = xs_get(ip_obj, "Evidence", [])
    ```

    #### Example usage for your Recorded Future IP case

    ```
    def rf_ip_evidence_for_domain(context: Dict[str, Any]) -> List[Dict[str, Any]]:
    a_records = xs_list(xs_get(context, "DomainDNSDetails.A", []))
    rf_ips = xs_records(context, "RecordedFuture.IP")

    matched = []

    for ip_obj in rf_ips:
        ip_name = xs_get(ip_obj, "name")

        if ip_name in a_records:
            matched.extend(xs_records(ip_obj, "Evidence"))

    return matched
    ```