Thursday, 2026-03-19 @11AM AST

Meeting Notes:

BPM Control Questionnaire

## Line of Businesses (LoB) – aka Business Groups and assigned Roles

@Ivan Carlo and @Kishor are discussing CS incidents from 2023 for CITCO BPM

Features available for those roles

The roles should be in AD (Active Directory) within Citco

Authentication – migrated to Ping from SiteMinder

Authorization –

Talking about UAT (lower env system) & Production

Risk Team – For Auditors (Production Env) – Need approval of Business Team

## Penetration Testing:

Last BPM: 2024-04-16

Confluence page of Isses found is shared by Kishor

Log4j vulnerabilities – issues – Pen Testing - Red team conducted it

Red Team conducted it

It should be done annually for each app

@Maria suggested reaching out to Red Team to be conducted in 2026

All issues are remediated

Post verification test after PenTest – check for issues is remediated or not

PenTest - only conducted on UAT (lower env) – Fix issues – Apply the same issues in Production – Because production must be live (if pen test is conducted on prod – it might break, and take time to fix the issues)

BPM - SLA1 – high userbase – so production uptime is critical

## Access Logs Questions

Login, logout, failed login attempts

@Kishor propose to give URL to check - @Ivan Carlo will look at that

@Maria – asked about what kind of information are included in the logs, who has access to the logs, @Kishor – Retention period 7/14 days, and Dev + SRE team would have access to the logs

@Maria – allow to edit/delete logs? - @Kishor – No

@Maria – asked about example for DB admin can edit

@Kishor – ELK, Kibana, ElastiSearch, TIBCO Logs

@Ivan Carlo – asked for screenshot of log retention config

@Maria – Policy regarding access logs – data retention period, critical (5 years) / non-critical (90 days), first time seeing only 7 days

@Ivan Carlo, @Kishor – can do for more than 7 days depending on business

@Kishor – Middleware logs are 7 days, TIBCO logs could have more retention periods

## Application Alerts / Anomaly Detection

Dynatrace – application monitoring the infrastructure tool, configuring the triggers for that – trigger alerts – Notification/Emails

Anomaly detection, Errors, Unusual Logging, unusual processing

@Kishor - showing Dynatrace to all, which kind of alerts and triggered emails, root cause, and impact

@Ivan Carlo – only detects infrastructure or can detect login alerts?

@Kishor - Ping / SiteMinder takes care of it, IDM team takes care of it

@Ivan Carlo – What kind of alters Dynatrace triggers for BPM, etc.

### Additional Qs:

In UAT / Test env – do we use production data? (@Ivan Carlo)

No (@Kishor)

Never sync Prod to UAT, it’s the other way around (my interpretation)

What kind of data is used for testing? (@Maria)

Business Testing team creates data in UAT (@Kishor)

Manual related to handling of data (guidance on how training or critical data are being processed) (@Ivan Carlo)

BPM is operational tool, user guide, how new users can train BPM, how to operate the application  (@Kishor)

There is no critical data being stored or processed.

### Last Discussion

Screenshots of UAT and Prod versions

Wednesday: 2026-03-25, 10.30 AM AST (Follow up)

Artifacts + Screenshots handover