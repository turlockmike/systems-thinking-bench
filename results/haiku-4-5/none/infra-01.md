# The Efficient Dehumidifier

**Problem:** `infra-01`  
**Model:** `claude-haiku-4-5`  
**Prompt tier:** none  
**Score:** 1/5

## Scenario

A small organic soap maker notices their bars are taking 20% longer to cure. They install a more powerful dehumidifier in the curing room. Bars harden faster than ever — cure time drops by 40%. Three months later, customers complain the soap dissolves in the shower within days instead of lasting weeks. Internal testing confirms: bars feel hard when shipped but break down rapidly in water.

**Question:** What went wrong with the soap?

## Model Response

# The Problem: Removing Water Too Quickly

The soap maker created a classic **case-hardening problem** by over-drying the bars during cure. Here's what went wrong:

## Why Extended Cure Matters

Soap curing isn't just about evaporation—it's about *controlled* transformation:

1. **Crystal structure formation** - Soap molecules need time to organize into stable crystalline matrices that hold the bar together
2. **Gradual dehydration** - Water should leave slowly from throughout the bar, not rapidly from the surface inward
3. **Proper saponification** - Chemical reactions that started at pour-time continue during cure, stabilizing the molecular structure

## What Excessive Dehumidification Caused

By removing water *too fast*:
- **Exterior hardened while interior remained weak** - Surface appeared solid, but interior structure never properly developed
- **Crystals didn't form properly** - Rushing the process prevented tight molecular bonding
- **Stress fractures developed internally** - Rapid outer drying while inner core retained moisture created mechanical weakness

The bars *felt* hard (deceiving initial inspection) but lacked the cohesive matrix needed to resist water breakdown.

## The Fix

- **Rebalance humidity** to 50-60% (moderate, not minimal)
- **Return to standard cure times** (typically 4-6 weeks)
- **Monitor quality, not just speed** - hardness ≠ durability

This is a reminder that in chemistry and material science, **faster optimization often breaks what you can't see.** The initial humidity problem needed adjustment, not elimination.

## Judge Scores

| Dimension | Score | Reasoning |
|-----------|:-----:|-----------|
| Frame | 0/1 | The response never identifies the embedded assumption that 'the curing process is too slow.' It implicitly accepts that the original slowdown was a problem ('The initial humidity problem needed adjustment, not elimination'), rather than recognizing that the increased cure time may have been a correct response to changed conditions. The frame goes entirely unquestioned. |
| Escape | 0/1 | The response stays squarely within the 'dehumidifier was too aggressive' frame and recommends rebalancing humidity and returning to standard cure times. It never asks the critical reframing question: 'Why did cure times increase by 20% in the first place?' This is essentially the shallow answer — calibrate the dehumidifier better. |
| Causal | 0/1 | The causal chain stops at the proximate cause: the dehumidifier removed water too fast, causing case-hardening. The response never traces back to the root cause — a potential recipe change (e.g., higher olive oil content) that legitimately required longer cure times. It treats the dehumidifier as the origin of the problem rather than a misguided response to an uninvestigated upstream change. |
| Dynamics | 0/1 | The response describes a linear material-science mechanism (fast drying → hard shell → weak interior) but does not identify feedback loops, emergent behavior, or cross-component cascades in the broader production system. There is no discussion of how customer-requested recipe changes propagate through cure chemistry to quality outcomes, or how the metric of cure speed created a self-deceiving feedback loop. |
| Purpose | 1/1 | The response explicitly distinguishes the metric from the purpose: 'hardness ≠ durability' and 'Monitor quality, not just speed.' It clearly notes that the bars passed inspection (metric) but failed in actual use (purpose), and warns that 'faster optimization often breaks what you can't see.' This is a genuine metric-vs-purpose distinction. |

**Total: 1/5**

