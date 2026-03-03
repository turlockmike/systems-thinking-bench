# Systems Thinking Benchmark for LLMs

Measures whether language models can question the frame of a problem rather than just reason within it.

## The Problem

LLMs are excellent at reasoning *within* a given frame but rarely question whether the frame itself is wrong. This benchmark presents 10 word problems where the surface-level diagnosis is plausible but incorrect — the real answer requires stepping outside the frame to identify hidden system dynamics.

## Results

> Full results with model responses and judge reasoning: [`results/`](results/)

### Haiku 4.5 — No Hints

| # | Problem | Frame | Escape | Causal | Dynamics | Purpose | Total |
|---|---------|:-----:|:------:|:------:|:--------:|:-------:|:-----:|
| 1 | [The Helpful Cache](results/haiku-4-5/none/infra-01.md) | 1 | 1 | 0 | 0 | 1 | **3** |
| 2 | [The Reliable Backup](results/haiku-4-5/none/infra-02.md) | 1 | 1 | 1 | 1 | 1 | **5** |
| 3 | [The Accurate Forecast](results/haiku-4-5/none/ml-01.md) | 1 | 1 | 1 | 0 | 1 | **4** |
| 4 | [The Slow Test Suite](results/haiku-4-5/none/sw-01.md) | 0 | 0 | 1 | 1 | 1 | **3** |
| 5 | [The Fair Algorithm](results/haiku-4-5/none/health-01.md) | 1 | 0 | 0 | 1 | 1 | **3** |
| 6 | [The Empty Queue](results/haiku-4-5/none/supply-01.md) | 0 | 0 | 0 | 0 | 0 | **0** |
| 7 | [The Successful Migration](results/haiku-4-5/none/sw-02.md) | 1 | 0 | 1 | 1 | 1 | **4** |
| 8 | [The Escalation Policy](results/haiku-4-5/none/org-01.md) | 0 | 0 | 0 | 0 | 1 | **1** |
| 9 | [The Green Dashboard](results/haiku-4-5/none/infra-03.md) | 1 | 1 | 1 | 1 | 1 | **5** |
| 10 | [The Productive Team](results/haiku-4-5/none/org-02.md) | 1 | 0 | 0 | 1 | 0 | **2** |
| | **Total** | **7/10** | **4/10** | **5/10** | **6/10** | **8/10** | **30/50** |

**Weakest dimension:** Frame Escape (40%) — Haiku identifies problems but doesn't reframe them.
**Hardest problems:** The Empty Queue (0/5), The Escalation Policy (1/5) — complete blind spots.

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

| # | ID | Domain | Title | Core Dynamic |
|---|-----|--------|-------|-------------|
| 1 | infra-01 | Infrastructure | The Helpful Cache | Cache masks data growth, amplifies root cause |
| 2 | infra-02 | Infrastructure | The Reliable Backup | Backup preceded corruption, not prevented it |
| 3 | ml-01 | ML/Data | The Accurate Forecast | 94% accuracy hides catastrophic failure on outliers |
| 4 | sw-01 | Software | The Slow Test Suite | Speed gain came from gutting integration tests |
| 5 | health-01 | Healthcare | The Fair Algorithm | Fairness constraint doesn't fix proxy variable |
| 6 | supply-01 | Supply Chain | The Empty Queue | Empty queue is lost buffer, not success |
| 7 | sw-02 | Software | The Successful Migration | Deployment speed up, development velocity down |
| 8 | org-01 | Organizational | The Escalation Policy | Escalation suppresses local problem-solving |
| 9 | infra-03 | Infrastructure | The Green Dashboard | Latency hiding across 8 services |
| 10 | org-02 | Organizational | The Productive Team | More people, less output; coordination overhead |

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
