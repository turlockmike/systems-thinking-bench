# The Empty Queue

**Problem:** `supply-01`  
**Model:** `claude-haiku-4-5`  
**Prompt tier:** none  
**Score:** 0/5

## Scenario

A fulfillment center installs a new conveyor system that moves packages 3x faster. Throughput increases for two weeks, then drops below the original level. The conveyors are working perfectly. The queue of packages waiting to be processed is always empty.

**Question:** Why did throughput drop despite the faster conveyors?

## Model Response

# The Bottleneck Shifted Upstream

The problem is a classic **constraint migration** issue. Here's what happened:

## Initial Boost (First Two Weeks)
The fulfillment center likely had a **backlog of packages** waiting to be processed. The faster conveyors cleared this backlog quickly, producing the throughput spike.

## The Real Limitation Emerges
Once the backlog was gone, the system hit a new constraint: **the upstream processes can't feed packages to the conveyor fast enough.**

Since the queue is always empty, the conveyors are now sitting idle waiting for packages. The bottleneck has shifted from the conveyor speed to whatever comes *before* it:
- Receiving/unloading packages from trucks
- Initial sorting or prep work
- Manual hand-offs or staging areas
- Other upstream equipment or manual processes

## Why Throughput Dropped Below Original
- The upstream processes were likely optimized (pace, staffing, workflow) to match the *original* conveyor speed
- They now can't fill the faster system's capacity
- This mismatch may have created inefficiencies or idle time that didn't exist before
- The system is potentially doing more work to move empty conveyors than before

## The Lesson
**Optimizing a single component doesn't improve system throughput if other components are constrained.** You need to identify and optimize the true bottleneck—which is often upstream or downstream of where you're looking, not the most obviously slow component.

To fix this, they should analyze and upgrade the upstream processes to match the conveyor's new capacity.

## Judge Scores

| Dimension | Score | Reasoning |
|-----------|:-----:|-----------|
| Frame | 0/1 | The response does not identify the embedded assumption. The key insight is that the old conveyor's slowness provided an unrecognized buffering function. Instead, the model simply relocates the bottleneck upstream, staying entirely within a constraint-migration frame. |
| Escape | 0/1 | The response shifts from 'downstream bottleneck' to 'upstream bottleneck,' which is merely moving the location of a constraint rather than genuinely reframing the problem. It never arrives at the buffering/variance-smoothing reframe that constitutes the deep insight. |
| Causal | 0/1 | The causal explanation is shallow: upstream processes can't feed packages fast enough. It doesn't trace the root cause—that removing the slow conveyor destroyed an accidental buffer, exposing workers to demand variance, which degrades human throughput even if average load is constant. |
| Dynamics | 0/1 | No specific feedback loops, emergent behavior, or cross-component cascades are identified. The response treats the problem as a simple linear constraint shift rather than recognizing the emergent buffering function, how variance kills human throughput, or how 'empty queue' is a misleading signal. |
| Purpose | 0/1 | The response takes 'empty queue' at face value as evidence of upstream starvation. It never questions whether the empty queue metric is misleading or distinguishes the metric (queue emptiness = efficiency) from the actual purpose (steady, sustainable throughput for human workers). |

**Total: 0/5**

