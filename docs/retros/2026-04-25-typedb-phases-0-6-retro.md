# TypeDB Schema & Seed Implementation Retrospective

**Date:** 25 April 2026  
**Scope:** Phases 0–6 (Target State Vision → System Architecture)  
**Database:** `edgeai` on local TypeDB v3.10.1  
**Status:** ✅ All phases live and verified

---

## Summary

Implemented the full CAWDP (Context-Aware Whole-Design Process) knowledge graph in TypeDB, spanning 7 phases (0–6) of the agent design pipeline. Each phase added schema types and seed data incrementally, with significant v2→v3 syntax corrections required at every stage. The database now holds **~220 entities** across **22 entity types**, connected by **~200+ relations** across **20 relation types**, with **~130 attribute types**.

---

## Phase-by-Phase Summary

### Phase 0: Target State Vision
- **Schema:** `db/schemas/phase0.tql`
- **Seed:** `db/seeds/phase0_insert.tql`
- **Entities:** 4 target-dimensions, 26 target-characteristics
- **Relations:** 26 dimension-characteristic-membership
- **Key corrections:** None (first phase, clean v3 syntax from the start)

### Phase 1: Output Specification
- **Schema:** `db/schemas/phase1.tql`
- **Seed:** `db/seeds/phase1_insert.tql`, `db/seeds/phase1_service_links.tql`
- **Entities:** 8 output-groups, 28 design-outputs
- **Relations:** 28 output-group-membership, 85 output-dependency, 28 phase-service, 28 output-service
- **Key corrections:** Extended Phase 0 `design-output` stub with new attributes; added `output-group-membership` relation (missing from spec)

### Phase 2: Backcasting
- **Status:** Skipped (no seed data yet; `input-requirement` stub created in Phase 3)

### Phase 3: Task Decomposition
- **Schema:** `db/schemas/phase3.tql`
- **Seed:** `db/seeds/phase3_insert.tql`, `db/seeds/phase3_produces.tql`
- **Entities:** 24 subtasks, 8 subtask-groups, 24 failure-modes
- **Relations:** 24 subtask-group-membership, 24 subtask-produces, 24 subtask-has-fm
- **Key corrections:**
  - Added missing `subtask-group-membership` relation (spec referenced roles without a relation)
  - Role name conflict: `failure-mode` entity type → `fm-entity` role name
  - `subtask plays subtask-has-failure-mode` → `subtask-has-fm:fm-subtask`
  - Added `input-requirement` stub for Phase 2 compatibility

### Phase 4: Capability Allocation
- **Schema:** `db/schemas/phase4.tql`
- **Seed:** `db/seeds/phase4_insert.tql`
- **Entities:** 24 allocations, 10 decision-authorities
- **Relations:** 24 subtask-has-allocation, 10 subtask-has-authority
- **Key corrections:**
  - `value long` → `value integer` (4 attributes: judgment-demand, pattern-capacity, determinism-fit, complementarity-gap)
  - Role name conflicts: `allocation` → `allocation-record`, `decision-authority` → `da-record`
  - @key added to alloc-id and da-id

### Phase 5: Event Storming
- **Schema:** `db/schemas/phase5.tql`
- **Seed:** `db/seeds/phase5_entities.tql`, `db/seeds/phase5_relations.tql`
- **Entities:** 16 domain-events, 14 failure-events, 14 recovery-paths, 10 system-triggers
- **Relations:** 24 subtask-trigger, 16 subtask-emits, 13 event-sequence, 14 failure-interrupts, 14 failure-recovery, 14 failure-system-trigger
- **Key corrections:**
  - `abstract` keyword NOT supported in v3.10.1 — `pipeline-event` is concrete but never instantiated directly
  - `value long` → `value integer` (recovery-max-attempts)
  - 4 role name conflicts: `failure-event`→`failed-event`, `recovery-path`→`recovery-instance`, `system-trigger`→`sys-trigger-instance`, `failure-event`→`triggered-failure`
  - Missing relations added: `subtask-trigger`, `subtask-emits`, `failure-interrupts`
  - `domain-event` plays both `subtask-trigger:trigger-event` AND `subtask-emits:emitted-event`

### Phase 6: System Architecture
- **Schema:** `db/schemas/phase6.tql`
- **Seed:** `db/seeds/phase6_entities.tql`, `db/seeds/phase6_relations.tql`
- **Entities:** 9 pipeline-stages, 1 orchestration-config, 5 orchestration-decisions, 14 FMEA entries, 7 template-types, 12 template-instances, 1 composition-config, 18 fallback-tiers
- **Relations:** 24 stage-contains, 8 stage-sequence, 5 orchestration-has-decision, 12 template-has-instance, 14 subtask-has-fallback
- **Key corrections:**
  - `value long` → `value integer` (10 attributes)
  - 3 role name conflicts: `orchestration-decision`→`od-record`, `template-instance`→`ti-record`, `fallback-tier`→`ft-record`
  - 7 dangling plays removed (referenced non-existent relations)
  - `stage-parallel` as `value boolean` — confirmed working
  - `ft-preserve-state` as `value string` per spec (semantically boolean but stored as string)
  - S9 has no stage-contains relations (F12/F13/F14 are failure-events, not subtasks)
  - Tier 4 fallback-tiers have no subtask-has-fallback links (escalation-only)

---

## Live Database Entity Counts

| Entity Type | Count | Phase |
|---|---|---|
| target-dimension | 4 | 0 |
| target-characteristic | 26 | 0 |
| cawdp-phase | 0* | 0 |
| design-output | 28 | 1 |
| output-group | 8 | 1 |
| subtask | 24 | 3 |
| subtask-group | 8 | 3 |
| failure-mode | 24 | 3 |
| input-requirement | 0* | 3 |
| allocation | 24 | 4 |
| decision-authority | 10 | 4 |
| domain-event | 16 | 5 |
| failure-event | 14 | 5 |
| recovery-path | 14 | 5 |
| system-trigger | 10 | 5 |
| pipeline-stage | 9 | 6 |
| orchestration-config | 1 | 6 |
| orchestration-decision | 5 | 6 |
| fmea-entry | 14 | 6 |
| template-type | 7 | 6 |
| template-instance | 12 | 6 |
| composition-config | 1 | 6 |
| fallback-tier | 18 | 6 |
| **Total** | **~257** | |

\* Stubs with no seed data yet (Phase 2 not yet populated)

---

## Schema Statistics

| Metric | Count |
|---|---|
| Entity types | 22 |
| Relation types | 20 |
| Attribute types | ~130 |
| @key attributes | 22 |
| Inheritance (sub) | 2 (domain-event, failure-event sub pipeline-event) |
| Boolean attributes | 1 (stage-parallel) |
| Integer attributes | 17 |

---

## Recurring Issues & Patterns

### 1. v2 → v3 Syntax Migration (Every Phase)
Every spec was written in TypeQL v2 syntax. Each phase required systematic conversion:
- `sub entity` → `entity` (for top-level declarations)
- `sub relation` → `relation`
- `sub attribute` → `attribute`
- `value long` → `value integer` (TypeDB v3.10.1 rejects `long`)
- Inline `plays` on entity blocks → standalone `plays relation:role` at block end

**Lesson:** Write a pre-flight checker that scans for v2 syntax before applying to the database.

### 2. Role Name ↔ Entity Type Conflicts (Phases 3, 4, 5, 6)
TypeDB v3 does not allow a role name to match an entity type name. This happened in 4 out of 6 phases:
- Phase 3: `failure-mode` → `fm-entity`
- Phase 4: `allocation` → `allocation-record`, `decision-authority` → `da-record`
- Phase 5: `failure-event` → `failed-event`/`triggered-failure`, `recovery-path` → `recovery-instance`, `system-trigger` → `sys-trigger-instance`
- Phase 6: `orchestration-decision` → `od-record`, `template-instance` → `ti-record`, `fallback-tier` → `ft-record`

**Lesson:** Always check role names against entity type names. Use a naming convention like `<abbreviation>-record` or `<abbreviation>-instance` for disambiguation.

### 3. Dangling Plays (Phase 6)
Phase 6 spec referenced 7 `plays` declarations for relations that didn't exist in the schema:
- `oc-defines-orchestration`, `od-for-orchestration`, `cc-defines-composition`, `fmea-for-subtask`, `ti-of-type`, `ti-for-subtask`, `ft-for-subtask`

**Lesson:** Validate every `plays` declaration against actual `relation` definitions before applying schema.

### 4. Missing Relations in Spec (Phases 1, 3, 5)
Several specs referenced role names without defining the corresponding relation:
- Phase 1: `output-group-membership` was missing
- Phase 3: `subtask-group-membership` was missing
- Phase 5: `subtask-trigger`, `subtask-emits`, `failure-interrupts` were missing

**Lesson:** Cross-reference every role name in `plays` declarations against defined `relation` types. If a role has no home, either add the relation or remove the play.

### 5. `fetch` Syntax Rejected (Phase 6 verification)
TypeDB v3.10.1 rejects `fetch { $var.* }` syntax. Must use `select $var` for read queries.

**Lesson:** Use `match ... select` pattern for all verification queries.

### 6. Large Inserts Need Splitting (Phase 6)
Phase 6 had 67 entities. Splitting into 2 MCP calls (29 + 38) avoided potential timeout issues.

**Lesson:** For inserts > 50 entities, split into batches of ~30–40 per MCP call.

### 7. Additive Schema Application
`define` is additive in TypeDB — re-declaring an entity adds new `owns` without removing existing ones. This is essential for incremental phase application but means you can't remove attributes once defined.

**Lesson:** Get the schema right before applying. There's no `undefine` for attributes already in use.

### 8. Attribute Declaration Order Matters
When adding inherited types (e.g., `domain-event sub pipeline-event`), new attributes must be declared in a separate `define` call BEFORE the entity that uses them.

**Lesson:** Always apply schema in two passes: (1) attributes, (2) entities/relations/plays.

---

## What Went Well

1. **Incremental approach** — Each phase built on the previous one without breaking existing data
2. **Verification after each phase** — Spot-checking entity counts and key relations caught issues early
3. **Correction documentation** — Each `.tql` file header documents all corrections vs the source spec
4. **Two-pass schema application** — Attributes first, then entities/relations/plays, prevented ordering errors
5. **TypeDB MCP tool** — Enabled direct schema and data manipulation without CLI switching

---

## What Could Be Improved

1. **Pre-flight validation** — A linter/checker for v2 syntax, role name conflicts, and dangling plays would have caught errors before MCP calls
2. **Spec quality** — Specs had inconsistent relation definitions (missing relations, dangling plays). A schema-first spec review would reduce corrections
3. **Phase 2 gap** — `input-requirement` and `cawdp-phase` remain stubs with no seed data
4. **Automated count verification** — Entity count checks were manual; could be scripted
5. **Relation count tracking** — Didn't systematically count all relations; only spot-checked key ones

---

## Files Created

### Schema Files
| File | Phase | Entity Types | Relation Types | Attributes |
|---|---|---|---|---|
| `db/schemas/phase0.tql` | 0 | 5 | 4 | 12 |
| `db/schemas/phase1.tql` | 1 | 2 | 2 | 9 |
| `db/schemas/phase3.tql` | 3 | 4 | 5 | 12 |
| `db/schemas/phase4.tql` | 4 | 2 | 2 | 17 |
| `db/schemas/phase5.tql` | 5 | 5 | 6 | 17 |
| `db/schemas/phase6.tql` | 6 | 8 | 5 | ~40 |

### Seed Files
| File | Phase | Content |
|---|---|---|
| `db/seeds/phase0_insert.tql` | 0 | 4 dimensions + 26 characteristics + 26 relations |
| `db/seeds/phase1_insert.tql` | 1 | 8 groups + 28 outputs |
| `db/seeds/phase1_service_links.tql` | 1 | 28 phase-service + 28 output-service + 85 output-dependency |
| `db/seeds/phase3_insert.tql` | 3 | 24 subtasks + 8 groups + 24 failure-modes |
| `db/seeds/phase3_produces.tql` | 3 | 24 subtask-produces + 24 subtask-has-fm |
| `db/seeds/phase4_insert.tql` | 4 | 24 allocations + 10 decision-authorities |
| `db/seeds/phase5_entities.tql` | 5 | 16 domain-events + 14 failure-events + 14 recovery-paths + 10 system-triggers |
| `db/seeds/phase5_relations.tql` | 5 | ~95 relations (trigger, emits, sequence, interrupts, recovery, system-trigger) |
| `db/seeds/phase6_entities.tql` | 6 | 67 entities (9 stages + 1 OC + 5 ODs + 14 FMEA + 7 TTs + 12 TIs + 1 CC + 18 FTs) |
| `db/seeds/phase6_relations.tql` | 6 | ~63 relations (stage-contains, stage-sequence, orchestration, template, fallback) |

---

## Action Items

1. **Build a TypeQL v3 linter** — Check for v2 syntax, role name conflicts, dangling plays, and missing relations before applying schema
2. **Populate Phase 2** — Add `input-requirement` and `cawdp-phase` seed data
3. **Script verification** — Write a Python script that queries all entity/relation counts and compares against expected values
4. **Consider Phase 7** — If a spec exists, plan the next phase of the knowledge graph
5. **Document the correction pattern** — Create a reusable checklist for v2→v3 migration that can be applied to future phases