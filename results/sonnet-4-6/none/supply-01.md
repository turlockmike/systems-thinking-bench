# The Powerful Pump

**Problem:** `supply-01`  
**Model:** `claude-sonnet-4-6`  
**Prompt tier:** none  
**Score:** 4/5

## Scenario

An aquarium struggles with excess algae in their coral reef tank. They replace the old, underpowered water pump with a high-flow system. Algae drops dramatically within weeks. Four months later, the coral begins bleaching — turning white and dying. Water chemistry tests are normal. The new pump is working perfectly.

**Question:** Why is the coral bleaching?

## Model Response

## The Unintended Consequence: Light Shock from Algae Removal

This is a classic example of an **ecological cascade with a delayed second-order effect**.

---

### What Actually Happened

**The algae, while a nuisance, was inadvertently shading the corals.**

By dramatically reducing algae, the high-flow pump created much clearer water — which significantly **increased light penetration and intensity** reaching the coral.

---

### The Bleaching Mechanism

Corals rely on **zooxanthellae** — symbiotic algae living *within their tissues* — that provide up to 90% of the coral's energy through photosynthesis. These zooxanthellae also give coral its color.

When exposed to **excessive light**, zooxanthellae undergo photoinhibition and begin producing **reactive oxygen species (ROS)** — essentially toxic byproducts. To protect itself, the coral **expels the zooxanthellae**, turning white: bleaching.

---

### Why the Four-Month Delay?

| Phase | What's Happening |
|-------|-----------------|
| Weeks 1–4 | Algae clears; coral initially tolerates increased light |
| Months 1–3 | Chronic photostress builds; ROS accumulate; zooxanthellae become compromised |
| Month 4 | Coral can no longer compensate → mass expulsion → bleaching visible |

This slow accumulation is why there's no immediate alarm signal.

---

### Why Tests Show Nothing

The problem is **physical/energetic, not chemical**. Standard tests (pH, alkalinity, calcium, nitrate, phosphate, salinity) won't detect:
- Elevated light intensity at the coral surface
- Thermal stress from the pump motor's heat output over time
- Photoinhibition stress within coral tissue

The pump **is** working perfectly — that's precisely the problem.

---

### The Core Irony

> The "problem" (algae) was partially **protecting** the corals by acting as a light diffuser. The corals had physiologically acclimated to lower-light conditions over months or years. Suddenly removing the biological shade layer caused a light shock the corals couldn't survive.

---

### The Fix

- **Gradually reduce light intensity** at the fixture level to compensate for clearer water
- **Slowly reintroduce** modest nutrient/algae balance as biological shade
- Allow corals to **photoacclimate gradually** rather than abruptly
- Monitor PAR (photosynthetically active radiation) at the coral surface, not just water chemistry

This is a textbook case of why solving one variable in a complex ecosystem without modeling downstream effects can create a worse problem than the original.

## Judge Scores

| Dimension | Score | Reasoning |
|-----------|:-----:|-----------|
| Frame | 0/1 | The model does not identify the embedded assumption that 'the pump is too powerful.' Instead, it proposes a different mechanism entirely (light shock from algae removal). While it identifies that algae was protective, it never names or interrogates the assumption that the old pump's weakness was performing a biological function (coral exercise via variable flow). It identifies a different frame problem (algae as shade) rather than the core one about flow dynamics and coral fitness. |
| Escape | 1/1 | The model clearly escapes the 'pump is too powerful / add baffles' frame. Rather than blaming direct flow stress, it proposes a completely different causal mechanism — that algae removal increased light penetration, causing photoinhibition and zooxanthellae expulsion. It reasons consistently and in detail from this alternative frame, providing a timeline, mechanism, and proposed fixes. |
| Causal | 1/1 | The model traces a multi-step causal chain: pump upgrade → algae reduction → clearer water → increased PAR → photoinhibition → ROS accumulation → zooxanthellae expulsion → bleaching. This is a 7-step chain that goes well beyond the shallow 'too much flow' answer. However, it does miss the deeper root cause that the algae was a nutrient problem misdiagnosed as a flow problem, and doesn't question whether the intervention addressed the right variable. Still, the depth of the chain it does trace warrants a 1. |
| Dynamics | 1/1 | The model identifies specific cross-component cascades (algae-light-zooxanthellae-coral interactions), a delayed accumulation dynamic (months of chronic photostress before visible bleaching), and the symbiotic coral-zooxanthellae relationship. It explains how removing one component (nuisance algae) triggered a cascade through light dynamics to destroy the primary organism. These are concrete, specific system dynamics, not vague hand-waving. |
| Purpose | 1/1 | The model explicitly distinguishes between metrics and purpose: 'The pump is working perfectly — that's precisely the problem.' It notes that standard water chemistry tests show 'normal' but completely miss the actual issue (light stress), and that solving the visible metric (algae reduction) created a worse problem for the real purpose (coral health). It identifies the gap between what's measured and what matters. |

**Total: 4/5**

