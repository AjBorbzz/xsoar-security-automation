# ServiceDesk Plus Custom Commands

### Add Notifications

**Command Name:**  service-desk-plus-add-notification
**Description:**  Add a Notification under a request.
**Arguments:** 
* request_id : 18 digit request ID
* subject    : Subject of this request.
* to         : email address to be sent.
* description: description content to be stored.
* type       : Type of notification - Default: email reply


### Get All Conversations
**Command Name:**  service-desk-plus-get-conversations
**Description:**  View the details of requets notifications.
**Arguments:** 
* request_id : The unique request id of the request that should be shown.

**Outputs:**
ServiceDeskPlus.Notifications : [List, Dict]

### Get All Notifications

### Add Notes