## Acronyms

ADIC – Application Development & Integration Center

API – Application Programming Programming Interface

AP – Action Processor

CDI – Citco Data Integration

TTL – Time-To-Live (cache)

HIL – Human-In-the-Loop

L1-L5 – Knowledge-Graph hierarchy levels (Product, …)

AuthMaster – Authentication & Authorization Service

ERS – Event Routing Service

AP – Action Processor

ERS-AP – Event Routing Service – Action Processor

NS – Notification Service

## Day4: 2026-04-16, Thursday

## Open Questions

What are the capabilities of notification services?

Can NS send an email?

Can NS push messages to SQS?

Can NS push messages to SNS?

@Bhanu – Action Required

# Question

Capabilities

Authentication, Authorization – for URLs

## Day3: 2026-04-15, Wednesday

## Open Questions

How is the Event Routing Service – Action Processor (ERS-AP) registry being built?

Via deployment_specs.yaml (using the Pytoml library)

Where is the event scheduler defined?

Who is responsible for running the event scheduler?

@Bhanu – Action Required

#	Question

Where is the schedule defined?

3	Who is responsible for running the event scheduler?

## Day 2: 2026-04-14, Tuesday

Context: KG/Optics

Where is the optic loader hosted?

What is GraphName? (Neptune DB API)

How would we know that data has been synced?

Can we get the CyberQuery?

Can we get access to the knowledge Graph to see what has been updated?

What is workflow API service? (That we are using to get data).

## Context: ADIC

Who is responsible for adding configuration?

Platform team

Business team

How does a business item propagate to the Knowledge Graph?

How is the knowledge synchronized? (Frequency)

Real-time

On-demand (confirmed)

Each Friday we receive an email (from whom?) and load workflows into the Knowledge Graph.

Follow-up: Why on-demand?

How often do workflows change?

Where is the data hosted?

Citco-Works

CDI

Who is responsible for running the workflow?

Manual

System

Who decides the following?

Process / Sub-Process

Task / Sub-Task

Who decides the dependencies (relations) on the Knowledge Graph?

How are the relations on the Knowledge Graph added?

Clarify the levels L1-L5:

L1: Product (certain)

L2: …

L3: …

L4: Process / Task?

L5: Process / Task?

## Context: Event Services

Where are events stored?

What is the role of Event Services?

Where is the mapping hosted?

Which API is being used?

If we need the raw payload (without mapped data), is that possible?

Can the routing service perform a pass-through? (Answer – NO)

If source-field data is missing, will blank data be sent? (Answer – YES)

If advanced_matching data is missing, will it fail? (Answer – YES)

Who is responsible for transferring received events to the Action Processor (AP)?

Is the event sent by the source via Event Services?

How do routing services forward source events to the AP?

What is the architecture behind the Event Routing Service?

How does a message reach the AP?

## Context: User Onboarding & Access

How is a user onboarded to CitcoWorks?

Through tenant roles – AuthMaster

How is a user added to a persona?

How are features hidden?

Based on role

Based on persona

Could this become an onboarding problem?

Who is the AuthMaster team? (Bhanu knows a person in Hyderabad)

How is data synced from AuthMaster?

Real-time?

API-based?

Frequency?

What is the TTL (Time-To-Live) for a cache?

How often is the cache flushed? (e.g., on service restart)

What happens when the cache is flushed?

What happens to the cache if a user is deleted from AuthMaster?

Do users receive a persona on each login?

## Context: Task Assignment & Exceptions

How are tasks assigned to users? (Confluence Page)

What if a user is on vacation? (Human-In-the-Loop)

In an exception status, who is assigned to the exception task type?

Persona – but what if the persona does not exist in citcoworks?

In which scenarios are exceptions created?

System exception

Business exception

What is the process for time-card generation?

Where can all process IDs be found?

Answer: AskCitco maintains a table

## Context: Interaction Service

Where are the files stored?

@Bhanu – Action Required

#	Question

23	What is the architecture behind the Event Routing Service?

29	Who is the AuthMaster team? (Bhanu knows a person in Hyderabad)

31	What is the TTL (Time-To-Live) for a cache?

32	How often is the cache flushed? (e.g., on service restart)

40	What is the process for time-card generation?

44	How would we know that data has been synced?

46	Can we get access to the knowledge Graph to see what has been updated?

47	Can we get a confluence page for how to manage (create, deploy) AP via ERS?

48	How to install vscode plugin for deploying the AP?

Where is it available/ which marketplace?

49	URL of the place where AP is being saved?

50	Which CloudWatch groups, queries, logs that we need to investigate for action processors? (Confluence Page)

51	What is the process of onboarding persona in Citco-works?

52	How should we investigate (check sync) if persona exists in both CitcoWorks and optics?

53	Who defines catalogue for reference service?