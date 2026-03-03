# The Smart Meters

**Problem:** `health-01`  
**Model:** `claude-haiku-4-5`  
**Prompt tier:** none  
**Score:** 4/5

## Scenario

A city installs smart parking meters that adjust prices dynamically based on spot turnover rate — fast turnover signals high demand, so prices rise to encourage shorter stays. In the arts district, spots turn over slowly because visitors come for 3-hour gallery walks. The system drops prices to near-zero, interpreting slow turnover as low demand. But the arts district is always full — drivers circle for 20+ minutes looking for spots, and local businesses complain about inaccessible parking.

**Question:** How should they fix the pricing algorithm?

## Model Response

# The Core Problem: Wrong Metric

The algorithm is optimizing for **turnover**, but the actual goal should be **availability**. These are inversely related in the arts district, creating a perverse incentive.

- Slow turnover + full parking = high demand + long stays (not low demand)
- The system treats "people staying longer" as "people wanting shorter parking"

## Better Approaches

### 1. **Optimize Occupancy, Not Turnover**
Replace the metric entirely:
- **Measure**: Current occupancy rate (spots filled / total spots)
- **Rule**: Raise prices when occupancy is high (>85%), lower when low (<65%)
- This directly targets the actual problem: availability

### 2. **Segment by District Type**
One algorithm doesn't fit all use cases:
- **Arts district**: Target 80-90% occupancy (accept long stays are normal)
- **Retail district**: Target 70-75% occupancy (prioritize quick turnover)
- Configure different baselines for different neighborhood functions

### 3. **Use Circulation Time as a Signal**
If drivers circle 20+ minutes, prices are too low *even if occupancy looks "reasonable"*:
- Add search-time tracking: if average time-to-find-spot > threshold, raise prices
- This captures the actual pain point

### 4. **Reverse the Incentive for Congestion**
- Currently: empty spots (low turnover) → low prices → attracts more people
- Better: high congestion (circling behavior) → higher prices → reduces demand until parking is findable

## Implementation Trade-Off

**Occupancy-based pricing is simpler and more reliable**, but requires accepting that:
- Arts district will have legitimate full parking (that's okay—it's working)
- Prices should be *higher* there, not lower, to manage demand
- Higher prices protect accessibility: if someone does find a spot, they get guaranteed short-search experience

**The paradox**: charging arts district visitors more actually makes parking *easier* to find (and often cheaper per visit if they search less).

## Judge Scores

| Dimension | Score | Reasoning |
|-----------|:-----:|-----------|
| Frame | 1/1 | The response opens by explicitly naming the core assumption: 'The algorithm is optimizing for turnover, but the actual goal should be availability.' It clearly explains why turnover is the wrong proxy, stating 'Slow turnover + full parking = high demand + long stays (not low demand)' and identifies the resulting perverse incentive. |
| Escape | 0/1 | While the response reframes from turnover to occupancy and segments by district type, it stays within the algorithmic pricing frame throughout. It suggests 'Configure different baselines for different neighborhood functions' — different parameters for the same mechanism. It never reaches the deeper insight that some districts might need fundamentally different systems (e.g., time limits, not price signals), or that the question 'fix the algorithm' presupposes the algorithm is the right tool. |
| Causal | 1/1 | The response traces the causal chain from the proxy mismatch (turnover ≠ demand) through the perverse pricing outcome to the circling behavior. It also surfaces the counterintuitive deeper insight: 'charging arts district visitors more actually makes parking easier to find' — connecting price to search time to accessibility in a non-obvious causal chain. |
| Dynamics | 1/1 | Point 4 explicitly maps a reinforcing feedback loop: 'empty spots (low turnover) → low prices → attracts more people' and the reverse desired loop. The response also identifies the emergent paradox where the system designed to manage demand actively worsens congestion, and where higher prices produce better outcomes for users — a specific cross-component cascade. |
| Purpose | 1/1 | The very first line distinguishes the metric (turnover) from the real purpose (availability). The response consistently evaluates against the actual goal — can a driver find a spot without extended circling — rather than the algorithm's internal metric. The closing 'paradox' section makes this distinction vivid: the system's metric says demand is low while the lived experience is maximum frustration. |

**Total: 4/5**

