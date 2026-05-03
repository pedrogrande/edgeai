# TypeDB Schema — Phase 5: Event Storming

```typeql
define

# ─── PHASE 5: EVENT STORMING ───

# A domain event — something that happened that the pipeline reacts to
domain-event sub entity,
    owns event-id,
    owns event-name,
    owns event-type,              # "trigger" | "milestone" | "failure" | "recovery" | "escalation"
    owns event-description,
    owns event-source,           # "human" | "agent" | "system" | "external"
    owns event-payload-schema,   # What data the event carries
    plays event-triggers-subtask,
    plays event-produced-by-subtask,
    plays event-follows-event,
    plays event-triggers-recovery;

# An event that triggers a subtask to execute
subtask-trigger sub relation,
    relates triggered-subtask,
    relates trigger-event,
    owns trigger-condition;      # Additional condition beyond event occurrence

# An event produced by completing a subtask
subtask-emits sub relation,
    relates emitting-subtask,
    relates emitted-event;

# Event sequencing
event-sequence sub relation,
    relates preceding-event,
    relates succeeding-event,
    owns sequence-condition;      # When this sequence applies

# Recovery path — what happens when a failure event occurs
recovery-path sub entity,
    owns recovery-id,
    owns recovery-description,
    owns recovery-type,           # "retry" | "escalate" | "rollback" | "rebranch" | "halt"
    owns recovery-actor,          # "human" | "agent" | "system"
    owns recovery-max-attempts,
    plays recovery-for-failure;

failure-has-recovery sub relation,
    relates failure-event,
    relates recovery-path;

# System-enforced triggers — the system MUST fire these, not agents
system-trigger sub entity,
    owns sys-trigger-id,
    owns sys-trigger-name,
    owns sys-trigger-condition,
    owns sys-trigger-action,
    owns sys-trigger-enforcement, # "preventive" | "detective" | "corrective"
    plays sys-trigger-for-event;

event-has-system-trigger sub relation,
    relates event-with-trigger,
    relates system-trigger;

# Attribute types
event-id sub attribute, value string;
event-name sub attribute, value string;
event-type sub attribute, value string;
event-description sub attribute, value string;
event-source sub attribute, value string;
event-payload-schema sub attribute, value string;
trigger-condition sub attribute, value string;
sequence-condition sub attribute, value string;
recovery-id sub attribute, value string;
recovery-description sub attribute, value string;
recovery-type sub attribute, value string;
recovery-actor sub attribute, value string;
recovery-max-attempts sub attribute, value long;
sys-trigger-id sub attribute, value string;
sys-trigger-name sub attribute, value string;
sys-trigger-condition sub attribute, value string;
sys-trigger-action sub attribute, value string;
sys-trigger-enforcement sub attribute, value string;
```

---

## Trigger Events — What Starts Each Subtask

### Wave 1-3: Foundation

| Event ID | Event Name | Type | Source | Payload | Triggers | Condition |
|----------|-----------|------|--------|---------|----------|-----------|
| E1 | `session_started` | trigger | human | `{user_id, session_id, timestamp}` | T1.1 | Human opens Design Studio and begins |
| E2 | `purpose_articulated` | milestone | human | `{purpose_statement, anti_goals, principal_declared}` | T1.2 | Purpose field non-empty + anti_goals ≥1 |
| E3 | `authority_class_selected` | milestone | human | `{class: extractor\|measurer\|assessor\|generator\|aggregator}` | T1.3 | Class matches 5-class taxonomy definition |
| E4 | `scope_boundary_drawn` | milestone | human | `{inside_scope[], outside_scope[], escalation_triggers[]}` | T1.4, T8.1 | inside ≥1 AND outside ≥1 AND escalation ≥1 |

### Wave 4-5: Architecture

| Event ID | Event Name | Type | Source | Payload | Triggers | Condition |
|----------|-----------|------|--------|---------|----------|-----------|
| E5 | `job_description_approved` | milestone | human | `{job_desc_id, authority_boundary, input_schema, output_schema}` | T1.5, T3.1 | "Agno dev can implement" gate passed |
| E6 | `contract_architecture_approved` | milestone | human | `{contract_id, enforcement_regime, revert_granularity, guard_count}` | T2.1, T4.2 | Authority class validated at T1.2; guards testable |
| E7 | `relational_profile_approved` | milestone | human | `{profile_id, tone, personality_purpose_link}` | T3.2 | personality-purpose link explicit |
| E8 | `template_cascade_complete` | milestone | agent | `{template_ids[], consistency_check: pass}` | T2.2 | Cross-template consistency check passed |

### Wave 6-7: Verification + Environment

| Event ID | Event Name | Type | Source | Payload | Triggers | Condition |
|----------|-----------|------|--------|---------|----------|-----------|
| E9 | `templates_validated` | milestone | collaborative | `{validation_results[], edge_case_count}` | T4.1, T5.1, T5.2 | Quality gate assertions all pass |
| E10 | `trust_ledger_designed` | milestone | agent | `{ledger_schema, query_dimensions[]}` | T7.1 | 3-axis queryability test passed |
| E11 | `operational_env_specified` | milestone | collaborative | `{tools[], context_budget_kb, kb_scope, memory_policy}` | T8.5 | Scope containment check passed |
| E12 | `autonomy_plan_approved` | milestone | human | `{levels[], thresholds[], demotion_triggers[]}` | T8.4 | Quantitative thresholds defined |

### Wave 8-9: Implementation

| Event ID | Event Name | Type | Source | Payload | Triggers | Condition |
|----------|-----------|------|--------|---------|----------|-----------|
| E13 | `code_generation_complete` | milestone | agent | `{agent_code, test_code, coverage_pct}` | T5.3, T6.1, T6.2 | Schema_registry validation passed |
| E14 | `integration_test_run` | trigger | system | `{test_results[], failures[]}` | T5.3 | Generated after E13 |
| E15 | `integration_passed` | milestone | collaborative | `{sign_off: bool, edge_case_resolutions[]}` | T6.3, T7.2 | Human sign-off on edge cases |
| E16 | `agent_design_complete` | milestone | system | `{all_outputs[], artefact_graph_complete: bool}` | — | All 28 outputs exist + quality gates passed |

---

## Failure Events — What Goes Wrong and How We Recover

### F1-F5: Foundation Failures

| F-ID | Failure Event | Triggered By | Impact | Recovery | Actor | Max Attempts |
|------|--------------|-------------|--------|----------|-------|-------------|
| F1 | `purpose_unclear` | E1 → T1.1 stalls (human can't articulate) | Blocks all downstream | Vision Mirror reflects tensions back; suggests "what if you had an agent that…" scenarios | agent | 3 (then escalate) |
| F2 | `purpose_conflict` | T1.1 produces >1 purpose | Authority class ambiguous | **Rebranch**: split into N agents, one per purpose | human | 1 (structural decision) |
| F3 | `authority_class_mismatch` | T1.2 class doesn't match job description evidence | Contract built on wrong foundation (KR9 cascade) | **Rollback** to T1.2; re-validate with 5-class definitions + stress test | collaborative | 2 |
| F4 | `scope_bloat` | T1.3 inside_scope too large | Agent tries to do too much | **Rebranch**: extract sub-domain into separate agent design | human | 1 |
| F5 | `scope_void` | T1.3 outside_scope captures everything | Agent can't do anything meaningful | **Escalate**: question whether agent is needed at all | human | 1 |

### F6-F8: Architecture Failures

| F-ID | Failure Event | Triggered By | Impact | Recovery | Actor | Max Attempts |
|------|--------------|-------------|--------|----------|-------|-------------|
| F6 | `contract_untestable` | T1.5 guard cannot be verified programmatically | Enforcement is decorative | **Rollback** to T1.5; redesign guard as system-checkable assertion | collaborative | 2 |
| F7 | `template_inconsistency` | T2.1 cross-template check fails | Downstream code inconsistent | **Retry** T2.1 with consistency constraint enforced | agent | 3 |
| F8 | `personality_purpose_mismatch` | T3.1 tone conflicts with authority class | User distrust — e.g. Genial Assessor | **Rollback** to T3.1; re-link personality to purpose | collaborative | 2 |

### F9-F11: Implementation Failures

| F-ID | Failure Event | Triggered By | Impact | Recovery | Actor | Max Attempts |
|------|--------------|-------------|--------|----------|-------|-------------|
| F9 | `schema_validation_failure` | T5.1 output doesn't match schema_registry | Generated code won't run | **Retry** T5.1 with schema constraint | agent | 3 |
| F10 | `integration_test_failure` | E14 produces failures | Agent doesn't work end-to-end | **Rollback** to T5.1; diagnose failure path, fix, regenerate | collaborative | 3 |
| F11 | `context_budget_exceeded` | T8.2 protocol produces >budget context | Hallucination risk, cost overrun | **Halt** + rollback context; redesign with lower ceiling | agent | 2 |

### F12-F14: Governance Failures

| F-ID | Failure Event | Triggered By | Impact | Recovery | Actor | Max Attempts |
|------|--------------|-------------|--------|----------|-------|-------------|
| F12 | `stale_spec_detected` | Specification aging trigger fires | Agent operates on outdated design | **Escalate** to human; schedule refresh per O16 | system | 1 (auto-detect) |
| F13 | `memory_governance_breach` | T8.4 retention policy violated | Silent assumption accumulation | **Halt** + purge to policy; flag to human | system | 1 (auto-enforce) |
| F14 | `boundary_drift_detected` | Pattern of overrides in trust ledger | Agent exceeding authority | **Escalate** to human; review autonomy level | system | 1 (auto-detect) |

---

## Event Flow Map

```
E1 session_started
 │
 ├─► T1.1 Purpose Discovery
 │    │
 │    ├─ [F1 purpose_unclear] ──► Vision Mirror reflects ──► retry T1.1
 │    ├─ [F2 purpose_conflict] ──► Rebranch: split agents ──► N parallel pipelines
 │    │
 │    ▼
 │   E2 purpose_articulated
 │    │
 │    ├─► T1.2 Authority Class Validation
 │    │    │
 │    │    ├─ [F3 authority_class_mismatch] ──► Rollback T1.2 ──► re-validate
 │    │    │
 │    │    ▼
 │    │   E3 authority_class_selected
 │    │    │
 │    │    ├─► T1.3 Scope Boundary Workshop
 │    │    │    │
 │    │    │    ├─ [F4 scope_bloat] ──► Rebranch: extract sub-domain
 │    │    │    ├─ [F5 scope_void] ──► Escalate: is agent needed?
 │    │    │    │
 │    │    │    ▼
 │    │    │   E4 scope_boundary_drawn
 │    │    │    │
 │    │    │    ├─► T1.4 Job Description ──► T8.1 Tool Audit (parallel)
 │    │    │    │    │
 │    │    │    │    ▼
 │    │    │    │   E5 job_description_approved
 │    │    │    │    │
 │    │    │    │    ├─► T1.5 Contract Architecture
 │    │    │    │    │    │
 │    │    │    │    │    ├─ [F6 contract_untestable] ──► Rollback T1.5
 │    │    │    │    │    │
 │    │    │    │    │    ▼
 │    │    │    │    │   E6 contract_architecture_approved
 │    │    │    │    │    │
 │    │    │    │    │    ├─► T2.1 Template Cascade
 │    │    │    │    │    │    │
 │    │    │    │    │    │    ├─ [F7 template_inconsistency] ──► Retry with constraint
 │    │    │    │    │    │    │
 │    │    │    │    │    │    ▼
 │    │    │    │    │    │   E8 template_cascade_complete
 │    │    │    │    │    │    │
 │    │    │    │    │    │    ├─► T2.2 Template Validation ──► T4.1 Trust Ledger ──► T8.2 Context Protocol
 │    │    │    │    │    │    │
 │    │    │    │    │    │    ▼
 │    │    │    │    │    │   E9 templates_validated
 │    │    │    │    │    │    │
 │    │    │    │    │    │    ├─► T5.1 Code ──► T5.2 Tests ──► T6.1-T6.3 Artefacts
 │    │    │    │    │    │    │    │
 │    │    │    │    │    │    │    ├─ [F9 schema_validation_failure] ──► Retry
 │    │    │    │    │    │    │    │
 │    │    │    │    │    │    │    ▼
 │    │    │    │    │    │    │   E13 code_generation_complete
 │    │    │    │    │    │    │    │
 │    │    │    │    │    │    │    ├─► T5.3 Integration Validation
 │    │    │    │    │    │    │    │    │
 │    │    │    │    │    │    │    │    ├─ [F10 integration_test_failure] ──► Rollback T5.1
 │    │    │    │    │    │    │    │    │
 │    │    │    │    │    │    │    │    ▼
 │    │    │    │    │    │    │    │   E15 integration_passed
 │    │    │    │    │    │    │    │    │
 │    │    │    │    │    │    │    │    ▼
 │    │    │    │    │    │    │    │   E16 agent_design_complete
 │    │    │    │    │    │    │    │
 │    │    │    │    │    │    │    ├── [F11 context_budget_exceeded] ──► Halt + redesign
 │    │    │    │    │    │    │    │
 │    │    │    │    │    │    ├── [F12 stale_spec_detected] ──► Escalate (ongoing)
 │    │    │    │    │    │    ├── [F13 memory_governance_breach] ──► Halt + purge (ongoing)
 │    │    │    │    │    │    └── [F14 boundary_drift_detected] ──► Escalate (ongoing)
```

---

## System-Enforced Triggers — The Speed Limiters

These fire regardless of agent compliance. The system enforces them structurally.

| ST-ID | Name | Condition | Action | Enforcement | Guards |
|-------|------|-----------|--------|-------------|--------|
| ST1 | `authority_class_gate` | E3 fires but class not in taxonomy | **Block** pipeline; cannot proceed to T1.3 | Preventive | DA2 |
| ST2 | `scope_completeness_gate` | E4 fires but outside_scope empty | **Block** pipeline; no scope without exclusion | Preventive | DA3 |
| ST3 | `contract_testability_gate` | E6 fires but any guard lacks assertion | **Block** pipeline; decorative enforcement rejected | Preventive | DA4 |
| ST4 | `template_consistency_gate` | E8 fires but cross-check fails | **Block** + retry T2.1 with constraint | Preventive | — |
| ST5 | `schema_compliance_gate` | E13 fires but output fails schema_registry | **Block** + retry T5.1 with schema | Preventive | — |
| ST6 | `integration_gate` | E15 fires but any edge case unresolved | **Block** deployment; human must resolve | Preventive | DA8 |
| ST7 | `context_budget_hard_ceiling` | Context protocol output > budget_kb | **Halt** + truncate to budget | Preventive | — |
| ST8 | `memory_retention_enforcement` | Memory entry exceeds max_age | **Purge** + log event | Corrective | — |
| ST9 | `spec_aging_trigger` | `now - assessedAt > refresh_cadence_days` | **Flag** to human review queue | Detective | DA12 |
| ST10 | `boundary_drift_detector` | Override rate > threshold in trust ledger | **Flag** for autonomy review | Detective | DA14 |

---

## Recovery Path Summary

| Type | Count | When Used | Actor Pattern |
|------|-------|-----------|---------------|
| **Retry** | 4 | Agent can fix with same inputs + constraint (F1, F7, F9, F11) | Agent retries, system enforces constraint |
| **Rollback** | 5 | Wrong foundation detected — must redo upstream (F3, F6, F8, F10) | Rollback to source subtask, collaborative redo |
| **Rebranch** | 2 | Structural decision: agent should split (F2, F4) | Human decides, N parallel pipelines spawn |
| **Escalate** | 4 | Human judgment required — can't auto-resolve (F5, F12, F14) | System flags, human decides |
| **Halt** | 3 | Governance breach — must stop (F11 on 2nd attempt, F13, ST7/ST8) | System halts, human must intervene |

---

## The Key Finding from Event Storming

**5 of 14 failures originate in SG1 (Foundation).** Wrong purpose, wrong class, wrong scope — these cascade downstream because they corrupt the foundation everything else builds on. The system-enforced triggers (ST1-ST3) exist specifically to prevent foundation errors from propagating.

**Rollback is the dominant recovery mode** (5 of 14). This validates the contract architecture's revert granularity — we need at least `per_subtask` granularity to rollback to the right point without losing work.

**3 failures are governance failures (F12-F14) that don't have a "once" timeline** — they're ongoing monitoring events. This is specification aging (CC-5) and boundary drift detection operating as designed. The system detects what the agent can't self-assess.

**The most dangerous failure is F3 (authority_class_mismatch)** because it's the KR9 cascade: wrong class → wrong contract → wrong code → wrong agent. It's caught by ST1 (preventive) at E3 and by F3 (detective) if it leaks past. **Two layers of defense for the highest-impact failure.**

---

## UPDATE

**Separate entity types.** Same pattern as PRISM — abstract base, concrete subtypes.

Here's why, through your own principles:

**1. The attribute overlap is tiny.** Shared: `id`, `name`, `description`, `source`. That's 4 of ~15+ total attributes. Everything else diverges:

- **Trigger/milestone events** have: `payload-schema`, `trigger-condition`, `sequence-condition`
- **Failure events** have: `recovery-path` (1-to-many), `system-trigger`, `severity/impact`, `cascade-chain`, `fallback-tier`

If they share one entity type, most attributes are absent on most instances. That's the EAV anti-pattern in a different coat.

**2. The relations are asymmetric.**

- `recovery-path` relates to failure events only. On the current schema, `failure-has-recovery` relates `failure-event` to `recovery-path` — but `failure-event` is just a `domain-event` with a string value. The relation says "only failures," the schema says "any event." That's a type collision at the relation level.
- `subtask-trigger` relates to trigger/milestone events only. A failure event doesn't trigger a subtask — it interrupts one.
- `event-sequence` relates to trigger/milestone events. Failure events have cascade chains, not sequences.

**3. The query shapes are different.**

```
# "What triggered this stage?" → domain-event
# "What failures are unresolved?" → failure-event  
# "What recovery paths exist for this failure type?" → failure-event → recovery-path
```

These are different entity shapes being asked different questions. One type with a discriminator field forces every query to filter first. Two types let TypeDB's type system do the work.

**Corrected schema:**

```typeql
define

# ── ABSTRACT BASE ──

pipeline-event sub entity, abstract,
    owns event-id,
    owns event-name,
    owns event-description,
    owns event-source,
    plays event-precedes-event,
    plays event-follows-event;

# ── TRIGGER & MILESTONE ──

domain-event sub pipeline-event,
    owns event-type,              # "trigger" | "milestone" — only 2 values, genuine classification
    owns event-payload-schema,
    owns event-condition,          # Additional condition for triggering
    plays event-triggers-subtask,
    plays event-produced-by-subtask;

# ── FAILURE ──

failure-event sub pipeline-event,
    owns failure-severity,         # Impact severity if not caught
    owns failure-cascade,          # What this failure causes downstream
    owns failure-detection-method, # How we know it happened
    plays failure-interrupts-subtask,
    plays failure-has-recovery,
    plays failure-triggers-system-trigger;

# ── RECOVERY ── (unchanged)

recovery-path sub entity,
    owns recovery-id,
    owns recovery-type,            # "retry" | "rollback" | "rebranch" | "escalate" | "halt"
    owns recovery-actor,
    owns recovery-max-attempts,
    owns recovery-description,
    plays recovery-for-failure;

failure-recovery sub relation,
    relates failure-event,
    relates recovery-path;

# ── SYSTEM TRIGGERS ── (unchanged, but now relate to failure-event specifically)

system-trigger sub entity,
    owns sys-trigger-id,
    owns sys-trigger-condition,
    owns sys-trigger-action,
    owns sys-trigger-enforcement,
    plays sys-trigger-responds-to;

failure-system-trigger sub relation,
    relates failure-event,
    relates system-trigger;

# ── EVENT SEQUENCING (on the base type — applies to both) ──

event-sequence sub relation,
    relates preceding-event,
    relates succeeding-event,
    owns sequence-condition;
```

**What this preserves:** Both event types share `event-id`, `event-name`, `event-description`, `event-source` via inheritance. Both can participate in `event-sequence` (a failure event can precede a recovery milestone event). Queries against `pipeline-event` return both types.

**What this fixes:** `recovery-path` now relates only to `failure-event` — structurally enforced, not filtered. `subtask-trigger` now relates only to `domain-event` — a failure can't accidentally be a trigger. `system-trigger` responds to `failure-event` — not to milestones. The type system is the documentation.

Same pattern as `prism-artefact` → 7 dimension entities. The abstract base carries shared attributes; the concrete subtypes carry their own shape. Type collision resolved at the schema level, not the query level.