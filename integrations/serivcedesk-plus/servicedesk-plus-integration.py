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
        if request_id:
            try:
                res = self.http_request(method='GET', url_suffix=f'requests/{request_id}/conversations', params=params)
                return res 
            except Exception as err:
                notif_unavailable = f'{err}'
                if '"status_code: 4000"' in notif_unavailable or '"status_code": 4007' in notif_unavailable:
                    return None