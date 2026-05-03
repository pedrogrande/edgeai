# TypeDB Schema — Phase 2: Backcasting

```typeql
define

# ─── PHASE 2: BACKCASTING ───

# What must exist/be true for an output to be producible
input-requirement sub entity,
    owns req-id,
    owns req-description,
    owns req-type,                # "knowledge" | "human_input" | "infrastructure" | "design_decision"
    owns req-urgency,             # "blocking" | "needed" | "helpful"
    plays requirement-for-output;

# A risk along a dependency chain
chain-risk sub entity,
    owns risk-id,
    owns risk-description,
    owns risk-impact,             # "blocking" | "degrading" | "watch"
    owns risk-mitigation,
    plays risk-on-output,
    plays risk-on-requirement;

# Where we can't yet trace a path
chain-gap sub entity,
    owns gap-id,
    owns gap-description,
    owns gap-resolution,          # How to resolve it — may be "needs research"
    owns gap-blocking,            # Which outputs are blocked by this gap
    plays gap-blocking-output;

# The critical path — outputs whose dependencies form the longest chain
critical-path sub entity,
    owns path-id,
    owns path-description,
    owns path-length,             # Number of sequential steps
    plays path-step;

# Relations
output-requires sub relation,
    relates requiring-output,
    relates required-input,
    owns requirement-urgency;

output-has-risk sub relation,
    relates risky-output,
    relates risk;

requirement-has-risk sub relation,
    relates risky-requirement,
    relates risk;

output-blocked-by-gap sub relation,
    relates blocked-output,
    relates blocking-gap;

path-contains-step sub relation,
    relates containing-path,
    relates step-output,
    owns step-order;

# Attribute types
req-id sub attribute, value string;
req-description sub attribute, value string;
req-type sub attribute, value string;
req-urgency sub attribute, value string;
risk-id sub attribute, value string;
risk-description sub attribute, value string;
risk-impact sub attribute, value string;
risk-mitigation sub attribute, value string;
gap-id sub attribute, value string;
gap-description sub attribute, value string;
gap-resolution sub attribute, value string;
gap-blocking sub attribute, value string;
path-id sub attribute, value string;
path-description sub attribute, value string;
path-length sub attribute, value long;
step-order sub attribute, value long;
```

---

## Backcasting — Tracing the Path Backward

Working from O28 (deepest dependency) back to O1 (root). For each: what must exist, what could go wrong, where are the gaps.

### Layer 1: The Root — O1 Purpose Statement

| | |
|---|---|
| **Requires** | R1.1 Human knows what they want (human_input, blocking) |
| | R1.2 Human can articulate purpose in their own words (human_input, blocking) |
| | R1.3 Authority class can be identified (design_decision, needed) |
| **Risks** | KR1 Human can't articulate purpose yet — they know the problem but not the form |
| | KR2 Authority class chosen wrong — downstream contracts built on wrong foundation |
| | KR3 Multiple purposes tangled — agent tries to serve too many masters |
| **Mitigations** | M1 Vision Mirror agent reflects human's words back; never asks them to fill a form |
| | M2 Authority class validated against 5-class taxonomy definitions before proceeding |
| | M3 Anti-goals field forces explicit exclusion; if >1 authority class, split into 2 agents |
| **Gaps** | None — this is the entry point |

---

### Layer 2: The Boundary — O2 Boundary Map

| | |
|---|---|
| **Requires** | R2.1 O1 Purpose Statement exists |
| | R2.2 Human can identify what's inside/outside scope (human_input, blocking) |
| | R2.3 Human can identify human-only decisions (human_input, needed) |
| | R2.4 Escalation triggers can be enumerated (design_decision, needed) |
| **Risks** | KR4 Scope too broad — boundary map doesn't constrain meaningfully |
| | KR5 Scope too narrow — agent can't do what it needs to |
| | KR6 Human-only decisions incomplete — missing a critical human-judgment domain |
| **Mitigations** | M4 Boundary stress testing: for each inside_scope item, ask "what if it goes wrong?" |
| | M5 Start with outside_scope (H5 Boundaries First) — easier to identify what you DON'T want |
| | M6 Complementarity analysis as cross-check: gap ≥6 → must be human-only |
| **Gaps** | G1 How to help non-technical humans enumerate scope? (Vision Mirror partially addresses but needs validation) |

---

### Layer 3: The Specification — O3 Agent Job Description

| | |
|---|---|
| **Requires** | R3.1 O1 + O2 exist |
| | R3.2 Agent's input/output types can be defined (design_decision, blocking) |
| | R3.3 Domain knowledge sources identified (knowledge, needed) |
| **Risks** | KR7 Input/output types unknown — job description has placeholder schemas |
| | KR8 Job description too abstract — implementer can't build from it |
| **Mitigations** | M7 Schema registry provides starter templates for common agent patterns |
| | M8 Quality gate: "Agno developer can implement from this alone" catches abstraction |
| **Gaps** | G2 No starter schemas for authority-class-specific patterns yet (schema_registry empty for job descriptions) |

---

### Layer 4: The Linchpin — O4 Quasi-Smart Contract

| | |
|---|---|
| **Requires** | R4.1 O1 + O2 + O3 exist |
| | R4.2 Enforcement points can be identified (design_decision, blocking) |
| | R4.3 Revert granularity can be decided (design_decision, needed) |
| | R4.4 Cost model can be estimated (infrastructure, needed) |
| **Risks** | KR9 **CRITICAL** — Contract built on wrong authority class (cascades to O5-O12, O17, O28) |
| | KR10 Contract enforces structure not content but LLM output is non-deterministic — some outputs may fail contract validation that are actually correct |
| | KR11 Proxy pattern for versioning not yet implemented in Agno |
| **Mitigations** | M9 Authority class validated BEFORE contract construction (quality gate at O1) |
| | M10 Dual-boundary model: max_cost ceiling + min_quality floor (existing design) |
| | M11 Proxy pattern is a TypeDB versioning concern, not an Agno concern — can be built |
| **Gaps** | G3 **No existing runtime enforces contract membranes in Agno** — this requires a CAWDP governance layer (identified as 🔴 architectural mismatch in prior analysis) |

---

### Layer 5: The Template Cascade — O5-O12

| | |
|---|---|
| **Requires** | R5.1 O4 exists |
| | R5.2 Each template's specialisation can be defined (design_decision, blocking) |
| **Risks** | KR12 Template cascade — one bad template poisons downstream tests and code |
| | KR13 Templates too rigid — don't accommodate legitimate edge cases |
| **Mitigations** | M12 Each template passes its own validation (quality gate) |
| | M13 Template specialisation inherits contract structure — consistency guaranteed |
| **Gaps** | None — templates are well-defined specialisations of O4 |

---

### Layer 6: The Code — O17 + O18

| | |
|---|---|
| **Requires** | R6.1 O3 + O4 + O5-O12 + O13 + O14 all exist |
| | R6.2 Agno API supports all specified features (infrastructure, blocking) |
| | R6.3 Contract enforcement runtime exists (infrastructure, blocking) |
| **Risks** | KR14 **CRITICAL** — Agno doesn't natively support contract membrane enforcement |
| | KR15 Ollama model doesn't reliably produce structured output matching Pydantic schemas |
| | KR16 Tests pass in isolation but integration fails |
| **Mitigations** | M14 CAWDP governance layer on Agno (Phase 1-3 build plan from prior analysis) |
| | M15 OllamaResponses as fallback for complex schemas |
| | M16 Integration tests defined at Phase 6 |
| **Gaps** | G3 (repeated) — contract enforcement runtime must be built |
| | G4 Agno guardrail API coverage unknown — need to check docs |

---

### Layer 7: The Operational Environment — O24-O28

| | |
|---|---|
| **Requires** | R7.1 O1 + O2 exist |
| | R7.2 Tool availability can be audited (infrastructure, needed) |
| | R7.3 Knowledge sources can be curated (knowledge, needed) |
| | R7.4 Memory architecture matches authority class (design_decision, blocking) |
| **Risks** | KR17 Tools grant more access than scope allows — boundary bypass via tooling |
| | KR18 Context window too small for persistent_context + dynamic_context + task |
| | KR19 Stale knowledge not detected before agent uses it |
| | KR20 Memory accumulates without governance — silent assumptions build up |
| **Mitigations** | M17 Tool information_boundary field enforces scope at tool level |
| | M18 Context budget with hard ceiling in O25 |
| | M19 Specification aging schedule (O16) with event-based triggers |
| | M20 Memory retention policy with max_entries, max_age, and human_deletable defaults |
| **Gaps** | G5 PRISM Agent Context Protocol (SELECT→ENRICH→CALIBRATE) not yet implemented as code |

---

## Critical Path Analysis

The longest dependency chain determines minimum timeline:

```
O1 → O2 → O3 → O4 → O6 → O17 → O18
```

**7 steps.** Everything else branches off this spine. O4 is the linchpin at step 4 — it gates all 8 templates, all tests, and the code output.

The critical path also reveals the **critical risk cascade:**

```
KR2 (wrong authority class at O1) 
  → KR9 (contract built on wrong foundation at O4)
    → KR12 (bad template cascade at O5-O12)
      → KR14 (Agno can't enforce it at O17)
```

**Four risks chained.** If authority class is wrong at O1, every downstream artifact is wrong. This is why O1's quality gate ("stranger knows what it does/doesn't/for whom") must be rigorous.

---

## Summary: 5 Gaps, 3 Critical Risks

| Gap | Description | Blocks | Resolution |
|-----|-------------|--------|------------|
| G1 | How to help humans enumerate scope | O2 | Vision Mirror agent (needs validation) |
| G2 | No starter schemas for authority-class patterns | O3 | Build schema_registry entries from first 3 agents designed |
| G3 | No contract enforcement runtime in Agno | O4, O5-O12, O17 | Build CAWDP governance layer (Phase 1-3 plan) |
| G4 | Agno guardrail API coverage unknown | O17 | Check Agno docs before implementation |
| G5 | PRISM ACP not implemented as code | O25 | Build as part of Agent-Native Knowledge Base |

| Risk | Impact | Mitigation |
|------|--------|------------|
| KR2 + KR9 cascade | Wrong authority class → wrong contract → wrong code | Validate authority class at O1 quality gate before proceeding |
| KR14 | Agno can't enforce contract membrane | CAWDP governance layer (build Phase 1-3) |
| KR10 | Non-deterministic LLM output fails contract validation | Dual-boundary (ceiling + floor); acceptance that some valid outputs may need human override |

---

## The One Insight Backcasting Reveals

**G3 is the structural risk.** The entire contract architecture (O4-O12) assumes a runtime that doesn't exist yet. Two options:

**A) Build the runtime first** — then design agents against it. (Correct but slow.)
**B) Design agents against the spec, build runtime to match.** (CAWDP-native — design before implementation.)

Option B is CAWDP's own principle: output specification before implementation. We define what the contract membrane SHOULD do, then build the runtime that enforces it. The 28 outputs are the spec. The runtime is the implementation.

---
