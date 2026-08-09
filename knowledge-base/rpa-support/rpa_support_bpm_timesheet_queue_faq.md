# BPM TimeSheet Submission to QUEUE FAQ

Source: RPA Support documentation

TimeSheet Submission to QUEUE FAQ
What is the EBS Timesheet submission queue name
Queue Name : com.citco.esb.ebs.timesheet.submit.request.v1
Server URL : tcp://genp-ems01a:7224,tcp://genp-ems01b:7224
How can I get total number of pending items in Queue
Open an SD ticket with MW Team with Category : System.MW.TIBCO-ESB to get the total number of pending
items from the below queue
Queue Name : com.citco.esb.ebs.timesheet.submit.request.v1
Server URL : tcp://genp-ems01a:7224,tcp://genp-ems01b:7224
Received EBS TIMESHEET SUBMIT PRODID BATCH NO [] Failure Email Alert
When BPMDEV Received an email from noreply@citco.com with subject : EBS TIMESHEET SUBMIT -[PROD]
 [<<JMS_CORRELATION_ID>>]  BATCH NO [<>>]- FAILED, Please perform following
1. Check failure reason for this alert :
a. If failure reason is "An IOException was thrown while trying to execute the Http method"
i. Please reach out to TIBCO MW Team on CTM-ITOps-PS-Middleware <CTMITOpsPSMiddleware@citco.com> to request the health check of
the Timecard APP on EBS PROD under Timecard Domain

ii. If Application is down, Open a SD ticket with category as "System.MW.TIBCO-ESB" to check the health and request to start the app.
iii. Once application is up, get the message from "com.citco.esb.ebs.timesheet.submit.request.dlq.v1" with filter on JMS Correlation ID and
search for BATCH ID , check with Kishor and push the message to EMS Q : com.citco.esb.ebs.timesheet.submit.request.v1 to reprocess
Received EBS TIMESHEET SUBMIT PRODID BATCH NO [] BPM UPDATE FAILED
When BPMDEV Received an email from noreply@citco.com with subject : EBS TIMESHEET SUBMIT -[PROD]
 [<<JMS_CORRELATION_ID>>]  BATCH NO [<>>]- BPM UPDATE FAILED Please perform following
1. Check failure reason for this alert :
a. If failure reason is 
Client received a 5xx response for invocation at resource path http://api.citco.com:80/bpm-process-
service/orchestra/timesheet/timecardEntities/updateTimecardStatus-{ActivityName=InvokeRESTAPI,
ProcessName=subprocess.updateBPMTimecardEntry, ModuleName=submitEBSTimecardQProcessor}
Please update manually by invoking API .
http://api.citco.combpm-process-service/orchestra/timesheet/timecardEntities/updateTimecardStatus
Verify the status of the timecard entries in BPM DB using the below query :
Get the status of Timecard Entries
Please note, the id's to be replace with the TS ID from the email Table. If the status of the Timecards are
"INPROGRESS", Invoke the API manually to update the entries:
API URL : http://api.citco.com:80/bpm-process-service/orchestra/timesheet/timecardEntities/updateTimecardStatus
Method : PUT
sm_user : <<>>
SELECT* FROMCTCO_BPMORC_TS_TIMECARD WHEREID IN(13435181,13428730,13449659,13433449,13443963,1340413
Body : JSON with data to be feed from the email Table
UpdateTimecardRequest
2nd Scenario
{ "timecardStatusUpdateDTO": [{ "failedReason": "HXC_TIMECARD_LOCKED: The timecard for &FULL_NAME is locked by another proc"status": "FAILED","timecardId": 13435181},{ "failedReason": "HXC_TIMECARD_LOCKED: The timecard for &FULL_NAME is locked by another proc"status": "FAILED","timecardId": 13428730},{ "failedReason": "HXC_TIMECARD_LOCKED: The timecard for &FULL_NAME is locked by another proc"status": "FAILED","timecardId": 13447161}]}

Please follow the above procedure to update the failed timecards to completed state.

