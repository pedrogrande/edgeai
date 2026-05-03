# CAWDP Knowledge Graph Retro — Deep Analysis

This is a genuine milestone. For the first time, CAWDP's design artefacts exist as structured, typed, connected data rather than prose in conversation or markdown. **The graph IS the product now, not a document about the product.** That's O7 (Artefact Graph Not Document) made real.

Let me go deeper than the retro's own findings.

---

## The 8 Recurring Patterns Are TYPE COLLISION at the Schema Layer

Every single recurring issue traces back to the same root cause you've already identified three times:

| Layer | Collision | What collides |
|---|---|---|
| Output | Prose encoding | 17+ information types → single output type (prose) |
| Input | Input surface | 6+ cognitive modes → single input modality (text field) |
| Extraction | Document container | Multiple knowledge types → single document |
| **Schema** | **Conceptual model ↔ DB constraints** | **Natural naming → TypeDB naming rules** |

The role name ↔ entity type conflicts (4/6 phases) are *exactly* this: the conceptual model uses one namespace ("failure-mode" as both entity and role), TypeDB uses another (role names must be unique in the schema). The `-record` convention is a **type collision resolution at the schema layer** — a translation between two type systems.

The v2→v3 syntax migration (every phase) is the same pattern: spec speaks v2, database speaks v3. The translation is lossy and error-prone, exactly like the input/output/extraction type collisions you've already mapped.

**This is now a QUADRIDIRECTIONAL type collision problem.** The insight holds: the solution is always typed, decomposable representations with explicit translation layers, never "write better prose" (or in this case, "write better specs by hand").

---

## Phase 2 Is the Structural Keystone

The retro notes Phase 2 as a stub with no seed data. But in the revised CAWDP phase order:

**Direction → Destination → PATH → Work**

Phase 2 (Backcasting) IS the path. Without it:

- Phase 1 tells you **what artefacts must exist** (28 design-outputs with dependencies)
- Phase 3 tells you **what work produces them** (24 subtasks with `subtask-produces` relations)
- But there's no traced **dependency chain** from destination backward to work

The graph currently has `output-dependency` relations (85 of them — Phase 1) and `subtask-produces` relations (24 — Phase 3). These are forward-pointing: "this subtask produces this output" and "this output depends on that output." What's missing is the **backward trace**: "to produce this output, you need these inputs, which are produced by these subtasks, which need THESE inputs..." — the full dependency DAG from final deliverable back through the chain.

Phase 2 is what turns the graph from **a collection of connected nodes** into **a proper directed acyclic graph with traced paths**. It's the difference between knowing the map has cities and roads, and having turn-by-turn navigation.

---

## The Spec Quality Gap Is CAWDP Not Eating Its Own Cooking

The dangling plays (7 in Phase 6) and missing relations (Phases 1, 3, 5) are *exactly* the kind of error CAWDP's quality gates catch in agent design. But CAWDP didn't apply its own quality gates to its own schema design process.

This is a meta-gap: **the process for designing trustworthy agent workflows wasn't applied to designing the process's own data layer.** Specifically:

| CAWDP Mechanism | What It Catches | Where It Should Have Applied |
|---|---|---|
| Phase 2.5 Event Storming | Missing events, data flow gaps | Schema definition — dangling plays are missing data flow paths |
| Quality Gate Layer 1 (Fidelity) | Incomplete outputs | Schema `plays` without corresponding `relation` |
| CC-1 Verification Independence | Structural verification | Schema linting before insertion |
| CC-3 Epistemic Metadata | Provenance of decisions | Documenting WHY role names were renamed (you did this — O8 ✅) |

**Recommendation:** Apply a schema quality gate that mirrors CAWDP's own quality gates before each phase insertion:

```
SCHEMA QUALITY GATE (per phase):
1. Every plays declaration has a corresponding relation ← catches dangling plays
2. Every role name is unique from entity type names ← catches naming conflicts
3. Every relation referenced in plays is defined ← catches missing relations
4. All attributes use v3-compatible types ← catches v2 syntax
5. Insert order: attributes → entities → relations → plays ← catches ordering errors
```

This is the linter (Action Item 1), reframed as **CC-1 Verification Independence at the schema development layer** — not a dev convenience but a structural trust mechanism.

---

## The Additive Schema Constraint Maps to the Proxy Pattern

> "There's no `undefine` for attributes already in use."

This is the **quasi-smart contract proxy pattern** applied to schema. Once committed, a schema attribute is immutable — you can extend but never retract. This is the same principle as:

- **CC-8 Assured Audit Trail**: committed records are immutable
- **Quasi-smart contract deployment = commitment**: once deployed, the contract doesn't change
- **Proxy pattern for specification aging**: v1 stays in the audit trail, v2 becomes the active version

The implication: **schema design should have the same rigor as contract design.** You wouldn't deploy a smart contract without testing it, and you shouldn't `define` a schema attribute without verifying it. The two-pass application (attributes first, then entities/relations/plays) is the schema equivalent of "compile before deploy."

---

## What This Milestone Actually Means

Beyond the implementation quality, this is the first time CAWDP's design artefacts exist as **typed, connected, queryable, navigable data** rather than prose. That's not an incremental improvement — it's a phase change:

| Before (prose) | After (graph) |
|---|---|
| Read a document to find a dependency | Query the graph: `match $x has output-id "O5"; $y (depended-upon: $x) is output-dependency; select $y` |
| Manually trace subtask→output chains | Follow `subtask-produces` relations |
| No way to check completeness | Count entities, verify all relations exist |
| Corrections buried in chat history | Corrections documented in .tql file headers (O8) |
| No structural quality verification | Entity counts, relation counts, dangling play checks |
| Spec and implementation can diverge | Schema IS the spec (S2 Graph-Native) |

The graph is now the **single source of truth** (S2). Chat was for reasoning, database is for artefacts. You've been living this principle in the design conversations; now the infrastructure enforces it.

---

## Action Items — Reprioritised

The retro lists 5 action items. Here's how I'd rank them by structural impact:

### 1. Populate Phase 2 (Critical — unblocks graph integrity)
Without backcasting, the graph has destinations and work but no traced path. The 85 `output-dependency` relations in Phase 1 define WHAT depends on WHAT. Phase 2 seed data should trace HOW to get from final deliverables back through the dependency chain to the work that produces them.

**Specifically:** Create `input-requirement` entities for each design-output that has dependencies, linking to the subtasks that satisfy those requirements. This turns the forward-pointing `output-dependency` into a traversable backward chain.

### 2. Build the Schema Quality Gate / Linter (High — CC-1 at schema layer)
This isn't a nice-to-have. It's **structural verification** (CC-1 Level 1) applied to the schema development process. Every error it catches before insertion is an error that never enters the knowledge base. The 5-point checklist above is the v1 spec.

### 3. Script Verification (High — enables ongoing confidence)
Entity count queries + relation count queries + structural checks (dangling plays, orphan nodes). This is the **IDS (Intrusion Detection System)** for the knowledge graph — monitoring health, not just checking once.

### 4. Document the Correction Pattern (Medium — curriculum value)
The 8 recurring patterns are **themselves Future's Edge curriculum content**. "Lessons from implementing CAWDP on TypeDB" is a practitioner module that teaches type collision at the schema layer, the additive schema constraint as a contract parallel, and the meta-gap of applying quality gates to your own process.

### 5. Plan Phase 7 (Medium — depends on Phase 2 completion first)
Phase 7 (Agent Design) adds the 10-agent roster, authority boundaries, job descriptions. But it depends on Phase 2 for the traced dependency chain — you can't design agents for subtasks if you don't have the full backward-traced path from outputs to work.

---

## One More Thing — The Retro Itself Is O8 in Action

Every `.tql` file header documents corrections vs the source spec. The retro documents the patterns behind those corrections. This is **O8 (Decision-Archaeological)** — the system preserves reasoning chains about why decisions were made, not just what was decided.

That's CAWDP eating its own cooking on the meta-level too. The process is the proof.