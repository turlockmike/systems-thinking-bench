# The Efficient Dehumidifier

**Problem:** `infra-01`  
**Model:** `claude-opus-4-6`  
**Prompt tier:** none  
**Score:** 4/5

## Scenario

A small organic soap maker notices their bars are taking 20% longer to cure. They install a more powerful dehumidifier in the curing room. Bars harden faster than ever — cure time drops by 40%. Three months later, customers complain the soap dissolves in the shower within days instead of lasting weeks. Internal testing confirms: bars feel hard when shipped but break down rapidly in water.

**Question:** What went wrong with the soap?

## Model Response



# The Dehumidifier "Fix": A Case Study in Solving the Wrong Problem

## The Short Answer

The more powerful dehumidifier created **surface-hardened bars with incomplete internal curing** — essentially a hard shell around a poorly structured interior. The soap *felt* ready but *wasn't*.

---

## What's Actually Happening During Proper Curing

Cold-process soap curing isn't just about "drying out." Several critical processes occur simultaneously over 4–6 weeks:

1. **Saponification completion** — residual lye and fats continue reacting slowly after the initial pour. This reaction needs *moisture present* to proceed.
2. **Crystal structure formation** — sodium soap molecules organize into stable crystalline lattice structures. This takes time and moderate (not extreme) moisture conditions.
3. **Glycerin integration** — natural glycerin produced during saponification distributes evenly throughout the bar and binds into the crystal matrix.
4. **Gradual, even water loss** — water exits slowly from the interior outward, allowing uniform structural development throughout the entire bar.

---

## What the Dehumidifier Actually Did

The aggressive dehumidification caused **several compounding problems:**

- **Rapid surface dehydration** created a hard, dense outer layer that *sealed in* interior moisture, preventing even curing throughout the bar. The surface passed a hardness check while the inside remained under-developed.
- **Incomplete saponification** — by stripping water too aggressively, the environment disrupted the ongoing lye-fat reaction that needs water as a medium. This leaves unreacted fats (soft, water-soluble components) in the bar.
- **Poor crystal formation** — the soap molecules never had time to organize into the tight, stable crystalline lattice that gives properly cured soap its water resistance. Think of it like flash-freezing vs. slow crystal growth — fast produces weak, disorganized structure.
- **Glycerin pooling** — instead of integrating uniformly, glycerin (which is hygroscopic) likely remained in concentrated pockets. In the shower, these pockets absorb water aggressively, accelerating breakdown from within.

---

## Why It Passed Internal Hardness Testing

This is the cruel part. The bars **genuinely were hard** — on the outside. A squeeze test, a surface durometer reading, even a weight-loss check would all look fine or better than normal. The dehumidifier *did* remove water. But hardness ≠ cure quality. The structural integrity that resists dissolution in water comes from **internal crystalline organization**, not surface dryness.

---

## The Deeper Lesson

The original problem — bars taking 20% longer to cure — was likely caused by something else entirely (seasonal humidity increase, a recipe change, a different oil batch). The correct investigation would have been:

1. **Diagnose why** cure time increased (humidity? recipe? temperature?)
2. **Address the root cause** rather than accelerating a symptom

Instead, they treated "cure time" as the variable to optimize, when cure time is really just a **proxy indicator** for a complex set of chemical and physical processes. Speeding up the proxy didn't speed up the underlying processes — it disrupted them.

This is a classic **Goodhart's Law** problem: *when a measure becomes a target, it ceases to be a good measure.* They optimized for "feels hard fast" and destroyed what hardness was supposed to indicate.

---

## The Fix

- Remove the overpowered dehumidifier (or dial it back significantly)
- Return to conditions that allow **slow, even curing** — moderate humidity, good airflow, patience
- Investigate the original 20% slowdown separately
- Add a **water dissolution test** to QC, not just hardness — actually place sample bars under running water for a timed period and measure mass loss

## Judge Scores

| Dimension | Score | Reasoning |
|-----------|:-----:|-----------|
| Frame | 1/1 | The response explicitly identifies that they treated cure time as the variable to optimize when it was actually a proxy indicator. It names this as a Goodhart's Law problem: 'when a measure becomes a target, it ceases to be a good measure.' It clearly states the correct investigation would have been to diagnose WHY cure time increased rather than accelerating the symptom. |
| Escape | 1/1 | The response clearly reframes from 'how to speed up curing' to 'why did cure time increase and what does cure time actually represent.' It reasons substantively from this new frame, distinguishing between the proxy (hardness/cure time) and the underlying chemical processes, and proposes a diagnostic approach instead of a symptom-acceleration approach. |
| Causal | 0/1 | The response traces the dehumidifier's effects in impressive chemical detail (incomplete saponification, poor crystal formation, glycerin pooling). However, it does NOT trace the root cause of WHY cure times increased. It only speculates with a list of possibilities ('seasonal humidity increase, a recipe change, a different oil batch'). The deep answer identifies the specific root cause — increased olive oil content requiring longer saponification. The response gestures at the right direction but never arrives at the actual root cause. |
| Dynamics | 1/1 | The response identifies multiple specific cascading interactions: surface dehydration sealing in moisture (creating a self-reinforcing barrier), water removal disrupting the saponification reaction that requires water as a medium, concentrated glycerin pockets that are hygroscopic and accelerate water absorption during use, and the compounding nature of these problems reinforcing each other. These are concrete cross-component cascades, not vague gestures. |
| Purpose | 1/1 | The response explicitly distinguishes the metric from the purpose: 'hardness ≠ cure quality' and 'The structural integrity that resists dissolution in water comes from internal crystalline organization, not surface dryness.' It invokes Goodhart's Law by name. It recommends replacing the surface hardness metric with a water dissolution test that actually measures what customers care about — soap longevity in the shower. |

**Total: 4/5**

