"""Additional class methods, required python libraries, functions and constants for custom ServiceDesk Plus Integration"""

from typing import Tuple, Dict, List, Any
from _collections import defaultdict # xsoar library 
import urllib3
import ast 
import json 
from datetime import datetime 
import html 
from html import escape 
import re 

# Other constants from OOTB ServiceDesk Plus were omitted to emphasize the custom/added scripts in the XSOAR ServiceDesk Plus integration.
HUMAN_READABLE_FIELDS_CHG_MOD = ['created_time', 'change_id', 'change_requester', 'description', 
                                 'status','title','scheduled_start_time']
CONTAINS_FIELDS = {"title", "description"}

class Client(BaseClient): 
    # Other script was omitted 
    # updated http_request : added data parameter
    def http_request(self, method, url_suffix, full_url=None, params=None, data=None):
        ok_codes = (200, 201, 401) # error response was included -> XSOAR OOTB 
        # update the self._http_request -> from BaseClient of XSOAR integration : add data parameter
        try:
            res = self._http_request(method, url_suffix, full_url=full_url, resp_type='response', ok_codes=ok_codes,
                                     params=params, data=data)
            # Other script goes here #
        except Exception as e:
            if 'SSL Certificate Verification Failed' in e.args[0]:
                return_error('SSL Certificate Verification Failed - try selecting \'Trust any certificate\' '
                             'checkbox in the integration configuration.')
            raise DemistoException(e.args[0])

    def get_requests_conversations(self, request_id: str = None, params: dict = None):
        """Get All conversations under requests.
        
            request_id : 18 digit id of the Request. 
            params: payload of the Request.
        """
        try:
            res = self.http_request(method='GET', url_suffix=f'requests/{request_id}/conversations', params=params)
            return res 
        except Exception as err:
            notif_unavailable = f'{err}'
            if '"status_code: 4000"' in notif_unavailable or '"status_code": 4007' in notif_unavailable:
                return None
                
    def get_notification(self, request_id: str = None, notification_item: dict = None):
        """
        Get a notfication item under a request. Check each notification type. If a notification has a type `NOTES` - notes endpoint will be used.
        """
        id_ = notification_item.get('id')
        type_ = notification_item.get('type')
        if type == 'NOTES':
            url_suffix = f'requests/{request_id}/notes/{id_}'
        else:
            url_suffix = f'requests/{request_id}/notifications/{id_}'

        try:
            res = self.http_request(method='GET', url_suffix=url_suffix)
            res['type'] = type_
            return res 
        
        except Exception as err:
            notif_unavailable = f'{err}'
            if '"status_code: 4000"' in notif_unavailable or '"status_code": 4007' in notif_unavailable:
                return None
            
    def get_changes(self, change_id: str = None, params : dict = None):
        """
        Get specific change request if change_id is provided, else all change requests will be displayed.
        """
        if change_id:
            return self.http_request(method='GET', url_suffix=f'changes/{change_id}')
        else:
            return self.http_request(method='GET', url_suffix='changes', params=params)
        

def create_changes_output(request: dict) -> dict: 
    """
    Creates the output specifically for Change API module.
    Args:
        request: A single request dict returned from the http_request.

    Returns:
        A dictionary containing required fields.
    """

    owner = request.get('change_owner') or {}
    requester = request.get('change_requester') or {}
    manager = request.get('change_manager') or {}
    status = request.get('status') or {}
    completed = request.get('completed_time') or {}
    created = request.get('created_time') or {}

    data = {
        "change_owner": owner.get('name'),
        "employee_id": owner.get('employee_id'),

        "change_requester": requester.get('email_id'),
        "is_technician": requester.get('is_technician'),

        "change_manager": manager.get('name'),

        "change_id": request.get('id'),
        "description": request.get('description'),
        "status": status.get('name'),

        "completed_time": completed.get('display_value'),
        "created_time": created.get('display_value'),

        "title": request.get('title'),
        "scheduled_start_time": request.get('scheduled_start_time'),
        "scheduled_end_time": request.get('scheduled_end_time')
    }

    return data

def create_human_readable_change_module(output: dict) -> dict:
    """
    Converts the output of a command to a human readable output specifically for Change API module.

    Args: 
        output: the output that should be converted to the human readable representation.
    Returns:
        dict: the dictionary that represents the human readable output.
    """

    hr = {}
    for field in HUMAN_READABLE_FIELDS_CHG_MOD:
        if output.get(field):
            hr[field] = output.get(field)

    return hr

def process_search_criteria(search_criteria, search_value):
    if search_criteria == 'change_owner':
        return {
            'field': 'change_owner.name',
            'value': search_value,
            'condition': 'eq'
        }
    field = (
        f"{search_criteria}.email_id"
        if search_criteria == 'change_requester'
        else search_criteria
    )

    return {
        'field': field,
        'value': search_value,
        'condition': 'contains' if search_criteria in CONTAINS_FIELDS else 'eq'
    }

def create_changes_list_info(start_index, row_count, filter_by, search_criteria, search_value):
    """
    Returning the list_info dictionary that should be used to filter the changes that are being returned.

    args: 
        start_index: the index of the first change that should be returned.
        row_count: the number of changes that should be returned.
        filter_by: filter by which to filter the returned changes request.
        search_criteria: search criteria option - refer to ServiceDesk Plus API doc.
        search_value: the value to search.

    Returns:
        A dictionary containing the list_info parameter that should be used for filtering the changes.
    """

    list_info = []
    if start_index:
        list_info['start_index'] = start_index
    if row_count:
        list_info['row_count'] = row_count
    if filter_by:
        list_info['filter_by'] = filter_by
    if search_criteria:
        list_info['search_criteria'] = process_search_criteria(search_criteria, search_value)

    list_info['sort_fields'] = [
        {
            "field": "created_time",
            "order": "desc"
        }
    ]

    return {
        "list_info": list_info
    }

def add_request_notification_command(client: Client, args: dict):
    request_id: str = args.get('request_id')
    subject: str = args.get('subject')
    to: list = argsToList(args.get('to'))
    description: str = args.get('description')
    type_: str = args.get('type')

    data = {
        "notification": {
            "subject": subject,
            "description": description,
            "to": to,
            "type": "reply" if "reply" in type_ else type_,
            "is_public": True
        }
    }

    payload = {"input_data": json.dumps(data, ensure_ascii=True)}
    result = client.http_request('POST', url_suffix=f'requests/{request_id}/notifications', data=payload)
    readable_output = tableToMarkdown("Notification Added: ", t=[data.get('notification')]) #tableToMarkdown an XSOAR function
    return readable_output, None, None

def process_notifications(client: Client, notification_list: list, request_id: str):
    res_data = []
    for item in notification_list:
        res_data.append(client.get_notification(request_id, item))

    return res_data

def process_raw_notification(raw_notifications: list):
    list_data = []
    for item in raw_notifications:
        data = {}
        if item.get('type') == 'NOTES':
            note = item.get('request_note')
            data['time'] = note.get('created_time').get('display_value')
            data['subject'] = note.get('request').get('subject')
            data['sender'] = note.get('performed_by').get('email_id')
            data['description'] = note.get('description')
            data['type'] = item.get('type')

        else:
            notification = item.get('notification')
            data['subject'] = notification.get('subject')
            data['description'] = notification.get('description')
            data['sender'] = notification.get('sender').get('email_id')
            raw_to = notification.get('to')
            data['to'] = ', '.join(raw_to) if isinstance(raw_to, list) else raw_to
            data['time'] = notification.get('time').get('display_value')
            data['type'] = item.get('type')

        list_data.append(data)

    return list_data


"""HTML templates for XSOAR layout dynamic section display"""

MAX_SOAR_HTML_LEN = 40_000 # limits and downsize the html length so that the code will still render html in XSOAR layout.

def sanitize_preview_html(raw_html: str) -> str:
    if not raw_html:
        return ""
    
    clean_html= html.unescape(str(raw_html))

    clean_html = re.sub(r"<script\b[^>]*>.*?</script>", "", clean_html, flags=re.I | re.S)
    clean_html = re.sub(r"<style\b[^>]*>.*?</style>", "", clean_html, flags=re.I | re.S)

    clean_html = re.sub(r"\son\w+=['\"][^'\"]*['\"]", "", clean_html, flags=re.I)

    clean_html = re.sub(
        r'href=["\'](?!https?://|mailto:)[^"\']*["\']',
        'href="#"',
        clean_html,
        flags=re.I
    )

    clean_html = re.sub(
        r'<img\b([^>]*?)src=["\'](?!https?://)[^"\']*["\']([^>]*?)/?>',
        "",
        clean_html,
        flags=re.I
    )

    clean_html = re.sub(
        r"<p[^>]*>\s*(?:&nbsp;|\s)*</p>",
        "",
        clean_html,
        flags=re.I
    )

    clean_html = re.sub(r"\\[nt]", "", clean_html)

    return clean_html.strip()


def minify_html(raw_html: str) -> str:
    """
    Reduces whitespace between tags and inside style attributes.
    Keeps HTML readable by browser/XSOAR but lowers len().
    """

    if not raw_html:
        return ""
    
    raw_html = re.sub(r">\s+<", "><", raw_html)
    raw_html = re.sub(r"\s{2,}", raw_html)
    raw_html = re.sub(r";\s+", ";", raw_html)
    raw_html = re.sub(r":\s+", ":", raw_html)
    raw_html = re.sub(r"\s*{\s*", "{", raw_html)
    raw_html = re.sub(r"\s*}\s*", "}", raw_html)

    return raw_html.strip()

def strip_html_to_text(value: str) -> str:
    """
    Used only for emergency truncation.
    Converts HTML preview into plain text to reduce size safely.
    """

    if not value:
        return ""
    
    value = sanitize_preview_html(value)
    value = re.sub(r"<br\s*/?>", "\n", value, flags=re.I)
    value = re.sub(r"</p\s*>", "\n", value, flags=re.I)
    value = re.sub(r"<[^>]+>","", value)
    value = html.unescape(value)
    return value.strip()

def truncate_text(value: str, max_chars: int) -> str:
    if not value:
        return ""
    
    value = str(value).strip()

    if len(value) <= max_chars:
        return value
    
    return value[:max_chars].rstrip() + "..."

def parse_notification_time(item: Dict[str, Any]):
    """
    Sort helper. Keeps invalid/missing dates at the bottom.
    """

    try: 
        return datetime.strptime(item.get("time", ""), "%b %d, %Y %I:%M %p")

    except Exception:
        return datetime.min
    
def render_empty_html() -> str:
    return (
        '<div style="font-family:Arial, Helvetica, sans-serif;'
        'padding:14px; color: #d2ddd2;">No Notifications found. </div>'
    )

def render_card_full(item: Dict[str, Any]) -> str:
    """
    Full visual version. Larger HTML - inline styles are more descriptive.
    """
    sender = escape(str(item.get("sender") or "System"))
    time = escape(str(item.get("time") or "N/A"))
    subject = escape(str(item.get("subject") or "N/A"))
    to = escape(str(item.get("to") or "N/A"))
    type_ = escape(str(item.get("type") or "N/A"))
    description = sanitize_preview_html(item.get("description") or "")
