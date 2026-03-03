# The Green Dashboard

**Problem:** `infra-03`  
**Model:** `claude-haiku-4-5`  
**Prompt tier:** none  
**Score:** 5/5

## Scenario

A platform team builds an observability dashboard. Every service has health checks: CPU < 80%, memory < 90%, error rate < 1%, latency p99 < 500ms. All metrics are green. Users are reporting that the application 'feels slow.' The team investigates each service individually — all healthy.

**Question:** Where is the problem?

## Model Response

# The Problem: Missing End-to-End Observability

You're observing a classic blindspot: **the team is measuring service health in isolation, not end-to-end user experience.**

## What's Actually Happening

Several likely culprits:

### 1. **Cascading Latencies Across Services**
- Service A: p99 latency = 150ms ✓
- Service B: p99 latency = 150ms ✓  
- Service C: p99 latency = 150ms ✓
- **User request hits all three sequentially = 450ms+ perceived latency**

The p99 of a sum ≠ sum of p99s. When services call each other, latencies compound.

### 2. **Missing Distributed Tracing**
They can't see:
- Request queuing between services
- Database connection pool exhaustion (appears as latency spike, not CPU/memory spike)
- Lock contention or synchronization wait times
- Third-party API delays

### 3. **Incomplete Metrics Coverage**
Their health checks don't measure:
- **End-to-end request latency** (edge to user)
- Higher percentiles (p99.9, max) where user pain lives
- Time spent *waiting* vs time spent *processing*
- Critical user journeys

### 4. **Resource Saturation Signals Missing**
- Database connections exhausted (requests queue)
- Thread pool saturation
- Network I/O bottlenecks
- Garbage collection pauses

## The Fix

- **Add distributed tracing** (Jaeger, Datadog) to see request flows
- **Define SLOs for user journeys**, not individual services
- **Monitor higher percentiles** (p95, p99, p99.9)
- **Add queue depth/wait time metrics**
- **Correlate frontend performance** with backend metrics

**TL;DR**: You're measuring if the engine is healthy, not if the car drives smoothly. 🚗

## Judge Scores

| Dimension | Score | Reasoning |
|-----------|:-----:|-----------|
| Frame | 1/1 | The response explicitly names the embedded assumption: 'the team is measuring service health in isolation, not end-to-end user experience.' The TL;DR metaphor ('measuring if the engine is healthy, not if the car drives smoothly') further clarifies why this frame is problematic. |
| Escape | 1/1 | The response clearly reframes from per-service health to user-experience-level observability. It reasons from this new frame throughout, proposing SLOs for user journeys rather than individual services, distributed tracing across request flows, and edge-to-user latency measurement. |
| Causal | 1/1 | The response traces the causal chain: individual services appear healthy → but latencies compound across sequential calls → because 'p99 of a sum ≠ sum of p99s' → root cause is that the dashboard architecture measures the wrong thing. It also identifies deeper causes like request queuing between services, connection pool exhaustion, and wait time vs. processing time distinctions. |
| Dynamics | 1/1 | The response identifies specific emergent behavior: three services at 150ms each producing 450ms+ user-perceived latency, with the explicit note that 'p99 of a sum ≠ sum of p99s.' It identifies cross-component cascades (sequential service calls compounding) and mentions inter-service queuing as an emergent phenomenon invisible to per-component metrics. |
| Purpose | 1/1 | The response clearly distinguishes the metric (per-service CPU, memory, error rate, latency thresholds) from the actual purpose (user experience). It explicitly states 'Define SLOs for user journeys, not individual services' and the TL;DR encapsulates this: 'measuring if the engine is healthy, not if the car drives smoothly.' |

**Total: 5/5**

