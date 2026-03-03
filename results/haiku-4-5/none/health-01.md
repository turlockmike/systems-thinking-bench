# The Fair Algorithm

**Problem:** `health-01`  
**Model:** `claude-haiku-4-5`  
**Prompt tier:** none  
**Score:** 3/5

## Scenario

A hospital uses an algorithm to allocate follow-up appointments. It predicts which patients are most likely to have complications and prioritizes them. An audit reveals that the algorithm schedules Black patients at significantly lower rates than white patients with the same conditions. The team is asked to add a fairness constraint to equalize scheduling rates.

**Question:** Will adding a fairness constraint fix the racial disparity?

## Model Response

# Adding a Fairness Constraint Alone Won't Fix the Problem

While a fairness constraint might **reduce the statistical disparity**, it likely won't address the underlying racial inequity. Here's why:

## The Constraint Only Treats the Symptom

**What a fairness constraint does:**
- Equalizes the scheduling rate between racial groups
- Addresses the *metric* of disparity

**What it doesn't do:**
- Investigate *why* the disparity exists
- Fix the root cause of the bias

## Likely Root Causes Still Unaddressed

The disparity suggests:

1. **Biased predictions**: The algorithm's "complication risk" predictions may be systematically lower for Black patients due to:
   - Biased training data (historical under-treatment patterns)
   - Proxy variables (zip code, insurance, socioeconomic status)
   - Data quality gaps (less complete medical histories for certain groups)

2. **Structural issues**: Problems in how the model was developed, validated, or deployed

## Risks of This Approach Alone

- **False confidence**: Creates appearance of fairness without addressing underlying bias
- **New inequities**: Equal *scheduling rates* don't ensure equal *care quality* if the risk predictions remain biased
- **Possible harm**: Might schedule low-risk white patients unnecessarily while missing complications in Black patients

## What Actually Needs to Happen

- Audit *why* disparities exist
- Validate whether risk predictions are accurate across racial groups
- Check for proxy variables encoding race
- Retrain on representative, unbiased data
- Use fairness constraint as *one tool* within comprehensive remediation
- Maintain ongoing monitoring

**The constraint is necessary but insufficient.**

## Judge Scores

| Dimension | Score | Reasoning |
|-----------|:-----:|-----------|
| Frame | 1/1 | The response identifies that the fairness constraint 'only treats the symptom' and that the real issue lies in proxy variables and structural factors encoded in the inputs. It explicitly states the constraint addresses the 'metric of disparity' but not the root cause, which identifies the problematic assumption that the output is the problem. |
| Escape | 0/1 | While the response gestures beyond the output-bias frame, it doesn't clearly reframe the problem as 'change what the model is predicting.' Its recommendations are generic (audit, retrain, monitor) rather than reasoning from a new frame that the proxy variable itself must be replaced with actual health need measurement. It stays in a 'fix the algorithm' frame rather than a 'the algorithm is measuring the wrong thing' frame. |
| Causal | 0/1 | The response lists possible causes (biased training data, proxy variables, data quality gaps) but doesn't trace the specific causal chain: spending used as proxy for health needs → Black patients have less healthcare access → lower spending → algorithm interprets them as healthier → lower scheduling. It identifies intermediate causes without pinpointing the root structural mechanism with specificity. |
| Dynamics | 1/1 | The response identifies a specific cross-component cascade: adding a fairness constraint equalizes scheduling rates but leaves risk predictions biased, resulting in 'scheduling low-risk white patients unnecessarily while missing complications in Black patients.' This is a concrete description of how the constraint interacts with the biased predictions to create a new, different harm pattern. |
| Purpose | 1/1 | The response explicitly distinguishes the metric (equal scheduling rates) from the actual purpose (equal care quality and accurate risk assessment). It states 'Equal scheduling rates don't ensure equal care quality if the risk predictions remain biased' and flags 'false confidence' as a risk of optimizing for the metric alone. |

**Total: 3/5**

