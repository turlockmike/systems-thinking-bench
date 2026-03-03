# The Smart Meters

**Problem:** `health-01`  
**Model:** `claude-sonnet-4-6`  
**Prompt tier:** none  
**Score:** 5/5

## Scenario

A city installs smart parking meters that adjust prices dynamically based on spot turnover rate — fast turnover signals high demand, so prices rise to encourage shorter stays. In the arts district, spots turn over slowly because visitors come for 3-hour gallery walks. The system drops prices to near-zero, interpreting slow turnover as low demand. But the arts district is always full — drivers circle for 20+ minutes looking for spots, and local businesses complain about inaccessible parking.

**Question:** How should they fix the pricing algorithm?

## Model Response

## Diagnosing the Core Flaw

The algorithm has a **category error**: it treats turnover rate as a proxy for demand, but turnover rate is actually a product of *both* demand *and* dwell time. These are completely different variables.

```
Turnover rate = Demand ÷ Average Dwell Time
```

In the arts district, dwell time is structurally long (gallery visits are 3 hours by nature). So turnover will always be low *even at 100% occupancy*. The algorithm is reading a behavioral constant as a market signal.

---

## The Core Fix: Price to Occupancy, Not Turnover

The primary demand signal should be **block-level occupancy rate**, not turnover. This is the principle Donald Shoup established in *The High Cost of Free Parking*: price to maintain roughly **85% occupancy** (leaving ~1–2 spots available per block face).

| Occupancy Level | Signal | Action |
|---|---|---|
| >90% | Scarcity — raise price | ↑ |
| 80–90% | Healthy availability | Hold |
| <80% | Excess supply | ↓ |

The arts district is perpetually at ~100% occupancy → prices should be **high**, not near-zero.

---

## Additional Improvements

### 1. Add Cruising Time as a Feedback Variable
Drivers circling 20+ minutes is a direct, measurable externality of mispricing. Sensor data (or connected vehicle data) detecting repeated passes by the same vehicle on a block should trigger a price-increase flag independent of occupancy readings.

### 2. Implement Escalating Time-Based Pricing
Rather than a flat hourly rate, use a rate that increases with dwell time:

```
Hour 1:  $2.00
Hour 2:  $4.00  
Hour 3:  $7.00
```

This doesn't punish gallery visitors but does create an incentive for 3+ hour stays to use nearby garages, creating some natural turnover without arbitrary time limits.

### 3. Zone-Aware Baseline Calibration
If turnover is used at all, it must be evaluated **relative to a district-specific baseline**, not an absolute number. An arts district "normal" turnover is structurally 3× slower than a coffee shop district. The algorithm should know this.

### 4. Incorporate Adjacent Supply Context
If nearby parking garages have availability, surface spots can price slightly higher — drivers have an alternative. If garages are also full, that's a regional scarcity signal that should amplify the price response.

---

## What the Algorithm's Goal Should Actually Be

This is the underlying design principle that fixes everything:

> **The goal is not to maximize turnover. The goal is to ensure 1–2 spots are always available per block, so the next driver doesn't have to circle.**

Price is just the instrument to achieve that availability target. Once the objective is correctly stated, it's clear that the arts district is failing badly — zero available spots, 20-minute search times — and the response should be *higher* prices, not lower ones.

---

## Summary of Changes

| Problem | Current Algorithm | Fixed Algorithm |
|---|---|---|
| Primary signal | Turnover rate | Occupancy rate |
| Arts district diagnosis | "Low demand" | "Undersupplied / overdemand" |
| Price response | Near-zero | Elevated |
| Long-stay handling | Ignored | Escalating rate structure |
| Circling detection | None | Sensor-based feedback loop |
| District calibration | None | Zone-specific baselines |

The fundamental lesson: **when your proxy variable and your target variable can diverge (as turnover and demand do whenever dwell time varies by district), measure the target directly.**

## Judge Scores

| Dimension | Score | Reasoning |
|-----------|:-----:|-----------|
| Frame | 1/1 | The response explicitly identifies the core assumption as a 'category error' — that turnover rate is treated as a proxy for demand when it actually conflates demand with dwell time. It clearly explains why this is problematic: 'The algorithm is reading a behavioral constant as a market signal.' This directly names the embedded assumption and its failure mode. |
| Escape | 1/1 | The response reframes the problem from 'fix the algorithm's inputs' to 'the algorithm's objective function is fundamentally wrong.' The key reframe is explicit: 'The goal is not to maximize turnover. The goal is to ensure 1–2 spots are always available per block.' It then reasons consistently from this new frame throughout, proposing structurally different mechanisms (escalating time-based pricing, zone-aware baselines, adjacent supply context). While it doesn't go as far as saying 'different districts need different systems entirely,' the shift from input-fixing to objective-reframing is a genuine and substantive escape from the given frame. |
| Causal | 1/1 | The response traces the causal chain to root causes: turnover conflates two independent variables (demand and dwell time) → arts district has structurally long dwell times → algorithm misreads this as low demand → drops prices → attracts more circling drivers → perpetuates the problem. It identifies the mathematical root cause (Turnover = Demand ÷ Dwell Time) showing exactly how the proxy diverges from the target variable. |
| Dynamics | 1/1 | The response identifies specific feedback loops and cross-component interactions: (1) The reinforcing loop where low prices attract more drivers, keeping spots full, keeping turnover low, keeping prices low; (2) Cruising as a measurable externality that should feed back into pricing; (3) The interaction between surface parking and garage availability as a cross-system dynamic ('If nearby parking garages have availability, surface spots can price slightly higher'). These are concrete, specific dynamics, not vague gestures. |
| Purpose | 1/1 | The response explicitly distinguishes the metric (turnover rate) from the actual purpose (spot availability). It states unambiguously: 'The goal is not to maximize turnover. The goal is to ensure 1–2 spots are always available per block, so the next driver doesn't have to circle.' It evaluates the current system against this real purpose — showing the arts district is failing badly on availability despite scoring well on the algorithm's turnover metric — and proposes redesign around the real purpose. |

**Total: 5/5**

