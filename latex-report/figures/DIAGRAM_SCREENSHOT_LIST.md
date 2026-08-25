# Diagram Screenshot List for SMU Report

**Instructions:** Open each file in VS Code/Kiro, preview the Mermaid diagram, and take a screenshot. Save with the filename specified below in `latex-report/figures/`.

**Legend:** ✅ = Captured | ❌ = Missing | ⚠️ = Optional

---

## Priority 1: Core Architecture Diagrams (Must Have)

### 1. AMG Dashboard Architecture ✅

**File:** `C:\Users\bbhagat\dev_work\AWS_Projects\ia-it-sre-infrastructure-monitoring-amg\docs\guides\architecture.md`
**Screenshot Name:** `fig-amg-architecture.png`
**Description:** Main SRE dashboard architecture showing CloudWatch → Grafana flow
**Status:** CAPTURED

### 2. AMG Deployment Flow ✅

**File:** `C:\Users\bbhagat\dev_work\AWS_Projects\ia-it-sre-infrastructure-monitoring-amg\docs\guides\architecture.md`
**Screenshot Name:** `fig-amg-deployment-flow.png`
**Description:** CI/CD pipeline from CodeCommit → CodePipeline → AMG
**Status:** CAPTURED (also `fig-amg-deployment-flow-1.png`)

### 3. Alarm Notification Architecture ✅

**File:** `C:\Users\bbhagat\dev_work\AWS_Projects\ia-it-sre-infrastructure-monitoring-amg\docs\operations\alarms-and-notifications.md`
**Screenshot Name:** `fig-alarm-notification-flow.png`
**Description:** CloudWatch Alarm → SNS → Lambda notification flow
**Status:** CAPTURED

### 4. Resource Discovery Flow (3-Tier Fallback) ✅

**File:** `C:\Users\bbhagat\dev_work\AWS_Projects\ia-resources-monitoring\docs\ARCHITECTURE.md`
**Screenshot Name:** `fig-resource-discovery-flow.png`
**Description:** Registry API → S3 → Local file fallback chain
**Status:** CAPTURED

### 5. Infrastructure Inventory API Architecture ✅

**File:** `C:\Users\bbhagat\dev_work\AWS_Projects\ia-it-sre-infrastructure-inventory\docs\architecture\architecture.md`
**Screenshot Name:** `fig-inventory-api-architecture.png`
**Description:** Lambda API Gateway architecture for resource inventory
**Status:** CAPTURED

### 6. IAM Role Architecture (Bonus) ✅

**File:** (User provided — not from repo docs)
**Screenshot Name:** `fig-IAM-Role-Architecture.png`
**Description:** IAM role architecture diagram
**Status:** CAPTURED

---

## Priority 2: RPA-LLM Agent Diagrams (Work Stream 6 - AI/GenAI)

### 7. RPA-LLM High-Level Architecture ✅

**File:** `C:\Users\bbhagat\dev_work\AWS_Projects\ml-rpa-status-llm-agent\docs\technical\architecture.md`
**Screenshot Name:** `fig-rpa-llm-architecture.png`
**Description:** LibreChat UI → ECS Fargate (FastAPI) → Bedrock Agent architecture
**Status:** CAPTURED

### 8. RPA-LLM Component Interaction Flow ✅

**File:** `C:\Users\bbhagat\dev_work\AWS_Projects\ml-rpa-status-llm-agent\docs\technical\architecture.md`
**Screenshot Name:** `fig-rpa-llm-interaction-flow.png`
**Description:** Sequence diagram: LibreChat → ECS → Bedrock → Lambda → KB
**Status:** CAPTURED

### 9. Lambda Functions Categories ✅

**File:** `C:\Users\bbhagat\dev_work\AWS_Projects\ml-rpa-status-llm-agent\docs\technical\lambda-functions.md`
**Screenshot Name:** `fig-rpa-llm-lambda-categories.png`
**Description:** Lambda function groupings (Core Agent, KB, Data Extract, Analytics, Utility)
**Status:** CAPTURED

### 10. Scheduled Functions Timeline ✅

**File:** `C:\Users\bbhagat\dev_work\AWS_Projects\ml-rpa-status-llm-agent\docs\technical\lambda-functions.md`
**Screenshot Name:** `fig-rpa-llm-schedule-timeline.png`
**Description:** UTC timeline showing EventStore, IRCOEKB, KB Ingestion, Usage Report schedules
**Status:** CAPTURED

---

## Priority 3: X-Ray & Tracing Diagrams (Work Stream 4) ⚠️

### 11. SQS Trace Propagation ⚠️ OPTIONAL

**File:** `C:\Users\bbhagat\dev_work\BitBucket_Projects\ia_meso_process\.kiro\specs\IISS-842-sqs-trace-propagation\design.md`
**Screenshot Name:** `fig-sqs-trace-propagation.png`
**Description:** Lambda Producer → SQS → Lambda Consumer trace flow
**Location in doc:** Look for the Mermaid diagram inside `<details>` block
**Status:** OPTIONAL — Skip if not needed

### 12. ECS ADOT Sidecar Architecture ⚠️ OPTIONAL

**File:** `C:\Users\bbhagat\dev_work\BitBucket_Projects\ia_meso_process\.kiro\specs\IISS-839-ecs-adot-sidecar\design.md`
**Screenshot Name:** `fig-ecs-adot-sidecar.png`
**Description:** ECS Task with ADOT collector sidecar
**Location in doc:** Look for the Mermaid diagram inside `<details>` block
**Status:** OPTIONAL — Skip if not needed

---

## Priority 4: Service-Specific Diagrams

### 13. MSK Cluster Topology ✅

**File:** `C:\Users\bbhagat\dev_work\AWS_Projects\ia-it-sre-infrastructure-monitoring-amg\docs\meridian-service-inventory\05-msk.md`
**Screenshot Name:** `fig-msk-topology.png`
**Description:** MSK cluster/topic/consumer group relationships
**Status:** CAPTURED

### 14. Request Flow (Concepts) ✅

**File:** `C:\Users\bbhagat\dev_work\AWS_Projects\ia-it-sre-infrastructure-monitoring-amg\docs\guides\concepts-explained.md`
**Screenshot Name:** `fig-request-flow-concepts.png`
**Description:** How a request flows through monitored services
**Status:** CAPTURED

---

## Priority 5: Live Dashboard Screenshots (From Grafana)

### 15. Grafana Dashboard - Overview Row ✅

**Source:** AMG Console (DEV workspace)
**Screenshot Name:** `fig-grafana-overview-row.png`
**Description:** Screenshot of Row 1-2 showing health overview and performance
**Status:** CAPTURED

### 16. Grafana Dashboard - Lambda Row ✅

**Source:** AMG Console (DEV workspace)
**Screenshot Name:** `fig-grafana-lambda-row.png`
**Description:** Screenshot of Lambda monitoring panels
**Status:** CAPTURED

### 17. Grafana Dashboard - ECS Row ✅

**Source:** AMG Console (DEV workspace)
**Screenshot Name:** `fig-grafana-ecs-row.png`
**Description:** Screenshot of ECS monitoring panels
**Status:** CAPTURED

### 18. CloudWatch Dashboard - Lambda Overview ✅

**Source:** AWS CloudWatch Console (DEV)
**Screenshot Name:** `fig-cloudwatch-lambda-dashboard.png`
**Description:** Screenshot of CloudWatch Lambda dashboard (ia-resources-monitoring)
**Status:** CAPTURED

### 19. X-Ray Service Map ✅

**Source:** AWS X-Ray Console or Grafana X-Ray panel
**Screenshot Name:** `fig-xray-service-map.png`
**Description:** X-Ray service map showing trace topology
**Status:** CAPTURED

---

## Priority 6: CI/CD Pipeline Screenshots ❌

### 20. CodePipeline - AMG Dashboard Pipeline ❌

**Source:** AWS CodePipeline Console
**Screenshot Name:** `fig-codepipeline-amg.png`
**Description:** Screenshot of ia-it-sre-infrastructure-monitoring pipeline
**Status:** NOT CAPTURED — Optional

### 21. CodePipeline - Inventory API Pipeline ❌

**Source:** AWS CodePipeline Console
**Screenshot Name:** `fig-codepipeline-inventory.png`
**Description:** Screenshot of ia-it-sre-infrastructure-inventory pipeline
**Status:** NOT CAPTURED — Optional

---

## Summary Table

| #  | Filename                            | Source Type     | Priority | Status |
| -- | ----------------------------------- | --------------- | -------- | ------ |
| 1  | fig-amg-architecture.png            | Mermaid         | P1       | ✅     |
| 2  | fig-amg-deployment-flow.png         | Mermaid         | P1       | ✅     |
| 3  | fig-alarm-notification-flow.png     | Mermaid         | P1       | ✅     |
| 4  | fig-resource-discovery-flow.png     | ASCII/Mermaid   | P1       | ✅     |
| 5  | fig-inventory-api-architecture.png  | Mermaid         | P1       | ✅     |
| 6  | fig-IAM-Role-Architecture.png       | User Provided   | P1       | ✅     |
| 7  | fig-rpa-llm-architecture.png        | ASCII           | P2       | ✅     |
| 8  | fig-rpa-llm-interaction-flow.png    | ASCII           | P2       | ✅     |
| 9  | fig-rpa-llm-lambda-categories.png   | ASCII           | P2       | ✅     |
| 10 | fig-rpa-llm-schedule-timeline.png   | ASCII           | P2       | ✅     |
| 11 | fig-sqs-trace-propagation.png       | Mermaid         | P3       | ⚠️     |
| 12 | fig-ecs-adot-sidecar.png            | Mermaid         | P3       | ⚠️     |
| 13 | fig-msk-topology.png                | Mermaid         | P4       | ✅     |
| 14 | fig-request-flow-concepts.png       | Mermaid         | P4       | ✅     |
| 15 | fig-grafana-overview-row.png        | Live Screenshot | P5       | ✅     |
| 16 | fig-grafana-lambda-row.png          | Live Screenshot | P5       | ✅     |
| 17 | fig-grafana-ecs-row.png             | Live Screenshot | P5       | ✅     |
| 18 | fig-cloudwatch-lambda-dashboard.png | Live Screenshot | P5       | ✅     |
| 19 | fig-xray-service-map.png            | Live Screenshot | P5       | ✅     |
| 20 | fig-codepipeline-amg.png            | Live Screenshot | P6       | ❌     |
| 21 | fig-codepipeline-inventory.png      | Live Screenshot | P6       | ❌     |

---

## Capture Summary

**Total Diagrams:** 21
- ✅ **Captured:** 17
- ⚠️ **Optional (skippable):** 2
- ❌ **Not captured:** 2 (CodePipeline screenshots — optional)

**All essential diagrams are captured!** The missing CodePipeline screenshots (P6) are optional and can be skipped if not needed.

---

## Files in figures/ folder

```
fig-alarm-notification-flow.png     ✅
fig-amg-architecture.png            ✅
fig-amg-deployment-flow.png         ✅
fig-amg-deployment-flow-1.png       ✅ (duplicate)
fig-cloudwatch-lambda-dashboard.png ✅
fig-grafana-ecs-row.png             ✅
fig-grafana-lambda-row.png          ✅
fig-grafana-overview-row.png        ✅
fig-IAM-Role-Architecture.png       ✅
fig-inventory-api-architecture.png  ✅
fig-msk-topology.png                ✅
fig-request-flow-concepts.png       ✅
fig-resource-discovery-flow.png     ✅
fig-rpa-llm-architecture.png        ✅
fig-rpa-llm-interaction-flow.png    ✅
fig-rpa-llm-lambda-categories.png   ✅
fig-rpa-llm-schedule-timeline.png   ✅
fig-xray-service-map.png            ✅
smu_logo.png                        (logo)
```

