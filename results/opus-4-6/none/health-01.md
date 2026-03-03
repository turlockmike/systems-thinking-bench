# The Smart Meters

**Problem:** `health-01`  
**Model:** `claude-opus-4-6`  
**Prompt tier:** none  
**Score:** 5/5

## Scenario

A city installs smart parking meters that adjust prices dynamically based on spot turnover rate — fast turnover signals high demand, so prices rise to encourage shorter stays. In the arts district, spots turn over slowly because visitors come for 3-hour gallery walks. The system drops prices to near-zero, interpreting slow turnover as low demand. But the arts district is always full — drivers circle for 20+ minutes looking for spots, and local businesses complain about inaccessible parking.

**Question:** How should they fix the pricing algorithm?

## Model Response

# The Core Flaw: Confusing Turnover with Demand

The algorithm treats **spot turnover rate** as a reliable proxy for demand, but it's not. Demand is about *how many people want a spot*, while turnover reflects *how long each person stays*. These are independent variables. The arts district has **high demand with long dwell times**, and the algorithm has no way to distinguish that from genuinely low demand.

This creates a vicious feedback loop:

> Long stays → slow turnover → algorithm drops price → cheap parking encourages even longer stays → turnover slows further → price drops again → district is permanently full with near-zero revenue

---

## The Fix: A Multi-Signal Approach

### 1. Make Occupancy Rate the Primary Demand Signal

This is the most important change. Following the well-established **85% target occupancy principle** (from Donald Shoup's parking research):

- **Above ~85% occupancy → raise prices**, regardless of turnover speed
- **Below ~85% occupancy → lower prices**, regardless of turnover speed
- The goal is to always keep roughly **1 in 7 spots open**, so arriving drivers can find a spot without circling

Occupancy directly measures what you actually care about: *are there spots available or not?* The arts district would immediately register as high-demand because it's at ~100% occupancy.

**Implementation:** Most smart meters already sit on occupancy sensors. The data is likely already being collected — it's just not being used as the pricing input.

### 2. Demote Turnover to a Secondary/Contextual Signal

Turnover rate isn't useless — it tells you about the **character** of demand and helps fine-tune policy. But it should inform *how* you manage demand, not *whether* demand exists:

| Signal Combination | Diagnosis | Response |
|---|---|---|
| High occupancy + high turnover | High demand, short visits (e.g., lunch district) | Raise base price |
| High occupancy + low turnover | High demand, long visits (arts district) | Raise price **and** consider progressive time-based rates |
| Low occupancy + high turnover | Moderate demand, quick errands | Prices are roughly right |
| Low occupancy + low turnover | Genuinely low demand | Lower prices |

The original algorithm only had one axis. You need both.

### 3. Introduce Progressive Time-Based Pricing

For districts like the arts district specifically, a flat hourly rate may not be enough even once occupancy-based pricing kicks in. Consider **escalating rates**:

- **Hour 1:** $2.00
- **Hour 2:** $3.00
- **Hour 3:** $5.00
- **Hour 4+:** $8.00/hr

This doesn't punish arts visitors — it creates a *gentle incentive* to use the 3-hour gallery walk efficiently rather than linger at a meter for 5 hours. It also signals that long-stay parkers might prefer a nearby garage or lot, freeing curb spots for higher turnover.

The key insight: **curb parking is the most spatially scarce resource**, so it should be priced to favor access, while long-stay demand gets redirected to off-street parking.

### 4. Add Cruising/Search-Time as a Validation Signal

If you can measure it (via connected car data, app-based reports, or traffic sensors detecting circling patterns), **average search time is perhaps the purest signal of parking failure**. Twenty minutes of circling is essentially proof that prices are too low, full stop. This can serve as a backstop:

> *If estimated search time exceeds X minutes, trigger a price floor or emergency rate increase regardless of other signals.*

---

## Deeper Architectural Lesson

The original system made a classic **proxy metric error** — optimizing for an indicator that's correlated with the target outcome in *some* contexts but diverges badly in others. The fix isn't just swapping one metric for another; it's building a model that's robust to different *types* of parking demand:

- **Short-stay commercial districts** (turnover ≈ demand — original algorithm works okay)
- **Long-stay cultural/entertainment districts** (turnover inversely misleading)
- **Residential-adjacent areas** (overnight patterns break both assumptions)
- **Mixed-use corridors** (demand patterns shift by time of day)

A well-designed system should let each zone weight its inputs differently, or better yet, let occupancy always anchor the pricing logic while turnover and dwell-time data shape supplementary policies like time limits and progressive rates.

---

## Summary

| Problem | Fix |
|---|---|
| Turnover used as sole demand proxy | Make **occupancy rate** the primary pricing signal |
| Algorithm can't distinguish low demand from long-stay high demand | Use **occupancy × turnover** as a two-dimensional signal |
| No incentive to limit stay duration | Add **progressive hourly pricing** |
| No failsafe for obvious parking failure | Use **cruising/search time** as a backstop trigger |
| One-size-fits-all logic across districts | Allow **zone-specific parameter tuning** |

The fundamental principle: **price parking so that a few spots are always available**. If every spot is full, the price is too low — no matter what the turnover rate says.

## Judge Scores

| Dimension | Score | Reasoning |
|-----------|:-----:|-----------|
| Frame | 1/1 | The response explicitly names the embedded assumption: 'The algorithm treats spot turnover rate as a reliable proxy for demand, but it's not.' It further elaborates this as a 'classic proxy metric error — optimizing for an indicator that's correlated with the target outcome in some contexts but diverges badly in others,' clearly articulating why turnover is a problematic proxy for demand. |
| Escape | 1/1 | The response reframes from 'the algorithm needs better inputs' to 'a one-size-fits-all mechanism is architecturally flawed for different parking ecologies.' The 'Deeper Architectural Lesson' section explicitly names four structurally different parking contexts (short-stay commercial, long-stay cultural, residential, mixed-use) and argues that 'the fix isn't just swapping one metric for another; it's building a model that's robust to different types of parking demand.' It also introduces non-price interventions like time limits, effectively reasoning from a new frame. |
| Causal | 1/1 | The response traces the full causal chain from the proxy metric error to its real-world consequences: the algorithm misreads long dwell times as low demand, drops prices, which attracts more drivers, keeps occupancy at 100%, perpetuates low turnover, and creates a permanently full district with near-zero revenue. It identifies the root cause as the conflation of an independent variable (dwell time) with the target variable (demand intensity). |
| Dynamics | 1/1 | The response identifies a specific reinforcing feedback loop: 'Long stays → slow turnover → algorithm drops price → cheap parking encourages even longer stays → turnover slows further → price drops again → district is permanently full with near-zero revenue.' It also identifies cross-component dynamics between curb parking and off-street alternatives, and how circling behavior emerges from mispriced curb spots. |
| Purpose | 1/1 | The response explicitly distinguishes the metric (turnover rate) from the actual purpose (parking availability). It states: 'Occupancy directly measures what you actually care about: are there spots available or not?' and concludes with the principle: 'price parking so that a few spots are always available. If every spot is full, the price is too low — no matter what the turnover rate says.' It evaluates the system against real accessibility, not the stated metric. |

**Total: 5/5**

