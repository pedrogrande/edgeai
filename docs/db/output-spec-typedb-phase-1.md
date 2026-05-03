# TypeDB Schema — Phase 1: Output Specification

Adding to the existing schema. New types only.

```typeql
define

# ─── PHASE 1: OUTPUT SPECIFICATION ───

# The 8 groups
output-group sub entity,
    owns group-id,                # e.g., "G1", "G5"
    owns group-name,              # e.g., "Identity", "Implementation"
    owns group-description,
    plays group-containing-output;

# Each output artefact
design-output sub entity,
    owns output-id,               # e.g., "O4"
    owns output-name,             # e.g., "Quasi-Smart Contract"
    owns output-purpose,          # One sentence
    owns prism-type,              # e.g., "intention", "entity", "knowledge"
    owns schema-registry-ref,     # References schema_registry entry for detailed schema
    owns quality-gate,            # How to verify it's good enough
    owns storage-location,        # "typeDB" | "code" | "derived_view"
    plays output-in-group,
    plays output-depends-on,
    plays output-dependency-of,
    plays serving-output;         # Links to target-characteristic via output-service

# Dependency chain — which outputs must exist before this one
output-dependency sub relation,
    relates depending-output,
    relates required-output,
    owns dependency-strength;     # "hard" (must exist) | "soft" (informs)

# ─── ATTRIBUTE TYPES ───

group-id sub attribute, value string;
group-name sub attribute, value string;
group-description sub attribute, value string;
output-id sub attribute, value string;
output-purpose sub attribute, value string;
prism-type sub attribute, value string;
schema-registry-ref sub attribute, value string;
quality-gate sub attribute, value string;
storage-location sub attribute, value string;
dependency-strength sub attribute, value string;
```

---

## The 28 Outputs — Compact Reference

Full schemas go in `schema_registry`. This table is for human scanning and insert queries.

### G1: Identity — Who This Agent Is

| ID | Name | Purpose | PRISM Type | Storage | Depends On | Quality Gate |
|----|------|---------|-----------|---------|------------|--------------|
| O1 | Purpose Statement | Mission, principal, authority class | intention | TypeDB | — | Stranger knows what it does/doesn't/for whom |
| O2 | Boundary Map | Inside/outside scope, escalations, human-only | intention+governance | TypeDB | O1 | Non-technical readable in 5 min; every outside_scope has escalation |
| O3 | Agent Job Description | Complete specification of role, capabilities, constraints | entity (schema_registry) | TypeDB | O1, O2 | Agno developer can implement from this alone |
| O4 | Quasi-Smart Contract | Enforcement membrane — all 8 primitives | entity (schema_registry) | TypeDB | O1-O3 | Every guard testable; budget halts structurally; revert granularity defined |

### G2: Contracts — The Operating Constitution

| ID | Name | Purpose | PRISM Type | Storage | Depends On | Quality Gate |
|----|------|---------|-----------|---------|------------|--------------|
| O5 | Input Contract | Validates every input | entity | TypeDB | O4 | Rejects invalid input structurally |
| O6 | Output Contract | Validates every output + epistemic metadata | entity | TypeDB | O4 | Injects epistemic metadata; authority class checked |
| O7 | Handoff Contract | Governs data transfer between actors | entity | TypeDB | O4 | Receiving input contract matches sending output |
| O8 | Verification Contract | Defines how outputs are verified | entity | TypeDB | O4 | Verification level specified; independent verifier defined |
| O9 | Decision Contract | Governs decisions affecting humans | entity | TypeDB | O4 | Human-only decision types listed; escalation threshold defined |
| O10 | Feedback Contract | Governs human→agent feedback | entity | TypeDB | O4 | Feedback types taxonomy; specification aging trigger defined |
| O11 | Escalation Contract | Governs when/how agent escalates | entity | TypeDB | O4 | Trigger conditions specific; timeout before default defined |
| O12 | Report Contract | Governs periodic/on-demand reporting | entity | TypeDB | O4 | Report type/audience/frequency defined |

### G3: Behaviour — How It Interacts

| ID | Name | Purpose | PRISM Type | Storage | Depends On | Quality Gate |
|----|------|---------|-----------|---------|------------|--------------|
| O13 | Relational Profile | Communication style, rapport approach | intention | TypeDB | O1, O2 | Tone matches authority class; personality-purpose link present; dependency guard |
| O14 | Progressive Autonomy Plan | 4-level autonomy progression with metrics | intention+governance | TypeDB | O2, O8 | Promotion requires quantitative evidence; autonomous has demotion triggers |

### G4: Verification — How We Know

| ID | Name | Purpose | PRISM Type | Storage | Depends On | Quality Gate |
|----|------|---------|-----------|---------|------------|--------------|
| O15 | Trust Ledger Schema | Records verification events, overrides, escalations | event+governance | TypeDB | O4, O8 | Queryable by time/class/agent; 3-level audit trail |
| O16 | Specification Aging Schedule | When/how specifications are reviewed | intention+temporal | TypeDB | O3, O4 | Every component has cadence; staleness queryable |

### G5: Implementation — The Running Agent

| ID | Name | Purpose | PRISM Type | Storage | Depends On | Quality Gate |
|----|------|---------|-----------|---------|------------|--------------|
| O17 | Agno Agent Code | Running implementation | — | Code files | O3, O4, O5-O12, O13, O14 | Passes all 8 template validations; cost within budget; boundaries revert not warn |
| O18 | Agno Agent Tests | Every design decision generates a test | — | Code files | O4, O5-O12 | Every guard, escalation trigger, must_escalate, and contract template has tests |

### G6: Human Artefacts

| ID | Name | Purpose | PRISM Type | Storage | Depends On | Quality Gate |
|----|------|---------|-----------|---------|------------|--------------|
| O19 | One-Page Boundary Map | Printable human-readable boundary map | derived view | Rendered from O2 | O2 | Non-technical person reads in 5 min |
| O20 | Agent Ops Manual Entry | Governance document for insurers/auditors | derived view | Rendered from O1-O16 | O1-O16 | PI insurer can assess risk from this doc |
| O21 | Design Decision Log | Decision archaeology — why, alternatives, reasoning | knowledge+epistemic | TypeDB | Continuous | Every major decision has entry; queryable "why" |

### G7: Ecosystem — What Compounds

| ID | Name | Purpose | PRISM Type | Storage | Depends On | Quality Gate |
|----|------|---------|-----------|---------|------------|--------------|
| O22 | Pattern Contribution | Novel patterns captured for reuse | knowledge+governance | TypeDB | O15 | Genuinely novel; has validation evidence |
| O23 | Curriculum Module Draft | Pedagogical value captured | knowledge | TypeDB | O21, O22 | Teachable from this module; honest about mistakes |

### G8: Operational Environment — How It Actually Works

| ID | Name | Purpose | PRISM Type | Storage | Depends On | Quality Gate |
|----|------|---------|-----------|---------|------------|--------------|
| O24 | Tool Specification | What agent can access/do; tools as boundary surface | entity+governance | TypeDB | O1, O2 | Every tool maps to inside_scope; critical tools require human authority |
| O25 | Context Specification | Budget-aware, relevance-scored context protocol | knowledge+epistemic | TypeDB | O1, O2, O24 | Budget bounded; excluded topics match outside_scope; no hallucination-priming |
| O26 | Knowledge Base Specification | Curated, scoped, epistemically tagged domain expertise | knowledge+epistemic+schema | TypeDB | O1, O2, O16 | KB scope matches O1; excluded topics match O2; freshness requirements defined |
| O27 | Memory Specification | What agent retains across sessions, with governance | knowledge+governance+temporal | TypeDB | O1, O2, O13 | Architecture matches authority class; human-deletable by default; dependency guard for collaborative |
| O28 | Storage & Output Specification | Where outputs go; TypeDB for data, files for code only | entity+governance+epistemic+temporal+schema | TypeDB | O3, O4, O5-O12, O21 | Every output has schema_registry entry; derived views generated not stored; code has traceability links |

---

## Dependency Graph — One Line Per Edge

```
O1 → O2
O2 → O13, O14, O19, O24
O1+O2 → O3
O1+O2+O3 → O4
O4 → O5, O6, O7, O8, O9, O10, O11, O12
O5-O12 → O17, O18
O4 → O15, O16, O28
O3+O4 → O16
O13 → O27
O2+O8 → O14
O4+O8 → O15
O1-O16 → O20
O15 → O22
O21+O22 → O23
O1+O2 → O24
O1+O2+O24 → O25
O1+O2+O16 → O26
```

---

## Key Queries This Enables

**"What depends on the Quasi-Smart Contract?"**
```
match $out (depending-output: $dep, required-output: $contract); 
$contract owns output-id "O4"; get $dep;
```
→ O5-O12, O15, O16, O17, O18, O28 — the contract is the linchpin

**"Which Phase 0 targets does O4 serve?"**
```
match $rel (serving-output: $out, served-target: $target);
$out owns output-id "O4"; get $target;
```
→ A2, A5, S1, S4

**"Which outputs have no dependencies?"**
```
match $out(sub entity, owns output-id); 
not $out (depending-output); get $out;
```
→ O1 (Purpose Statement) — everything starts here

**"Which targets still need outputs assigned?"**
```
match $target(sub entity, owns characteristic-id); 
not $target (served-target); get $target;
```
→ Reveals gaps in output coverage

---
