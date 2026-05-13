# Custom ServiceDesk Plus Integration

### Limitation of Out of the Box ServiceDesk Plus Integration

The XSOAR ServiceDesk Plus integration focuses on the <b>Request</b> module of ServiceDesk, and yet the integration is incomplete. In this custom ServiceDesk Plus Integration, I've added essential API modules which I believe is necessary and should be helpful to utilize by users. The out of the box ServiceDesk Plus Integration does not have <b>Change</b> Request Module; No <b>Add Notification</b>; and the most part, No <b>Get Conversations/Notifications</b>. 

Also, the official ServiceDesk Plus API documentation failed to provide details of instruction for 'Add Notification' and 'Get Conversations/Notifications'. I had to research and find these answers from their community forum and eventually ended up in their Postman repository or testing environment ground some sort. 

### Solution:

1. Added Change Request :

    Requirements: 

    **Ensure Change Permissions scope :** `Add` , `View`, `Edit`

2. Added View All Notification API Endpoint :

    This operation lets you view the details of all notification under Request.

    `{{base_url}}/api/v3/requests/<request_id>/notifications`

3. Added View All Conversations:

    This operation lets you view the details of all conversations under Request.

    `{{base_url}}/api/v3/requests/<request_id>/conversations?input_data={"list_info":{"start_index":1,"sort_order":"desc","row_count":500},"notes":true}`

    **Note: this was extracted from the POSTMAN Documentation, I will update this endpoint to compare what is based in the documentation and what is truly working in their API module.

    
