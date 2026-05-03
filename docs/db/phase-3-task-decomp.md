# TypeDB Schema — Phase 3: Task Decomposition

```typeql
define

# ─── PHASE 3: TASK DECOMPOSITION ───

subtask sub entity,
    owns subtask-id,              # e.g., "T1.1"
    owns subtask-name,
    owns subtask-description,
    owns cognitive-type,          # "mechanical" | "analytical" | "generative" | "evaluative" | "intuitive"
    owns actor-hint,              # "human" | "agent" | "system" | "collaborative" (refined in Phase 4)
    owns subtask-order,           # Execution sequence within group
    plays subtask-in-group,
    plays subtask-depends-on-subtask,
    plays subtask-produces-output,
    plays subtask-requires-input,
    plays subtask-has-failure-mode;

subtask-group sub entity,
    owns subgroup-id,             # e.g., "SG1" maps to output group G1
    owns subgroup-name,
    plays group-containing-subtask;

subtask-dependency sub relation,
    relates depending-subtask,
    relates required-subtask,
    owns dep-type;                # "hard" | "soft"

subtask-produces sub relation,
    relates producing-subtask,
    relates produced-output;      # Links to design-output

subtask-requires-req sub relation,
    relates requiring-subtask,
    relates required-input;       # Links to input-requirement from Phase 2

failure-mode sub entity,
    owns fm-id,
    owns fm-name,
    owns fm-description,
    owns fm-invert-boundary,      # The authority boundary = inverse of this failure
    plays fm-for-subtask;

subtask-has-fm sub relation,
    relates subtask-with-fm,
    relates failure-mode;

# Attribute types
subtask-id sub attribute, value string;
subtask-name sub attribute, value string;
subtask-description sub attribute, value string;
cognitive-type sub attribute, value string;
actor-hint sub attribute, value string;
subtask-order sub attribute, value long;
subgroup-id sub attribute, value string;
subgroup-name sub attribute, value string;
dep-type sub attribute, value string;
fm-id sub attribute, value string;
fm-name sub attribute, value string;
fm-description sub attribute, value string;
fm-invert-boundary sub attribute, value string;
```

---

## The 22 Subtasks — Compact Reference

### SG1: Identity — Produces O1-O4

| ID | Name | Cognitive | Actor | Produces | Depends On | Failure Mode |
|----|------|-----------|-------|----------|------------|--------------|
| T1.1 | Purpose Discovery | intuitive | human | O1 | — | FM1: Multiple purposes tangled → boundary: anti-goals field enforced |
| T1.2 | Authority Class Validation | evaluative | human | O1 | T1.1 | FM2: Wrong class chosen → boundary: 5-class taxonomy check before proceeding |
| T1.3 | Scope Boundary Workshop | intuitive+evaluative | collaborative | O2 | T1.1, T1.2 | FM3: Scope too broad/narrow → boundary: stress test each inside_scope item |
| T1.4 | Job Description Drafting | generative | agent | O3 | T1.1-T1.3 | FM4: Too abstract to implement → boundary: "Agno dev can implement from this alone" gate |
| T1.5 | Contract Architecture | analytical+generative | collaborative | O4 | T1.4 | FM5: **CRITICAL** — contract on wrong foundation → boundary: authority class validated at T1.2 |

### SG2: Contracts — Produces O5-O12

| ID | Name | Cognitive | Actor | Produces | Depends On | Failure Mode |
|----|------|-----------|-------|----------|------------|--------------|
| T2.1 | Template Cascade | mechanical+generative | agent | O5-O12 | T1.5 | FM6: Inconsistent specialisations → boundary: cross-template consistency check |
| T2.2 | Template Validation | evaluative | collaborative | quality gate | T2.1 | FM7: Template passes in isolation, fails in combination → boundary: integration validation |

### SG3: Behaviour — Produces O13-O14

| ID | Name | Cognitive | Actor | Produces | Depends On | Failure Mode |
|----|------|-----------|-------|----------|------------|--------------|
| T3.1 | Relational Profile Design | intuitive | human | O13 | T1.1, T1.3 | FM8: Personality decorates, not serves → boundary: personality-purpose link must be explicit |
| T3.2 | Autonomy Plan Design | analytical+evaluative | collaborative | O14 | T1.3, T2.2 | FM9: Promotion without evidence → boundary: quantitative threshold for each level |

### SG4: Verification — Produces O15-O16

| ID | Name | Cognitive | Actor | Produces | Depends On | Failure Mode |
|----|------|-----------|-------|----------|------------|--------------|
| T4.1 | Trust Ledger Design | analytical | agent | O15 | T1.5, T2.1 | FM10: Ledger can't query by dimension → boundary: 3-axis queryability test |
| T4.2 | Aging Schedule Design | evaluative+analytical | collaborative | O16 | T1.4, T1.5 | FM11: Cadences too rigid → boundary: event-based triggers supplement calendar |

### SG5: Implementation — Produces O17-O18

| ID | Name | Cognitive | Actor | Produces | Depends On | Failure Mode |
|----|------|-----------|-------|----------|------------|--------------|
| T5.1 | Agent Code Generation | generative | agent | O17 | T1.1-T4.2 | FM12: **CRITICAL** — Agno can't enforce contract → boundary: CAWDP governance layer |
| T5.2 | Test Suite Generation | generative | agent | O18 | T2.1, T5.1 | FM13: Tests pass but miss edge cases → boundary: FMEA-driven test design |
| T5.3 | Integration Validation | evaluative | collaborative | gate | T5.1, T5.2 | FM14: Isolated pass, integrated fail → boundary: end-to-end pipeline test |

### SG6: Human Artefacts — Produces O19-O21

| ID | Name | Cognitive | Actor | Produces | Depends On | Failure Mode |
|----|------|-----------|-------|----------|------------|--------------|
| T6.1 | Boundary Map Render | mechanical | system | O19 | T1.3 | FM15: Map too technical → boundary: 5-minute readability test |
| T6.2 | Ops Manual Render | mechanical | system | O20 | T1.1-T4.2 | FM16: Manual doesn't answer insurer questions → boundary: PI insurer review template |
| T6.3 | Decision Log Capture | analytical | agent | O21 | continuous | FM17: Decisions logged without reasoning → boundary: "why" field required |

### SG7: Ecosystem — Produces O22-O23

| ID | Name | Cognitive | Actor | Produces | Depends On | Failure Mode |
|----|------|-----------|-------|----------|------------|--------------|
| T7.1 | Pattern Identification | analytical | agent | O22 | T4.1 | FM18: False pattern → boundary: validation evidence required |
| T7.2 | Curriculum Module Draft | generative | agent | O23 | T6.3, T7.1 | FM19: Module too abstract → boundary: teachable from this module gate |

### SG8: Operational Environment — Produces O24-O28

| ID | Name | Cognitive | Actor | Produces | Depends On | Failure Mode |
|----|------|-----------|-------|----------|------------|--------------|
| T8.1 | Tool Audit & Spec | analytical+intuitive | collaborative | O24 | T1.1, T1.3 | FM20: Tool grants more access than scope → boundary: tool-to-scope mapping required |
| T8.2 | Context Protocol Design | analytical | agent | O25 | T1.1, T1.3, T8.1 | FM21: Context window overflow → boundary: hard ceiling with budget accounting |
| T8.3 | Knowledge Base Spec | analytical+intuitive | collaborative | O26 | T1.1, T1.3, T4.2 | FM22: KB scope wider than agent scope → boundary: KB scope must match O2 |
| T8.4 | Memory Architecture | analytical+evaluative | collaborative | O27 | T1.1, T1.2, T3.1 | FM23: Memory without governance → boundary: retention policy + human-deletable default |
| T8.5 | Storage Specification | mechanical+analytical | agent | O28 | T1.4, T2.1 | FM24: Output schema mismatch → boundary: schema_registry validation for every output |

---

## Execution Waves

Sequential within groups. Parallel across groups where dependencies allow.

```
Wave 1 ── T1.1 Purpose Discovery
         │
Wave 2 ── T1.2 Authority Class Validation
         │
Wave 3 ── T1.3 Scope Boundary Workshop ───── T8.1 Tool Audit (starts parallel)
         │                                    │
Wave 4 ── T1.4 Job Description ───────────── T3.1 Relational Profile
         │                                    │
Wave 5 ── T1.5 Contract Architecture ──────── T4.2 Aging Schedule
         │                                    │
Wave 6 ── T2.1 Template Cascade ──────────── T4.1 Trust Ledger ──── T8.2 Context Protocol
         │                                                              │
Wave 7 ── T2.2 Template Validation ──────── T3.2 Autonomy Plan ─────── T8.3 KB Spec ── T8.4 Memory ── T8.5 Storage
         │                                                              │
Wave 8 ── T5.1 Agent Code ── T5.2 Test Suite ── T6.1-T6.3 Artefacts
         │
Wave 9 ── T5.3 Integration Validation ── T7.1-T7.2 Ecosystem
```

**9 waves.** Critical path runs through SG1 → SG2 → SG5 (7 steps on the spine). SG3, SG4, SG6, SG7, SG8 branch off where dependencies allow.

---

## The Key Finding from Decomposition

**T1.2 (Authority Class Validation) is the single highest-leverage subtask.** If the authority class is wrong, 19 downstream subtasks produce wrong artifacts. It's a 2-minute decision that determines the correctness of ~85% of subsequent work.

The 5-class taxonomy check at T1.2 is not optional. It's the **speed limiter**, not the speed limit sign.

