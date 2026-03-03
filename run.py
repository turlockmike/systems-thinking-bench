#!/usr/bin/env python3
"""Systems Thinking Benchmark for LLMs.

Measures whether models can question the frame of a problem rather than
just reason within it. Scores 5 dimensions of systems thinking on 10
word problems using LLM-as-judge evaluation.

Uses the `claude` CLI for authentication (no API key needed).

Usage:
    python run.py --model sonnet
    python run.py --compare haiku sonnet opus
    python run.py --judge-only results/sonnet_20260303_141500.json
    python run.py --model sonnet --problems 1,3,5
"""

import argparse
import json
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROBLEMS_FILE = Path(__file__).parent / "problems.json"
RESULTS_DIR = Path(__file__).parent / "results"

MODEL_ALIASES = {
    "haiku": "claude-haiku-4-5",
    "sonnet": "claude-sonnet-4-6",
    "opus": "claude-opus-4-6",
}

JUDGE_MODEL = "claude-opus-4-6"
MAX_TOKENS_RESPONSE = 16384
MAX_TOKENS_JUDGE = 4096

DIMENSIONS = [
    "frame_identification",
    "frame_escape",
    "causal_depth",
    "system_dynamics",
    "purpose_alignment",
]

PROMPT_TIERS = {
    "none": "You are a helpful assistant. Answer the question thoroughly.",

    "hint": """\
You are a helpful assistant. When analyzing scenarios, consider whether the \
obvious answer might be missing something. Think carefully before responding.""",

    "deep": """\
You are taking a test that evaluates systems thinking ability.
For each scenario, analyze it carefully. Do not simply address the surface-level question.
Consider: What assumptions are embedded in this scenario? What is the real problem here?
What causal chains, feedback loops, or system dynamics might be at play?
Is the system actually serving its intended purpose, or just optimizing a metric?
Give a thorough analysis.""",
}

DEFAULT_PROMPT_TIER = "none"

JUDGE_SYSTEM = """\
You are an expert evaluator of systems thinking.
You will be given a scenario, a question, a model's response, and reference material.
Score the response on exactly 5 binary dimensions (0 or 1).

Scoring rubric:

1. FRAME IDENTIFICATION (0 or 1)
   0 = Response does not identify the embedded assumption in the scenario
   1 = Response explicitly names the assumption/frame and why it's problematic

2. FRAME ESCAPE (0 or 1)
   0 = Response stays within the given frame or only vaguely gestures beyond it
   1 = Response clearly reframes the problem and reasons from the new frame

3. CAUSAL DEPTH (0 or 1)
   0 = Response addresses only surface-level or proximate causes
   1 = Response traces the causal chain to root causes

4. SYSTEM DYNAMICS (0 or 1)
   0 = Response treats components in isolation or only mentions vague "interactions"
   1 = Response identifies specific feedback loops, emergent behavior, or cross-component cascades

5. PURPOSE ALIGNMENT (0 or 1)
   0 = Response evaluates the system by its stated metric
   1 = Response distinguishes the metric from the actual purpose and evaluates against the real purpose

You MUST respond with ONLY valid JSON in exactly this format (no markdown, no commentary):
{
  "frame_identification": {"score": 0, "reasoning": "..."},
  "frame_escape": {"score": 0, "reasoning": "..."},
  "causal_depth": {"score": 0, "reasoning": "..."},
  "system_dynamics": {"score": 0, "reasoning": "..."},
  "purpose_alignment": {"score": 0, "reasoning": "..."},
  "total": 0
}

Be strict. A score of 1 means the response genuinely demonstrates the skill with specifics, \
not merely mentions a keyword. Vaguely gesturing at "unintended consequences" without \
concrete details is a 0."""


# ---------------------------------------------------------------------------
# Claude CLI interface
# ---------------------------------------------------------------------------

def claude_call(prompt, *, model, system_prompt=None, max_tokens=16384):
    """Call the claude CLI with a prompt via stdin. Returns response text.

    Uses `claude -p --output-format json` for structured output.
    Runs in full isolation: no tools, MCP servers, skills, settings, or
    session persistence — only the model, prompt, and system prompt.
    """
    cmd = [
        "claude", "-p",
        "--model", model,
        "--max-turns", "1",
        "--output-format", "json",
        # Isolation flags — prevent any external context from leaking in
        "--tools", "",                # no tools (pure reasoning)
        "--strict-mcp-config",        # block all MCP servers (no --mcp-config = none)
        "--disable-slash-commands",   # no skills/plugins
        "--setting-sources", "",      # no user/project settings or CLAUDE.md
        "--no-session-persistence",   # don't save benchmark sessions to disk
    ]
    if system_prompt:
        cmd += ["--system-prompt", system_prompt]

    env = {k: v for k, v in __import__("os").environ.items() if k != "CLAUDECODE"}
    proc = subprocess.run(
        cmd,
        input=prompt,
        capture_output=True,
        text=True,
        timeout=300,
        env=env,
        cwd="/tmp",  # clean CWD — no project-level CLAUDE.md
    )

    if proc.returncode != 0:
        raise RuntimeError(f"claude CLI failed (exit {proc.returncode}): {proc.stderr[:500]}")

    # Parse JSON output
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        # Might be NDJSON — take the last result line
        for line in reversed(proc.stdout.strip().split("\n")):
            try:
                data = json.loads(line)
                if data.get("type") == "result":
                    break
            except json.JSONDecodeError:
                continue
        else:
            raise RuntimeError(f"Failed to parse claude CLI output: {proc.stdout[:500]}")

    # Extract the response text
    result_text = data.get("result", "")
    if not result_text:
        # Try content blocks
        for block in data.get("content", []):
            if isinstance(block, dict) and block.get("type") == "text":
                result_text = block["text"]
                break

    usage = data.get("usage", {})
    cost = data.get("total_cost_usd", 0) or 0
    input_tokens = usage.get("input_tokens", 0) or 0
    output_tokens = usage.get("output_tokens", 0) or 0

    return {
        "text": result_text,
        "cost": cost,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
    }


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

def load_problems(indices=None):
    """Load problems from JSON. Optionally filter by 1-based indices."""
    with open(PROBLEMS_FILE) as f:
        problems = json.load(f)
    if indices:
        idx_set = {int(i) - 1 for i in indices.split(",")}
        problems = [p for i, p in enumerate(problems) if i in idx_set]
    return problems


def resolve_model(name):
    """Resolve short aliases to full model IDs."""
    return MODEL_ALIASES.get(name, name)


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_problem(model, problem, prompt_tier):
    """Send one problem to the model, return response dict."""
    user_msg = f"{problem['scenario']}\n\n{problem['question']}"
    system_prompt = PROMPT_TIERS[prompt_tier]
    resp = claude_call(user_msg, model=model, system_prompt=system_prompt,
                       max_tokens=MAX_TOKENS_RESPONSE)
    return {
        "problem_id": problem["id"],
        "model": model,
        "prompt_tier": prompt_tier,
        "response": resp["text"],
        "input_tokens": resp["input_tokens"],
        "output_tokens": resp["output_tokens"],
        "cost": resp["cost"],
    }


def run_all(model, problems, prompt_tier):
    """Run all problems against a model. Returns list of result dicts."""
    results = []
    for i, problem in enumerate(problems):
        label = f"[{i+1}/{len(problems)}] {problem['id']}: {problem['title']}"
        print(f"  {label}...", end=" ", flush=True)
        t0 = time.time()
        result = run_problem(model, problem, prompt_tier)
        elapsed = time.time() - t0
        print(f"done ({result['output_tokens']} tok, ${result['cost']:.3f}, {elapsed:.1f}s)")
        results.append(result)
    return results


# ---------------------------------------------------------------------------
# Judge
# ---------------------------------------------------------------------------

def build_judge_message(problem, response_text):
    """Build the structured message for the judge."""
    dynamics = "\n".join(f"- {d}" for d in problem["key_dynamics"])
    return f"""## Scenario
{problem['scenario']}

## Question Asked
{problem['question']}

## The Implicit Frame
{problem['frame']}

## Key System Dynamics to Look For
{dynamics}

## Shallow Answer (what a surface-level response looks like)
{problem['shallow_answer']}

## Deep Answer (what a strong systems-thinking response looks like)
{problem['deep_answer']}

## Model's Response (this is what you are scoring)
{response_text}

Score this response on the 5 dimensions. Be calibrated: the shallow answer would score \
0-1 total. The deep answer would score 4-5."""


def parse_judge_json(text):
    """Extract JSON from judge response, handling markdown fences."""
    # Strip markdown fences if present
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```\s*$", "", text)
    text = text.strip()

    # Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try extracting first { ... } block
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    return None


def judge_response(problem, response_text, judge_model):
    """Score a single response using LLM-as-judge."""
    msg = build_judge_message(problem, response_text)
    resp = claude_call(msg, model=judge_model, system_prompt=JUDGE_SYSTEM,
                       max_tokens=MAX_TOKENS_JUDGE)
    scores = parse_judge_json(resp["text"])
    if scores is None:
        print(f"\n    WARNING: Failed to parse judge response for {problem['id']}")
        print(f"    Raw: {resp['text'][:200]}")
        scores = {
            dim: {"score": None, "reasoning": "Parse failure"} for dim in DIMENSIONS
        }
        scores["total"] = None
    else:
        # Recompute total from dimension scores for consistency
        total = 0
        for dim in DIMENSIONS:
            s = scores.get(dim, {}).get("score")
            if isinstance(s, (int, float)):
                total += s
        scores["total"] = total
    return scores


def judge_all(problems, run_results, judge_model):
    """Judge all responses. Returns list of scored result dicts."""
    problem_map = {p["id"]: p for p in problems}
    scored = []
    for i, result in enumerate(run_results):
        pid = result["problem_id"]
        problem = problem_map[pid]
        label = f"[{i+1}/{len(run_results)}] {pid}"
        print(f"  {label}...", end=" ", flush=True)
        t0 = time.time()
        scores = judge_response(problem, result["response"], judge_model)
        elapsed = time.time() - t0
        total = scores.get("total", "?")
        print(f"done (score: {total}/5, {elapsed:.1f}s)")
        scored.append({**result, "scores": scores})
    return scored


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def short_dim(dim):
    """Short display name for a dimension."""
    return {
        "frame_identification": "Frame",
        "frame_escape": "Escape",
        "causal_depth": "Causal",
        "system_dynamics": "Dynamics",
        "purpose_alignment": "Purpose",
    }[dim]


def print_results(model, scored_results):
    """Print a formatted results table for one model."""
    print(f"\n{'='*78}")
    print(f"Systems Thinking Benchmark Results")
    print(f"{'='*78}")
    prompt_tier = scored_results[0].get("prompt_tier", "?") if scored_results else "?"
    print(f"Model:       {model}")
    print(f"Prompt:      {prompt_tier}")
    print(f"Date:        {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Header
    hdr = f" {'#':>2} | {'Problem':<28} | {'Frame':>5} | {'Escpe':>5} | {'Causl':>5} | {'Dynmc':>5} | {'Purps':>5} | {'Total':>5}"
    sep = "-" * len(hdr)
    print(hdr)
    print(sep)

    dim_totals = {d: 0 for d in DIMENSIONS}
    overall = 0
    count = 0
    total_cost = 0

    for i, r in enumerate(scored_results):
        scores = r["scores"]
        vals = []
        for dim in DIMENSIONS:
            s = scores.get(dim, {}).get("score")
            if isinstance(s, (int, float)):
                dim_totals[dim] += s
                vals.append(f"{int(s):>5}")
            else:
                vals.append(f"{'?':>5}")
        total = scores.get("total")
        if isinstance(total, (int, float)):
            overall += total
            count += 1
            total_str = f"{int(total):>5}"
        else:
            total_str = f"{'?':>5}"

        total_cost += r.get("cost", 0)
        pid = r["problem_id"]
        print(f" {i+1:>2} | {pid:<28} | {' | '.join(vals)} | {total_str}")

    print(sep)

    # Averages
    n = len(scored_results)
    avg_vals = []
    for dim in DIMENSIONS:
        avg_vals.append(f"{dim_totals[dim]/n:>5.1f}")
    avg_total = f"{overall/n:>5.1f}" if count else "?"
    print(f" {'':>2} | {'AVERAGE':<28} | {' | '.join(avg_vals)} | {avg_total}")

    print(f"\nOVERALL SCORE: {int(overall)}/{n * 5}")
    if total_cost > 0:
        print(f"Run cost:     ${total_cost:.3f}")
    print()

    # Dimension breakdown
    print("Dimension Breakdown:")
    max_possible = n
    for dim in DIMENSIONS:
        pct = dim_totals[dim] / max_possible * 100 if max_possible else 0
        print(f"  {short_dim(dim):<22} {int(dim_totals[dim]):>3}/{max_possible} ({pct:.0f}%)")
    print()


def print_comparison(all_model_results):
    """Print a comparison table across models."""
    print(f"\n{'='*78}")
    print("Model Comparison")
    print(f"{'='*78}")

    hdr = f" {'Model':<24} | {'Frame':>5} | {'Escpe':>5} | {'Causl':>5} | {'Dynmc':>5} | {'Purps':>5} | {'TOTAL':>7}"
    sep = "-" * len(hdr)
    print(hdr)
    print(sep)

    for model, scored in all_model_results.items():
        n = len(scored)
        max_per_dim = n
        max_total = n * 5
        dim_totals = {d: 0 for d in DIMENSIONS}
        overall = 0

        for r in scored:
            scores = r["scores"]
            for dim in DIMENSIONS:
                s = scores.get(dim, {}).get("score")
                if isinstance(s, (int, float)):
                    dim_totals[dim] += s
            t = scores.get("total")
            if isinstance(t, (int, float)):
                overall += t

        vals = [f"{int(dim_totals[d]):>2}/{max_per_dim}" for d in DIMENSIONS]
        short_model = model.replace("claude-", "").replace("-", " ")
        print(f" {short_model:<24} | {' | '.join(vals)} | {int(overall):>3}/{max_total}")

    print(sep)
    print()


def save_results(model, scored_results, judge_model, problems):
    """Save results as structured markdown + JSON under results/{model}/{tier}/."""
    prompt_tier = scored_results[0].get("prompt_tier", "deep") if scored_results else "deep"
    short = model.replace("claude-", "")
    out_dir = RESULTS_DIR / short / prompt_tier
    out_dir.mkdir(parents=True, exist_ok=True)

    problem_map = {p["id"]: p for p in problems}

    n = len(scored_results)
    dim_totals = {d: 0 for d in DIMENSIONS}
    problem_totals = {}
    overall = 0
    total_cost = 0

    for r in scored_results:
        scores = r["scores"]
        t = scores.get("total", 0) or 0
        overall += t
        problem_totals[r["problem_id"]] = t
        total_cost += r.get("cost", 0)
        for dim in DIMENSIONS:
            s = scores.get(dim, {}).get("score")
            if isinstance(s, (int, float)):
                dim_totals[dim] += s

    # --- raw JSON (for programmatic use) ---
    raw = {
        "meta": {
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "judge_model": judge_model,
            "prompt_tier": prompt_tier,
            "system_prompt": PROMPT_TIERS.get(prompt_tier, ""),
            "version": "1.0",
            "num_problems": n,
            "total_cost": round(total_cost, 4),
        },
        "results": scored_results,
        "summary": {
            "model": model,
            "overall_score": int(overall),
            "max_score": n * 10,
            "dimension_totals": {d: int(dim_totals[d]) for d in DIMENSIONS},
            "per_problem_totals": problem_totals,
        },
    }
    json_path = out_dir / "results.json"
    with open(json_path, "w") as f:
        json.dump(raw, f, indent=2)

    # --- summary report (report.md) ---
    tier_desc = {"none": "No hints", "hint": "Gentle hint", "deep": "Full coaching"}
    lines = [
        f"# {short} — {tier_desc.get(prompt_tier, prompt_tier)}",
        "",
        f"**Model:** `{model}`  ",
        f"**Prompt tier:** {prompt_tier} — {tier_desc.get(prompt_tier, '')}  ",
        f"**Judge:** `{judge_model}`  ",
        f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  ",
        f"**Cost:** ${total_cost:.3f}  ",
        "",
        "## Scores",
        "",
        "| # | Problem | Frame | Escape | Causal | Dynamics | Purpose | Total |",
        "|---|---------|:-----:|:------:|:------:|:--------:|:-------:|:-----:|",
    ]

    for i, r in enumerate(scored_results):
        scores = r["scores"]
        pid = r["problem_id"]
        title = problem_map.get(pid, {}).get("title", pid)
        vals = []
        for dim in DIMENSIONS:
            s = scores.get(dim, {}).get("score")
            vals.append(str(int(s)) if isinstance(s, (int, float)) else "?")
        total = scores.get("total")
        total_str = str(int(total)) if isinstance(total, (int, float)) else "?"
        lines.append(f"| {i+1} | {title} | {' | '.join(vals)} | **{total_str}** |")

    max_per_dim = n * 2
    avg_vals = [f"{dim_totals[d]/n:.1f}" for d in DIMENSIONS]
    lines.append(f"| | **Average** | {' | '.join(avg_vals)} | **{overall/n:.1f}** |")

    lines += [
        "",
        f"**Overall: {int(overall)}/{n * 5}**",
        "",
        "## Dimension Breakdown",
        "",
    ]
    max_per_dim = n
    for dim in DIMENSIONS:
        pct = dim_totals[dim] / max_per_dim * 100 if max_per_dim else 0
        lines.append(f"- **{short_dim(dim)}**: {int(dim_totals[dim])}/{max_per_dim} ({pct:.0f}%)")

    report_path = out_dir / "report.md"
    with open(report_path, "w") as f:
        f.write("\n".join(lines) + "\n")

    # --- per-problem response files ---
    for i, r in enumerate(scored_results):
        pid = r["problem_id"]
        problem = problem_map.get(pid, {})
        title = problem.get("title", pid)
        scores = r["scores"]
        total = scores.get("total", "?")

        plines = [
            f"# {title}",
            "",
            f"**Problem:** `{pid}`  ",
            f"**Model:** `{model}`  ",
            f"**Prompt tier:** {prompt_tier}  ",
            f"**Score:** {total}/5",
            "",
            "## Scenario",
            "",
            problem.get("scenario", ""),
            "",
            f"**Question:** {problem.get('question', '')}",
            "",
            "## Model Response",
            "",
            r.get("response", ""),
            "",
            "## Judge Scores",
            "",
            "| Dimension | Score | Reasoning |",
            "|-----------|:-----:|-----------|",
        ]
        for dim in DIMENSIONS:
            entry = scores.get(dim, {})
            s = entry.get("score", "?")
            s_str = str(int(s)) if isinstance(s, (int, float)) else "?"
            reasoning = entry.get("reasoning", "").replace("|", "\\|").replace("\n", " ")
            plines.append(f"| {short_dim(dim)} | {s_str}/1 | {reasoning} |")

        plines += ["", f"**Total: {total}/5**", ""]

        prob_path = out_dir / f"{pid}.md"
        with open(prob_path, "w") as f:
            f.write("\n".join(plines) + "\n")

    print(f"Results saved to {out_dir}/")
    print(f"  report.md    — score summary")
    print(f"  results.json — raw data")
    print(f"  *.md         — per-problem responses")
    return out_dir


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Systems Thinking Benchmark for LLMs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  python run.py --model sonnet\n"
               "  python run.py --compare haiku sonnet opus\n"
               "  python run.py --judge-only results/sonnet_20260303.json\n",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--model", help="Single model to evaluate (e.g., sonnet, opus)")
    group.add_argument("--compare", nargs="+", help="Models to compare")
    group.add_argument("--judge-only", help="Re-judge existing results file")
    parser.add_argument("--problems", help="Comma-separated problem indices, 1-based (e.g., 1,3,5)")
    parser.add_argument("--judge-model", default=JUDGE_MODEL, help=f"Model for judging (default: {JUDGE_MODEL})")
    parser.add_argument("--prompt", choices=list(PROMPT_TIERS), default=DEFAULT_PROMPT_TIER,
                        help="Prompt tier: 'none' (no hints), 'hint' (gentle nudge), 'deep' (full coaching). Default: none")
    args = parser.parse_args()

    # Verify claude CLI is available
    try:
        subprocess.run(["claude", "--version"], capture_output=True, timeout=10)
    except FileNotFoundError:
        print("ERROR: `claude` CLI not found. Install it first.", file=sys.stderr)
        sys.exit(1)

    problems = load_problems(args.problems)
    judge_model = resolve_model(args.judge_model)

    prompt_tier = args.prompt
    tier_label = {"none": "no hints", "hint": "gentle hint", "deep": "full coaching"}[prompt_tier]

    if args.model:
        model = resolve_model(args.model)
        print(f"Running {len(problems)} problems against {model} (prompt: {tier_label})...")
        run_results = run_all(model, problems, prompt_tier)
        print(f"\nJudging with {judge_model}...")
        scored = judge_all(problems, run_results, judge_model)
        print_results(model, scored)
        save_results(model, scored, judge_model, problems)

    elif args.compare:
        all_results = {}
        for name in args.compare:
            model = resolve_model(name)
            print(f"\n{'='*78}")
            print(f"Running: {model} (prompt: {tier_label})")
            print(f"{'='*78}")
            run_results = run_all(model, problems, prompt_tier)
            print(f"\nJudging with {judge_model}...")
            scored = judge_all(problems, run_results, judge_model)
            print_results(model, scored)
            save_results(model, scored, judge_model, problems)
            all_results[model] = scored

        print_comparison(all_results)

    elif args.judge_only:
        path = Path(args.judge_only)
        if not path.exists():
            print(f"ERROR: File not found: {path}", file=sys.stderr)
            sys.exit(1)
        with open(path) as f:
            data = json.load(f)
        run_results = data["results"]
        model = data["meta"]["model"]
        print(f"Re-judging {len(run_results)} results from {model} with {judge_model}...")
        scored = judge_all(problems, run_results, judge_model)
        print_results(model, scored)
        save_results(model, scored, judge_model, problems)


if __name__ == "__main__":
    main()
