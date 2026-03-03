# Systems Thinking Benchmark for LLMs

Measures whether language models can question the frame of a problem rather than just reason within it.

## The Problem

LLMs are excellent at reasoning *within* a given frame but rarely question whether the frame itself is wrong. This benchmark presents 10 word problems where the surface-level diagnosis is plausible but incorrect — the real answer requires stepping outside the frame to identify hidden system dynamics.

## How It Works

Each problem presents a realistic scenario with an embedded assumption. The model's response is scored by an LLM judge (Opus) on 5 dimensions:

| Dimension | What It Measures |
|-----------|-----------------|
| **Frame Identification** | Does it name the embedded assumption? |
| **Frame Escape** | Does it reframe the problem? |
| **Causal Depth** | Does it trace root causes, not just symptoms? |
| **System Dynamics** | Does it identify feedback loops and emergent behavior? |
| **Purpose Alignment** | Does it distinguish the metric from the actual goal? |

Each dimension is scored 0-2. Maximum score per problem: 10. Maximum total: 100.

## Prompt Tiers

The benchmark supports three levels of system prompt coaching via `--prompt`:

- **`none`** (default) — No hints. Just "answer the question thoroughly."
- **`hint`** — Gentle nudge: "consider whether the obvious answer might be missing something."
- **`deep`** — Full coaching: explicitly tells the model to look for assumptions, feedback loops, and metric gaming.

The gap between `none` and `deep` scores reveals how much a model depends on prompting vs. innate systems thinking ability.

## The 10 Problems

| # | ID | Domain | Title | Core Dynamic |
|---|-----|--------|-------|-------------|
| 1 | infra-01 | Infrastructure | The Helpful Cache | Fix masks data growth, amplifies root cause |
| 2 | infra-02 | Infrastructure | The Reliable Backup | Backup preceded corruption, not prevented it |
| 3 | ml-01 | ML/Data | The Accurate Forecast | 94% accuracy hides catastrophic failure on outliers |
| 4 | sw-01 | Software | Faster CI | Speed gain came from gutting integration tests |
| 5 | ml-02 | ML/Data | The Fair Algorithm | Fairness constraint doesn't fix proxy variable |
| 6 | sw-02 | Software | The Empty Queue | Empty queue is lost buffer, not success |
| 7 | sw-03 | Software | Monolith to Microservices | Deployment speed up, development velocity down |
| 8 | org-01 | Organizational | Junior Engineers | Stopped learning; cut senior pipeline |
| 9 | infra-03 | Infrastructure | Green Dashboard | Latency hiding across 8 services |
| 10 | org-02 | Organizational | Adding Engineers | More people, less output; coordination overhead |

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

# Re-judge existing results with a different judge model
python run.py --judge-only results/haiku_4_5_none_20260303.json
python run.py --judge-only results/haiku_4_5_none_20260303.json --judge-model sonnet
```

## Isolation

Every model invocation runs in full isolation — no tools, no user configuration, no external context:

- `--tools ""` — pure reasoning, no tool use
- `--strict-mcp-config` — no MCP servers
- `--disable-slash-commands` — no skills/plugins
- `--setting-sources ""` — no user/project settings or CLAUDE.md
- `--no-session-persistence` — sessions not saved to disk
- CWD set to `/tmp` — no project-level configuration

The model sees only the system prompt and the problem. Nothing else.

## Example Output

```
==============================================================================
Systems Thinking Benchmark Results
==============================================================================
Model:       claude-haiku-4-5
Prompt:      none
Date:        2026-03-03 13:33:54

  # | Problem                      | Frame | Escpe | Causl | Dynmc | Purps | Total
----------------------------------------------------------------------------------
  1 | infra-01                     |     2 |     1 |     1 |     1 |     1 |     6
  2 | infra-02                     |     2 |     2 |     2 |     2 |     2 |    10
  3 | ml-01                        |     2 |     2 |     1 |     1 |     2 |     8
----------------------------------------------------------------------------------
    | AVERAGE                      |   2.0 |   1.7 |   1.3 |   1.3 |   1.7 |   8.0

OVERALL SCORE: 24/30
```

## License

MIT
