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
Score the response on exactly 5 dimensions, each 0-2 points.

Scoring rubric:

1. FRAME IDENTIFICATION (0-2)
   0 = Response accepts the scenario's framing without question
   1 = Response hints at or partially identifies the embedded assumption
   2 = Response explicitly names the assumption/frame and why it's problematic

2. FRAME ESCAPE (0-2)
   0 = Response stays entirely within the given frame
   1 = Response gestures beyond the frame but primarily answers within it
   2 = Response clearly reframes the problem and reasons from the new frame

3. CAUSAL DEPTH (0-2)
   0 = Response addresses only the proximate/surface cause
   1 = Response traces one level deeper than the surface
   2 = Response traces the full causal chain to root causes

4. SYSTEM DYNAMICS (0-2)
   0 = Response treats components in isolation
   1 = Response identifies some interactions or secondary effects
   2 = Response identifies feedback loops, emergent behavior, or cross-component cascades

5. PURPOSE ALIGNMENT (0-2)
   0 = Response evaluates only whether the system "works" (meets its stated metric)
   1 = Response questions whether the metric reflects the actual goal
   2 = Response clearly distinguishes the metric from the purpose and evaluates against the real purpose

You MUST respond with ONLY valid JSON in exactly this format (no markdown, no commentary):
{
  "frame_identification": {"score": 0, "reasoning": "..."},
  "frame_escape": {"score": 0, "reasoning": "..."},
  "causal_depth": {"score": 0, "reasoning": "..."},
  "system_dynamics": {"score": 0, "reasoning": "..."},
  "purpose_alignment": {"score": 0, "reasoning": "..."},
  "total": 0
}

Be strict. A score of 2 means the response genuinely demonstrates the skill, not merely \
mentions a keyword. A mediocre response that vaguely gestures at "unintended consequences" \
without specifics is a 1, not a 2."""


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
0-3 total. The deep answer would score 9-10."""


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
        print(f"done (score: {total}/10, {elapsed:.1f}s)")
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

    print(f"\nOVERALL SCORE: {int(overall)}/{n * 10}")
    if total_cost > 0:
        print(f"Run cost:     ${total_cost:.3f}")
    print()

    # Dimension breakdown
    print("Dimension Breakdown:")
    max_possible = n * 2
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
        max_per_dim = n * 2
        max_total = n * 10
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


def save_results(model, scored_results, judge_model):
    """Save results to JSON file."""
    RESULTS_DIR.mkdir(exist_ok=True)
    prompt_tier = scored_results[0].get("prompt_tier", "deep") if scored_results else "deep"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    short = model.replace("claude-", "").replace("-", "_")
    path = RESULTS_DIR / f"{short}_{prompt_tier}_{ts}.json"

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

    output = {
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

    with open(path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"Results saved to {path}")
    return path


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
        save_results(model, scored, judge_model)

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
            save_results(model, scored, judge_model)
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
        save_results(model, scored, judge_model)


if __name__ == "__main__":
    main()
