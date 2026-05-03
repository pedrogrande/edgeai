Great question. The shortcuts reference "known patterns" but I never made the patterns themselves explicit. Let me fix that.

## The Five Validated Patterns

Each pattern comes from one of our six agent design exercises. Each has been validated through the full CAWDP process. Each pre-fills significant portions of the template.

---

### Pattern 1: The Signal Detector

**Source**: Watchman (Run 1), confirmed by Sentinel (Run 3)

**What it is**: An agent that monitors a continuous stream and signals when something relevant is found. It does not interpret, assess, or recommend — it detects and reports.

**When you match this pattern**:
- Your agent monitors something (data, events, signals, content)
- The output is informational — it doesn't change the world
- Missing a signal is worse than a false alarm
- The agent runs on a schedule or is event-triggered
- Human judgment is required after detection, not during

**Pre-filled sections**:

| Section | Pre-fill |
|---|---|
| **Identity** | Extractor or Measurer. Stance: constraint-oriented. "I detect and report; I do not interpret or judge." |
| **Worst failure** | False negative (missed signal). Often invisible — the signal was there and the agent didn't see it. |
| **Architecture** | Single Agent, single mode |
| **Progressive autonomy** | Standard 4-level, per-output-type if multiple signal types |
| **Authority boundary** | "Never interpret, never judge, never recommend. Signal what is detected; the human decides what it means." |
| **Human touchpoint** | Specification time (human defines what to detect, what counts, what thresholds) |
| **Null-state output** | REQUIRED. "Nothing found in this cycle" or heartbeat. Silence is never acceptable. |
| **Health monitoring** | False negative rate (critical), false positive rate (important), signal accuracy, consecutive silence detection |
| **Harm assessment** | NOT REQUIRED (informational output only) |
| **SuggestionRisk** | NOT REQUIRED (no generative output) |
| **Mode count** | 1 (single mode) |
| **Reversibility** | N/A (informational output) |

**Sections that still need detailed attention**: Purpose (what to detect), Output Specification (signal schema), Task Decomposition (what to extract/measure), Capability Allocation (what thresholds require human judgment), Event Storming (what happens when signals are missed or false).

---

### Pattern 2: The Multi-Lens Analyst

**Source**: Analyser (Run 2)

**What it is**: An agent that assesses a single input across multiple dimensions, each with different authority boundaries. It produces a structured analysis where different fields have different rules.

**When you match this pattern**:
- Your agent evaluates a single input across multiple criteria or dimensions
- Different dimensions have different authority boundaries (some measure, some assess, some extract)
- The output is a structured analysis, not a binary judgment
- The agent doesn't make final decisions — it prepares a multi-dimensional assessment
- Human judgment interprets the full picture

**Pre-filled sections**:

| Section | Pre-fill |
|---|---|
| **Identity** | Multi-class. Different fields have different class assignments. Stance: mixed (extracting = constraint-oriented, assessing = mixed). |
| **Worst failure** | Fabrication (hallucinating content that isn't in the input) for Extractor fields; overconfidence for Assessor fields |
| **Architecture** | Single Agent with per-field authority boundaries (enforced in both schema and prompt) |
| **Progressive autonomy** | Standard 4-level, but per-output-type (deterministic fields earn trust faster) |
| **Authority boundary** | Per-field. Each field has its own boundary: extractors never judge, measurers never interpret, assessors never finalise. |
| **Human touchpoint** | Specification time (human defines rubrics, scales, what counts as relevant) |
| **Null-state output** | Partial output with flags > no output > silent failure. If 3 of 4 fields can be completed, output those 3 with the 4th flagged as missing. |
| **Health monitoring** | Per-field accuracy, fabrication rate, confidence calibration |
| **Harm assessment** | NOT REQUIRED (informational output) |
| **SuggestionRisk** | NOT REQUIRED (no generative output) |
| **Mode count** | 1 per field, but the agent switches between modes for different fields |
| **Reversibility** | N/A (informational output) |

**Sections that still need detailed attention**: Which fields are which class, the rubrics and scales for each dimension, the per-field authority boundaries in schema and prompt, the partial output strategy.

---

### Pattern 3: The Discovery Explorer

**Source**: Prospector (Run 4)

**What it is**: An agent that generates novel insights, connections, or ideas from a body of knowledge. Its value is in what's new, not just what's correct. It must balance validity (being right) with novelty (being surprising).

**When you match this pattern**:
- Your agent's primary value is novelty, not just accuracy
- The output is generative — it creates new connections, insights, or ideas
- "Technically correct but obvious" is the worst failure
- Human judgment is required for novelty assessment (the agent can't self-assess novelty)
- The agent may exhaust its source material over time

**Pre-filled sections**:

| Section | Pre-fill |
|---|---|
| **Identity** | Generator + Assessor (two-hat pattern). Stance: possibility-oriented for generation, constraint-oriented for evaluation. |
| **Worst failure** | Valid-but-obvious (technically correct, reveals nothing new). Looks like success. |
| **Architecture** | Single Agent with two-hat mode switching (generate → evaluate), attempt budget (default: 3) |
| **Progressive autonomy** | Validity can go autonomous; novelty NEVER goes fully autonomous. Human calibration is always required for novelty assessment. |
| **Authority boundary** | Generator: "never be vague, never fabricate." Assessor: "never finalise, never rate novelty without human calibration." |
| **Human touchpoint** | Specification time + discovery time (human learns alongside the agent, calibrating novelty) |
| **Null-state output** | REQUIRED. `novelty_declining` signal — honest "couldn't find anything novel" rather than forcing weak insight. |
| **Health monitoring** | Novelty rating (human-calibrated), validity rating, coverage map, corpus exhaustion tracking, diversity metrics |
| **Harm assessment** | NOT REQUIRED (informational output — insights don't change the world) |
| **SuggestionRisk** | NOT REQUIRED (insights are suggestions, not actions) |
| **Mode count** | 2 (within-interaction: generate then evaluate) |
| **Reversibility** | Fully reversible (insights are informational) |
| **Diversity enforcement** | REQUIRED. InsightType enumeration, coverage maps, history tracking, source diversity. Without these, the agent defaults to the easiest type of discovery. |
| **Corpus exhaustion** | MUST be planned for. The source material is finite. Include coverage tracking, novelty trend monitoring, and a `corpus_exhausted` signal. |

**Sections that still need detailed attention**: The specific novelty/validity rubric, the source material and coverage strategy, the attempt budget, the diversity enforcement mechanisms.

---

### Pattern 4: The Learning Scaffold

**Source**: Tutor (Run 5)

**What it is**: An agent that helps a human learn or develop a skill, where success is measured by the human needing the agent less over time. The agent's role DECREASES as the human's capability INCREASES.

**When you match this pattern**:
- Your agent's purpose is to help a human become more capable
- Success = human independence, not agent utility
- The agent must actively reduce its own usefulness over time
- There are at least two human roles (learner + educator/coach/manager)
- Assisted performance can mask dependency — the worst failure looks like success

**Pre-filled sections**:

| Section | Pre-fill |
|---|---|
| **Identity** | Assessor + Generator (scaffold/independence modes). Stance: possibility-oriented toward the learner's possibility, constraint-oriented toward the scaffolding plan. |
| **Worst failure** | Dependency (learner succeeds with the agent but fails without it). Looks like success. |
| **Architecture** | Single Agent with two-mode switching ACROSS interactions (scaffold mode + independence mode) |
| **Progressive autonomy** | INVERTED. Learner earns independence, not agent. Scaffolding: Full → Partial → Minimal → Independent. |
| **Authority boundary** | "Never give the answer when the learner can reach it. Never assess without improving. Never become necessary." |
| **Human touchpoint** | Scaffold time (decreases over time) + calibration time (educator defines objectives and reviews progress) |
| **Null-state output** | Not applicable (the agent is always present during sessions, but its ROLE changes) |
| **Health monitoring** | Assisted-vs-unassisted gap (dependency indicator), independence trajectory, scaffolding level trend, misconception resolution rate, learner confidence |
| **Harm assessment** | NOT REQUIRED (informational/coaching output — the agent can frustrate, but not cause external harm) |
| **SuggestionRisk** | NOT REQUIRED (suggestions are learning exercises, not actions that change the world) |
| **Mode count** | 2 (across-interaction: scaffold in one session, independence check in another) |
| **Reversibility** | Fully reversible (learning exercises can be redone) |
| **Dependency indicator** | REQUIRED. Track assisted performance vs unassisted performance. If the gap is growing, the agent is creating dependency, not learning. |
| **Independence checks** | REQUIRED. Structurally separate from learning interactions. The learner should not know they're being tested. |
| **Human roles** | ALWAYS 2+: learner (empowerment toward independence) + educator (empowerment toward better curriculum/data) |
| **Success metric direction** | INVERSE. Less agent utility = more success. Primary metric: unassisted performance, not agent output quantity. |
| **Scaffold reduction** | REQUIRED. The agent must have explicit mechanisms for reducing its own usefulness: scaffolding levels that decrease, transition criteria, regression criteria. |

**Sections that still need detailed attention**: The specific subject matter, the scaffolding strategies, the learning objectives, the misconceptions to track, the transition and regression criteria.

---

### Pattern 5: The Review Partner

**Source**: Code Reviewer (Run 6)

**What it is**: An agent that evaluates a human's work across multiple dimensions and suggests improvements, where the suggestions can cause harm if wrong and accepted. It prepares a structured review for human judgment — it never decides, approves, or rejects.

**When you match this pattern**:
- Your agent evaluates something the human produced
- The agent can suggest changes that, if accepted, have real-world consequences
- Multiple evaluation dimensions have different stakes (some are critical, some are minor)
- The agent must prioritise — critical issues must not be buried in minor ones
- The agent can see problems but can't always safely solve them

**Pre-filled sections**:

| Section | Pre-fill |
|---|---|
| **Identity** | Assessor + Generator + Self-evaluator (three-mode: assess → generate → self-evaluate). Stance: constraint-oriented toward existing system, possibility-oriented toward improvements. |
| **Worst failure** | Agent-caused harm through accepted output (wrong suggestion merged = production damage). Also: missed critical issue (false negative with external harm). |
| **Architecture** | Single Agent with three-mode switching (assess → generate → self-evaluate for safety) |
| **Progressive autonomy** | PER-DIMENSION. Low-stakes dimensions (style) go autonomous quickly. High-stakes dimensions (security, correctness) go slowly or NEVER. |
| **Authority boundary** | "Never approve, never reject, never merge. Recommendations only. Never suggest a fix for a problem you can't safely fix." |
| **Human touchpoint** | Verification time (human reviews agent findings and decides) + calibration time (human adjusts severity thresholds) |
| **Null-state output** | "No significant issues found" — but this must still include the review dimensions checked |
| **Health monitoring** | Per-dimension false negative rate, per-dimension false positive rate, suggestion acceptance rate, suggestion error rate (the critical one), review completeness, developer self-correction rate |
| **Harm assessment** | REQUIRED. Agent output can cause external harm if accepted. |
| **SuggestionRisk** | REQUIRED on every generative output. SAFE → LOW_RISK → MEDIUM_RISK → HIGH_RISK → DO_NOT_SUGGEST. |
| **Mode count** | 3 (assess → generate → self-evaluate for safety) |
| **Reversibility** | VARIES by suggestion type (SAFE = fully reversible, DO_NOT_SUGGEST = effectively irreversible) |
| **Dimension separation** | REQUIRED in output. Critical issues (security, correctness) MUST be presented before minor issues (style). Type collision resolution applies to output structure. |
| **DO_NOT_SUGGEST** | REQUIRED as a valid output. "I can see the problem but I can't safely suggest a fix" is a sign of trustworthiness. |
| **Human roles** | ALWAYS 2+: the person who produced the work (developer/writer/creator) + the person who approves it (reviewer/manager/editor) |
| **Output structure = emotional design** | REQUIRED. Typed, separated, prioritised sections. "15 issues" = judgment. "2 security + 3 correctness + 10 style" = partnership. |
| **Post-merge feedback loop** | REQUIRED if applicable. False negatives are detected by real-world consequences (production bugs, incidents). This is the most expensive feedback loop — progressive autonomy must be conservative for dimensions with external consequences. |

**Sections that still need detailed attention**: The specific evaluation dimensions, the severity thresholds per dimension, the SuggestionRisk classification for each dimension, the per-dimension progressive autonomy timeline, the false negative detection mechanism.

---

## The Pattern Selection Guide

To determine which pattern matches your agent, answer these questions in order:

```
1. Can your agent's output cause external harm if accepted and acted on?
   ├── YES → Start with Pattern 5 (Review Partner)
   │         Then add per-dimension autonomy and harm assessment
   └── NO → Continue

2. Is your agent's primary purpose to help a human become more capable independently?
   ├── YES → Start with Pattern 4 (Learning Scaffold)
   │         Then add subject-specific scaffolding strategies
   └── NO → Continue

3. Is your agent's primary value in novelty (surprising, unexpected insights)?
   ├── YES → Start with Pattern 3 (Discovery Explorer)
   │         Then add source-specific coverage and diversity mechanisms
   └── NO → Continue

4. Does your agent assess a single input across multiple dimensions with different rules?
   ├── YES → Start with Pattern 2 (Multi-Lens Analyst)
   │         Then add dimension-specific rubrics and per-field boundaries
   └── NO → Continue

5. Does your agent monitor a stream and signal when something is found?
   ├── YES → Start with Pattern 1 (Signal Detector)
   │         Then add signal-specific detection criteria
   └── NO → You have a novel pattern. Start from Section 0 with no pre-fills.
```

## What Each Pattern Pre-fills

| Template Section | Pattern 1: Signal | Pattern 2: Analyst | Pattern 3: Discovery | Pattern 4: Scaffold | Pattern 5: Review |
|---|---|---|---|---|---|
| **0 Identity** | Partial | Partial | Partial | Partial | Partial |
| **0 Harm Assessment** | ✗ (N/A) | ✗ (N/A) | ✗ (N/A) | ✗ (N/A) | ✓ (Required) |
| **0 Worst Failure** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **1 Output Types** | Signal + null-state | Per-field analysis | Insight + coverage + exhaustion signal | Learning interaction + understanding model + independence trajectory | Structured review + issues + suggestions + risk assessment |
| **1 Null-state** | ✓ (Required) | Partial output + flags | ✓ (novelty_declining) | N/A | ✓ (no issues found) |
| **1 SuggestionRisk** | ✗ (N/A) | ✗ (N/A) | ✗ (N/A) | ✗ (N/A) | ✓ (Required) |
| **2 Backcasting** | Simple chain | Per-field chains | Generate → verify cycle | Circular dependency | Assess → generate → verify chain |
| **3 Task Decomposition** | Extract/Measure | Per-field classes | Generate + Assessor | Assessor + Generator | Assessor + Generator + Self-evaluator |
| **4 Complementarity** | Spec-time only | Spec-time + verification | Spec-time + discovery | Scaffold + calibration | Verification + calibration |
| **4 Progressive Autonomy** | Standard 4-level | Per-output-type | Validity yes, novelty never | INVERTED | PER-DIMENSION |
| **4 Human Roles** | 1 | 1 | 1 | 2+ | 2+ |
| **5 Failure Events** | Missed signal, false alarm | Fabrication, overconfidence | Valid-but-obvious, corpus exhaustion | Dependency trap, frustration | Agent-caused harm, missed critical, alert fatigue |
| **6 Architecture** | Single Agent | Single Agent per-field | Single Agent 2-mode | Single Agent 2-mode (across) | Single Agent 3-mode |
| **7 Authority Boundary** | Never interpret | Per-field boundaries | Never be vague / never finalise novelty | Never give answers / never become necessary | Never approve / never suggest unsafe fix |
| **7 Hardest Boundary** | When signal is ambiguous | When assessment is borderline | When novelty is subjective | When learner is frustrated | When developer asks for quick fix |
| **8 Human Experience** | Single role | Single role | Single role | 2 roles (learner + educator) | 2+ roles (creator + reviewer + lead) |
| **8 Output Structure** | Typed signal | Per-field structured | Insight + novelty rating | Scaffold level + independence trajectory | Typed/separated/prioritised sections |
| **9 Health Metrics** | False negative/positive | Per-field accuracy | Novelty/validity/coverage | Assisted-vs-unassisted gap | Per-dimension false negative/positive, suggestion error |
| **9 False Negative Detection** | Monitoring system | Human review | Human novelty rating | Assisted-vs-unassisted gap | Production incidents |

**Key**: ✓ = Pre-filled with validated pattern, ✗ = Not applicable, Partial = Some elements pre-filled, context-specific elements still needed.

## What the Patterns DON'T Pre-fill

Every pattern still requires the designer to specify:

1. **Purpose and domain** — What is this agent FOR? What domain does it operate in?
2. **Specific outputs and schemas** — What exactly does it produce? (The pattern gives types, not schemas.)
3. **Specific authority boundaries** — What exactly does this agent never do? (The pattern gives the class boundary, not the domain-specific one.)
4. **Specific failure modes** — What exactly goes wrong in this domain? (The pattern gives the structural failure mode, not the domain-specific one.)
5. **Specific human roles and empowerment targets** — Who exactly does this agent serve? (The pattern gives the number and type, not the specific roles.)
6. **Specific progressive autonomy timeline** — How fast does trust build in this domain? (The pattern gives the model, not the timeline.)
7. **Specific testable hypotheses** — What exactly are we testing? (The pattern gives the metric types, not the specific hypotheses.)

The patterns give you the STRUCTURE — the architecture, the mode count, the progressive autonomy model, the authority boundary class, the failure mode type, the health monitoring categories. The designer fills in the SUBSTANCE — the domain, the schemas, the specific boundaries, the specific timeline, the specific hypotheses.

That's exactly the right division of labour. The patterns encode what we've learned from six validated agent designs. The designer brings what no pattern can provide: the specific purpose, domain, and context of their agent.