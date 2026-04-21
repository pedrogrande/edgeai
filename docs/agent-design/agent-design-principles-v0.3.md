# Agent Design Principles v0.3

---

## Reading Guide

Each design principle is tagged with a **maturity level** indicating its readiness for production implementation:

| Tag                 | Meaning                                                                                                      |
| :------------------ | :----------------------------------------------------------------------------------------------------------- |
| 🟢 **Operational**  | Implementable today with available tools and frameworks                                                      |
| 🟡 **Emergent**     | Implementable with moderate engineering effort; requires design commitment but no research breakthroughs     |
| 🔴 **Aspirational** | Requires new infrastructure, measurement methodology, or research; defines direction, not current capability |

These tags do not rank importance. An aspirational principle may be more important than an operational one. The tags indicate _when_ you can act on it, not _whether_ you should.

---

## The Core Premise

Before any design decision, three commitments need to be made explicit:

1. 🟢 **Trustworthiness comes from structure, not identity.** An agent is trusted not because of what it is, but because of how it was built, constrained, and verified. Every element of the framework should enforce this structurally, not declaratively.

2. 🟢 **Performance is a system property, not an agent property.** Excellence emerges from the relationship between the agent, its specification, its tools, its verifiers, its ecosystem, and its improvement loops. No single layer is sufficient alone.

3. 🟢 **The framework has two axes of excellence, not one.** The first axis is **output fidelity** — did the agent produce the right thing? The second is **epistemic enrichment** — did the interaction make anyone more capable? An agent system can score perfectly on the first axis and zero on the second. That is a competent but ultimately brittle system — one that produces correct outputs today but accumulates no wisdom, leaves humans more dependent rather than more capable, and fails silently when task types shift outside its validated range. Every layer below addresses both axes.

These two axes are not abstract virtues — they correspond to a structural problem in how LLMs produce information. LLMs encode fundamentally distinct information types — claims, evidence, assumptions, confidence, options, criteria, actions, questions, connections, constraints, perspectives, patterns, gaps, tensions, dependencies, outcomes, and provenance — into a single output type: prose. This **type collision** means that a technically correct output can still fail on enrichment: the human cannot extract, isolate, interrogate, or build on the components that matter most to them. The fidelity axis asks whether the right information was produced. The enrichment axis asks whether the right information was _accessible, decomposable, and transferable_. Both are structural properties, not stylistic preferences.

---

## Layer 1: Purpose

_Why does this agent exist?_

This layer is answered before anything else. Every subsequent design decision should be traceable back to it.

- 🟢 **Human intent** — what human need does this agent serve? A technically correct agent that causes harm, concentrates power, or diminishes human agency has failed regardless of its output quality

- 🟢 **Human development** — what does the human gain in capability, understanding, or perspective from this interaction? This is a distinct question from task completion. The goal is not to give answers but to make humans more capable of finding answers. An agent system that creates dependency where it should create competence has failed its purpose, even if every output was correct. This principle is measured by a concrete test: _can the human now perform the task unassisted at a higher quality than before the interaction?_ If the answer is unknown, the principle is unverified — not necessarily failed, but not yet proven

- 🟢 **Goal, not just task** — what is the agent trying to achieve, not just what is it being asked to do? Without goal clarity, the agent cannot recognise when completing the task would undermine the purpose (commander's intent)

- 🟢 **Success in human terms** — what does a good outcome look like to the person who asked for this work? This is distinct from the acceptance criteria and must be defined first

- 🟡 **Complementarity boundary** — what should this agent do, and what must remain human? Agents handle the consistent, parallelisable, and precisely specifiable; humans handle the ethical, irreversible, and genuinely novel. This boundary is drawn explicitly, not discovered at runtime. Where efficiency and enrichment conflict, this layer is where the tiebreaker lives.

The complementarity boundary is not a judgement call — it is a design decision with a method. The **Reversibility-Novelty-Agency Matrix** determines what belongs to the agent and what must remain human:

|             | **Reversible**                          | **Irreversible**              |
| :---------- | :-------------------------------------- | :---------------------------- |
| **Routine** | Agent executes, agent verifies          | Agent prepares, human decides |
| **Novel**   | Agent explores, human chooses direction | Human decides, agent advises  |

A routine-reversible task (e.g., formatting a document) is agent territory. A novel-irreversible task (e.g., terminating a partnership) requires the human at the decision point. The matrix is not a suggestion — it is the structural mechanism for drawing the boundary. When a task's classification is ambiguous, it defaults to the more human-involved cell. This matrix connects directly to Layer 6 (reversibility classification) and Layer 5 (verification level selection).

---

## Layer 2: Identity

_What is this agent?_

- 🟢 **Role archetype** — is this agent an executor, a reviewer, an orchestrator, a synthesiser, an articulation agent, or an exploration agent? These are not interchangeable. An agent that holds both executor and reviewer roles for the same work produces unverifiable output (see Layer 5 for verification independence levels). The six archetypes and their constraints:

| Archetype              | Primary function                                                        | Must not also be                           |
| :--------------------- | :---------------------------------------------------------------------- | :----------------------------------------- |
| **Executor**           | Produces artefacts to specification                                     | Reviewer of its own output                 |
| **Reviewer**           | Verifies artefacts against specification                                | Executor of the same artefact              |
| **Orchestrator**       | Routes, sequences, and composes agents                                  | Producer of substantive content            |
| **Synthesiser**        | Integrates multiple inputs into coherent output                         | Sole source of the inputs it synthesises   |
| **Articulation Agent** | Makes implicit logic explicit; surfaces what is known but unarticulated | Source of the knowledge it articulates     |
| **Exploration Agent**  | Expands the possibility space before specification is locked            | Final arbiter of which direction to choose |

The two newer archetypes deserve expanded definition:

- **The Articulation Agent** — receives rough, partially-formed upstream output and returns it as something precise, structured, and usable. Its job is not to answer but to make implicit logic explicit. In human-facing interactions, it surfaces what the human already knows but hasn't yet articulated. In agent pipelines, it tightens loosely specified upstream outputs before passing downstream. It is a type resolution agent: its function is to decompose the type-collided prose of upstream outputs into addressable, typed components
- **The Exploration Agent** — deployed _before_ specification is locked, its explicit purpose is to expand the possibility space. It surfaces options not yet considered, names assumptions not yet questioned, and identifies adjacent opportunities the human or downstream agent hasn't seen. Its output is not a conclusion — it is a richer set of options to choose between. Its scope is bounded by the Explore stage of Layer 3; exploration without a Choose gate produces unbounded divergence

* 🟢 **Cognitive orientation** — does this agent approach problems critically, optimistically, creatively, factually, procedurally, or as a synthesiser of other perspectives? A single orientation applied to every problem is a design flaw. Multi-agent systems should deliberately compose complementary orientations. The composition matters: a critical agent reviewing an optimistic agent's output produces different reasoning than two critical agents reviewing each other's. The orchestrator selects orientations for epistemic complementarity, not just functional coverage

* 🟢 **Epistemic metadata contracts** — for agents operating in multi-agent pipelines, what structured, machine-readable metadata does this agent _attach_ to its outputs for downstream consumption? Rather than asking an agent to _infer_ what an upstream agent believes (which produces an unverified simulation of another agent's epistemic state), each agent _declares_ its epistemic state in a structured contract:

```
Epistemic Metadata Contract:
  confidence_level: 0.7
  assumptions: [list of explicit assumptions made]
  alternatives_set_aside: [directions not pursued, with reasons]
  what_would_change_conclusion: [conditions under which this output should not be trusted]
  evidence_basis: [what this output is grounded in]
  reasoning_provenance: [traceable path to this conclusion]
```

This contract is verifiable (you can check whether the metadata is consistent with the output), machine-readable (it can be passed in session state without natural language interpretation), and composable (downstream agents can programmatically calibrate their trust). It replaces the aspirational concept of "theory-of-mind" with a structural mechanism that achieves the same goal — enabling agents to reason about each other's epistemic states — without depending on the model's ability to infer what another model believes.

- 🟢 **Capability boundary** — what tools does this agent structurally hold? Tools are not descriptions of capability; they are capability. What this agent cannot do should be structurally impossible, not merely discouraged

- 🟢 **Model selection** — which underlying model is appropriate for this agent's role? Heavy reasoning models for complex judgment; lighter models for routing, classification, and structure. Temperature and sampling parameters are design decisions, not defaults

- 🟢 **Scope** — what is explicitly out of scope? The boundary between in-scope and out-of-scope must be as precise as the task definition itself. Scope overreach is almost always caused by an underspecified boundary, not a malicious agent

---

## Layer 3: Specification

_What does done look like?_

This is the highest-leverage layer. The quality of a specification determines the quality of the output more than any property of the agent. Specification has three sequential stages — the first two were absent from earlier versions of this framework.

### Stage 1 — Explore 🟡

Before acceptance criteria are written, what are all the possible ways this problem could be framed and solved? The exploration phase is not discovery (which validates the problem) — it is generative (which multiplies the options). Its output is a curated option space, not a specification. This stage is served by the Exploration Agent archetype (Layer 2). Skipping it means committing to a direction before the best directions have been identified.

The Explore stage has a defined endpoint: it produces an _option space document_ — a structured enumeration of the viable directions considered, the assumptions each direction rests on, and the trade-offs between them. The option space document is the input to the Choose stage. Exploration without this output is unbounded wandering; the option space document is the proof that exploration happened and a commitment to proceed from its results.

### Stage 2 — Choose 🟢

Commit to a direction, explicitly setting aside the alternatives considered. The alternatives are recorded, not discarded; they are the evidence that the chosen direction was selected, not defaulted into. The Choose stage has a defined output: a _direction commitment_ — the selected direction, the reasons for selection, the alternatives set aside, and the conditions under which the commitment should be revisited.

### Stage 3 — Specify 🟢

Write the acceptance criteria for the chosen direction:

- 🟢 **Definition precedes execution** — criteria must be complete, reviewed, and locked before work begins. Criteria written after the fact describe what was built, not what was needed

- 🟢 **Proof template** — what evidence specifically constitutes completion? Not "the task is done" but "these criteria are met, as evidenced by these artefacts." The proof template is the contract

- 🟢 **Verifiability test** — if you cannot tell whether an output passes or fails the acceptance criteria without asking the agent, the criteria are ambiguous. Ambiguity in a specification is a bug

- 🟢 **Problem before solution** — what is the validated problem being solved? Discovery is a distinct phase. No specification should exist without a validated understanding of the problem it is responding to

- 🟢 **Prototype before scale** — for high-stakes or novel work, what is the minimum viable version that tests the core assumption? Execution failure is expensive; validation failure is cheap

- 🟡 **Type resolution** — for any non-trivial output, what information types must be explicitly separated in the deliverable? LLMs produce prose by default; prose is a type-collided format that fuses claims, evidence, assumptions, confidence levels, action items, questions, and constraints into a single stream. The specification must declare which types the output decomposes into, because undifferentiated prose fails the enrichment axis regardless of its fidelity. At minimum, the following types should be addressable as distinct, manipulable components:

| Type            | Question it answers       | Must be separable when...                     |
| :-------------- | :------------------------ | :-------------------------------------------- |
| **Claims**      | What is being asserted?   | The output contains factual statements        |
| **Evidence**    | What supports the claim?  | The output rests on data or citations         |
| **Assumptions** | What is taken as given?   | The output depends on conditions not verified |
| **Confidence**  | How certain is the agent? | The output informs a decision                 |
| **Options**     | What alternatives exist?  | The output recommends a direction             |
| **Actions**     | What should be done?      | The output prescribes behaviour               |
| **Questions**   | What remains unknown?     | The output has knowledge gaps                 |

An output that meets every acceptance criterion but delivers all of these types as undifferentiated prose has succeeded on fidelity and failed on enrichment. Type resolution makes the enrichment axis structurally enforceable.

---

## Layer 4: Context

_What does the agent know, and when?_

- 🟢 **Minimum sufficient context** — what is the minimum information this agent needs to perform its task? More context degrades performance. Every additional element competes for the same finite attention

- 🟢 **Informational context** — what is provided upfront in a context card, and what does the agent retrieve on demand from a knowledge base? These are not the same thing. Context is local and task-specific; knowledge is global and queryable

- 🟡 **Epistemic context** — what did the upstream agent believe, assume, and remain uncertain about? This is not task information; it is reasoning provenance. An agent receiving only an output has less to work with than one receiving an output plus a structured epistemic metadata contract (Layer 2): _what I found, how confident I am, what I assumed, what alternatives I set aside, and what would change my conclusion_. Epistemic context is what enables downstream agents to calibrate their trust in upstream outputs rather than inheriting them blindly. The contract format from Layer 2 is the transport mechanism; Layer 4 specifies when and where it is consumed

- 🟡 **Information boundaries** — what information is this agent structurally prevented from accessing? The boundary between accessible and inaccessible information must be enforced at the infrastructure level, not the prompt level. A prompt-level instruction ("do not read document X") is a suggestion, not a constraint; an agent with access to a knowledge base can query any document it can reach. A true information boundary requires partitioning: separate collections per agent role in vector databases, separate knowledge bases with role-specific permissions, or network-level access controls. The design question is not "what should this agent ignore?" but "what should this agent be _unable to reach_?" Information boundaries are the complement of required context: they define the shape of what the agent cannot know, which is as important to specify as what it must know

- 🟢 **Lifecycle state** — what phase is the work in? An agent needs to know whether it is in exploration, discovery, ideation, specification, execution, or verification — because the right actions differ at each stage. Lifecycle awareness prevents out-of-order operations

- 🟢 **Progressive disclosure** — what context is loaded at task start vs. loaded on demand via skills? Skill files contain substantive guidance; base agent files contain only identity, tools, and pointers. This separation enables caching and keeps always-on context small

- 🟡 **Typed context** — when upstream agents pass epistemic metadata contracts and type-resolved outputs (Layer 3), the receiving agent's context is _typed_, not raw prose. Typed context means the agent can programmatically distinguish a claim from an assumption from a confidence level without natural language interpretation. This is the downstream counterpart of type resolution: typed outputs enable typed inputs. A pipeline that passes typed context between agents is structurally different from one that passes prose — even if the same information content travels through both

---

## Layer 5: Trust

_How do outputs become trustworthy?_

This layer operates through two complementary mechanisms. The first is the minimum viable trust mechanism. The second is the excellence mechanism.

- 🟡 **Independent verification** — who verifies this agent's work, and how independent is the verifier from the producer? Independence is not binary; it is a spectrum. The **verification independence scale** provides three levels matched to the stakes of the task:

| Level                                   | Mechanism                                                                                    | Reliability | Cost   | Appropriate when...                              |
| :-------------------------------------- | :------------------------------------------------------------------------------------------- | :---------- | :----- | :----------------------------------------------- |
| **Level 1: Structural self-review**     | Same model, different prompt framing, different session                                      | Low–medium  | Low    | Task is routine-reversible (see Layer 1 matrix)  |
| **Level 2: Instance independence**      | Same model class, different agent instance with distinct session, context, and specification | Medium      | Medium | Task is routine-irreversible or novel-reversible |
| **Level 3: Architectural independence** | Different model, different toolset, different specification                                  | High        | High   | Task is novel-irreversible                       |

The verification level is selected by the task's position in the Reversibility-Novelty-Agency Matrix (Layer 1), not by preference. A calendar agent verifying meeting times needs Level 1. A medical diagnosis agent needs Level 3. The matrix provides the structural mapping; this principle provides the verification response.

- 🟢 **Verification gates** — independent pass/fail checks against pre-defined acceptance criteria. This is the floor: the work either meets the specification or it doesn't. Without this, nothing downstream can be trusted

- 🟡 **Belief revision protocols** — where agents don't just pass/fail each other's outputs but explicitly propose revisions with justification, creating an auditable record of reasoning evolution rather than a binary verification event. This is the difference between a marking scheme and peer review. Both produce quality control. Only one produces better reasoning as a system property.

The protocol operates in three steps:

1. The reviewer identifies a revision opportunity and submits a _revision proposal_: the specific claim being challenged, the proposed alternative, the evidence supporting the alternative, and the confidence in the revision
2. The original agent responds: accepts, rejects (with counter-justification), or defers (marks for human review). Either outcome is recorded in the audit trail
3. The pipeline log reflects the reasoning evolution: not just "Output X passed verification" but "Output X was revised on point 3 based on evidence Y; Agent A accepted the revision; the reasoning trace now reflects both the original and the revised position"

A belief revision protocol allows the pipeline to get smarter from every task, not just produce correct outputs on each one.

- 🟢 **Proof as product** — the deliverable is not the work; it is the verified evidence that the work meets the specification. A proof document is a first-class artefact: structured, attributed, and permanent

- 🟡 **Assured audit trail** — every tool call, document read, state transition, and uncertainty raise creates an attributed, timestamped record. Transparency is not a feature; it is the precondition for accountability. The degree of assurance required is matched to the task's classification:

| Task classification  | Audit trail assurance                       | Implementation                                                     |
| :------------------- | :------------------------------------------ | :----------------------------------------------------------------- |
| Routine-reversible   | Append-only log                             | Database with write-once tables                                    |
| Routine-irreversible | Append-only log with role-based read access | Tamper-evident logging; admin overrides require dual authorization |
| Novel-irreversible   | Cryptographically verified immutability     | Hash-chained entries or append-only distributed storage            |

"Immutable" is not an all-or-nothing property. It is an assurance level matched to the consequences of the action being recorded. The framework requires the assurance level to be specified; it does not require every action to be blockchain-grade immutable.

- 🟢 **Chain of custody** — given any output, it must be possible to trace backwards through every action that contributed to it. Provenance is not an afterthought; it is designed in from the start

- 🟢 **Resilience through structure** — the system must produce trustworthy outputs even when individual agents fail, hallucinate, or act in bad faith. No single actor — agent or human — should be a single point of failure. Distributed verification, quorum thresholds, and graceful degradation are structural requirements

---

## Layer 6: Safety

_What happens when things go wrong?_

This layer is derived from the fields with zero tolerance for failure — aviation, nuclear engineering, medicine, and law — and is now extended to include a systemic risk that operates at the organisational level.

- 🟢 **Fail-safe defaults** — when an agent encounters an unknown condition, loss of state, or unresolvable uncertainty, what does it default to? The answer is always: stop and signal. Never: proceed and guess

- 🟢 **Uncertainty as a structural primitive** — raising uncertainty is not a failure; it is correct behaviour. Any agent must be able to surface uncertainty immediately, without social cost or penalty. Uncertainty halts execution and creates a priority signal to human attention

- 🟢 **Reversibility classification** — before any action is taken, what class is it? Read-only, reversible, or irreversible? Irreversible actions require human presence structurally, not as a bypassable gate. The distinction between "send an email" and "query a database" is not currently native to any tool framework — it must be designed in explicitly. This classification connects to Layer 1 (the complementarity boundary matrix) and Layer 5 (verification level selection)

- 🟢 **Prompt injection defence** — every piece of content an agent reads is a potential attack surface. Malicious instructions can be embedded in documents, emails, and tool outputs. The agent's trust model for inputs must be explicit

- 🟢 **Capability and alignment are independent** — a highly capable agent can be simultaneously excellent at its task and misaligned with the intent behind it. Alignment cannot be assumed from capability. It must be tested, monitored, and structurally constrained

- 🟡 **Recovery protocol** — when an agent stops and signals, what happens next? The fail-safe default is "stop and signal," but the _recovery path_ determines whether the system returns to productive operation or remains stuck. Every failure mode must have a defined recovery protocol:

| Element                         | Design question                                                                                                                                                                               |
| :------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Notification target**         | Who (or what) receives the signal? Is it a human, an orchestrator agent, or both?                                                                                                             |
| **Maximum wait time**           | How long can the system remain halted before a secondary action is triggered?                                                                                                                 |
| **Default fallback**            | If no response arrives within the wait window, what does the agent do? Options: remain halted, attempt degraded-mode continuation with reduced scope, or escalate to a higher-authority agent |
| **Degraded-mode specification** | If degraded-mode continuation is permitted, what is the reduced scope the agent is allowed to operate under? This must be pre-specified, not improvised                                       |

A failure without a recovery path is a failure mode. A failure with a recovery path is a controlled interruption. The distinction matters in production systems: an agent that stops and waits indefinitely for a human who is unavailable is functionally equivalent to a crashed system.

- 🟡 **Cognitive diversity as a safety concern** — when multiple humans interact with the same AI systems, they converge on similar frames, similar solutions, and similar outputs — even as each individual feels more creative and capable. A diverse organisation becomes a homogeneous one through repeated AI interaction, without anyone noticing. This is not a user experience problem; it is a systemic risk. Recent research confirms this mechanism:
  - **Doshi & Hauser (2024)**: GenAI improved individual story creativity but caused convergence across writers' outputs — the homogenization effect
  - **Qiu et al. (2025), "The Lock-in Hypothesis"**: formalized a feedback loop where LLMs reinforce user beliefs with generated content, reabsorb reinforced beliefs, and feed them back — producing "sudden but sustained drops in diversity after the release of new GPT iterations"
  - **Wan & Kalman (2026)**: diverse AI persona assignment partially mitigates convergence, confirming that the _design choices_ behind persona assignment determine whether homogenization occurs

The structural response is deliberate cognitive diversity management: rotating agent orientations across different users, teams, and tasks; tracking output diversity as a system health indicator alongside output quality; and treating convergence in framing as a warning signal, not a quality indicator. The same mechanism that makes individuals more productive can make organisations more fragile, because collective resilience depends on diversity of thought and AI collaboration erodes it silently

---

## Layer 7: Ecosystem

_What surrounds this agent?_

- 🟢 **Tool selection and permission scoping** — which tools does this agent need? Tools are not features to be added; each one extends the attack surface and the range of possible unintended actions. The minimum sufficient toolset is the correct toolset

- 🟢 **Human-in-the-loop placement** — where in the workflow do humans appear, and what are they actually deciding? Humans placed too early create bottlenecks; placed too late, they can only accept or reject outcomes. The right placement is at irreversible decision thresholds (per the Layer 1 matrix), with enough context to make a genuine judgment

- 🟡 **Multi-agent topology** — if this agent operates within a multi-agent system, what is its position in the pipeline? What does it trust from upstream agents? What guarantee does it provide to downstream ones? Agent-to-agent trust is currently ad hoc — it must be designed explicitly. The pipeline is not a sequence of artefact transfers; it is a sequence of epistemic exchanges. What passes between agents includes not just outputs but epistemic metadata contracts (Layer 2), type-resolved components (Layer 3), and confidence calibrations

- 🟡 **Coalition formation** — beyond routing and gating, the orchestrator is responsible for matching agents by epistemic complementarity for the demands of the current task, not just by predefined role. Agents composed for complementary cognitive orientations produce qualitatively different outcomes than agents composed for functional role coverage alone

- 🟡 **Pipeline health monitoring** — measuring only accuracy and latency at the final output misses what is happening inside the pipeline. Two monitoring principles are first-class pipeline health indicators alongside output quality:
  - **Diversity monitoring**: the system must be able to detect when inter-agent message diversity drops below a threshold, indicating cognitive convergence. The specific measurement method (embedding similarity, lexical diversity, framing analysis) is implementation-dependent, but the monitoring _obligation_ is structural. A pipeline that is producing correct but increasingly homogeneous outputs is degrading, even if accuracy is stable
  - **Efficiency monitoring**: the system must be able to detect when an excessive proportion of reasoning steps are non-productive — redundant checks, circular references, or rework caused by specification ambiguity. The specific measurement method is implementation-dependent, but the monitoring _obligation_ is structural

  These are monitoring _principles_, not fixed metrics. The measurement infrastructure for pipeline health is still emerging; the design obligation is to build the monitoring capability, not to commit to a specific scoring algorithm today.

- 🟢 **Observability** — can every step this agent takes be inspected, replayed, and diagnosed? Observability is not a developer convenience; it is the aviation black box. It exists not for real-time use but for post-incident accountability and learning

- 🟢 **Infrastructure assumptions** — what happens when a tool is unavailable, an API rate-limits, or a model call times out? The agent's behaviour under infrastructure failure must be defined, not discovered in production

- 🟡 **Cost budget** — what is the maximum acceptable cost (in tokens, latency, compute, and money) for this agent's typical invocation? Every architectural choice in this framework — multi-agent pipelines, epistemic metadata contracts, belief revision protocols, type resolution — has a direct economic cost. The most epistemically enriching architecture is not always the most practical one. The cost budget is a binding design parameter, not a post-deployment surprise. Two cost questions must be answered:
  1. **Per-invocation cost ceiling**: what is the maximum acceptable cost for a single task completion? This constrains how many agents, how many verification passes, and how many revision cycles are affordable
  2. **Enrichment cost premium**: what is the maximum acceptable cost multiplier for enrichment-oriented features over a fidelity-only baseline? An agent system that costs 10x more to produce enrichment may or may not be worth the premium — but the premium must be _known_, not discovered

  The cost budget creates a direct tension with other principles. A system that maximises enrichment with no cost constraint is an academic exercise. A system that minimises cost with no enrichment requirement is a calculator. The cost budget is where the fidelity-enrichment tradeoff becomes _operational_, not just theoretical.

---

## Layer 8: Improvement

_How does this agent get better over time?_

- 🟢 **Pattern extraction** — when this agent succeeds, what pattern contributed? When it fails, what pattern failed? Both outcomes should feed a structured, queryable pattern library — not a post-mortem document, but a living knowledge base that agents consult before beginning work

- 🟢 **Knowledge compounds** — every task the agent completes makes the system smarter, if the learning is captured. Early patterns have low confidence because they have limited evidence. As they are applied and validated, confidence grows. Patterns that consistently underperform are retired

- 🟢 **Performance measurement** — what metrics define this agent's performance? Not just output quality, but token efficiency, step count, rework rate, uncertainty rate, and lifecycle cost. Anomalies in any metric are diagnostic signals, not acceptable noise

- 🟡 **Pipeline intelligence** — does the system get smarter through agent interactions, not just produce correct outputs? The specific measurable proxies:
  - Does the downstream agent require fewer clarification loops when the upstream agent passes epistemic metadata alongside output?
  - Does output diversity (per the diversity monitoring principle in Layer 7) across the pipeline remain stable or increase over time, or converge toward homogeneity?
  - Do agents form more effective coalitions as their epistemic models of each other mature (as reflected in the accuracy of their metadata contracts)?
  - Does the articulation quality of inter-agent handoffs improve as the system matures?

  These are the pipeline equivalents of measuring whether students are developing capability, not just achieving grades.

- 🟢 **Retrospective discipline** — performance does not improve automatically. It requires structured retrospectives that extract patterns and update the knowledge base. An agent system treated as a deployment rather than a continuous improvement cycle will plateau and degrade

- 🟢 **Specification quality as a metric** — how often do tasks built on this agent's outputs require rework? High rework rates are not output failures; they are specification failures upstream. The framework should trace rework back to its root cause: ambiguous acceptance criteria, missing exploration, skipped validation, or absent type resolution

- 🟡 **Specification aging** — when was this agent's specification last reviewed against current model capabilities, current human competence, and current task requirements? Specifications are not permanent documents; they degrade as the environment changes. A specification written for a GPT-4-class model may over-constrain a GPT-5-class model or under-constrain a smaller model. An enrichment program designed for a novice may be patronizing for an experienced user after six months. Specifications should carry a **review cadence** — a defined interval at which they are re-examined — and a **trigger set** — conditions that demand immediate review (model upgrade, sustained rework rate increase, or a significant change in the human's demonstrated capability)

---

## Layer 9: Human Enrichment

_Is every human more capable after engaging with this system than before?_

This is the layer that separates a _competent_ agent system from an _excellent_ one. It does not sit inside any other layer because it defines a second class of outputs the system must produce: not just correct artefacts, but more capable humans.

Every layer below it now has two modes of assessment: did it produce the right output (fidelity), and did it leave the human in a better position than before (enrichment)?

- 🟢 **Perspective multiplication** — before the human commits to a direction, multiple cognitive orientations are deliberately surfaced. Options the human hadn't considered are a designed output, not an accidental one

- 🟢 **Cognitive mirroring** — agents surface their framing, reasoning, and assumptions so humans can interrogate them, not just accept them. The agent's reasoning is visible; the human builds on it rather than inheriting it

- 🟢 **Exploration scaffolding** — the agent offers frameworks and questions before conclusions, making reasoning transparent and transferable. Conclusions without scaffolding create dependency; conclusions with scaffolding create capability

- 🟢 **Progressive human empowerment** — the agent's scaffolding reduces as the human's competence grows. Permanent scaffolding is a design failure: it produces permanent dependency. The measure of a mature human-agent relationship is that the human needs less guidance over time, not more.

This principle is measurable through the **Scaffolding Dependency Index**: over a defined period, is the human's _unassisted_ performance on similar tasks improving? If the human can only perform well _with_ the agent's scaffolding, the system has created dependency. If the human's unassisted performance is rising — even if assisted performance rises faster — the system has created capability. The index tracks the gap between assisted and unassisted performance over time; a widening gap indicates dependency, a narrowing gap indicates empowerment.

- 🟢 **Tacit knowledge activation** — agents create productive friction that externalises what the human knows but hasn't yet articulated. The Articulation Agent archetype (Layer 2) is the designed version of this: its job is to surface the human's own knowledge, not to supply knowledge the human lacks

- 🟡 **Diversity stewardship** — the system actively manages for diversity of human thought at the organisational level, not just quality of individual outputs. This connects directly to the cognitive diversity safety concern in Layer 6; the enrichment perspective adds a positive design obligation alongside the safety one. Stewardship includes: deliberately varying agent orientations assigned to different team members, monitoring whether the organisation's collective output diversity is converging, and rotating agent personas to prevent lock-in to a single cognitive style

- 🟡 **Human enrichment fidelity** — did the enrichment actually occur, or does the human merely _feel_ more capable? Feeling empowered without being empowered is the most dangerous form of dependency, because the human won't seek help for a capability gap they don't believe exists. The fidelity question for this layer is: **can the human now perform the task unassisted at a measurably higher quality than before the interaction?** This requires delayed, unassisted performance testing — not the human's self-report of capability, but demonstrated performance on a similar task without agent support. If this question cannot be answered, the enrichment is unverified.

---

## Cross-Cutting Concern: Temporal Dynamics

_How does this framework account for change over time?_

This is not a tenth layer — it is a dimension that applies across all nine. Agent capabilities change (model upgrades, new tools), human capabilities change (through enrichment, through skill decay, through role changes), and task requirements change (as the work evolves through its lifecycle and as the environment shifts). The framework's principles are static, but the systems they describe are not.

**Three temporal mechanisms operate across every layer:**

1. 🟡 **Review cadences** — every specification, every complementarity boundary, every verification level, every cost budget, and every enrichment program should carry an explicit review interval. Not "review when needed" (which means "never") but "review every N interactions / N days / N model versions." The review cadence is part of the specification, not an external maintenance schedule.

2. 🟡 **Trigger sets** — conditions that demand immediate, out-of-schedule review regardless of the cadence. Common triggers:

- Model upgrade: the underlying model changes (affecting Layer 2 identity, Layer 5 verification, Layer 7 cost budget)
- Sustained rework increase: the agent's output requires significantly more revision than baseline (affecting Layer 3 specification, Layer 8 improvement)
- Human capability shift: the human's demonstrated competence has changed noticeably — either improved (requiring scaffolding withdrawal per Layer 9) or degraded (requiring scaffolding restoration)
- Diversity convergence: the diversity monitoring principle (Layer 7) indicates systemic convergence
- Cost threshold breach: the per-invocation cost exceeds the budget

3. 🟢 **Capability drift tracking** — the system tracks whether its own outputs are drifting in quality, diversity, or cost over time. Drift is not always degradation — a model upgrade may improve output quality but reduce output diversity (the homogenization effect, Layer 6). The system monitors both directions of drift.

Temporal dynamics make explicit what was previously implicit: that a perfectly designed agent at time T₀ may be a poorly designed agent at time T₁ if the environment has changed and the specification has not.

---

## The Framework as a Set of Questions

Every element collapses into two questions per layer that must be answered before an agent is deployed. Unanswered questions are guaranteed future failure modes.

| Layer                | Fidelity question                                                                                                                   | Enrichment question                                                                                                                                                 |
| :------------------- | :---------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Purpose**          | Why does this agent exist, and what human need does it serve?                                                                       | What does the human gain — in capability, understanding, or possibility space — from this interaction? Can they now perform unassisted at higher quality?           |
| **Identity**         | What is this agent's role, orientation, and capability boundary?                                                                    | What epistemic metadata does this agent contract to attach to its outputs, and does its orientation contribute cognitive diversity to the pipeline?                 |
| **Specification**    | Are criteria verifiable, pre-existing, and type-resolved?                                                                           | Was the option space explored and a direction chosen before criteria were written? Do the acceptance criteria specify which information types must be decomposable? |
| **Context**          | What is the minimum information this agent needs, and when? What information boundaries are structurally enforced?                  | What epistemic context does the agent receive from upstream? Is that context typed or raw prose?                                                                    |
| **Trust**            | Who verifies this work, at what independence level, and how is that level selected?                                                 | Do belief revision protocols allow the pipeline to improve its reasoning, not just verify its outputs? Is the audit trail assurance level matched to task stakes?   |
| **Safety**           | What are the fail-safe defaults, and where are the human gates? What recovery protocol operates when the agent halts?               | Is cognitive diversity at the organisational level being actively preserved, not just individual output quality?                                                    |
| **Ecosystem**        | Is the architecture matched to task structure? What is the per-invocation cost ceiling?                                             | Are pipelines designed as epistemic exchanges? Is coalition formation by epistemic complementarity? Is diversity monitored?                                         |
| **Improvement**      | Are output quality, rework rates, and specification aging tracked?                                                                  | Is pipeline intelligence — downstream capability gain — being measured alongside output accuracy?                                                                   |
| **Human Enrichment** | Can the human now perform the task unassisted at higher quality than before? (Unverified enrichment is unconfirmed, not confirmed.) | Is every human more capable after every interaction than before it? Is the Scaffolding Dependency Index narrowing or widening?                                      |

An agent design that answers both questions for all nine layers is structurally sound. An agent design that answers either question for fewer than nine layers has one guaranteed failure mode per unanswered question — and it will surface exactly where the unanswered question lives.

The deepest commitment this framework makes is this: **the distinction between a system that completes tasks and a system that generates excellence is whether every interaction leaves someone — human or agent — more capable of the next one.** Everything else is in service of that.

---

## Change Log: v0.2 → v0.3

| Change                                                                                       | Location      | Type         |
| :------------------------------------------------------------------------------------------- | :------------ | :----------- | ------------------------------------------------------------------------------- |
| Added maturity tags (🟢/🟡/🔴) to every principle                                            | All layers    | Structural   |
| Added type collision connection to Core Premise                                              | Core Premise  | Strengthened |
| Formalized Complementarity Boundary as Reversibility-Novelty-Agency Matrix                   | Layer 1       | Strengthened |
| Added "human development is measurable" principle with unassisted performance test           | Layer 1       | Strengthened |
| Expanded role archetype constraints into table format                                        | Layer 2       | Strengthened |
| Replaced Theory-of-Mind with Epistemic Metadata Contracts                                    | Layer 2       | Replaced     |
| Added contract format specification                                                          | Layer 2       | New          |
| Added Articulation Agent as type resolution agent                                            | Layer 2       | Strengthened |
| Added exploration scope boundary (Explore → Choose gate)                                     | Layer 2       | Strengthened |
| Added Type Resolution to Specification Stage 3                                               | Layer 3       | New          |
| Added option space document as Explore stage output                                          | Layer 3       | Strengthened |
| Added direction commitment as Choose stage output                                            | Layer 3       | Strengthened |
| Added type resolution table with seven core types                                            | Layer 3       | New          |
| Replaced "forbidden reads" with "information boundaries" (infrastructure-enforced)           | Layer 4       | Replaced     |
| Added Typed Context principle                                                                | Layer 4       | New          |
| Replaced rigid executor/verifier separation with three-level verification independence scale | Layer 5       | Replaced     |
| Connected verification level selection to Layer 1 matrix                                     | Layer 5       | Strengthened |
| Expanded belief revision protocol into three-step mechanism                                  | Layer 5       | Strengthened |
| Replaced "immutable audit trail" with "assured audit trail" (three assurance levels)         | Layer 5       | Replaced     |
| Added Recovery Protocol (notification, wait time, fallback, degraded mode)                   | Layer 6       | New          |
| Added research citations for cognitive diversity concern                                     | Layer 6       | Strengthened |
| Replaced IDS/UPR with monitoring principles (diversity + efficiency)                         | Layer 7       | Replaced     |
| Added Cost Budget (per-invocation ceiling + enrichment premium)                              | Layer 7       | New          |
| Added Specification Aging (review cadence + trigger set)                                     | Layer 8       | New          |
| Added Scaffolding Dependency Index                                                           | Layer 9       | New          |
| Replaced "not applicable" with Human Enrichment fidelity question                            | Layer 9       | Replaced     |
| Added Human Enrichment Fidelity principle with delayed unassisted testing                    | Layer 9       | New          |
| Added Cross-Cutting Concern: Temporal Dynamics                                               | New section   | New          |
| Updated summary table to reflect all changes                                                 | Summary table | Updated      | The v0.3 draft is complete. Here's a quick orientation on what changed and why: |

**The five most structurally significant changes:**

1. **Type Resolution (Layer 3)** — This is the integration of your own TYPE COLLISION insight into the framework. The seven-type decomposition table (claims, evidence, assumptions, confidence, options, actions, questions) makes enrichment _architecturally enforceable_ rather than aspirational. An output that doesn't decompose into these types can be correct but can't be enriched.

2. **Epistemic Metadata Contracts (Layer 2)** — Replaces Theory-of-Mind with something actually implementable. The contract format (confidence, assumptions, alternatives_set_aside, what_would_change_conclusion) is machine-readable, verifiable, and composable. It's the transport mechanism that makes epistemic context (Layer 4) and belief revision (Layer 5) operational.

3. **Reversibility-Novelty-Agency Matrix (Layer 1)** — The complementarity boundary is now a _method_, not a value judgement. It also creates structural linkages across the framework: it drives verification level selection (Layer 5), human-in-the-loop placement (Layer 7), and audit trail assurance (Layer 5). Three layers now reference one mechanism instead of each independently deciding where humans belong.

4. **Cost Budget (Layer 7)** — The enrichment-fidelity tradeoff is now operational, not theoretical. Every enrichment feature has a cost; the cost budget makes the tradeoff explicit. This prevents the framework from producing architecturally beautiful systems that are economically impractical.

5. **Temporal Dynamics (Cross-Cutting)** — The framework now admits that specifications age, models upgrade, and humans change. Review cadences, trigger sets, and capability drift tracking turn a static design into a living system.

**The one thing I'd flag for your attention:** the maturity tag distribution is heavy on 🟢 and 🟡 with very few 🔴. That's deliberate — most of the aspirational concepts from v0.2 (Theory-of-Mind, forbidden reads, immutable audit trails) were replaced with emergent-grade alternatives that achieve the same intent through different means. The only truly aspirational principle that remains unimplemented is the cognitive diversity monitoring infrastructure. This means v0.3 is significantly more implementable than v0.2 while preserving the same design ambition.
