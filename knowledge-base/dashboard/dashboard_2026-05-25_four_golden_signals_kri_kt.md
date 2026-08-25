# Four Golden Signals — KT Session with Kri Labos
**Date:** May 25, 2026 — 9:47 AM
**Meeting:** Centralized Dashboard (IISS-487 context)
**Presenter:** Kristia Marie Labos (Kri), Senior SRE Mentor

---

## 1. Response Time / Latency
- Client-side response time (general) — for all apps in Dynatrace; later advanced mode
- How long requests take to fulfill a response
- Overall → HoneyComb view
- Response time → Top List panel
- 200ms → 2s → performance degradation threshold

## 2. Throughput / Traffic
- Disk throughput read/write
- Number of requests per transaction
- Load Trends visualization
- Load spikes for one hour → autoscaling response
- Load high throughout → increase capacity
- Sudden load spike → could be DDoS; additional Gateway; Load Balancer
- Team proposes mitigation (load balancer count decisions made elsewhere)

## 3. Errors / Failure Rate
- Graph for failure rate — edit using advanced mode (next meeting)
- 5xx errors; 4xx errors; 3xx errors
- % rate is required
- 3–5% threshold; more than 5% = service issue or deployment problem
- Purpose: detect incidents quickly, track reliability, compliance to SLO/SLA
- Logs in error-rate → different dashboard for error logs (another tool)
- e.g. Spring-boot, Go, Kibana for log-level errors

## 4. Saturation / Resource Usage
- How well our system handles its current load
- CPU, Memory, Thread Count, DB connection counts
- CPU 95% → system at capacity → may slow down
  - BPM: 80% is acceptable threshold
- Purpose: prevent outages, capacity planning, bottleneck prediction

---

## TODOs from the session (action items for IISS-487 dashboard):
- Fix panel data
- Explore different types of graphs
- Add Top K panel
- FIFO Queue for E-binder → threshold for queue (10/20) — no duplicates
- Redis row
- RDS row
- Explore more AWS regions
- SQS needed to check backlog of Kafka queues
- SQS AWS — queues are very stable
- Messages IN/OUT for Kafka → No Bytes in and out (key metric)
