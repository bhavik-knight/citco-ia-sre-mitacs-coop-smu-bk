# IA Support Model

**Source:** `smu/KnowledgeBase/INTAUT-IA Support Model-150826-193649.pdf`

---

## Overview

This document outlines the three-tiered support model for Innovation IT services,
incorporating AI-driven first-line support, specialized IT support, and SRE expertise.

---

## Support Schedule (Follow the Sun)

| Region | Shift | Hours (ET) |
|--------|-------|-----------|
| Asia — 1st shift | 2 resources | 6 PM – 2 AM ET |
| Asia — 2nd shift | 1 resource | 2 AM – 11 AM ET |
| **North America** | **1 resource** | **11 AM – 7 PM ET** |

North America slot = our SRE shift for RPA support rotation.

---

## SLA Matrix

| Support Level | Acknowledgement | Resolution Target | Coverage |
|--------------|----------------|------------------|---------|
| L1 — AI Support | Immediate | 15 min | 24/7 |
| L2 — Innovation IT Support | 1 hour | 8 hours | Follow the Sun |
| L3 — SRE Support | 1 day | As per Incident | Follow the Sun |

Platform incident = RPA, AWS, Macro are either inaccessible or have a major
performance degradation impacting service.

---

## Ticket Ownership Rules

1. **Acknowledge = Own** — The person who acknowledges a ticket is responsible for driving
   it to resolution. Escalate to process owner and email details if unable to resolve,
   but always provide initial observation done.
2. **SLA is Team Accountability** — If a ticket is approaching SLA breach, the on-shift
   team is responsible for picking it up regardless of who originally acknowledged it.
3. **Exceptions** — Processes pending formal handover (not yet trained across shifts).

---

## Shift Handover Process

### Outgoing Shift
- Update all open SD tickets with current status, actions taken, and blockers
- Log shift summary including open tickets on Confluence shift handover page
- Flag any tickets approaching SLA breach to incoming shift (Confluence + Teams if urgent)

### Incoming Shift
- Review Confluence shift handover log at start of shift
- Pick up any tickets approaching SLA breach immediately
- Acknowledge new incoming tickets within Response Time SLA

### Handover Note Template (in SD Ticket)
- **Actions Taken** — What was done during this shift
- **Pending** — What remains to be done
- **Blockers** — If any (access, dependency, vendor response)
- **Next Step** — Clear instruction for incoming shift
- **Status** — In Progress / Blocked / Pending Vendor / Pending Info
- **SLA Deadline** — Date/Time

---

## Support Levels Structure

### Level 1 — AI Support (RPA Support Agent)
- **Team:** AI/LLM System | **Hours:** 24/7 | **Escalation:** IA_IT_SRE@citco.com
- Responsibilities: Real-time process status monitoring, user inquiries, basic
  troubleshooting, FAQ responses, knowledge base queries, standard documentation

### Level 2 — Innovation IT Support
- **Team:** Innovation IT Support Team | **Hours:** 24/5 | **Contact:** innovation_it_support@citco.com
- **Bot Management & Analysis:** Complex bot failure analysis, root cause investigation,
  failure pattern identification, impact assessment, resolution planning, bot performance tuning
- **Process Management:** Process optimization, configuration management, parameter optimization
- **Technical Support:** Advanced troubleshooting, system integration problems, service requests
- **Access Management:** User access management, privileged access control, access audit trails
- **IA Incidents:** Open IA Incident JIRA and email IA_INCIDENTS@citco.com; keep ia_it_sre@citco.com in CC

#### Escalation Criteria to L3
- Unresolved by L2 / requiring deep technical expertise / system-wide impact
- Critical: production outages, major service degradation, data integrity, security incidents
- Performance: severe degradation, resource exhaustion, scaling issues

### Level 3 — SRE Support
- **Team:** Innovation IT SRE | **Contact:** ia_it_sre@citco.com | **Coverage:** Follow the Sun
- **Response Time SLA:** 1 day

#### L3 Responsibilities
1. **Production Support & Troubleshooting**
   - Critical issue resolution (complex production issues, system-wide failures,
     performance degradation, service disruptions, integration failures)
   - Advanced technical support (deep-dive analysis, complex bug investigation,
     system behavior analysis, performance bottlenecks, service dependencies)

2. **Root Cause Analysis**
   - Detailed technical analysis, impact assessment, failure pattern identification,
     system log analysis, performance metrics review
   - Solution design, fix implementation, testing and validation, documentation updates,
     prevention measures

3. **Service Improvement**
   - Performance optimization (response time, resource utilization, system efficiency,
     bottleneck elimination)
   - Reliability enhancement (stability improvements, error reduction, service resilience,
     recovery procedures, failure prevention)

4. **IA Incidents**
   - Open IA Incident JIRA and email IA_INCIDENTS@citco.com; keep ia_it_sre@citco.com in CC
   - Send email notice with ticket to application contacts for integration issues

5. **Platform Support / Monitoring**
   - SRE responsible for configuring alerts (IISS-487 and related)

---

## Channels We Monitor During Support

- **SD Portal** — primary ticket queue (IISS-267 RPA Support Standardization)
- **innovation_it_support@citco.com** — L2 support email; we check and handle L2 items
- **IA_INCIDENTS@citco.com** — IA incident notifications
- **ia_it_sre@citco.com** — SRE-level escalations
- **Microsoft Teams** — Direct messages, group channels, urgent shift-to-shift flags
- **Confluence** — Shift handover log, process runbooks, SOP documentation

---

## Support Scope

### In Scope
- Intelligent Automation (budgeted processes): AWS (ECS, EC2, Lambdas), Blue Prism,
  CDI, VBA macros (Citco Recon Tools), UiPath, LLM Agent
- Automation Support (1–3 requests per year)

### Out of Scope
- Enhancement requests over 40 hours
- BPM support (handled separately under BPM support budget)
- Bank support (legacy BP migration processes owned by Bank IT)
- Citizen developer support

---

## Support Handover Checklist (Process Onboarding to Support)

1. **Hypercare** — Process under developer hypercare for 2 weeks, no open issues
2. **Support Documentation** — Developer provides AWS/UiPath support guide
3. **Support Documentation Review** — Support team reviews and approves
4. **Business User Guide** — Uploaded to TO SharePoint, signed off by business team
5. **Handover Sessions** — Developer schedules handover to support team after hypercare
