# The Powerful Pump

**Problem:** `supply-01`  
**Model:** `claude-haiku-4-5`  
**Prompt tier:** none  
**Score:** 2/5

## Scenario

An aquarium struggles with excess algae in their coral reef tank. They replace the old, underpowered water pump with a high-flow system. Algae drops dramatically within weeks. Four months later, the coral begins bleaching — turning white and dying. Water chemistry tests are normal. The new pump is working perfectly.

**Question:** Why is the coral bleaching?

## Model Response

# The Coral Bleaching Mystery

This is a classic case of **unintended consequences**. The coral is bleaching due to **light stress**, and the problem is that the algae was actually helping the coral.

## What Happened

**Before:** The excess algae provided three critical benefits:
- **Natural shading** - Filtered and scattered intense aquarium lighting
- **Nutrient competition** - Consumed excess nitrogen and phosphorus
- **Light diffusion** - Reduced harmful UV and excessive photosynthetically active radiation (PAR)

**After:** When the high-flow pump eliminated the algae:
- The water became much **clearer**, allowing more intense light to reach the coral
- The coral lost its **natural shade canopy**
- Increased water movement also increased light penetration

## Why Bleaching Occurred

The elevated light exposure stressed the coral's symbiotic zooxanthellae (the algae living in the coral's tissue that provides color and nutrition). The coral expelled these algae in a stress response—that's bleaching—which is why the coral appears white.

## The Solution

The aquarium needs to:
1. **Reduce light intensity** or photoperiod
2. **Allow some algae to naturally regrow** as a buffer
3. **Add shade** (plants, rock formations, diffusers)
4. **Use softer/diffused lighting** instead of direct, intense LEDs

The lesson: in reef tanks, "excess" algae isn't always bad—it's often the ecosystem maintaining balance in ways we don't immediately recognize.

## Judge Scores

| Dimension | Score | Reasoning |
|-----------|:-----:|-----------|
| Frame | 0/1 | The response does not identify the embedded assumption that 'the pump is too powerful.' More importantly, it completely misses the key insight that the old pump's weakness was performing a hidden biological function (coral exercise via variable flow). Instead, it invents a light-stress frame that, while creative, does not name or challenge the actual embedded assumption. |
| Escape | 1/1 | The response does genuinely escape the 'pump is too powerful → add diffusers' frame. It constructs an entirely different causal explanation (algae removal → light stress → bleaching) and reasons consistently from that new frame. While it's not the ideal reframe from the reference, it is a clear and coherent reframe away from the shallow answer. |
| Causal | 0/1 | The response traces a multi-step but ultimately incorrect causal chain (pump → algae removal → clearer water → light stress → zooxanthellae expulsion). It misses the true root causes: the algae was a nutrient problem misdiagnosed as a flow problem, and the old pump's variable flow served as a fitness mechanism for the coral's symbiotic zooxanthellae. The light-shading hypothesis is plausible-sounding but doesn't reach the actual root cause. |
| Dynamics | 1/1 | The response identifies a specific cross-component cascade: pump change → algae elimination → increased light penetration → coral stress → bleaching. It also names multiple functions the algae served (shading, nutrient competition, light diffusion), showing awareness that components serve multiple roles in the system. These are specific enough to count as cross-component cascades. |
| Purpose | 0/1 | The response's final lesson gestures at 'algae isn't always bad' but doesn't clearly distinguish the stated metric (algae reduction) from the actual purpose (coral health). It doesn't identify the deeper misdiagnosis: the algae was a symptom of excess nutrients, not a flow problem. Its solution—'allow algae to regrow as a buffer'—actually reinforces the wrong frame, treating algae as inherently beneficial rather than recognizing it as a symptom of an underlying nutrient problem that needs addressing. |

**Total: 2/5**

