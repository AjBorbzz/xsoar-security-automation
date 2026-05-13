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