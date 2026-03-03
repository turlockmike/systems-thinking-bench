# Benchmark Results

Results are organized by model and prompt tier.

## How to Read

Each `{model}/{tier}/` directory contains:

- **`report.md`** — Score summary table with overall and per-dimension breakdown
- **`{problem-id}.md`** — Full detail for each problem: scenario, model response, and judge scoring with reasoning
- **`results.json`** — Raw data for programmatic use

## Available Results

### [haiku-4-5](haiku-4-5/)

| Tier | Overall | Frame | Escape | Causal | Dynamics | Purpose |
|------|:-------:|:-----:|:------:|:------:|:--------:|:-------:|
| [none](haiku-4-5/none/report.md) | **33/50** (66%) | 7/10 | 5/10 | 4/10 | 8/10 | 9/10 |

### [sonnet-4-6](sonnet-4-6/)

| Tier | Overall | Frame | Escape | Causal | Dynamics | Purpose |
|------|:-------:|:-----:|:------:|:------:|:--------:|:-------:|
| [none](sonnet-4-6/none/report.md) | **46/50** (92%) | 8/10 | 9/10 | 9/10 | 10/10 | 10/10 |

### [opus-4-6](opus-4-6/)

| Tier | Overall | Frame | Escape | Causal | Dynamics | Purpose |
|------|:-------:|:-----:|:------:|:------:|:--------:|:-------:|
| [none](opus-4-6/none/report.md) | **45/50** (90%) | 9/10 | 9/10 | 8/10 | 9/10 | 10/10 |

## Scoring

Each problem is scored on 5 binary dimensions (0 or 1):

| Dimension | Question |
|-----------|----------|
| **Frame Identification** | Did it name the embedded assumption? |
| **Frame Escape** | Did it reframe the problem? |
| **Causal Depth** | Did it trace root causes? |
| **System Dynamics** | Did it identify feedback loops? |
| **Purpose Alignment** | Did it distinguish metric from purpose? |

**Max score per problem: 5. Max total: 50.**

## Prompt Tiers

- **none** — No coaching. Just "answer the question thoroughly."
- **hint** — Gentle nudge: "consider whether the obvious answer might be missing something."
- **deep** — Full coaching: explicitly asks for assumptions, feedback loops, metric gaming.
