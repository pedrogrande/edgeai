Absolutely — these principles add **transformative** value. My original template captured *what an agent is*; your principles capture *what makes it trustworthy, enriching, and alive over time*. The gaps they expose in my template are significant:

| My Original Template | What Your Principles Reveal Is Missing |
|---|---|
| Single "purpose" field | No distinction between task completion and human development; no complementarity boundary |
| No archetype concept | Agent could accidentally hold executor + reviewer roles simultaneously |
| Flat output format | No type resolution — prose is the default, type collision is invisible |
| No epistemic metadata | No mechanism for agents to declare what they believe, assumed, or set aside |
| Verification = "escalation path" | No independence scale, no belief revision, no proof-as-product |
| Safety = content filter + PII | No reversibility classification, no recovery protocol, no cognitive diversity concern |
| No enrichment axis | No scaffolding, no progressive empowerment, no dependency tracking |
| No temporal dimension | No review cadence, no trigger sets, no specification aging |

Below is the **fully redesigned template**, structured around your 9 layers plus the cross-cutting temporal concern. Each question maps to a specific principle and is tagged with its maturity level so you know what's implementable today vs. what requires engineering investment.

---

# 🧩 Agent Design Questionnaire v2.0

> **Aligned with Agent Design Principles v0.3**  
> Fill in each section. When you return it, I will produce a complete Agno Agent Spec that addresses both axes: **output fidelity** and **epistemic enrichment**.  
> Maturity tags: 🟢 Operational · 🟡 Emergent · 🔴 Aspirational

---

## Layer 1: Purpose

> _Why does this agent exist?_

### Fidelity Question: Why does this agent exist, and what human need does it serve?

| # | Question | Maturity | Your Answer |
|---|----------|:---------:|-------------|
| 1.1 | **Human intent** — What human need does this agent serve? What harm, power concentration, or agency reduction would constitute failure even if outputs are correct? | 🟢 | |
| 1.2 | **Goal, not just task** — What is the agent trying to *achieve*, not just what is it being asked to *do*? (Commander's intent) | 🟢 | |
| 1.3 | **Success in human terms** — What does a good outcome look like to the person who asked for this work? (Distinct from acceptance criteria — define this first.) | 🟢 | |
| 1.4 | **Agent name** — Short, memorable identifier (e.g. `invoice_parser`) | 🟢 | |
| 1.5 | **One-line purpose** — Single sentence capturing the agent's reason for being | 🟢 | |

### Enrichment Question: What does the human gain — in capability, understanding, or possibility space — from this interaction?

| # | Question | Maturity | Your Answer |
|---|----------|:---------:|-------------|
| 1.6 | **Human development** — What does the human gain in capability, understanding, or perspective? Can they perform the task unassisted at higher quality after the interaction? | 🟢 | |
| 1.7 | **Complementarity boundary** — What must remain human? Use the Reversibility-Novelty-Agency Matrix below to classify the agent's primary task domain: | 🟡 | |

**Reversibility-Novelty-Agency Matrix** (classify your agent's primary task):

| | **Reversible** | **Irreversible** |
|:---|:---|:---|
| **Routine** | ☐ Agent executes, agent verifies | ☐ Agent prepares, human decides |
| **Novel** | ☐ Agent explores, human chooses direction | ☐ Human decides, agent advises |

_Where efficiency and enrichment conflict, this is the tiebreaker._

---

## Layer 2: Identity

> _What is this agent?_

### Fidelity Question: What is this agent's role, orientation, and capability boundary?

| # | Question | Maturity | Your Answer |
|---|----------|:---------:|-------------|
| 2.1 | **Role archetype** — Select one. Each archetype has a constraint on what it must NOT also be: | 🟢 | |

| Archetype | Function | Must not also be |
|:---|:---|:---|
| ☐ **Executor** | Produces artefacts to specification | Reviewer of its own output |
| ☐ **Reviewer** | Verifies artefacts against specification | Executor of the same artefact |
| ☐ **Orchestrator** | Routes, sequences, composes agents | Producer of substantive content |
| ☐ **Synthesiser** | Integrates multiple inputs into coherent output | Sole source of the inputs it synthesises |
| ☐ **Articulation Agent** | Makes implicit logic explicit; type resolution | Source of the knowledge it articulates |
| ☐ **Exploration Agent** | Expands possibility space before specification is locked | Final arbiter of which direction to choose |

| # | Question | Maturity | Your Answer |
|---|----------|:---------:|-------------|
| 2.2 | **Cognitive orientation** — How does this agent approach problems? Choose one primary: `critical` / `optimistic` / `creative` / `factual` / `procedural` / `synthesising`. In multi-agent systems, explain how orientations are composed for epistemic complementarity. | 🟢 | |
| 2.3 | **Capability boundary** — What tools does this agent structurally hold? What it cannot do should be *structurally impossible*, not merely discouraged. | 🟢 | |
| 2.4 | **Model selection** — Which model? (e.g. `gpt-4o`, `claude-3-5-sonnet`, `gpt-4o-mini`). Heavy reasoning for complex judgment; lighter models for routing/classification. | 🟢 | |
| 2.5 | **Model parameters** — Temperature (0.0–1.0), reasoning effort (`low`/`medium`/`high`), max tokens. These are design decisions, not defaults. | 🟢 | |
| 2.6 | **Scope — what is out** — What is explicitly out of scope? The boundary must be as precise as the task definition. | 🟢 | |

### Enrichment Question: What epistemic metadata does this agent contract to attach to its outputs?

| # | Question | Maturity | Your Answer |
|---|----------|:---------:|-------------|
| 2.7 | **Epistemic metadata contract** — For multi-agent pipelines, what structured metadata does this agent attach to outputs? (If standalone, write "standalone — no downstream consumers".) | 🟢 | |

```yaml
epistemic_metadata_contract:
  confidence_level:        # 0.0–1.0
  assumptions:             # [list of explicit assumptions]
  alternatives_set_aside:  # [directions not pursued, with reasons]
  what_would_change_conclusion:  # [conditions under which output should not be trusted]
  evidence_basis:          # [what this output is grounded in]
  reasoning_provenance:    # [traceable path to this conclusion]
```

| # | Question | Maturity | Your Answer |
|---|----------|:---------:|-------------|
| 2.8 | **Cognitive diversity contribution** — Does this agent's orientation contribute diversity to the pipeline, or does it duplicate an existing one? | 🟡 | |

---

## Layer 3: Specification

> _What does done look like?_

### Fidelity Question: Are criteria verifiable, pre-existing, and type-resolved?

#### Stage 1 — Explore 🟡

| # | Question | Maturity | Your Answer |
|---|----------|:---------:|-------------|
| 3.1 | **Option space** — What are all the ways this problem could be framed and solved? (If using an Exploration Agent, reference its output here. If not, enumerate 3+ viable directions.) | 🟡 | |
| 3.2 | **Option space document** — For each direction: the assumptions it rests on, and the trade-offs vs. other directions. This is the proof that exploration happened. | 🟡 | |

#### Stage 2 — Choose 🟢

| # | Question | Maturity | Your Answer |
|---|----------|:---------:|-------------|
| 3.3 | **Direction commitment** — Selected direction, reasons for selection, alternatives set aside (recorded, not discarded), and conditions under which the commitment should be revisited. | 🟢 | |

#### Stage 3 — Specify 🟢

| # | Question | Maturity | Your Answer |
|---|----------|:---------:|-------------|
| 3.4 | **Acceptance criteria** — Complete, verifiable criteria that must be locked before work begins. If you can't tell whether output passes/fails without asking the agent, the criteria are ambiguous — and ambiguity is a bug. | 🟢 | |
| 3.5 | **Proof template** — What evidence specifically constitutes completion? Not "the task is done" but "these artefacts exist, meeting these criteria." | 🟢 | |
| 3.6 | **Validated problem** — What is the validated problem being solved? (Discovery is a distinct phase.) | 🟢 | |
| 3.7 | **Prototype before scale** — What is the minimum viable version that tests the core assumption? | 🟢 | |

### Enrichment Question: Was the option space explored before criteria were written? Do criteria specify which information types must be decomposable?

| # | Question | Maturity | Your Answer |
|---|----------|:---------:|-------------|
| 3.8 | **Type resolution** — Which of the following information types must be explicitly separated in the output? Check all that apply, and specify the format for each (e.g. structured field, separate section, metadata tag): | 🟡 | |

| Type | Question it answers | Must be separable when... | Include? | Format |
|:-----|:---|:---|:---:|:---|
| **Claims** | What is being asserted? | Output contains factual statements | ☐ | |
| **Evidence** | What supports the claim? | Output rests on data or citations | ☐ | |
| **Assumptions** | What is taken as given? | Output depends on unverified conditions | ☐ | |
| **Confidence** | How certain is the agent? | Output informs a decision | ☐ | |
| **Options** | What alternatives exist? | Output recommends a direction | ☐ | |
| **Actions** | What should be done? | Output prescribes behaviour | ☐ | |
| **Questions** | What remains unknown? | Output has knowledge gaps | ☐ | |

---

## Layer 4: Context

> _What does the agent know, and when?_

### Fidelity Question: What is the minimum information this agent needs, and what information boundaries are structurally enforced?

| # | Question | Maturity | Your Answer |
|---|----------|:---------:|-------------|
| 4.1 | **Minimum sufficient context** — What is the minimum information this agent needs? More context degrades performance. Every additional element competes for finite attention. | 🟢 | |
| 4.2 | **Informational context** — What is provided upfront (context card) vs. retrieved on demand (knowledge base)? Context is local/task-specific; knowledge is global/queryable. | 🟢 | |
| 4.3 | **Knowledge bases** — List vector databases, file stores, or URLs (name + description). | 🟢 | |
| 4.4 | **Information boundaries** 🟡 — What information is this agent *structurally prevented* from accessing? (Not "should ignore" — must be *unable to reach*. Specify: separate collections, role-specific permissions, or network-level controls.) | 🟡 | |
| 4.5 | **Lifecycle state** — What phase is the work in? (exploration / discovery / ideation / specification / execution / verification). Right actions differ at each stage. | 🟢 | |
| 4.6 | **Progressive disclosure** — What context is loaded at task start vs. loaded on demand via skills? Base files = identity, tools, pointers. Skill files = substantive guidance. | 🟡 | |
| 4.7 | **Agent memory** — `short-term` (session) / `long-term` (persistent) / `both` / `none`. | 🟢 | |

### Enrichment Question: What epistemic context does the agent receive from upstream? Is that context typed or raw prose?

| # | Question | Maturity | Your Answer |
|---|----------|:---------:|-------------|
| 4.8 | **Epistemic context** — What did the upstream agent believe, assume, and remain uncertain about? (If standalone, write "N/A — no upstream".) | 🟡 | |
| 4.9 | **Typed context** — Does the receiving agent get typed, structured inputs (claims separate from assumptions separate from confidence) or raw prose? Typed context enables programmatic distinction without natural language interpretation. | 🟡 | |

---

## Layer 5: Trust

> _How do outputs become trustworthy?_

### Fidelity Question: Who verifies this work, at what independence level, and how is that level selected?

| # | Question | Maturity | Your Answer |
|---|----------|:---------:|-------------|
| 5.1 | **Verification independence level** — Select based on your Layer 1 matrix classification: | 🟡 | |

| Level | Mechanism | Reliability | Cost | When to use |
|:---|:---|:---|:---|:---|
| ☐ **Level 1: Structural self-review** | Same model, different prompt/session | Low–Med | Low | Routine-reversible |
| ☐ **Level 2: Instance independence** | Same model class, different agent instance | Medium | Medium | Routine-irreversible or novel-reversible |
| ☐ **Level 3: Architectural independence** | Different model, different tools, different spec | High | High | Novel-irreversible |

| # | Question | Maturity | Your Answer |
|---|----------|:---------:|-------------|
| 5.2 | **Verification gates** — What are the independent pass/fail checks against acceptance criteria? Without these, nothing downstream can be trusted. | 🟢 | |
| 5.3 | **Proof as product** — The deliverable is not the work; it is the verified evidence that the work meets the specification. Describe the proof document structure. | 🟡 | |
| 5.4 | **Assured audit trail** — What assurance level is required? Select based on task classification: | 🟡 | |

| Task classification | Assurance | Implementation |
|:---|:---|:---|
| ☐ Routine-reversible | Append-only log | Database with write-once tables |
| ☐ Routine-irreversible | Append-only log + role-based read | Tamper-evident logging; admin override = dual auth |
| ☐ Novel-irreversible | Cryptographic immutability | Hash-chained entries or append-only distributed storage |

| # | Question | Maturity | Your Answer |
|---|----------|:---------:|-------------|
| 5.5 | **Chain of custody** — Given any output, can you trace backwards through every action that contributed? How? | 🟢 | |
| 5.6 | **Resilience through structure** — Is any single actor (agent or human) a single point of failure? If so, what failsafe eliminates it? | 🟢 | |

### Enrichment Question: Do belief revision protocols allow the pipeline to improve its reasoning, not just verify its outputs?

| # | Question | Maturity | Your Answer |
|---|----------|:---------:|-------------|
| 5.7 | **Belief revision protocol** — Will agents propose revisions with justification, creating an auditable record of reasoning evolution? If yes, the three-step protocol applies: (1) Reviewer submits revision proposal, (2) Original agent accepts/rejects/defers, (3) Pipeline log reflects reasoning evolution. | 🟡 | |

---

## Layer 6: Safety

> _What happens when things go wrong?_

### Fidelity Question: What are the fail-safe defaults, and where are the human gates?

| # | Question | Maturity | Your Answer |
|---|----------|:---------:|-------------|
| 6.1 | **Fail-safe defaults** — When the agent encounters an unknown condition, loss of state, or unresolvable uncertainty, what does it default to? (Must be: **stop and signal**. Never: proceed and guess.) | 🟢 | |
| 6.2 | **Uncertainty as a structural primitive** — How does the agent surface uncertainty? (Must halt execution and create a priority signal without penalty.) | 🟢 | |
| 6.3 | **Reversibility classification** — Before any action, what class is it? | 🟢 | |

| Action class | Definition | Human gate required? |
|:---|:---|:---|
| ☐ **Read-only** | No state change | No |
| ☐ **Reversible** | State change can be undone | No (but agent verifies) |
| ☐ **Irreversible** | State change cannot be undone | **Yes — structurally, not bypassably** |

List this agent's actions and their classifications:

| Action | Classification | Human gate? |
|:---|:---|:---|
| | | |

| # | Question | Maturity | Your Answer |
|---|----------|:---------:|-------------|
| 6.4 | **Prompt injection defence** — Every piece of content the agent reads is a potential attack surface. What is the explicit trust model for inputs? | 🟢 | |
| 6.5 | **Capability vs. alignment** — How will you test and monitor that the agent remains aligned with intent, not just capable at its task? | 🟢 | |
| 6.6 | **Recovery protocol** — When the agent stops and signals, what happens next? | 🟡 | |

```yaml
recovery_protocol:
  notification_target:       # Who/what receives the signal? (human, orchestrator, both)
  maximum_wait_time: