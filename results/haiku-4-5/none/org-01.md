# The Escalation Policy

**Problem:** `org-01`  
**Model:** `claude-haiku-4-5`  
**Prompt tier:** none  
**Score:** 1/5

## Scenario

A support team implements a strict escalation policy: if a ticket isn't resolved in 2 hours, it escalates to a senior engineer. After implementation, average resolution time drops from 6 hours to 3 hours. Six months later, their two best senior engineers quit.

**Question:** Why did the senior engineers quit, and what should the team do?

## Model Response

# Why the Senior Engineers Likely Quit

The improvement in resolution time probably masks a **burnout problem** for senior engineers:

1. **Escalation overwhelm**: The 2-hour threshold likely created a high volume of escalated tickets flowing to them. They became the bottleneck, not the solution.

2. **Unsustainable firefighting**: Senior engineers probably shifted from meaningful work to constant reactive escalation handling—long hours, constant interruptions, no deep work.

3. **Unaddressed root causes**: The policy created urgency but didn't fix *why* junior engineers were stuck at 2 hours. The seniors were just absorbing the overflow.

4. **Career stagnation**: High-performing engineers lost time for mentoring, learning, innovation, and technical growth.

---

# What the Team Should Do

**Stop optimizing for speed alone:**

- **Analyze escalation patterns**: Which tickets? Which engineers? Are juniors actually improving?
- **Address root causes**: Better training, documentation, tools, and clearer procedures—not just faster escalation
- **Adjust the policy**: Maybe escalation isn't automatic; different tickets need different SLAs
- **Invest in junior engineers**: Sustainable mentoring relationships, skill-building, not just fast hand-offs
- **Measure sustainability**: Track job satisfaction, retention, burnout signals—not just resolution time

**Involve senior engineers in the fix.** Ask them what they need. Their departure is a signal the current system isn't working for your best people.

The irony: the escalation policy improved metrics while destroying the team's capacity to sustain them.

## Judge Scores

| Dimension | Score | Reasoning |
|-----------|:-----:|-----------|
| Frame | 0/1 | The response frames the problem primarily as 'escalation overwhelm' and 'unsustainable firefighting' — which is the shallow, embedded frame. It never explicitly names or challenges the assumption that the problem is overload, nor identifies that the real issue is the destruction of the learning mechanism that creates senior engineers. |
| Escape | 0/1 | The response stays within the overload/burnout frame throughout. While it gestures toward junior development ('Are juniors actually improving?', 'skill-building'), these are positioned as solutions to reduce escalation volume, not as recognition that the old struggle-based learning was the mechanism that produced senior engineers. It never reframes the core problem as a broken talent pipeline. |
| Causal | 0/1 | The response addresses proximate causes: too many escalations, firefighting, career stagnation. It notes the policy 'didn't fix why junior engineers were stuck at 2 hours' but never traces the causal chain to its root: the policy removed the struggle that develops juniors into seniors, permanently cementing the current seniors as an irreplaceable ceiling. The deepest causal link — that the policy itself destroyed the development mechanism — is absent. |
| Dynamics | 0/1 | The closing line ('improved metrics while destroying the team's capacity') gestures at a systemic tension but doesn't identify specific feedback loops or cascading dynamics. The critical loop — policy removes learning → juniors stop growing → no new seniors are produced → existing seniors bear permanent load → seniors quit → even fewer seniors → system collapse — is never articulated. No emergent behavior or reinforcing loops are specified. |
| Purpose | 1/1 | The response explicitly distinguishes the metric (resolution time) from broader organizational health: 'Stop optimizing for speed alone,' 'Track job satisfaction, retention, burnout signals—not just resolution time,' and the final irony about improving metrics while destroying capacity. This demonstrates awareness that the stated metric diverged from the actual purpose. |

**Total: 1/5**

