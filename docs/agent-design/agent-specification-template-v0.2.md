# Agent Specification Template

## Section 0: Identity & Purpose
**Cognitive mode: IMAGINE**

### Shortcut
If your agent matches a known pattern, the identity questions may be pre-filled. But EVERY agent should answer all four identity questions — they determine everything that follows.

### Questions

**Q1: What IS this agent?**
> What is it at its core? Not what it does, but what it IS. A scaffold, not a teacher. A review partner, not a reviewer. A learning catalyst, not a knowledge transfer engine.

**Q2: What is its stance toward possibility?**
> Is it possibility-oriented (expands what's possible — discovery, learning, creative), constraint-oriented (operates within defined boundaries — assessment, compliance, monitoring), or mixed? If mixed, which dimensions are possibility-oriented and which are constraint-oriented?

| Phase Position | Characteristic Stance | Typical Orientation |
|---|---|---|
| P0 Purpose | Pure possibility | Possibility-oriented |
| P1 Outputs | Formed possibility | Possibility → Constraint |
| P2 Backcasting | Transitional | Mixed |
| P3 Decomposition | Constructive | Mixed |
| P4 Allocation | Constrained | Constraint-oriented |
| P5 Event Storming | Adversarial (but constructive) | Constraint-oriented |
| P6 Architecture | Structural | Constraint-oriented |
| P7 Agent Design | Concrete | Constraint-oriented |
| P8 Human Experience | Reopened possibility | Possibility-oriented (for the human) |
| P9 Validation | Proven | Constraint-oriented |

**Q3: What would VIOLATE its identity?**
> Not behavioural rules (those come later) — existential violations. What would make this agent NOT be what it claims to be? For a tutor: becoming necessary. For a code reviewer: approving a merge. For a sentinel: being silent when danger exists.

**Q4: What would it mean for this agent to be WRONG?**
> Rank the failure modes by severity. Identify which ones look like success (the worst failures often do). For each failure mode, rate: visibility (how easy to detect) and severity (how much harm).

| Failure Mode | Severity (1-5) | Visibility (Hidden/Apparent) | Looks Like Success? |
|---|---|---|---|
| [Failure 1] | | | |
| [Failure 2] | | | |
| [Failure 3] | | | |
| [Failure N] | | | |

### Harm Assessment (Required if Shortcut 1 = YES)

| Question | Answer |
|---|---|
| Can this agent's output cause external harm if accepted and acted on? | |
| What kind of harm? (Financial, physical, legal, reputational, operational) | |
| How reversible are the consequences? (Fully → Effectively irreversible) | |
| What is the worst-case harm scenario? | |
| Who bears the consequence of the agent being wrong? | |

### Principles Table

| Layer | Fidelity (What must be true) | Enrichment (How does this expand human capability?) |
|---|---|---|
| **Purpose** | [What is this agent FOR?] | [Can the human eventually do more WITHOUT the agent than they could before?] |
| **Identity** | [What IS this agent? What would violate its identity?] | [Is the human's capability increasing or their dependency increasing?] |
| **Specification** | [What outputs MUST exist?] | [Were alternative outputs explored?] |
| **Context** | [What information does the agent need?] | [Does the agent adapt to the human's pace, style, and gaps?] |
| **Trust** | [How is trust earned and maintained?] | [Does trust increase or decrease over time? In what dimensions?] |
| **Safety** | [What are the primary safety risks?] | [Does the agent have mechanisms for reducing its own role when the human is ready?] |
| **Ecosystem** | [Who/what does this agent interact with?] | [Can the human use other resources independently?] |
| **Improvement** | [What metrics track improvement?] | [Is the agent getting better at its job? Is the human getting better at theirs?] |
| **Human Enrichment** | [How does this agent expand human capability?] | [Can the human eventually teach others what they've learned?] |

---

## Section 1: Output Specification
**Cognitive mode: SPECIFY**

### Shortcut
If your agent matches a known pattern, many output types are pre-filled:
- **Monitoring/signal agents**: Signal output + null-state output + heartbeat
- **Analysis agents**: Per-field structured analysis + confidence scores
- **Discovery agents**: Insight output + novelty rating + coverage map + exhaustion signal
- **Educational agents**: Learning interaction + understanding model + scaffolding plan + independence trajectory
- **Review/assessment agents**: Structured review + issue list + suggestion list + risk assessment + pattern tracking

### Questions

**Q1: What artefacts MUST exist when this agent's work is done?**
> List every output the agent must produce. Each output should have a unique ID, purpose, type, schema, and dependencies.

| Output ID | Output Name | Purpose | PRISM Type | Depends On | Quality Gate |
|---|---|---|---|---|---|
| O1 | | | | | |
| O2 | | | | | |
| ... | | | | | |

**Q2: For each output, what is its authority boundary?**
> What is this output allowed to do, and what is it NEVER allowed to do? For harm-capable agents: what is the risk level if this output is wrong and accepted?

| Output | Authority Boundary | Risk if Wrong | Reversibility |
|---|---|---|---|
| O1 | | | |
| O2 | | | |
| ... | | | |

**Q3: What external inputs does this agent need that it CANNOT define itself?**
> Pre-conditions that must come from the human or system. The agent cannot operate without these.

| Input ID | Input Name | Source | Required Before |
|---|---|---|---|
| | | | |
| | | | |

**Q4: Is there a null-state output?**
> If this agent monitors, signals, or detects anything, it MUST produce output in the null state. What does "nothing found" look like?

**Q5: Is there a dependency indicator?**
> If this agent helps humans become more capable, is there an assisted-vs-unassisted performance metric? If not applicable, state why.

---

## Section 2: Backcasting
**Cognitive mode: TRACE**

### Shortcut
If your agent produces a single output type with simple dependencies, backcasting is straightforward. For complex outputs, trace each dependency chain.

### Questions

**Q1: Working backward from each output, what inputs/dependencies are required?**
> Start from the final output and trace the chain backward. Every output depends on something — what?

| Output | Depends On | Which Depends On | External Input Required |
|---|---|---|---|
| [Final output] | [Intermediate] | [Earlier intermediate] | [What the human must provide] |
| | | | |
| | | | |

**Q2: Are there circular dependencies?**
> Some outputs depend on inputs that depend on the outputs (e.g., understanding model depends on interactions, but interactions depend on understanding model). Identify these and specify how the cycle is broken.

**Q3: What is the longest dependency chain?**
> The longest chain determines the minimum number of steps before the final output can be produced.

---

## Section 3: Task Decomposition
**Cognitive mode: DECOMPOSE**

### Shortcut
Use the 5-class taxonomy to classify each subtask. The class determines the authority boundary and failure mode.

| Class | Authority Boundary | Characteristic Failure Mode | Never... |
|---|---|---|---|
| **Extractor** | Extracts, never judges | Hallucination (fabricating what isn't there) | Judge, interpret, assess |
| **Measurer** | Measures, never interprets | Noise-as-signal (measuring noise as meaningful) | Interpret meaning, assign significance |
| **Assessor** | Assesses, never finalises | Overconfidence (being certain about uncertain things) | Make final decisions, declare outcomes |
| **Generator** | Generates, never assumes correctness | Fabrication/vagueness (making things up or being uselessly vague) | Be vague, fabricate, assume it's correct |
| **Aggregator** | Aggregates, never adds | Omission (missing something that should be included) | Add new information, interpret, judge |

### Questions

**Q1: Decompose the task into subtasks.**
> Each subtask should have one primary cognitive type. If a subtask requires multiple types, split it.

| ID | Subtask | Cognitive Type | Class | Authority Boundary | Failure Mode |
|---|---|---|---|---|---|
| T1 | | | | | |
| T2 | | | | | |
| ... | | | | | |

**Q2: Are there any subtasks that require both generation and assessment?**
> If yes, consider: (a) two-hat mode switching within a single agent, (b) two-mode switching across interactions, or (c) separate specialist agents. The choice depends on stakes and coupling.

**Q3: Does any subtask require self-evaluation of generated output?**
> If yes, this is a three-mode pattern (assess → generate → self-evaluate). Required for harm-capable agents where generated output can cause external harm if wrong.

---

## Section 4: Capability Allocation
**Cognitive mode: ALLOCATE**

### Shortcut
Use the complementarity matrix format. For each subtask, score Human capability (1-10), Agent capability (1-10), and calculate the gap. Allocation rules:

- **Gap ≥ 6**: Human-only (human is significantly better)
- **Gap 3-5**: Collaborative (both contribute meaningfully)
- **Gap ≤ 2**: Agent-primary or System (agent is as good or better)
- **Gap negative**: Agent has clear advantage; consider Agent-primary with human verification

### Questions

**Q1: For each subtask, what is the complementarity allocation?**

| ID | Subtask | Cognitive Type | Reversibility | H Score | A Score | Gap | Allocation |
|---|---|---|---|---|---|---|---|
| T1 | | | | | | | |
| T2 | | | | | | | |
| ... | | | | | | | |

**Q2: For harm-capable agents, what is the reversibility of each subtask's output?**
> Classify each subtask's output reversibility: Fully reversible → Mostly reversible → Partially reversible → Barely reversible → Effectively irreversible. Higher irreversibility requires more human verification.

| ID | Subtask | Output Reversibility | Verification Required |
|---|---|---|---|
| T1 | | | |
| ... | | | |

**Q3: How many human roles does this agent serve? What are their empowerment targets?**

| Role | Who | What They Need | Empowerment Target |
|---|---|---|---|
| Role 1 | | | Informing → Enabling → Amplifying → Liberating |
| Role 2 | | | |
| Role 3 | | | |

**Q4: Is progressive autonomy standard or inverted?**
- **Standard**: Agent earns more trust over time. Primary metric: trust earned.
- **Inverted**: Human earns more independence over time. Primary metric: human independence. Agent's role decreases by design.

If inverted, specify the scaffolding levels: Full Scaffold → Partial Scaffold → Minimal Scaffold → Independent.

**Q5: For multi-dimensional evaluation, specify progressive autonomy per dimension.**

| Dimension | Stakes | Autonomy Trajectory | Full Autonomy? |
|---|---|---|---|
| [Dimension 1] | [Low/Medium/High/Critical] | [Fast/Standard/Slow/Never] | [Yes/No] |
| [Dimension 2] | | | |
| ... | | | |

---

## Section 5: Event Storming
**Cognitive mode: STRESS-TEST**

### Shortcut
For single-agent, low-stakes use cases, this section can be lightweight. For multi-agent, high-stakes, or harm-capable agents, this section is essential.

### Questions

**Q1: What domain events trigger this agent?**

| Event | Trigger | Produces |
|---|---|---|
| | | |
| | | |

**Q2: What failure events can occur?**
> For each failure, specify detection, recovery, and who catches it.

| Failure Event | Detection | Recovery | Who Catches |
|---|---|---|---|
| | | | |
| | | | |

**Q3: What is the worst failure that looks like success?**
> Identify the failure mode that is hardest to detect because it looks like the agent is working well. For educational agents: dependency. For discovery agents: valid-but-obvious. For code reviewers: wrong suggestion accepted. What is it for this agent?

**Q4: What are the hardest moments for maintaining the authority boundary?**
> When is it most tempting for the agent to violate its own boundaries? For a tutor: when the learner is frustrated and asks for the answer. For a code reviewer: when the developer asks for a quick fix. For this agent: [?]

---

## Section 6: System Architecture
**Cognitive mode: ARCHITECT**

### Shortcut
Use the architecture decision tree:

```
How many cognitive modes and what are the stakes?
│
├── Single mode, low stakes
│   → Single Agent
│   → Pattern: Watchman
│
├── Multi-mode (different classes per field), moderate stakes
│   → Single Agent with per-field boundaries
│   → Pattern: Analyser
│
├── Multi-mode, high stakes, class collision
│   → Workflow with specialist agents
│   → Pattern: Sentinel
│
├── Generate-then-verify cycle, discovery-oriented
│   → Single Agent with two-hat mode switching
│   → Attempt budget (default: 3)
│   → Pattern: Prospector
│
├── Scaffold-independence cycle, educational
│   → Single Agent with two-mode (across-interaction) switching
│   → Scaffolding levels: Full → Partial → Minimal → Independent
│   → Pattern: Tutor
│
└── Assess-generate-self-evaluate, harm-capable
    → Single Agent with three-mode switching
    → SuggestionRisk on every generative output
    → Pattern: Code Reviewer
```

### Questions

**Q1: What is the composition decision?**
> Single Agent, Single Agent with mode-switching, Team, or Workflow? Justify based on stakes, class collision, and coupling.

**Q2: What mode(s) does this agent operate in?**
> Single mode, two-mode (within-interaction), two-mode (across-interaction), or three-mode (assess-generate-self-evaluate)?

**Q3: What is the orchestration configuration?**

| Parameter | Value | Rationale |
|---|---|---|
| Composition | | |
| Invocation | | |
| Model | | |
| Structured Output | | |
| Tools | | |
| Memory | | |
| Session | | |
| Modes | | |

**Q4: FMEA — What are the most critical failure modes?**

| Component | Failure Mode | Effect | Severity | Mitigation |
|---|---|---|---|---|
| | | | | |
| | | | | |
| | | | | |

---

## Section 7: Agent Design
**Cognitive mode: DESIGN**

### Shortcut
Use the 5-class × 3-orientation taxonomy to classify the agent:

| | Possibility-Oriented | Bridge-Oriented | Constraint-Oriented |
|---|---|---|---|
| **Extractor** | Discovers what exists | Translates between forms | Retrieves defined information |
| **Measurer** | Explores measurement dimensions | Calibrates between methods | Measures against defined scales |
| **Assessor** | Surfaces possibilities | Evaluates trade-offs | Judges against defined criteria |
| **Generator** | Explores solution space | Iterates on approaches | Produces within defined constraints |
| **Aggregator** | Discovers connections | Translates between formats | Compiles defined outputs |

### Questions

**Q1: Agent Identity**

| Field | Value |
|---|---|
| Agent ID | |
| Agent Class | [Extractor / Measurer / Assessor / Generator / Aggregator] |
| Agent Orientation | [Possibility / Bridge / Constraint] |
| Mission | |
| Authority Boundary | |
| Identity Violation | [What would violate this agent's identity?] |
| Worst Failure | [What would it mean for this agent to be WRONG? Rank by severity] |
| Stance Toward Possibility | [From Q2 in Section 0] |

**Q2: Hard Constraints**
> List every hard constraint. For harm-capable agents, include SuggestionRisk constraints.

| # | Constraint | Rationale |
|---|---|---|
| 1 | | |
| 2 | | |
| ... | | |

**Q3: What is the hardest boundary moment?**
> When is it most tempting for the agent to violate its authority boundary? This is where the boundary is most likely to fail.

**Q4: Progressive Autonomy Timeline**

If standard:
| Period | Behaviour | Human Verification |
|---|---|---|
| [Phase 1] | | |
| [Phase 2] | | |
| [Phase N] | | |

If inverted:
| Period | Scaffolding Level | What Changes | Transition Criteria |
|---|---|---|---|
| [Phase 1] | Full Scaffold | | |
| [Phase 2] | Partial Scaffold | | |
| [Phase 3] | Minimal Scaffold | | |
| [Phase 4] | Independent | | |

If per-dimension:
| Dimension | Autonomy Trajectory | Full Autonomy? |
|---|---|---|
| | | |
| | | |

**Q5: Epistemic Metadata**
> What confidence, provenance, and uncertainty information does each output carry?

| Output | Confidence Field | Provenance Field | Uncertainty Field |
|---|---|---|---|
| | | | |
| | | | |

**Q6: Fallback Behaviour**
> What does the agent do when it can't complete its primary task?

| Condition | Fallback |
|---|---|
| | |
| | |

**Q7: Cost Budget**
> Per-interaction and per-session token/cost limits. Halt condition.

| Metric | Budget | Halt Condition |
|---|---|---|
| Per interaction | | |
| Per session | | |

**Q8: Specification Aging**
> When and how should this agent's specification be reviewed?

| Component | Review Cadence | Trigger for Early Review |
|---|---|---|
| | | |
| | | |

---

## Section 8: Human Experience
**Cognitive mode: EMPATHIZE**

### Questions

**Q1: For each human role, what is the cognitive load budget?**

| Role | Interaction | Frequency | Cognitive Load | Duration |
|---|---|---|---|---|
| | | | | |
| | | | | |

**Q2: What is the System Empowerment Assessment for each role?**

| Role | Level | Description |
|---|---|---|
| [Role 1] | Constraining → Informing → Enabling → Amplifying → Liberating | |
| [Role 2] | | |
| [Role 3] | | |

**Q3: How does the output structure affect the emotional experience?**
> For agents that produce feedback, assessments, or reviews: how does the structure of the output create the recipient's emotional experience? "15 issues" feels like judgment; "2 security + 3 correctness + 10 style" feels like partnership. Design the output structure for emotional impact.

| Output Type | Undifferentiated Format | Typed/Separated Format | Emotional Difference |
|---|---|---|---|
| | | | |
| | | | |

**Q4: Does this agent involve independence checks?**
> For educational/coaching agents: independence checks must be structurally separate from learning interactions. The learner should not know they're being tested.

For review/assessment agents: the review format must prevent critical issues from being buried in minor issues. Security findings come before style suggestions.

---

## Section 9: Validation & Iteration
**Cognitive mode: VERIFY**

### Questions

**Q1: What are the testable hypotheses?**

| ID | Hypothesis | How to Test | Success Criteria |
|---|---|---|---|
| H1 | | | |
| H2 | | | |
| H3 | | | |
| ... | | | |

**Q2: What are the health monitoring metrics?**

| Metric | Target | Alert Threshold | Action |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

**Q3: What is the false negative detection mechanism?**
> For agents where missed signals cause harm: how are false negatives detected? What is the cost of a false negative? For code reviewers, it's production incidents. For sentinels, it's health monitoring. For tutors, it's the assisted-vs-unassisted gap.

**Q4: What is the progressive autonomy timeline?**
> (Already specified in Section 7. This is the verification: does the timeline make sense given the health monitoring metrics?)

---
