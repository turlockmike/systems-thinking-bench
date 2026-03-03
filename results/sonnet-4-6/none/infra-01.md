# The Efficient Dehumidifier

**Problem:** `infra-01`  
**Model:** `claude-sonnet-4-6`  
**Prompt tier:** none  
**Score:** 2/5

## Scenario

A small organic soap maker notices their bars are taking 20% longer to cure. They install a more powerful dehumidifier in the curing room. Bars harden faster than ever — cure time drops by 40%. Three months later, customers complain the soap dissolves in the shower within days instead of lasting weeks. Internal testing confirms: bars feel hard when shipped but break down rapidly in water.

**Question:** What went wrong with the soap?

## Model Response

## The Case-Hardening Problem

What happened is a classic **differential curing failure** — the soap maker solved the wrong problem and created a much worse one.

---

## What Proper Curing Actually Does

Soap curing isn't simply "drying out." It involves several simultaneous processes:

1. **Completing saponification** — residual lye finishing its reaction with oils
2. **Gradual, even water evaporation** — allowing moisture to migrate from the interior outward uniformly
3. **Crystalline structure formation** — soap molecules (sodium salts of fatty acids) slowly organizing into stable, interlocking crystal lattices
4. **Glycerin redistribution** — the natural byproduct of saponification distributing evenly throughout the bar

All of these take **time and require moisture to move slowly and evenly.**

---

## What the Powerful Dehumidifier Did

The aggressive dehumidification created extreme low-humidity conditions, causing:

### Surface Case-Hardening
- The outer layer dried and hardened extremely rapidly
- This hard "shell" then **trapped remaining moisture inside** the bar
- The interior never properly cured — it remained relatively soft, incompletely crystallized, and with poorly distributed glycerin

### The Deceptive Result
| What They Measured | What It Actually Indicated |
|---|---|
| Bar feels hard | **Surface** is hard |
| Reduced cure time | Time for surface to harden |
| Passes shipping intact | Shell is structurally sound |
| ❌ Not measured | Internal cure state |

---

## Why the Bars Failed in the Shower

When water reached the improperly cured interior:

- **Incompletely crystallized soap** dissolves rapidly — without stable crystal structure, there's nothing to resist water penetration
- **Glycerin pockets** (glycerin is highly hygroscopic) acted as water channels, accelerating interior breakdown
- The hard shell couldn't compensate — once water breached it, the bar essentially fell apart from the inside out

This is physically analogous to case hardening in ceramics, wood drying, and bread baking — a common failure mode whenever surfaces are dried too aggressively.

---

## The Original Problem Was Misdiagnosed

The 20% increase in cure time likely had an identifiable, fixable cause:
- Seasonal humidity increase → modest dehumidification might have been fine
- New oil batch with different fatty acid profile → recipe adjustment needed
- Different water content in lye solution → formulation check needed

Instead, they overcorrected with a blunt instrument.

---

## The Core Lesson

> **Surface hardness ≠ cured soap.** The "cure time" they were measuring was actually just *surface set time* — a proxy metric that became meaningless once dehumidification was extreme enough to harden the exterior independently of the interior.

The fix would require:
- Gentler, controlled humidity reduction (not elimination)
- Rotating/flipping bars to promote even moisture migration
- Testing cure quality by **dissolution rate** and **internal moisture content**, not just surface feel
- Extending cure time rather than trying to compress it

## Judge Scores

| Dimension | Score | Reasoning |
|-----------|:-----:|-----------|
| Frame | 0/1 | The response says 'The Original Problem Was Misdiagnosed' but never identifies the key embedded assumption: that the 20% longer cure time was a malfunction rather than the correct response to changed conditions. It still treats the increased cure time as having an 'identifiable, fixable cause' (seasonal humidity, new oil batch, etc.) — meaning it still frames the longer cure as a problem to be solved, not as the process working correctly. |
| Escape | 0/1 | The response stays squarely within the 'dehumidifier was too aggressive' frame — which is essentially the shallow answer with much more chemical/physical detail. It never reframes to 'the longer cure time IS the correct cure time for changed ingredients.' The suggestion to 'extend cure time' appears at the end as one bullet among several fixes, not as the central reframe. |
| Causal | 0/1 | The response traces the proximate mechanism (case hardening → trapped moisture → incomplete crystallization → rapid dissolution) in excellent detail, but never identifies the actual root cause: a recipe change (e.g., increased olive oil content) that inherently requires longer saponification. The response speculates about possible causes of the 20% increase but doesn't identify the real one, and critically, doesn't recognize that the root cause made the longer cure necessary and correct. |
| Dynamics | 1/1 | The response identifies a specific cross-component cascade: surface hardening trapping moisture which prevents interior crystallization, which creates glycerin pockets that act as water channels accelerating interior breakdown. It also identifies a measurement dysfunction dynamic — surface hardness decoupling from internal cure state under extreme dehumidification — which is a concrete system dynamic (Goodhart's Law). |
| Purpose | 1/1 | The response explicitly distinguishes the metric (surface hardness / surface set time) from the actual purpose (complete internal saponification and crystallization). The highlighted callout 'Surface hardness ≠ cured soap' and the table showing what was measured vs. what wasn't measured clearly separate the proxy from the real goal. It recommends measuring dissolution rate and internal moisture content instead. |

**Total: 2/5**

