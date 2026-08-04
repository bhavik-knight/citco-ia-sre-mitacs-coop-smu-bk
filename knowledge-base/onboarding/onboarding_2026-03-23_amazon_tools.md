# AWS Databases

## Relational

ACID property – Atomicity, Consistency, Isolation, Durability

### Amazon RDS

Single AZ – primary Instance

Multi AZ – Primary instance in one zone, stand by – in Another zone, Read Replica – in other zone

### Aurora

Pro - Scale automatically, perform faster, costs lower

Both suitable for OLTP (Online Transactional Process) - constantly changing data

### Redshift

– Data Warehouse

Analyze all data using standard SQL

Not DataLake – NoSQL

Concurrent scaling – fast query performance

Redshift-Spectrum – structure + semi structured

OLAP – Online Analytical Process

## NoSQL

### Dynamo DB

No rigid schema

Update schema any time

### DocumentDB

MongoDB compatible

Collection (Table)

Field (Column)

## In-Memory

### For Caching

Amazon Elasti-Cache:

Redis, Em-cached

Stored data in memory

DB caching faster performance on common data/queries

Data Partitioning

Memcached – multi-threaded, simple, scalable, lack of data-replication

Redis – Advance Data Structure, PubSub, message, Geospatial Support, Point in Time snapshot support – cluster mote – multiple primary nodes

### Amazon Key Spaces

Apache Cassandra – wide column datastore - compatible

### Neptune (Graph DB)

Fully managed, fast, reliable

Billions of relationships

Relationships are important here. Graphs Structure: Nodes (entity) + Edges (relation between entities)

Relational DB asks, "what data do I have?" Neptune asks "how is everything connected?"

### Amazon Time Stream

Serverless time series db

IoT & Operational Application

### Amazon Quantum Ledger (QLDB)

Immutable transactional logs

## Graph DB

### Neptune

https://ask.citco.com/share/o6xqMfRKqggiYN3XJCulr

Graph DB – AWS – Launch Amazon Neptune

Select Instances – They are large – No free tier

Create Read Replica in different zones

DB instance Identifier – NoSQL graph

VPC Subnet – Defaults

Other Settings – Defaults

Delete protection

Uncheck enable delete protection (to be able to delete)

Gremlin or RDF/SPARQL (which one?) not both, only one of those

RDG SPARQL – Specialized

Gremlin – Generic (Neo4j)

Jupyter Notebook – served by – Amazon Sagemaker EcoSystem

GraphDB – ML workload

No Graph Browser in Neptune (could be available now)

15 mins to create resources

2 instances (reader + writer)

High level monitoring

New type of client

EC2 + Jupyter Notebook + Neptune Instance.

Course link: https://www.linkedin.com/learning/cloud-nosql-for-sql-professionals/use-aws-neptune?u=88729490

## AWS Lambda

## Basics

Serverless

Old server – configure, monitor, server

Create Lamda Function

AWS manages, scales, secures server

Cheaper than EC2

Can write in any programming language

Native support for the following

Java, Go, PS, NodeJS, C#, Python, Ruby

Can choose available memory for run-time

## AWS CloudWatch

Collect – Monitor - Act - Analyze (CMAA)

Collect:

Metrics + Logs from AWS Resources, Application, Servers

Monitor:

Dashboard

Alerts

Act:

Automatically responds when something goes wrong with app resources

Triggers auto scaling, stopping instances (to reduce overage), trigger other workflows with Lambda, SNS, CloudFormation etc.

Analyze:

Deep dive and analyze existing metrics/logs

Strategy to improve and implement

Create metrics and logs again to verify and monitor

performance of the improvements

### AWS CloudWatch Services

### Metrics

Describe performance of apps/services

Free metrics for EC2, EBS, RDS

15 months retention

For EC2

1 min (detailed) – charged more

5 mins automatically – free

For metrics:

Default 1 min

1 seconds – high resolution

### Logs

Monitor, store, access log files from

EC2, CloudTrail Route 53, On-premises servers

Types:

Vended Logs – VPC, 53 (on behalf of customer)

Published by AW = API Gateway, Lambda, CloudTrail (30+ )

Log from On-Premises Servers (CloudWatch Agent, PutLogData API)

View, Query, Filter Logs, Archive – For future

CloudWatch Agent needs to be installed to do that

### Alarms

Triggers one or more applications based on metrics related to setting threshold

Metric Alarm – one single event

Composite Alarm – alarm states based on other alarms

How to?

Specify Metric

Configure actions

Actions are in the form of

SNS – notification

EC2 action – start, shutdown, terminate, reboot

Auto Scale

System Manager

Billing

Trigger Lambdas

Status

OK, In Alarm (outside the defined threshold), Insufficient Data

### Events

Event: Realtime stream of events that describe changes in AWS resources, schedule events (cron jobs)

Rules: Matches to events that we monitor and route to one or more targets

Targets:

EC2 instance

Lambda

Invoke ECS task

SNS Topics

SQS Queues

Works with

CloudTrail (Capture API calls)

CloudFormation (Declare event rules in templates)

Config (Detect and react changes in Data)

AKA Amazon EventBridge

New features added here

### CloudWatch Logs

CW Watch Agent

PutLogs API – (Lambda / AWS CLI)

Metric Filter (filter pattern) to check for anomalies, error code, warnings

Assign Metric based on filter

Difference between Alarms and Events

### Dashboard

Reusable graphs + visualize resources

Graph metrics and logs data into single dashboard

EC2 – CPU Utilization, memory, disk usages

## AWS CloudFormation

### Basics

AI Chat link - https://ask.citco.com/share/pSls4zyAvyTprA11JCOKG

IaC (Infrastructure as a Code)

Key concepts:

Templates, Stacks, Change Sets

Simple Infrastructure management

Quickly replicate Infrastructure (through templates)

Easily control and track changes to Infrastructure (by rollback actions / version control on templates)

Template:

Define

how resources are created

connection between resources

permissions

Write Infrastructure in Code

<YAML> or <JSON> file for templates

Declare multiple resources that work together for infrastructure

Stack:

Manage related resources as a single unit

Defined by the stack’s CF-template

E.g. EC2 Instance, Security Instance, Autoscaling, RDS – etc. resources – CF – Template.

Change Set:

Help in previewing how the stacks update might impact the running resources

Before making changes, generate a change set – which is summary of proposed changes

Allows to see impact of changes in resources on the current stack

### CF Templates:

Resources, versions, descriptions and metadata

Difference between parameters, mappings and output

JSON / YAML Files

Difference between Stack / Template

Stack - set of resources treated as a single unit

Template – helps create/update/edit stacks

Read template: (all other sections are optional except resources)

Resources (Mandatory)

Version

Description

Metadata

Parameters

Rules

Mapping

Conditions

Output