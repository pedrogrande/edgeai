## Phase 7 — Agent Registry

### TypeDB Schema Additions

```typeql
define

# ── PHASE 7: AGENT REGISTRY ──

agent-entry sub entity,
    owns agent-id,
    owns agent-name,
    owns agent-class,               # 5-class taxonomy
    owns agent-mission,              # One sentence
    owns agent-authority-boundary,   # Inverse of failure mode — hard constraint
    owns agent-failure-mode,         # Characteristic failure mode for this class
    owns agent-allocation-mode,      # From Phase 4: "human-primary" | "agent-primary" | "collaborative"
    owns agent-deployment-wave,      # 1-7, follows pipeline stages
    owns agent-cc1-pair-ref,         # ID of CC-1 verification partner (if any)
    plays agent-assigned-to-subtask,
    plays agent-in-stage,
    plays cc1-agent-a,
    plays cc1-agent-b;

# ── RELATIONS ──

agent-subtask sub relation,
    relates agent-for-subtask,
    relates subtask-for-agent;

agent-stage sub relation,
    relates stage-agent,
    relates agent-stage;

cc1-verification-pair sub relation,
    relates cc1-pair-agent-a,
    relates cc1-pair-agent-b,
    owns cc1-verification-type;     # "output_validation" | "design_governance" | "code_test"

# ── ATTRIBUTES ──

agent-id sub attribute, value string;
agent-name sub attribute, value string;
agent-class sub attribute, value string;
agent-mission sub attribute, value string;
agent-authority-boundary sub attribute, value string;
agent-failure-mode sub attribute, value string;
agent-allocation-mode sub attribute, value string;
agent-deployment-wave sub attribute, value long;
agent-cc1-pair-ref sub attribute, value string;
cc1-verification-type sub attribute, value string;
```

---

### The Registry — 21 Agents, 3 System-Only, 7 Waves

| ID | Name | Class | Subtask | Mission | Authority Boundary | Failure Mode | Allocation | Wave | Stage | CC-1 Pair |
|----|------|-------|---------|---------|-------------------|---------------|-------------|------|-------|-----------|
| A01 | **Vision Mirror** | Assessor | T1.1 | Reflect purpose back; surface what's unstated | Never decide the purpose — only reflect and surface | Overconfidence | Human-primary | 1 | S1 | — |
| A02 | **Authority Validator** | Assessor | T1.2 | Validate authority class against 5-class taxonomy | Never assign the class — only validate against definitions | Overconfidence | Collaborative | 1 | S1 | — |
| A03 | **Scope Challenger** | Assessor | T1.3 | Stress-test boundary; find gaps and overreach | Never draw the boundary — only challenge what's drawn | Overconfidence | Human-primary | 2 | S2 | — |
| A04 | **Job Drafter** | Generator | T1.4 | Draft complete agent job description from scope + authority | Never finalise — human approves every job description | Fabrication / Vagueness | Agent-primary | 3 | S3 | A07 (at G3) |
| A05 | **Contract Architect** | Assessor | T1.5 | Structure contract architecture; define enforcement regime options | Never choose the enforcement regime — only structure the options | Overconfidence | Collaborative | 3 | S3 | — |
| A06 | **Template Cascade** | Generator | T2.1 | Generate all 8 template types in consistent cascade | Never validate your own templates — separate validator checks | Fabrication / Inconsistency | Agent-primary | 4 | S4 | A07 |
| A07 | **Template Validator** | Assessor | T2.2 | Validate template consistency, schema compliance, cross-template coherence | Never fix what you find — only flag inconsistencies | Overconfidence | Collaborative | 5 | S5 | A06 |
| A08 | **Profile Designer** | Generator | T3.1 | Draft agent personality linked to purpose and audience | Never finalise personality — human approves | Fabrication | Collaborative | 3 | S3 | A09 |
| A09 | **Personality Validator** | Assessor | T3.2 | Validate personality-purpose alignment; surface mismatches | Never override the personality — only surface misalignment | Overconfidence | Collaborative | 5 | S5 | A08 |
| A10 | **Autonomy Planner** | Assessor | T4.1 | Plan progressive autonomy thresholds from shadow to autonomous | Never set thresholds — only propose progression | Overconfidence | Collaborative | 5 | S5 | — |
| A11 | **Context Protocol** | Generator | T4.2 | Design agent context protocol with budget-aware retrieval | Never validate your own protocol — separate validation at G4 | Fabrication | Agent-primary | 4 | S4 | — |
| A12 | **Code Generator** | Generator | T5.1 | Generate Agno agent code from job description + contract + templates | Never validate your own code — separate test generator tests | Fabrication / Hallucination | Agent-primary | 6 | S6 | A13 |
| A13 | **Test Generator** | Generator | T5.2 | Generate test suite from FMEA entries + contract guards | Never mark your own tests as passed — separate validator confirms | Fabrication | Agent-primary | 6 | S6 | A12 |
| A14 | **Integration Validator** | Assessor | T5.3 | Run integration tests; flag failures and edge cases | Never approve integration — only flag results | Overconfidence | Collaborative | 7 | S7 | — |
| A15 | **Pattern Spotter** | Aggregator | T7.1 | Surface recurring patterns across completed agent designs | Never add patterns not present in the data — only surface what's there | Omission | Agent-primary | 7 | S7 | — |
| A16 | **Curriculum Drafter** | Generator | T7.2 | Draft Future's Edge curriculum module from completed design | Never finalise curriculum — human approves | Fabrication / Vagueness | Collaborative | 7 | S7 | — |
| A17 | **Tool Auditor** | Extractor | T8.1 | Extract tool requirements from job description + scope | Never judge tool suitability — only extract capabilities | Hallucination | Collaborative | 2 | S2 | — |
| A18 | **KB Specifier** | Generator | T8.2 | Design knowledge base schema and ingestion specification | Never validate your own KB design — Template Validator checks at G5 | Fabrication | Agent-primary | 4 | S4 | A07 (at G5) |
| A19 | **Memory Architect** | Generator | T8.3 | Design memory architecture with retention and retrieval policies | Never finalise memory policy — human approves | Fabrication | Collaborative | 5 | S5 | A20 |
| A20 | **Memory Governor** | Assessor | T8.4 | Assess memory governance compliance; flag policy violations | Never enforce policy — only assess compliance | Overconfidence | Collaborative | 5 | S5 | A19 |
| A21 | **Context Budget** | Measurer | T8.5 | Measure context allocation; calculate token budgets per knowledge source | Never interpret what the budget should be — present the measurement | Noise-as-signal | Agent-primary | 6 | S6 | — |

---

### System-Only Subtasks (No Agent)

| Subtask | Name | Mechanism | Stage |
|---------|------|-----------|-------|
| T6.1 | Boundary Map Rendering | TypeDB query → formatted one-page view | S6 |
| T6.2 | Ops Manual Rendering | TypeDB query → formatted insurer-ready document | S6 |
| T6.3 | Decision Log Compilation | TypeDB query → decisions with reasoning chains | S6 |

These are **derived views** — they read existing artefacts from the graph and render them. No generation, no judgment, no hallucination risk. The artefact graph IS the source of truth; rendered documents are views.

---

### Distribution by Class

| Class | Count | Agents | Characteristic Boundary |
|-------|-------|--------|-------------------------|
| **Assessor** | 9 | A01, A02, A03, A05, A07, A09, A10, A14, A20 | "Never [decide/assign/fix/override/approve] — only [surface/validate/flag/propose/assess]" |
| **Generator** | 9 | A04, A06, A08, A11, A12, A13, A16, A18, A19 | "Never finalise / Never validate your own — human approves or separate validator checks" |
| **Extractor** | 1 | A17 | "Never judge — only extract" |
| **Measurer** | 1 | A21 | "Never interpret — present the measurement" |
| **Aggregator** | 1 | A15 | "Never add — only surface what's there" |

**9 Assessors + 9 Generators = 86% of the roster.** This is structurally expected — the pipeline's core work is generating specifications (Generators) and validating them (Assessors). The Extractor/Measurer/Aggregator roles handle the remaining preparatory and analytical work.

---

### CC-1 Verification Pairs

| Pair | Agent A | Agent B | Type | What's Separated |
|------|---------|---------|------|------------------|
| VP-1 | A06 Template Cascade | A07 Template Validator | Output validation | Generation ↔ Validation |
| VP-2 | A08 Profile Designer | A09 Personality Validator | Output validation | Design ↔ Alignment check |
| VP-3 | A12 Code Generator | A13 Test Generator | Code-test | Implementation ↔ Verification |
| VP-4 | A19 Memory Architect | A20 Memory Governor | Design-governance | Architecture ↔ Compliance |

**4 CC-1 pairs.** Each pair separates a Generator from its Assessor counterpart. The Generator produces; the Assessor evaluates. Never the same agent does both — structural, not prompt-based.

**Agents without CC-1 pairs** are either: (a) Assessors with no corresponding Generator (A01, A02, A03, A05, A10, A14), (b) Generators validated by system gates not agent pairs (A04 at G3, A11 at G4, A16 at G7, A18 at G5), or (c) non-Generators (A15, A17, A21).

---

### Deployment Waves

| Wave | Stage | Agents | Parallelism |
|------|-------|--------|-------------|
| 1 | S1 Purpose | A01 Vision Mirror, A02 Authority Validator | Sequential (A01 first — purpose before classification) |
| 2 | S2 Scope | A03 Scope Challenger, A17 Tool Auditor | Parallel (scope + tool audit independent) |
| 3 | S3 Specification | A04 Job Drafter, A05 Contract Architect, A08 Profile Designer | A04 first → then A05 ∥ A08 (contracts and profiles depend on job desc) |
| 4 | S4 Templating | A06 Template Cascade, A11 Context Protocol, A18 KB Specifier | Parallel (three different template domains) |
| 5 | S5 Validation | A07 Template Validator, A09 Personality Validator, A10 Autonomy Planner, A19 Memory Architect, A20 Memory Governor | Parallel (all validation/design tasks, no cross-dependencies within S5) |
| 6 | S6 Generation | A12 Code Generator