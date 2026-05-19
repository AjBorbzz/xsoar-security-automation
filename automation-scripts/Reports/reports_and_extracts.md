# Reports and Extract Files:

### Reporting 

Export report to XSLX or CSV - Use the XSOAR's Common Script's ExportToXSLX or ExportToCSV Script, but if you want a more custom export, you can use this script: 

```python
"""For multiple reports and multiple sheets You can still utilize the ExportToXSLX and wrap it with a Python function"""

# data transformation

# sheet_name transformation.

def export_xlsx_file(filename: str, data: str, sheet_name: str):
    res = demisto.executeCommand(
        "ExportToXLSX",
        {
            "file_name": file_name,
            "data": data,
            "sheet_name": sheet_name
        }
    )

    if is_error(res):
        raise DemistoException(f"ExportToXLSX failed: {get_error(res)}")
```
