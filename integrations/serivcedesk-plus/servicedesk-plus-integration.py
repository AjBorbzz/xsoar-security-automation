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
        