# The Diligent Proofreaders

**Problem:** `infra-02`  
**Model:** `claude-opus-4-6`  
**Prompt tier:** none  
**Score:** 5/5

## Scenario

A publishing house notices more typos reaching print. They audit the proofreading team: accuracy is 99.8%, virtually flawless. Management increases the proofreading budget by 30%, hiring additional reviewers and adding a second pass. Six months later, typo rates in published books are unchanged.

**Question:** How should they fix the typo problem?

## Model Response

# The Problem Isn't Where They're Looking

This is a classic systems-thinking trap: **they're optimizing the one part of the pipeline that's already working.**

## The Core Diagnosis

Proofreading is at **99.8% accuracy**. That's essentially a solved problem. Even if you doubled the team, you'd move from catching 99.8% of errors to maybe 99.9%. That's negligible. Pouring 30% more budget into it is like sharpening an already razor-sharp knife while ignoring the fact that someone keeps dropping the food on the floor.

**The typos reaching print are not a proofreading failure. They're being introduced *somewhere else* in the pipeline — likely *after* proofreading or in volumes proofreading was never designed to handle.**

## Where to Actually Look

The real causes are almost certainly **upstream or downstream** of proofreading:

- **Post-proofread changes.** Are editors, typesetters, or authors making "small fixes" after the proofread is complete? Every late-stage revision that bypasses the proofread pass injects unreviewed text.
- **Typesetting and layout.** Are errors being introduced when manuscripts are converted to final format — text reflow, font substitutions, copy-paste artifacts?
- **Increased volume or pace.** Are they publishing more titles or on tighter schedules, meaning manuscripts arrive in rougher shape, overwhelming even a near-perfect proofread?
- **Tooling and process changes.** Did they switch writing software, content management systems, or formatting pipelines in a way that introduces new classes of error?
- **Scope mismatch.** Is proofreading only reviewing *part* of the text (e.g., body copy but not captions, headers, footnotes, back matter)?

## What They Should Actually Do

1. **Trace the typos backward.** Take the actual typos found in published books and determine *at what stage* they were introduced. Were they in the original manuscript? Present during the proofread? Or introduced *after*?
2. **Lock the text after proofreading.** Institute a hard rule: no changes after the final proofread without a re-review. This single policy change likely addresses the biggest source of leakage.
3. **Audit the full production pipeline**, not just the proofreading team. Map every step from manuscript to printed page and identify where text is being touched.
4. **Invest upstream.** If manuscripts are arriving messier, address *that* — better style guides, author checklists, or editorial standards — rather than expecting proofreading to compensate.

## The Broader Lesson

This is a **Theory of Constraints** problem. Improving a non-bottleneck does nothing for the system. When a component is already at 99.8%, the constraint is *definitionally elsewhere*. The publishing house made the mistake of:

- Measuring the **performance** of one team ✓
- Assuming that team's domain was the **source** of the problem ✗

**The question was never "how good is our proofreading?" It was "where are the typos coming from?" — and no one asked it.**

## Judge Scores

| Dimension | Score | Reasoning |
|-----------|:-----:|-----------|
| Frame | 1/1 | The response explicitly identifies the embedded assumption: 'they're optimizing the one part of the pipeline that's already working.' It directly names that management assumed proofreading was the failure point when it isn't, and closes with: 'The question was never how good is our proofreading? It was where are the typos coming from? — and no one asked it.' |
| Escape | 1/1 | The response decisively reframes from 'fix proofreading' to 'audit the full production pipeline and trace typos backward to their origin.' It reasons extensively from this new frame, proposing concrete steps like tracing typos backward, locking text post-proofread, and investing upstream. |
| Causal | 1/1 | The response goes well beyond surface causes, identifying multiple specific root cause categories: post-proofread changes bypassing review, typesetting/layout introducing errors, increased volume overwhelming the system, tooling/process changes introducing new error classes, and scope mismatches. It traces the causal chain (upstream error introduction → volume overwhelms near-perfect filter → typos in print). While it doesn't pinpoint the specific fictional AI tool, it correctly identifies 'tooling and process changes' as a candidate and explains the mechanism. |
| Dynamics | 1/1 | The response identifies specific system dynamics: Theory of Constraints (improving a non-bottleneck does nothing), the throughput relationship where 99.8% accuracy still passes errors if input volume explodes, and the cross-component cascade where late-stage revisions bypass the quality gate. It explains concretely why adding 30% proofreading budget yields negligible improvement (moving from 99.8% to maybe 99.9%). |
| Purpose | 1/1 | The response clearly distinguishes the metric (99.8% proofreading accuracy) from the actual purpose (reducing typos in published books). It explicitly calls out the disconnect: 'Measuring the performance of one team ✓ / Assuming that team's domain was the source of the problem ✗.' It evaluates against the real goal — fewer typos in print — rather than the proxy metric. |

**Total: 5/5**

