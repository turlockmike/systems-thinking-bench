# The Diligent Proofreaders

**Problem:** `infra-02`  
**Model:** `claude-haiku-4-5`  
**Prompt tier:** none  
**Score:** 4/5

## Scenario

A publishing house notices more typos reaching print. They audit the proofreading team: accuracy is 99.8%, virtually flawless. Management increases the proofreading budget by 30%, hiring additional reviewers and adding a second pass. Six months later, typo rates in published books are unchanged.

**Question:** How should they fix the typo problem?

## Model Response

# The Real Problem Isn't Proofreading Accuracy

This is a classic case of **treating the symptom, not the disease**. A 99.8% accuracy rate is excellent—the issue lies elsewhere in the system.

## What's Actually Happening

Before spending more on proofreading, they need to ask:
- **Did publication volume increase?** If they're printing 30% more books, even with 99.8% accuracy, absolute errors will rise
- **Where do typos actually originate?** Are they coming from manuscripts, typesetting, printing, or being introduced during "corrections"?
- **Are corrections being properly implemented?** More reviewers catching errors doesn't help if those fixes don't make it to print

## What They Should Do Instead

1. **Map the full system**: Track where typos enter and exit at each stage—manuscript → proofreading → typesetting → printing. The problem might be upstream (author quality, insufficient editorial guidance) or downstream (typesetting workflow, printing process).

2. **Analyze the data**: 
   - What % of typos are new vs. reintroduced?
   - Are certain types of errors dominating?
   - Did volume, content type, or staff turnover change?

3. **Focus on leverage points**, not effort:
   - Better manuscript intake standards or author guidelines
   - Smarter automation (advanced spell-check, consistency tools)
   - Process redesign at the real bottleneck

4. **Question the assumption**: If proofreading is already 99.8% accurate, pouring resources there hits diminishing returns. The problem is probably systemic, not individual reviewer competence.

**The lesson**: More resources applied to an already-efficient process won't fix inefficiencies elsewhere.

## Judge Scores

| Dimension | Score | Reasoning |
|-----------|:-----:|-----------|
| Frame | 1/1 | The response explicitly identifies the flawed assumption: 'If proofreading is already 99.8% accurate, pouring resources there hits diminishing returns. The problem is probably systemic, not individual reviewer competence.' It clearly names the embedded frame that proofreading needs fixing and explains why it's wrong. |
| Escape | 1/1 | The response reframes from 'fix proofreading' to 'map the full production pipeline and find the real source of errors.' It reasons from this new frame by proposing upstream (manuscript quality, editorial guidance) and downstream (typesetting, printing) investigations, and explicitly redirects effort away from proofreading. |
| Causal | 0/1 | The response lists plausible possibilities (volume increase, manuscript quality, typesetting errors, corrections not implemented) but does not trace the causal chain to a specific root cause. It functions as a diagnostic framework rather than an actual root-cause analysis. The deep answer identifies a specific upstream tool change generating 5x errors; this response stays at the question-asking level. |
| Dynamics | 1/1 | The response identifies a specific throughput dynamic: 'If they're printing 30% more books, even with 99.8% accuracy, absolute errors will rise.' It also identifies a correction-reintroduction cascade ('more reviewers catching errors doesn't help if those fixes don't make it to print') and the diminishing-returns dynamic of adding capacity to an already-efficient stage. These are concrete cross-component interactions. |
| Purpose | 1/1 | The response clearly distinguishes the metric (99.8% proofreading accuracy) from the actual purpose (fewer typos in published books). It explicitly states that high accuracy at the proofreading stage is insufficient when the problem lies elsewhere, and that 'more resources applied to an already-efficient process won't fix inefficiencies elsewhere.' |

**Total: 4/5**

