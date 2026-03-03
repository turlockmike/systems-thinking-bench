# Systems Thinking Benchmark for LLMs

Measures whether language models can question the frame of a problem rather than just reason within it.

## The Problem

LLMs are excellent at reasoning *within* a given frame but rarely question whether the frame itself is wrong. This benchmark presents 10 word problems where the surface-level diagnosis is plausible but incorrect — the real answer requires stepping outside the frame to identify hidden system dynamics.

## Results

> Full results with model responses and judge reasoning: [`results/`](results/)

### Model Comparison — No Hints

| Model | Overall | Frame | Escape | Causal | Dynamics | Purpose | Cost |
|-------|:-------:|:-----:|:------:|:------:|:--------:|:-------:|-----:|
| [Haiku 4.5](results/haiku-4-5/none/report.md) | **33/50** (66%) | 7/10 | 5/10 | 4/10 | 8/10 | 9/10 | $0.06 |
| [Opus 4.6](results/opus-4-6/none/report.md) | **45/50** (90%) | 9/10 | 9/10 | 8/10 | 9/10 | 10/10 | $0.38 |
| [Sonnet 4.6](results/sonnet-4-6/none/report.md) | **46/50** (92%) | 8/10 | 9/10 | 9/10 | 10/10 | 10/10 | $0.53 |

### Per-Problem Breakdown

| # | Problem | Haiku | Sonnet | Opus |
|---|---------|:-----:|:------:|:----:|
| 1 | [The Efficient Dehumidifier](results/haiku-4-5/none/infra-01.md) | 1 | 2 | 4 |
| 2 | [The Diligent Proofreaders](results/haiku-4-5/none/infra-02.md) | 4 | 5 | 5 |
| 3 | [The Reliable Route](results/haiku-4-5/none/ml-01.md) | 4 | 5 | 5 |
| 4 | [The Specialized Kitchen](results/haiku-4-5/none/sw-01.md) | 4 | 5 | 5 |
| 5 | [The Smart Meters](results/haiku-4-5/none/health-01.md) | 4 | 5 | 5 |
| 6 | [The Powerful Pump](results/haiku-4-5/none/supply-01.md) | 2 | 4 | **1** |
| 7 | [The Efficient Curriculum](results/haiku-4-5/none/sw-02.md) | 5 | 5 | 5 |
| 8 | [The Quality Standard](results/haiku-4-5/none/org-01.md) | 5 | 5 | 5 |
| 9 | [The Perfect Ingredients](results/haiku-4-5/none/infra-03.md) | 3 | 5 | 5 |
| 10 | [The Bigger Ensemble](results/haiku-4-5/none/org-02.md) | 1 | 5 | 5 |

**The Powerful Pump** is the hardest problem — even Opus scores 1/5, missing the biological fitness mechanism entirely. **The Efficient Dehumidifier** also trips up all models on causal depth (recipe change → cure time change → dehumidifier skips chemistry).

## How It Works

Each problem presents a realistic scenario with an embedded assumption. The model's response is scored by an LLM judge (Opus) on 5 binary dimensions:

| Dimension | Question |
|-----------|----------|
| **Frame Identification** | Did it name the embedded assumption? |
| **Frame Escape** | Did it reframe the problem and reason from the new frame? |
| **Causal Depth** | Did it trace the full causal chain to root causes? |
| **System Dynamics** | Did it identify feedback loops or emergent behavior? |
| **Purpose Alignment** | Did it distinguish the metric from the actual goal? |

Each dimension is 0 or 1. Max per problem: 5. Max total: 50.

## Prompt Tiers

The benchmark supports three levels of system prompt coaching via `--prompt`:

- **`none`** (default) — No hints. Just "answer the question thoroughly."
- **`hint`** — Gentle nudge: "consider whether the obvious answer might be missing something."
- **`deep`** — Full coaching: explicitly tells the model to look for assumptions, feedback loops, and metric gaming.

The gap between `none` and `deep` scores reveals how much a model depends on prompting vs. innate systems thinking.

## The 10 Problems

Each problem uses a novel, domain-specific scenario to avoid pattern-matching to well-known examples. The underlying system dynamics are real, but the contexts are unusual enough that models must actually reason rather than recall.

| # | ID | Domain | Title | Core Dynamic |
|---|-----|--------|-------|-------------|
| 1 | infra-01 | Artisan Manufacturing | The Efficient Dehumidifier | Fix accelerates a process that needs time; symptom treatment skips necessary chemistry |
| 2 | infra-02 | Publishing | The Diligent Proofreaders | Downstream stage is perfect; problem is upstream tool nobody evaluated |
| 3 | ml-01 | Aviation | The Reliable Route | Aggregate metric hides failures concentrated on the routes where they matter most |
| 4 | sw-01 | Culinary | The Specialized Kitchen | Decomposing integration destroys the responsive adaptation that was the actual craft |
| 5 | health-01 | Urban Planning | The Smart Meters | Proxy variable (turnover) measures usage pattern, not demand; single mechanism can't serve different ecologies |
| 6 | supply-01 | Marine Biology | The Powerful Pump | Removing a constraint destroys a hidden biological function; symptom fix kills the organism |
| 7 | sw-02 | Education | The Efficient Curriculum | Optimized stated goal (grammar) and destroyed the social mechanism that drove learning behavior |
| 8 | org-01 | Craftsmanship | The Quality Standard | Eliminating failure removes the exploration that produces both bad outcomes and breakthroughs |
| 9 | infra-03 | Perfumery | The Perfect Ingredients | Component quality doesn't predict system quality; interactions dominate perception |
| 10 | org-02 | Music | The Bigger Ensemble | Implicit coordination was the product; adding people forces explicit coordination that kills spontaneity |

## Usage

Requires the [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code).

```bash
# Run a single model (default: no prompt coaching)
python run.py --model haiku
python run.py --model sonnet
python run.py --model opus

# Test with different prompt tiers
python run.py --model haiku --prompt none
python run.py --model haiku --prompt hint
python run.py --model haiku --prompt deep

# Compare models head-to-head
python run.py --compare haiku sonnet opus

# Run a subset of problems
python run.py --model haiku --problems 1,3,5

# Re-judge existing results
python run.py --judge-only results/haiku-4-5/none/results.json
python run.py --judge-only results/haiku-4-5/none/results.json --judge-model sonnet
```

## Isolation

Every model invocation runs in full isolation — no tools, no user config, no external context:

- `--tools ""` — pure reasoning, no tool use
- `--strict-mcp-config` — no MCP servers
- `--disable-slash-commands` — no skills/plugins
- `--setting-sources ""` — no user/project settings or CLAUDE.md
- `--no-session-persistence` — sessions not saved to disk
- CWD set to `/tmp` — no project-level configuration

The model sees only the system prompt and the problem. Nothing else.

## License

MIT
