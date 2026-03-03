# The Helpful Cache

**Problem:** `infra-01`  
**Model:** `claude-haiku-4-5`  
**Prompt tier:** none  
**Score:** 3/5

## Scenario

A web application's response times have degraded from 50ms to 1200ms over the past month. The team adds a Redis cache in front of the database. Response times improve to 40ms. Two months later, the database server's disk fills up and crashes. Investigation reveals the database has grown 10x in that period.

**Question:** What went wrong?

## Model Response

# The Core Problem: They Treated the Symptom, Not the Cause

The team made a classic mistake: **they cached their way out of investigating the real issue.**

## What Actually Went Wrong

1. **Misdiagnosed the Problem**
   - The degraded response times (50ms → 1200ms) were likely a *symptom* of the database growing and queries slowing down
   - Instead of asking "Why is the database growing?", they asked "How do we make queries faster?"

2. **Cache Masked the Real Problem**
   - Redis improved response times dramatically (40ms), which felt like victory
   - This success reduced urgency to investigate the underlying cause
   - The database continued growing 10x unaddressed for 2 months

3. **No Monitoring or Data Lifecycle Management**
   - They never implemented:
     - Database growth monitoring/alerting
     - Data retention/cleanup policies
     - Data archival strategies
     - Investigation into *why* data was accumulating

## What Likely Caused the 10x Growth

- Unintended data duplication
- Logs/audit trails never being purged
- Old test data not being cleaned up
- A data sync/import process running incorrectly
- Application bugs inserting duplicate records

## The Lesson

**Caching is great—but not as a substitute for root cause analysis.** 

The correct approach would have been:
1. Investigate why response times degraded initially
2. Monitor database growth metrics
3. *Then* apply performance optimizations like caching
4. Maintain ongoing observability of database health

They created technical debt that eventually came due spectacularly (database crash).

## Judge Scores

| Dimension | Score | Reasoning |
|-----------|:-----:|-----------|
| Frame | 1/1 | The response explicitly names the embedded assumption: 'Instead of asking Why is the database growing?, they asked How do we make queries faster?' and calls it a misdiagnosis. It clearly identifies that the team framed the problem as a performance/caching issue rather than investigating the symptom. |
| Escape | 1/1 | The response reframes the problem as one of root cause analysis rather than performance optimization. It reasons from this new frame by proposing they should have investigated why response times degraded before applying caching, and evaluates the outcome from this reframed perspective. |
| Causal | 0/1 | The response traces from slow responses back to database growth, but critically misses the amplification chain. It says the cache 'masked' the problem and the database 'continued growing 10x unaddressed,' treating the growth rate as independent of the cache. The deep insight—that the cache enabled more traffic which drove more writes which accelerated the very growth causing the problem—is absent. The 'What Likely Caused the 10x Growth' section lists generic possibilities (logs, duplication) rather than the cache-driven amplification. |
| Dynamics | 0/1 | The response does not identify the critical feedback loop: cache → more capacity → more traffic → more writes → faster data growth → bigger crash. It treats the cache and the data growth as parallel issues (cache masks, growth continues independently) rather than as a reinforcing feedback loop where the fix actively amplifies the root cause. |
| Purpose | 1/1 | The response notes that the 40ms response time 'felt like victory' and that 'this success reduced urgency to investigate the underlying cause,' effectively distinguishing between the metric (response time) and the actual purpose (sustainable system health). It evaluates the outcome against real system reliability rather than just the response time number. |

**Total: 3/5**

