# The Productive Team

**Problem:** `org-02`  
**Model:** `claude-haiku-4-5`  
**Prompt tier:** none  
**Score:** 2/5

## Scenario

A team of 6 engineers ships features consistently. Management adds 4 more engineers to accelerate delivery. After onboarding, the team's output drops. Management assumes it's temporary — new engineers need ramp-up time. Eight months later, output is still lower than the original 6-person team.

**Question:** What should management do?

## Model Response

# The Real Problem: Eight Months Is Too Long to Wait

Management needs to stop diagnosing and start investigating. By now, "ramp-up time" is clearly not the issue. Something structural is broken.

## What's Likely Actually Happening

- **Communication overhead exploded** — you went from 15 possible communication pairs (6 people) to 45 (10 people). Meetings, code reviews, and coordination now consume time that used to go to shipping.
- **Bottlenecks emerged** — maybe the original 6 had informal processes that broke under scale, or one person became a gatekeeper for reviews/decisions.
- **Integration problems** — the original team's chemistry and informal knowledge transfer worked for them but isn't scaling to the new hires.
- **Context drag** — mentoring new engineers is pulling original team members away from features.

## What Management Should Actually Do

1. **Diagnose systematically, not philosophically**
   - Track where time actually goes: feature work vs. meetings vs. code review vs. mentoring vs. rework
   - Ask both original and new engineers what's blocking them
   - Look at actual velocity data — is it features, quality, or both?

2. **Fix the system, not the people**
   - Reorganize into smaller sub-teams with clear ownership boundaries
   - Reduce decision bottlenecks (who's blocking code reviews?)
   - Streamline meetings and interruptions
   - Improve documentation so new engineers get context faster

3. **Restructure for scale**
   - One manager may not effectively lead 10 engineers — consider splitting into two teams
   - Create clearer architectural boundaries so teams don't constantly step on each other

4. **Honestly evaluate the hire quality**
   - Are the 4 new engineers the right fit? Sometimes the answer is a difficult personnel decision.

## The Deeper Lesson

Software output doesn't scale linearly with headcount. The team grew 67%, but output went down — that's a flashing warning sign that you've hit the team's organizational limits, not a patience problem.

**Eight months of patience is eight months of lost diagnosis time.**

## Judge Scores

| Dimension | Score | Reasoning |
|-----------|:-----:|-----------|
| Frame | 1/1 | The response does identify the linear scaling assumption as wrong ('Software output doesn't scale linearly with headcount') and challenges management's patience framing ('ramp-up time is clearly not the issue'). However, it doesn't go deep into naming the specific mechanism — that shared implicit context is the real asset being diluted — treating communication overhead as the primary explanation. |
| Escape | 0/1 | The response stays within the original frame. Its solutions — reorganize into sub-teams, split into two teams, improve documentation, track velocity — all assume the 10-person team is a given and just needs better management. It never asks whether hiring was the right intervention at all, whether the bottleneck was even people, or whether the real constraint might be technical debt, unclear requirements, or organizational friction. The deep answer explicitly notes that splitting into two teams makes things worse. |
| Causal | 0/1 | The response identifies proximate causes (communication overhead, mentoring drag, bottleneck emergence) but doesn't trace to root causes. It never asks: why were the original 6 productive? What made that team work? Was the bottleneck actually people, or something else entirely (technical debt, unclear requirements, organizational friction)? It doesn't recognize that the fundamental asset — shared mental models and implicit context — was diluted, not just that 'overhead increased.' |
| Dynamics | 1/1 | The response identifies specific dynamics: communication pairs growing from 15 to 45 (structural scaling), mentoring pulling original engineers away from feature work (cross-component cascade), and informal processes breaking under scale (emergent behavior). However, it doesn't articulate reinforcing feedback loops, such as how the shift from implicit to explicit coordination creates more need for explicit coordination, making things progressively worse. |
| Purpose | 0/1 | The response accepts 'output' and 'delivery speed' as the goal without questioning whether that metric captures the actual purpose. It doesn't distinguish between shipping features (the metric) and delivering customer value (the purpose). It never asks whether the original 6 were actually bottlenecked on delivery speed or whether 'accelerate delivery' was the right goal in the first place. |

**Total: 2/5**

