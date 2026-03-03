# The Diligent Proofreaders

**Problem:** `infra-02`  
**Model:** `claude-sonnet-4-6`  
**Prompt tier:** none  
**Score:** 5/5

## Scenario

A publishing house notices more typos reaching print. They audit the proofreading team: accuracy is 99.8%, virtually flawless. Management increases the proofreading budget by 30%, hiring additional reviewers and adding a second pass. Six months later, typo rates in published books are unchanged.

**Question:** How should they fix the typo problem?

## Model Response

## The Core Diagnostic Problem

The critical clue is that **adding more proofreading had zero effect**. This is actually strong evidence that proofreading is *not the source of the problem*. Management identified a plausible cause without verifying the causal link, then doubled down on a solution that can't work.

---

## Where the Typos Are Probably Coming From

If errors survive a 99.8%-accurate double-pass proofreading process, they are almost certainly being **introduced after proofreading**. Common culprits in publishing:

| Stage | How Errors Enter |
|---|---|
| **Typesetting/layout** | Copy-paste errors, OCR conversion, reformatting |
| **Author corrections** | Authors review galleys and introduce new errors while "fixing" old ones |
| **Late editorial changes** | Last-minute revisions that bypass the proofread manuscript |
| **File conversion** | Manuscript → print-ready PDF transformations |
| **Plate/digital prep** | Final production steps touching the text |

---

## What They Should Actually Do

### 1. Map the Entire Workflow, Not Just One Stage
Trace every point where the text is *touched* between "proofreading complete" and "book printed." The error is likely entering at one of those handoffs.

### 2. Verify the Causal Chain
Compare the *proofread manuscript* directly with the *final printed book*. Are the typos in the approved manuscript, or are they new? This one check would have revealed the real problem immediately.

### 3. Lock the Manuscript After Approval
Implement a strict policy: **no text changes after final proof without a mandatory re-proof cycle.** Author corrections and editorial tweaks are a notorious source of post-proof contamination.

### 4. Audit the Right Metric
99.8% accuracy sounds extraordinary, but:
- It may be measuring accuracy *within proofreading's scope* rather than end-to-end accuracy
- At 100,000 words, 99.8% still means ~200 errors per book
- More importantly, if errors appear *downstream*, proofreading accuracy is irrelevant

### 5. Apply Theory of Constraints Logic
Adding capacity to a non-bottleneck does nothing. The constraint here isn't proofreading throughput—it's an unidentified post-proof contamination point. All the budget increase accomplished was making a non-problem more efficient.

---

## The Broader Lesson

The publishing house made a classic systems error:

> **They assumed the location of the problem rather than tracing it.**

The presence of typos in the *output* was taken as evidence of failures in *proofreading*, skipping the step of verifying whether the proofread manuscript was clean. This is symptom-chasing without root cause analysis.

**The fix**: Before spending a dollar, compare the approved proof to the final print. The mismatch will point directly to the real culprit—likely in under-scrutinized production stages that no one thought to audit because they don't carry the word "proofreading."

## Judge Scores

| Dimension | Score | Reasoning |
|-----------|:-----:|-----------|
| Frame | 1/1 | The response explicitly names the embedded assumption: 'Management identified a plausible cause without verifying the causal link, then doubled down on a solution that can't work.' It later summarizes: 'They assumed the location of the problem rather than tracing it.' The response clearly identifies that the scenario's frame equating 'typos in output' with 'proofreading failure' is the core diagnostic error. |
| Escape | 1/1 | The response clearly reframes the problem away from proofreading and toward a full-workflow investigation. It proposes mapping every stage where text is touched, comparing proofread manuscripts to final printed books, and identifies specific alternative error introduction points (typesetting, author corrections, file conversion, late editorial changes). While the reframe focuses on downstream contamination rather than the reference's upstream volume explosion, it is a genuine, well-reasoned escape from the original frame. |
| Causal | 1/1 | The response traces beyond proximate causes. It reasons: high accuracy + no improvement from added capacity → errors are not in this stage → must identify actual introduction points. It applies Theory of Constraints logic (adding capacity to a non-bottleneck does nothing). It also briefly identifies the volume issue ('99.8% still means ~200 errors per book'). While it doesn't identify the specific upstream trigger (AI drafting tool) from the reference, it constructs a coherent causal chain to root-level production processes rather than staying at the surface. |
| Dynamics | 1/1 | The response identifies multiple specific system dynamics: (1) Theory of Constraints — adding capacity at a non-bottleneck has zero effect on throughput; (2) Cross-stage contamination — errors introduced at handoff points between proofreading and print propagate undetected; (3) Metric-system disconnect — stage-level accuracy (99.8%) can be decoupled from system-level output quality. These are concrete, named dynamics, not vague gestures. |
| Purpose | 1/1 | The response explicitly distinguishes the metric from the purpose: '99.8% accuracy sounds extraordinary, but... It may be measuring accuracy within proofreading's scope rather than end-to-end accuracy' and 'if errors appear downstream, proofreading accuracy is irrelevant.' It evaluates against the real purpose (typo-free published books) rather than the stated metric (proofreading accuracy), recognizing these can diverge completely. |

**Total: 5/5**

