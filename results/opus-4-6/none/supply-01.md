# The Powerful Pump

**Problem:** `supply-01`  
**Model:** `claude-opus-4-6`  
**Prompt tier:** none  
**Score:** 1/5

## Scenario

An aquarium struggles with excess algae in their coral reef tank. They replace the old, underpowered water pump with a high-flow system. Algae drops dramatically within weeks. Four months later, the coral begins bleaching — turning white and dying. Water chemistry tests are normal. The new pump is working perfectly.

**Question:** Why is the coral bleaching?

## Model Response

# The High Flow Itself Is Killing the Coral

The key phrase in the puzzle is: *"The new pump is working perfectly."* That's not a reassurance — it's the diagnosis. **The pump is too powerful for the coral, and the very flow that eliminated the algae is now chronically stressing the coral to death.**

## The Mechanism

Corals depend on a thin, calm **boundary layer** of water sitting directly against their tissue. This microscopic zone is where they:

- Exchange gases (O₂ and CO₂)
- Absorb dissolved nutrients
- Extend their polyps to feed
- Maintain their protective mucus coating

An overpowered pump **strips this boundary layer away**. The coral polyps can't extend, can't feed, and are mechanically battered 24/7. Over weeks and months, this chronic stress triggers the coral to **expel its symbiotic zooxanthellae** — the photosynthetic algae living *inside* its tissue that give it color and up to 90% of its energy. That expulsion is what we see as bleaching.

## Why It Took Four Months

Coral bleaching from flow stress isn't instant. The coral draws on energy reserves, tries to adapt, and slowly deteriorates. The delay is characteristic of **chronic mechanical stress** rather than an acute chemical event — which is also why water chemistry tests come back normal. Nothing is chemically wrong. The damage is physical.

## The Deeper Lesson: The Fix *Was* the Problem

This is a classic **systems-thinking trap**:

- Low flow → algae thrives (original problem)
- High flow → algae dies, but coral also dies (new problem)
- The correct solution was **moderate, appropriate flow** — enough to discourage algae settlement without overwhelming the coral

The pump wasn't broken. It was working *too well*. The same force that scoured algae off the surfaces was also scouring the life out of the coral — just slowly enough that the cause wasn't obvious.

## Judge Scores

| Dimension | Score | Reasoning |
|-----------|:-----:|-----------|
| Frame | 0/1 | The response does not identify the embedded assumption. It explicitly adopts the 'pump is too powerful' frame ('The pump is too powerful for the coral') rather than recognizing that the old pump's weakness was performing a hidden biological function. It treats the problem as excessive force, not as the removal of a beneficial constraint. |
| Escape | 0/1 | The response stays squarely within the 'pump power' frame. It concludes the solution is 'moderate, appropriate flow' — essentially the shallow answer of dialing back the pump. It never reframes the algae as a nutrient problem misdiagnosed as a flow problem, nor does it consider that the old pump's variable, weak flow was an accidental fitness mechanism rather than simply being 'less powerful.' |
| Causal | 0/1 | The response traces a mechanistic chain (high flow → boundary layer stripping → polyp retraction → zooxanthellae expulsion) but this is the proximate, surface-level causal story. It does not reach the root cause: the algae problem was a nutrient issue misdiagnosed as a flow issue, and the old pump was providing variable currents that kept the coral physiologically strong. The response mistakes a detailed proximate mechanism for root-cause analysis. |
| Dynamics | 0/1 | The response describes a linear causal chain (excess flow → physical stress → bleaching) but does not identify feedback loops, emergent behavior, or cross-component cascades. It misses the coral-algae competition dynamic (healthy coral competes for space with algae), the feedback loop between coral fitness and zooxanthellae health, and how the old system's 'weakness' created an emergent beneficial property. |
| Purpose | 1/1 | The response does distinguish between the stated metric and the actual purpose. It explicitly notes that the pump 'working perfectly' is the diagnosis, not a reassurance, and that solving the algae symptom created a new problem for the primary organism. The section 'The Fix Was the Problem' captures the metric/purpose divergence — algae removal ≠ reef health. |

**Total: 1/5**

