# Agent Design Principles Template

> **Purpose:** A complementary template that captures principled design decisions _before_ filling in the Agno Agent Design Template. Answers from this template _pre-populate_ specific questions in the Agno template, ensuring every agent is built on sound trust, safety, and enrichment foundations — not just feature completeness.

---

## How This Template Works

This template is the **first step**. It captures decisions about _why_ the agent exists, _what must stay human_, _how outputs become trustworthy_, and _whether the human is actually enriched_. These answers then **pre-populate** the Agno template so that feature and tool choices follow from principle, not the other way around.

### The Pipeline

```
1. Fill in THIS Principles Template  →  2. Answers auto-fill the Agno Template  →  3. Design Agent generates code
```

### How to Use

1. **Fill in this template first** — short answers are fine; "I don't know" is a valid answer.
2. Each section shows **which Agno template questions it pre-populates** (marked with `→ Agno #.#`).
3. After completing both templates, the Design Agent has everything it needs: principled decisions AND implementation specifics.
4. Each question is tagged with a **maturity level** from the principles document:
   - 🟢 **Operational** — implementable today
   - 🟡 **Emergent** — implementable with moderate effort
   - 🔴 **Aspirational** — defines direction, not current capability

> 💡 **If you've already filled in the Agno template**, you can still use this principles template. Where this template's answers conflict with what you wrote in the Agno template, the principles template wins — it captures deeper design intent.

---

## Section 1: Purpose

_Why does this agent exist?_

| Question | Your Answer |
|---|---|
| **1.1** What human need does this agent serve? 🟢 *Not what it does — why it exists. What would be lost if this agent didn't exist? Who benefits and how?* | |
| **1.2** What should the human be able to do _unassisted_ after using this agent? 🟢 *This is the enrichment test. If the human can only perform well _with_ the agent, the system has created dependency. Describe what capability improvement looks like.* | |
| **1.3** What is the goal — not just the task? 🟢 *Example: Task = "summarize documents." Goal = "help researchers stay current without reading everything." The goal is the commander's intent — it's what guides the agent when the task specification is ambiguous.* | |
| **1.4** What does a good outcome look like to the person who asked for this work? 🟢 *This is distinct from acceptance criteria. It's the human's success metric, in their own terms — before we translate it into technical specifications.* | |
| **1.5** What should this agent _never_ do? What decisions or actions must remain human? 🟢 *Draw the complementarity boundary. Use the matrix below to classify your agent's primary tasks.* | |

**Reversibility-Novelty Matrix** 🟢 — Classify this agent's primary tasks:

| | **Reversible** | **Irreversible** |
|---|---|---|
| **Routine** | Agent executes, agent verifies | Agent prepares, human decides |
| **Novel** | Agent explores, human chooses direction | Human decides, agent advises |

*Which cell does your agent primarily operate in? Your answer: ______*

> **Feeds Agno template:**
> - **1.1** → Informs purpose description (1.1) — adds _why_ beyond _what_
> - **1.3** → Cognitive mode (1.3) — archetype is informed by matrix position
> - **1.5** → Human-in-the-loop (4.2) — complementarity boundary determines which actions need approval
> - **1.5** → Architecture (2.1) — irreversible tasks need more verification, possibly more agents

---

## Section 2: Identity

_What is this agent?_

| Question | Your Answer |
|---|---|
| **2.1** What role archetype is this agent? 🟢 *Pick one: **Executor** — Produces artefacts to specification · **Reviewer** — Verifies artefacts against specification · **Orchestrator** — Routes, sequences, and composes agents · **Synthesiser** — Integrates multiple inputs into coherent output · **Articulation Agent** — Makes implicit logic explicit; surfaces what is known but unarticulated · **Exploration Agent** — Expands the possibility space before specification is locked* | |
| **2.2** What cognitive orientation does this agent bring? 🟢 *Pick one or describe: Critical (finds flaws) · Optimistic (sees opportunities) · Creative (generates alternatives) · Factual (sticks to evidence) · Procedural (follows process) · Synthesiser (integrates perspectives)* | |
| **2.3** What must this agent be structurally _unable_ to do? 🟢 *Not "discouraged from doing" — structurally prevented. Example: a reviewer must not be able to produce the artefact it reviews. A financial agent must not be able to execute irreversible transactions.* | |
| **2.4** If this agent is part of a pipeline, what does it promise to downstream agents? 🟡 *What confidence level, assumptions, and alternatives-set-aside does it attach to its outputs? (See epistemic metadata contract below. "Not applicable" is valid for standalone agents.)* | |

**Epistemic Metadata Contract** 🟡 — If this agent sends outputs to other agents, what structured metadata does it attach?

| Metadata Field | Description | Your Answer |
|---|---|---|
| `confidence_level` | How confident is this agent in its output? (0–1 scale) | |
| `assumptions` | What assumptions does this output rest on? | |
| `alternatives_set_aside` | What directions were considered but not pursued, and why? | |
| `what_would_change_conclusion` | Under what conditions should this output not be trusted? | |
| `evidence_basis` | What is this output grounded in? | |

> **Feeds Agno template:**
> - **2.1** → Cognitive mode (1.3) — archetype refines the cognitive classification
> - **2.2** → Persona/instructions (7.2) — cognitive orientation shapes the system prompt
> - **2.3** → Tool selection (4.1) — structural prevention means not including tools that enable the forbidden action
> - **2.3** → Guardrails (5.3) — structural impossibility is enforced through guardrails
> - **2.4** → Memory/learning (3.2) — epistemic metadata can be stored and passed between sessions
> - **2.4** → Output format (5.2) — structured metadata needs structured output (Pydantic/JSON)

---

## Section 3: Specification

_What does done look like?_

| Question | Your Answer |
|---|---|
| **3.1** Before writing acceptance criteria — what other directions were considered? 🟡 *List 2–3 alternative approaches and why you chose this one. If you haven't explored alternatives yet, describe what exploration would look like. "Defaulted into this direction" is a warning sign.* | |
| **3.2** What constitutes proof of completion? 🟢 *Not "the task is done" — what _evidence_ proves the criteria are met? Example: "The agent produced a summary" is not proof. "The summary covers all 5 required topics and each topic is supported by at least 2 cited sources" is proof.* | |
| **3.3** Can someone else verify whether the output passes or fails — without asking the agent? 🟢 *If verification requires subjective judgment that only the agent or requestor can make, the criteria are ambiguous. "Yes" or describe the ambiguity.* | |
| **3.4** For high-stakes or novel work: what is the minimum viable version that tests the core assumption? 🟢 *Prototype before scale. Execution failure is expensive; validation failure is cheap. What is the smallest version that would prove the concept works? "Not applicable" is valid for routine tasks.* | |
| **3.5** Which information types must be separable in the output? 🟡 *Check all that apply. Undifferentiated prose fails the enrichment axis — even if it's correct. See type table below.* | |

**Type Resolution** 🟡 — Which types must be explicitly separated in the output?

| Type | Question It Answers | Include? (✓/✗) | Why |
|---|---|---|---|
| Claims | What is being asserted? | | |
| Evidence | What supports the claim? | | |
| Assumptions | What is taken as given? | | |
| Confidence | How certain is the agent? | | |
| Options | What alternatives exist? | | |
| Actions | What should be done? | | |
| Questions | What remains unknown? | | |

> **Feeds Agno template:**
> - **3.5** → Output format (5.2) — type resolution almost always requires structured output (JSON/Pydantic), not free-form text
> - **3.2** → Guardrails (5.3) — proof templates can become output validation post-hooks
> - **3.3** → Reasoning (5.1) — if criteria are ambiguous, the agent needs deeper reasoning capabilities
> - **3.4** → Architecture (2.1) — prototyping may mean starting with a simpler single-agent before building a Team/Workflow
> - **3.5** → Persona/instructions (7.2) — type resolution requirements go into the system prompt

---

## Section 4: Context

_What does the agent know, and when?_

| Question | Your Answer |
|---|---|
| **4.1** What is the minimum information this agent needs to perform its task? 🟢 *More context degrades performance. List only what's essential. Everything else should be retrieved on demand.* | |
| **4.2** What information must this agent be _unable_ to reach? 🟡 *Not "should ignore" — structurally prevented from accessing. Example: a performance review agent should not be able to access salary data. This is the complement of required context.* | |
| **4.3** What lifecycle phase will this agent typically operate in? 🟢 *Pick one: Exploration (expanding options) · Discovery (validating the problem) · Ideation (generating ideas) · Specification (defining criteria) · Execution (producing artefacts) · Verification (checking outputs). The right actions differ at each stage.* | |
| **4.4** If this agent receives output from an upstream agent, should it receive the upstream agent's reasoning and confidence — or just the output? 🟡 *Raw output alone means the agent trusts blindly. Receiving reasoning provenance (assumptions, confidence, alternatives set aside) enables calibrated trust. "Just the output" is valid but is a deliberate choice, not a default.* | |

> **Feeds Agno template:**
> - **4.1** → Knowledge sources (3.1) — minimum sufficient context drives knowledge base design
> - **4.2** → Knowledge sources (3.1) — information boundaries may require separate knowledge bases or role-based access
> - **4.3** → Persona/instructions (7.2) — lifecycle phase shapes system prompt behavior
> - **4.4** → Memory/learning (3.2) — epistemic context between agents requires memory infrastructure
> - **4.4** → Output format (5.2) — passing epistemic metadata requires structured output

---

## Section 5: Trust

_How do outputs become trustworthy?_

| Question | Your Answer |
|---|---|
| **5.1** What is the task's position in the Reversibility-Novelty Matrix? 🟢 *(Revisiting from Section 1 for verification implications.)* Use the classification to select the verification level: | |
| Routine + Reversible → **Level 1: Structural self-review** (same model, different prompt/session) | |
| Routine + Irreversible OR Novel + Reversible → **Level 2: Instance independence** (different agent instance, different session/context) | |
| Novel + Irreversible → **Level 3: Architectural independence** (different model, different toolset, different specification) | |
| **5.2** What are the pass/fail verification gates? 🟢 *Specific, checkable criteria. Not "looks good" but "meets these defined conditions." List 2–5 gates if applicable.* | |
| **5.3** What level of audit trail is required? 🟡 *Match to task classification:* | |
| Routine-reversible → Append-only log | |
| Routine-irreversible → Append-only log with role-based read access | |
| Novel-irreversible → Cryptographically verified immutability | |
| **5.4** Should verification include belief revision (not just pass/fail)? 🟡 *In a belief revision protocol, reviewers propose specific revisions with evidence, and the original agent accepts, rejects, or defers. This produces an auditable reasoning evolution — not just a binary pass/fail. Only worth the cost for high-stakes or novel tasks. Pick one: Yes · No · Only for novel-irreversible tasks* | |

> **Feeds Agno template:**
> - **5.1** → Architecture (2.1) — Level 3 verification requires a separate reviewer Agent in a Team
> - **5.1** → Human-in-the-loop (4.2) — Level 2 and 3 tasks need human verification
> - **5.2** → Guardrails (5.3) — verification gates can become post-hooks
> - **5.3** → Observability (6.5) — audit trail level determines observability requirements
> - **5.4** → Architecture (2.1) — belief revision requires a Team or Workflow with reviewer agents

---

## Section 6: Safety

_What happens when things go wrong?_

| Question | Your Answer |
|---|---|
| **6.1** When the agent encounters an unknown condition or unresolvable uncertainty, what should it do? 🟢 *The correct default is: stop and signal for human attention. Never proceed and guess. "Stop and signal" is the safe default. Confirm or describe a different behavior.* | |
| **6.2** Classify the agent's primary actions by reversibility: 🟢 | |
| **Read-only** (e.g., search, summarize, analyze) | |
| **Reversible** (e.g., draft an email, create a list, generate a report) | |
| **Irreversible** (e.g., send an email, execute a trade, delete data) | |
| **6.3** If the agent stops and signals, what happens next? 🟡 *Define the recovery protocol: who gets notified? How long can the system wait? What is the fallback if no one responds? What is the reduced scope for degraded-mode operation (if permitted)?* | |
| **Notification target:** | |
| **Maximum wait time:** | |
| **Default fallback:** | |
| **Degraded-mode scope (if applicable):** | |
| **6.4** Is there a risk that repeated use of this agent could make all users think the same way? 🟡 *Agents that provide similar framing, similar answers, and similar suggestions to multiple users can cause cognitive convergence — the organization becomes homogeneous without anyone noticing. Pick one: Low risk (diverse user base, diverse tasks) · Medium risk (similar tasks, different users) · High risk (similar tasks, similar users) · I don't know* | |

> **Feeds Agno template:**
> - **6.1** → Guardrails (5.3) — fail-safe behavior becomes a system prompt instruction and/or a guardrail
> - **6.2** → Human-in-the-loop (4.2) — irreversible actions require human approval
> - **6.3** → Architecture (2.1) — recovery protocols may require an Orchestrator agent
> - **6.3** → Observability (6.5) — notification and fallback need observability infrastructure
> - **6.4** → Persona/instructions (7.2) — high-risk agents need cognitive orientation variation in their prompts

---

## Section 7: Ecosystem

_What surrounds this agent?_

| Question | Your Answer |
|---|---|
| **7.1** If this agent is part of a multi-agent system, what is its position in the pipeline? 🟡 *What does it receive from upstream? What does it pass downstream? What does it trust from upstream? "Standalone" is a valid answer.* | |
| **7.2** What is the minimum sufficient toolset? 🟢 *Every tool extends the attack surface and the range of unintended actions. List only the tools this agent needs — not every tool it could use. If you listed tools in the Agno template (4.1), justify each one against this principle.* | |
| **7.3** What happens when a tool is unavailable, an API rate-limits, or a model call times out? 🟢 *Describe the behavior under infrastructure failure. "Try again" is not a complete answer — how many retries? What's the fallback after retries are exhausted?* | |
| **7.4** What is the maximum acceptable cost per invocation? 🟡 *Two-part answer:* | |
| **Per-invocation cost ceiling:** (in tokens, latency, or money) | |
| **Enrichment cost premium:** (maximum acceptable cost multiplier for enrichment features over a fidelity-only baseline) | |
| **7.5** Where in the workflow should humans appear, and what are they deciding? 🟢 *Not "should humans be involved?" (they should) — but where specifically, and what judgment are they making? Humans placed too early create bottlenecks; placed too late they can only rubber-stamp.* | |

> **Feeds Agno template:**
> - **7.1** → Architecture (2.1) and sub-roles (2.2) — pipeline position defines the agent's role in the system
> - **7.2** → Tool selection (4.1) — minimum sufficient toolset refines the tool list
> - **7.3** → Guardrails (5.3) — infrastructure failure behavior becomes error handling
> - **7.4** → Cost constraints (8.1) — per-invocation ceiling and enrichment premium refine the budget
> - **7.5** → Human-in-the-loop (4.2) — specific placement, not just "yes/no"

---

## Section 8: Improvement

_How does this agent get better over time?_

| Question | Your Answer |
|---|---|
| **8.1** When this agent succeeds, what pattern contributed? When it fails, what pattern failed? 🟢 *Describe what you'd want to capture. "We'll figure it out later" means the learning won't happen.* | |
| **8.2** What metrics define this agent's performance? 🟢 *Not just output quality. Consider: token efficiency, step count, rework rate, uncertainty rate, and lifecycle cost. List 2–5 metrics.* | |
| **8.3** How often should this agent's specification be reviewed? 🟡 *Not "when needed" (that means never). Pick an interval: After every N interactions · Every N days · Every N model versions · Other (specify)* | |
| **8.4** What conditions should trigger an immediate review, regardless of the schedule? 🟡 *Common triggers: model upgrade, sustained increase in rework, human capability shift, cost threshold breach. List applicable triggers.* | |

> **Feeds Agno template:**
> - **8.1** → Memory/learning (3.2) — pattern capture requires memory infrastructure
> - **8.2** → Observability (6.5) — performance metrics need monitoring infrastructure
> - **8.3–8.4** → These are operational requirements not currently in the Agno template; they inform the deployment plan

---

## Section 9: Human Enrichment

_Is every human more capable after engaging with this system than before?_

| Question | Your Answer |
|---|---|
| **9.1** Will this agent surface multiple perspectives before the human commits to a direction? 🟢 *Pick one: Yes — deliberately offers alternatives and frames · No — provides single best answer · Depends on the question (describe when)* | |
| **9.2** Will the agent show its reasoning, assumptions, and framing — not just its conclusions? 🟢 *This enables the human to interrogate and build on the reasoning rather than inherit it. Pick one: Yes — reasoning is always visible · Partially — visible on request · No — only conclusions are shown* | |
| **9.3** Will the agent offer frameworks and questions before conclusions? 🟢 *Conclusions without scaffolding create dependency. Conclusions with scaffolding create capability. Pick one: Yes — scaffolding before conclusions · Sometimes — depends on the question · No — just conclusions* | |
| **9.4** Should the agent's support reduce over time as the human gains competence? 🟢 *Permanent scaffolding is a design failure. Pick one: Yes — progressive empowerment · No — consistent support level · I don't know how to measure this* | |
| **9.5** Can the human perform this task unassisted at higher quality after using the agent? 🟡 *This is the enrichment fidelity test. If the answer is "I don't know," the enrichment is unverified — not failed, but not proven. Pick one: Yes (describe how you'd measure it) · Not yet (describe what's missing) · I don't know* | |
| **9.6** If multiple humans or teams use this agent, should the agent deliberately vary its cognitive orientation across users? 🟡 *This prevents organizational convergence — the silent homogenization that occurs when diverse people repeatedly interact with the same cognitive style. Pick one: Yes — rotate orientations across users/teams · No — consistent orientation for all · Not applicable — single user · I don't know* | |

> **Feeds Agno template:**
> - **9.1** → Persona/instructions (7.2) — perspective multiplication shapes the system prompt
> - **9.2** → Reasoning (5.1) — cognitive mirroring requires reasoning capabilities
> - **9.3** → Persona/instructions (7.2) — scaffolding behavior goes into the system prompt
> - **9.4** → Memory/learning (3.2) — progressive empowerment requires tracking human capability over time
> - **9.5** → Memory/learning (3.2) — measuring enrichment fidelity requires longitudinal data
> - **9.6** → Architecture (2.1) — orientation rotation across users may require multiple agents or dynamic prompts

---

## Section 10: Temporal Dynamics

_How does this system account for change over time?_

| Question | Your Answer |
|---|---|
| **10.1** How often should each of these be reviewed? 🟡 | |
| **Specification & acceptance criteria:** | |
| **Complementarity boundary (what stays human):** | |
| **Verification level:** | |
| **Cost budget:** | |
| **Enrichment strategy:** | |
| **10.2** Which of these trigger conditions should cause an immediate review? 🟡 *Check all that apply:* | |
| ☐ Underlying model is upgraded or changed | |
| ☐ Sustained increase in rework rate | |
| ☐ Human's demonstrated competence has noticeably changed | |
| ☐ Output diversity is converging (multiple users get similar outputs) | |
| ☐ Per-invocation cost exceeds budget | |
| ☐ Other (describe): | |
| **10.3** Should the system track whether its own outputs are drifting in quality, diversity, or cost over time? 🟢 *Pick one: Yes — monitor all three · Yes — monitor quality and cost only · No · Don't know — recommend for me* | |

> **Feeds Agno template:**
> - **10.1** → These review cadences inform operational runbooks and maintenance schedules
> - **10.2** → Trigger sets inform guardrail and monitoring design
> - **10.3** → Observability (6.5) — drift tracking requires observability infrastructure

---

## Cross-Reference: How This Template Pre-Populates the Agno Template

| Agno Template Question | Fed By Principles Template Questions |
|---|---|
| **1.1** Purpose | Principles 1.1, 1.3, 1.4 |
| **1.2** Users | Principles 1.2, 1.5 |
| **1.3** Cognitive mode | Principles 2.1, 2.2, 1.5 (matrix position) |
| **2.1** Complexity / Architecture | Principles 5.1 (verification level), 6.3 (recovery protocol), 7.1 (pipeline position), 9.6 (orientation rotation) |
| **2.2** Sub-roles / Steps | Principles 7.1 (pipeline position), 5.1 (reviewer agents) |
| **3.1** Knowledge sources | Principles 4.1 (minimum context), 4.2 (information boundaries) |
| **3.2** Memory / Learning | Principles 8.1 (pattern capture), 2.4 (epistemic metadata), 9.4–9.5 (enrichment tracking) |
| **4.1** Tools | Principles 7.2 (minimum sufficient toolset), 2.3 (capability boundary) |
| **4.2** Human approval | Principles 1.5 (complementarity boundary), 5.1 (verification level), 6.2 (reversibility classification), 7.5 (human placement) |
| **5.1** Reasoning | Principles 3.3 (verifiability), 3.5 (type resolution), 9.2 (cognitive mirroring) |
| **5.2** Output format | Principles 3.5 (type resolution), 2.4 (epistemic metadata) |
| **5.3** Guardrails | Principles 6.1 (fail-safe defaults), 6.2 (reversibility), 5.2 (verification gates), 7.3 (infrastructure failure) |
| **5.4** Session state | Principles 4.3 (lifecycle state), 4.4 (epistemic context) |
| **6.5** Observability | Principles 5.3 (audit trail level), 8.2 (performance metrics), 10.3 (drift tracking) |
| **7.2** Persona / Instructions | Principles 2.2 (cognitive orientation), 9.1–9.3 (enrichment behaviors), 6.4 (diversity), 4.3 (lifecycle phase) |
| **8.1** Cost constraints | Principles 7.4 (cost ceiling + enrichment premium) |

---

## Quick Reference: Principles Decisions → Design Impact

| If you decided... | The design impact is... |
|---|---|
| Task is Novel + Irreversible (matrix) | Level 3 verification (different model, different toolset) + human at every irreversible decision |
| Task is Routine + Reversible (matrix) | Level 1 verification (structural self-review) + agent can operate more autonomously |
| Agent is an Executor archetype | It must NOT review its own output — add a separate Reviewer agent |
| Agent is an Exploration Agent | It must NOT be the final arbiter — human or downstream agent chooses |
| Cognitive orientation is Critical | System prompt frames toward finding flaws, not confirming assumptions |
| Type resolution requires Claims, Evidence, Confidence | Output must be structured (JSON/Pydantic), not free-form text |
| Irreversible actions exist | Human-in-the-loop confirmation is required for those actions |
| Enrichment is a goal | Agent must show reasoning (5.1), offer alternatives (7.2 persona), and track capability growth (3.2 memory) |
| Audit trail is Routine-irreversible | Need role-based read access to session logs |
| Audit trail is Novel-irreversible | Need cryptographic immutability (hash-chained or append-only distributed storage) |
| Cost ceiling is defined | Model choice and verification passes must stay within ceiling |
| Cognitive convergence is a risk | Rotate agent orientations, monitor output diversity |
| Specification review cadence is set | Add scheduled review triggers to operational runbook |
| Prototype before scale is needed | Start with minimum viable version, validate before investing in full implementation |
| Multiple users need diversity | Consider multiple agent variants or dynamic prompts with rotated orientations |

---

*This template ensures every Agno agent is built on principled foundations — trust, safety, enrichment, and temporal awareness — not just feature completeness. When both templates are filled in, the Design Agent has everything needed to generate a well-structured, trustworthy, human-enriching agent.*