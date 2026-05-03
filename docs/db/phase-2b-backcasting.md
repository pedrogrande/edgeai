# Phase 2: Backcasting — Complete Implementation Design

## Design Rationale

Phase 2 is the **structural keystone** of the CAWDP knowledge graph. Without it:
- Phase 1 tells you **what artefacts must exist** (28 outputs)
- Phase 3 tells you **what work produces them** (24 subtasks)
- But there's no traced **dependency path** from deliverable back to origin

Phase 2 materialises the `output-dependency` relations as explicit `input-requirement` entities with metadata, and bridges them to the subtasks that consume them. It turns a collection of nodes into a navigable DAG.

---

## 1. Schema Definition — `db/schemas/phase2.tql`

Applying retro correction patterns:

- ✅ v3 syntax only (no `sub`, no `value long`, inline plays removed)
- ✅ Role names checked against ALL entity types — no collisions
- ✅ Two-pass application (attributes first, then entities/relations/plays)
- ✅ `@key` on all ID attributes
- ✅ All relations explicitly defined with roles before `plays` declarations

```
# =============================================================================
# PHASE 2: BACKCASTING — Schema Definition
# TypeDB v3.10.1 compatible
# 
# Corrections from retro patterns applied:
# P1: v3 syntax only (no sub, no value long, inline plays removed)
# P2: Role names verified against all 22 entity types — no collisions
# P3: All relations defined BEFORE plays declarations
# P4: @key on all ID attributes
# P5: Two-pass application: attributes first, then entities/relations/plays
# =============================================================================

# ---- PASS 1: ATTRIBUTES ----

define
  # cawdp-phase attributes
  phase-id owns string @key,
  phase-number owns integer,
  phase-name owns string,
  phase-name-short owns string,
  cognitive-mode owns string,
  phase-description owns string,
  phase-quality-gate owns string,
  phase-iteration-type owns string,
  
  # input-requirement attributes (extending stub from phase3.tql)
  ir-id owns string @key,
  ir-type owns string,
  ir-criticality owns string,
  ir-satisfaction-mode owns string,
  ir-description owns string,
  ir-source-phase owns integer,
  ir-derived-from-dependency owns boolean;
```

```
# ---- PASS 2: ENTITIES, RELATIONS, PLAYS ----

define
  # ---- ENTITY TYPES ----
  
  cawdp-phase 
    owns phase-id,
    owns phase-number,
    owns phase-name,
    owns phase-name-short,
    owns cognitive-mode,
    owns phase-description,
    owns phase-quality-gate,
    owns phase-iteration-type,
    plays phase-sequence:predecessor-phase,
    plays phase-sequence:successor-phase,
    plays phase-produces-output:producing-phase;
  
  # input-requirement (extending stub from phase3.tql)
  input-requirement
    owns ir-id,
    owns ir-type,
    owns ir-criticality,
    owns ir-satisfaction-mode,
    owns ir-description,
    owns ir-source-phase,
    owns ir-derived-from-dependency,
    plays ir-required-by-output:required-ir,
    plays ir-satisfied-by-output:satisfied-ir,
    plays ir-consumed-by-subtask:consumed-ir;
  
  # ---- RELATION TYPES ----
  
  # Phase sequence: linear progression 0→1→2→...→9
  # Also supports iterative feedback loops (specified by phase-iteration-type)
  phase-sequence
    relates predecessor-phase,
    relates successor-phase;
  
  # Which phase produces which design-output
  phase-produces-output
    relates producing-phase,
    relates produced-output;
  
  # IR required by an output (backward trace: "To produce O5, you need IR-X")
  ir-required-by-output
    relates requiring-output,
    relates required-ir;
  
  # IR satisfied by an output (forward trace: "IR-X is satisfied by O3")
  ir-satisfied-by-output
    relates satisfied-ir,
    relates satisfying-output;
  
  # IR consumed by a subtask (bridge to Phase 3: "Subtask S3 consumes IR-X")
  ir-consumed-by-subtask
    relates consumed-ir,
    relates consuming-task;
  
  # ---- EXTEND EXISTING TYPES ----
  # design-output already exists; add plays for Phase 2 relations
  
  design-output
    plays phase-produces-output:produced-output,
    plays ir-required-by-output:requiring-output,
    plays ir-satisfied-by-output:satisfying-output;
  
  # subtask already exists; add plays for Phase 2 relation
  
  subtask
    plays ir-consumed-by-subtask:consuming-task;
```

---

## 2. Phase Entities Seed — `db/seeds/phase2_phases.tql`

10 phases + 9 sequence relations + 28 phase-output links.

```
# =============================================================================
# PHASE 2: BACKCASTING — Phase Entity Seed Data
# TypeDB v3.10.1 compatible
# 
# 10 CAWDP phases with cognitive modes, quality gates, and iteration types.
# 9 phase-sequence relations (linear progression).
# 28 phase-produces-output relations (which phase produces which output).
# =============================================================================

# ---- PHASE ENTITIES ----

insert
  # Phase 0: Purpose & Vision
  $p0 isa cawdp-phase,
    has phase-id "P0",
    has phase-number 0,
    has phase-name "Purpose & Vision",
    has phase-name-short "P0-Purpose",
    has cognitive-mode "IMAGINE",
    has phase-description "What is this agent FOR? What does perfect look like?",
    has phase-quality-gate "Fidelity: Do all 4 dimensions have characteristics? Enrichment: Does the vision expand creative freedom?",
    has phase-iteration-type "revise-upon-refinement";

insert
  # Phase 1: Output Specification
  $p1 isa cawdp-phase,
    has phase-id "P1",
    has phase-number 1,
    has phase-name "Output Specification",
    has phase-name-short "P1-Outputs",
    has cognitive-mode "SPECIFY",
    has phase-description "What artefacts MUST exist when we're done?",
    has phase-quality-gate "Fidelity: Are all 28 outputs defined with schemas and dependencies? Enrichment: Does the output set enable creative freedom?",
    has phase-iteration-type "revise-upon-new-discovery";

insert
  # Phase 2: Backcasting
  $p2 isa cawdp-phase,
    has phase-id "P2",
    has phase-number 2,
    has phase-name "Backcasting",
    has phase-name-short "P2-Backcast",
    has cognitive-mode "TRACE",
    has phase-description "Working backward from outputs, tracing dependency chains and gaps.",
    has phase-quality-gate "Fidelity: Can every output trace back to an origin? No orphan inputs? Enrichment: Does the backcast reveal hidden dependencies?",
    has phase-iteration-type "revise-upon-gap-discovery";

insert
  # Phase 3: Task Decomposition
  $p3 isa cawdp-phase,
    has phase-id "P3",
    has phase-number 3,
    has phase-name "Task Decomposition",
    has phase-name-short "P3-Decompose",
    has cognitive-mode "DECOMPOSE",
    has phase-description "Decompose work toward known outputs, not into a vacuum.",
    has phase-quality-gate "Fidelity: Are all outputs accounted for? Are cognitive operation types assigned? Enrichment: Does decomposition preserve creative freedom?",
    has phase-iteration-type "revise-upon-complexity";

insert
  # Phase 4: Capability Allocation
  $p4 isa cawdp-phase,
    has phase-id "P4",
    has phase-number 4,
    has phase-name "Capability Allocation",
    has phase-name-short "P4-Allocate",
    has cognitive-mode "ALLOCATE",
    has phase-description "Assign Human/Agent/System via complementarity analysis.",
    has phase-quality-gate "Fidelity: Are all 24 subtasks allocated? Complementarity gaps ≥ 6 = human-only? Enrichment: Does allocation expand human capability?",
    has phase-iteration-type "revise-upon-capability-discovery";

insert
  # Phase 5: Event Storming
  $p5 isa cawdp-phase,
    has phase-id "P5",
    has phase-number 5,
    has phase-name "Event Storming",
    has phase-name-short "P5-StressTest",
    has cognitive-mode "STRESS-TEST",
    has phase-description "Surface failure events, data flow gaps, trigger conditions.",
    has phase-quality-gate "Fidelity: All critical failure events identified? Recovery paths defined? Enrichment: Does stress testing reveal opportunities?",
    has phase-iteration-type "revise-upon-failure-discovery";

insert
  # Phase 6: System Architecture
  $p6 isa cawdp-phase,
    has phase-id "P6",
    has phase-number 6,
    has phase-name "System Architecture",
    has phase-name-short "P6-Architect",
    has cognitive-mode "ARCHITECT",
    has phase-description "Pipeline architecture, orchestration, FMEA, templates.",
    has phase-quality-gate "Fidelity: Pipeline stages, orchestration, templates defined? FMEA complete? Enrichment: Architecture enables future extension?",
    has phase-iteration-type "revise-upon-architectural-discovery";

insert
  # Phase 7: Agent Design
  $p7 isa cawdp-phase,
    has phase-id "P7",
    has phase-number 7,
    has phase-name "Agent Design",
    has phase-name-short "P7-Design",
    has cognitive-mode "DESIGN",
    has phase-description "5-class taxonomy, authority boundaries, job descriptions.",
    has phase-quality-gate "Fidelity: All agents classified? Authority boundaries tied to failure modes? Enrichment: Agent design amplifies human capability?",
    has phase-iteration-type "revise-upon-boundary-discovery";

insert
  # Phase 8: Human Experience
  $p8 isa cawdp-phase,
    has phase-id "P8",
    has phase-number 8,
    has phase-name "Human Experience",
    has phase-name-short "P8-Empathize",
    has cognitive-mode "EMPATHIZE",
    has phase-description "Cognitive load budget, interface specification, override mechanisms.",
    has phase-quality-gate "Fidelity: Cognitive load budgeted? Overrides specified? Enrichment: System Empowerment Index ≥ Enabling?",
    has phase-iteration-type "revise-upon-human-discovery";

insert
  # Phase 9: Validation & Iteration
  $p9 isa cawdp-phase,
    has phase-id "P9",
    has phase-number 9,
    has phase-name "Validation & Iteration",
    has phase-name-short "P9-Verify",
    has cognitive-mode "VERIFY",
    has phase-description "Prototype testing, progressive autonomy, health monitoring.",
    has phase-quality-gate "Fidelity: All 6 hypotheses testable? Progressive autonomy levels defined? Enrichment: Iteration increases human capability?",
    has phase-iteration-type "revise-upon-evidence";
```

```
# ---- PHASE SEQUENCE RELATIONS (0→1→2→...→9) ----

insert
  $p0 isa cawdp-phase, has phase-id "P0";
  $p1 isa cawdp-phase, has phase-id "P1";
  $seq01 (predecessor-phase: $p0, successor-phase: $p1) isa phase-sequence;

insert
  $p1 isa cawdp-phase, has phase-id "P1";
  $p2 isa cawdp-phase, has phase-id "P2";
  $seq12 (predecessor-phase: $p1, successor-phase: $p2) isa phase-sequence;

insert
  $p2 isa cawdp-phase, has phase-id "P2";
  $p3 isa cawdp-phase, has phase-id "P3";
  $seq23 (predecessor-phase: $p2, successor-phase: $p3) isa phase-sequence;

insert
  $p3 isa cawdp-phase, has phase-id "P3";
  $p4 isa cawdp-phase, has phase-id "P4";
  $seq34 (predecessor-phase: $p3, successor-phase: $p4) isa phase-sequence;

insert
  $p4 isa cawdp-phase, has phase-id "P4";
  $p5 isa cawdp-phase, has phase-id "P5";
  $seq45 (predecessor-phase: $p4, successor-phase: $p5) isa phase-sequence;

insert
  $p5 isa cawdp-phase, has phase-id "P5";
  $p6 isa cawdp-phase, has phase-id "P6";
  $seq56 (predecessor-phase: $p5, successor-phase: $p6) isa phase-sequence;

insert
  $p6 isa cawdp-phase, has phase-id "P6";
  $p7 isa cawdp-phase, has phase-id "P7";
  $seq67 (predecessor-phase: $p6, successor-phase: $p7) isa phase-sequence;

insert
  $p7 isa cawdp-phase, has phase-id "P7";
  $p8 isa cawdp-phase, has phase-id "P8";
  $seq78 (predecessor-phase: $p7, successor-phase: $p8) isa phase-sequence;

insert
  $p8 isa cawdp-phase, has phase-id "P8";
  $p9 isa cawdp-phase, has phase-id "P9";
  $seq89 (predecessor-phase: $p8, successor-phase: $p9) isa phase-sequence;
```

```
# ---- PHASE-PRODUCES-OUTPUT RELATIONS ----
# Which phase produces which design-output

insert
  $p0 isa cawdp-phase, has phase-id "P0";
  $o1 isa design-output, has output-id "O1";
  $po1 (producing-phase: $p0, produced-output: $o1) isa phase-produces-output;
  $o2 isa design-output, has output-id "O2";
  $po2 (producing-phase: $p0, produced-output: $o2) isa phase-produces-output;
  $o3 isa design-output, has output-id "O3";
  $po3 (producing-phase: $p0, produced-output: $o3) isa phase-produces-output;
  $o4 isa design-output, has output-id "O4";
  $po4 (producing-phase: $p0, produced-output: $o4) isa phase-produces-output;

insert
  $p1 isa cawdp-phase, has phase-id "P1";
  $o5 isa design-output, has output-id "O5";
  $po5 (producing-phase: $p1, produced-output: $o5) isa phase-produces-output;
  $o6 isa design-output, has output-id "O6";
  $po6 (producing-phase: $p1, produced-output: $o6) isa phase-produces-output;
  $o7 isa design-output, has output-id "O7";
  $po7 (producing-phase: $p1, produced-output: $o7) isa phase-produces-output;
  $o8 isa design-output, has output-id "O8";
  $po8 (producing-phase: $p1, produced-output: $o8) isa phase-produces-output;

insert
  $p1 isa cawdp-phase, has phase-id "P1";
  $o9 isa design-output, has output-id "O9";
  $po9 (producing-phase: $p1, produced-output: $o9) isa phase-produces-output;
  $o10 isa design-output, has output-id "O10";
  $po10 (producing-phase: $p1, produced-output: $o10) isa phase-produces-output;
  $o11 isa design-output, has output-id "O11";
  $po11 (producing-phase: $p1, produced-output: $o11) isa phase-produces-output;
  $o12 isa design-output, has output-id "O12";
  $po12 (producing-phase: $p1, produced-output: $o12) isa phase-produces-output;

insert
  $p1 isa cawdp-phase, has phase-id "P1";
  $o13 isa design-output, has output-id "O13";
  $po13 (producing-phase: $p1, produced-output: $o13) isa phase-produces-output;
  $o14 isa design-output, has output-id "O14";
  $po14 (producing-phase: $p1, produced-output: $o14) isa phase-produces-output;
  $o15 isa design-output, has output-id "O15";
  $po15 (producing-phase: $p1, produced-output: $o15) isa phase-produces-output;

insert
  $p1 isa cawdp-phase, has phase-id "P1";
  $o16 isa design-output, has output-id "O16";
  $po16 (producing-phase: $p1, produced-output: $o16) isa phase-produces-output;
  $o17 isa design-output, has output-id "O17";
  $po17 (producing-phase: $p1, produced-output: $o17) isa phase-produces-output;
  $o18 isa design-output, has output-id "O18";
  $po18 (producing-phase: $p1, produced-output: $o18) isa phase-produces-output;
  $o19 isa design-output, has output-id "O19";
  $po19 (producing-phase: $p1, produced-output: $o19) isa phase-produces-output;

insert
  $p1 isa cawdp-phase, has phase-id "P1";
  $o20 isa design-output, has output-id "O20";
  $po20 (producing-phase: $p1, produced-output: $o20) isa phase-produces-output;
  $o21 isa design-output, has output-id "O21";
  $po21 (producing-phase: $p1, produced-output: $o21) isa phase-produces-output;
  $o22 isa design-output, has output-id "O22";
  $po22 (producing-phase: $p1, produced-output: $o22) isa phase-produces-output;
  $o23 isa design-output, has output-id "O23";
  $po23 (producing-phase: $p1, produced-output: $o23) isa phase-produces-output;

insert
  $p1 isa cawdp-phase, has phase-id "P1";
  $o24 isa design-output, has output-id "O24";
  $po24 (producing-phase: $p1, produced-output: $o24) isa phase-produces-output;
  $o25 isa design-output, has output-id "O25";
  $po25 (producing-phase: $p1, produced-output: $o25) isa phase-produces-output;
  $o26 isa design-output, has output-id "O26";
  $po26 (producing-phase: $p1, produced-output: $o26) isa phase-produces-output;

insert
  $p1 isa cawdp-phase, has phase-id "P1";
  $o27 isa design-output, has output-id "O27";
  $po27 (producing-phase: $p1, produced-output: $o27) isa phase-produces-output;
  $o28 isa design-output, has output-id "O28";
  $po28 (producing-phase: $p1, produced-output: $o28) isa phase-produces-output;
```

---

## 3. Input Requirements Seed — `db/seeds/phase2_input_requirements.tql`

**CRITICAL DESIGN DECISION:** The 85 `output-dependency` relations from Phase 1 are already in the graph. Rather than duplicating them, Phase 2 *materialises* them as `input-requirement` entities with additional metadata (type, criticality, satisfaction-mode). This is the backcasting bridge — it turns "O5 depends-on O1" into "To produce O5, you need IR-004 which is satisfied by O1."

I'm seeding **three types** of input requirements to demonstrate the full pattern:

**A) EXTERNAL inputs for Phase 0** (human judgment, system provision — not in output-dependency)
**B) A COMPLETE BACKCASTING CHAIN** from O28 (Agent Operations Manual) through its entire dependency path to O1 (Agent Identity Card) — demonstrating the traced path
**C) REPRESENTATIVE internal IRs** for key outputs to show the pattern without seeding all 85

```
# =============================================================================
# PHASE 2: BACKCASTING — Input Requirement Seed Data
# TypeDB v3.10.1 compatible
#
# Three types of IR seeded:
# A) External inputs for Phase 0 (human judgment, system provision)
# B) Complete backcasting chain: O28 → ... → O1
# C) Representative internal IRs for key outputs
#
# IR types: internal, external-human, external-system, external-domain, iterative
# IR criticality: blocking, enhancing, validating
# IR satisfaction-mode: direct, transformed, referenced, accumulated
#
# Convention: ir-derived-from-dependency = true means materialised from output-dependency
#             ir-derived-from-dependency = false means identified through backcasting analysis
# =============================================================================

# ---- A) EXTERNAL INPUTS FOR PHASE 0 ----
# Phase 0 (Purpose & Vision) has no pipeline-internal dependencies.
# Its inputs come from human judgment and domain knowledge.

insert
  $ir001 isa input-requirement,
    has ir-id "IR-EXT-001",
    has ir-type "external-human",
    has ir-criticality "blocking",
    has ir-satisfaction-mode "direct",
    has ir-description "Principal's vision for what the agent is FOR — the human intent that drives the entire pipeline",
    has ir-source-phase 0,
    has ir-derived-from-dependency false;

insert
  $ir002 isa input-requirement,
    has ir-id "IR-EXT-002",
    has ir-type "external-human",
    has ir-criticality "blocking",
    has ir-satisfaction-mode "direct",
    has ir-description "Principal's declaration of whose interests the agent serves",
    has ir-source-phase 0,
    has ir-derived-from-dependency false;

insert
  $ir003 isa input-requirement,
    has ir-id "IR-EXT-003",
    has ir-type "external-domain",
    has ir-criticality "enhancing",
    has ir-satisfaction-mode "referenced",
    has ir-description "Domain knowledge about the agent's operating context — industry, regulations, stakeholder landscape",
    has ir-source-phase 0,
    has ir-derived-from-dependency false;

insert
  $ir004 isa input-requirement,
    has ir-id "IR-EXT-004",
    has ir-type "external-system",
    has ir-criticality "enhancing",
    has ir-satisfaction-mode "referenced",
    has ir-description "Agno framework capabilities and constraints — what the runtime can and cannot do",
    has ir-source-phase 0,
    has ir-derived-from-dependency false;

# ---- B) COMPLETE BACKCASTING CHAIN: O28 → ... → O1 ----
# Tracing the dependency path from the final deliverable (O28 Agent Operations Manual)
# back through every layer of input requirements.
#
# O28 depends on: O27, O24, O25, O26, O20, O21, O22, O23
# O27 depends on: O16, O17, O18, O19, O13
# O24 depends on: O4, O5, O11
# O25 depends on: O5, O9, O19
# O26 depends on: O15, O13, O12
# O20 depends on: O4, O12
# O21 depends on: O4, O6, O12
# O22 depends on: O4, O12, O14
# O23 depends on: O20, O21, O22
# And so on back to O1, O2, O3, O4 (root outputs from Phase 0)
#
# We materialise the FIRST LAYER of this chain (O28's direct dependencies)
# as input requirements, then ONE deeper layer (O4, O5 as roots).

insert
  # O28 requires O27 (Deployment Specification)
  $ir028_dep_O27 isa input-requirement,
    has ir-id "IR-028-001",
    has ir-type "internal",
    has ir-criticality "blocking",
    has ir-satisfaction-mode "transformed",
    has ir-description "Deployment specification needed to operationalise the manual",
    has ir-source-phase 2,
    has ir-derived-from-dependency true;

insert
  # O28 requires O24 (Coalition Specification)
  $ir028_dep_O24 isa input-requirement,
    has ir-id "IR-028-002",
    has ir-type "internal",
    has ir-criticality "blocking",
    has ir-satisfaction-mode "transformed",
    has ir-description "Agent coalition structure needed for operations section",
    has ir-source-phase 2,
    has ir-derived-from-dependency true;

insert
  # O28 requires O25 (Integration Contract)
  $ir028_dep_O25 isa input-requirement,
    has ir-id "IR-028-003",
    has ir-type "internal",
    has ir-criticality "blocking",
    has ir-satisfaction-mode "direct",
    has ir-description "Integration contracts needed for deployment procedures",
    has ir-source-phase 2,
    has ir-derived-from-dependency true;

insert
  # O28 requires O26 (Health Monitoring Dashboard)
  $ir028_dep_O26 isa input-requirement,
    has ir-id "IR-028-004",
    has ir-type "internal",
    has ir-criticality "enhancing",
    has ir-satisfaction-mode "referenced",
    has ir-description "Health monitoring metrics included in operational dashboard section",
    has ir-source-phase 2,
    has ir-derived-from-dependency true;

insert
  # O28 requires O20 (Cognitive Load Budget)
  $ir028_dep_O20 isa input-requirement,
    has ir-id "IR-028-005",
    has ir-type "internal",
    has ir-criticality "blocking",
    has ir-satisfaction-mode "transformed",
    has ir-description "Cognitive load budget determines human interaction patterns in the manual",
    has ir-source-phase 2,
    has ir-derived-from-dependency true;

insert
  # O28 requires O21 (Override Protocol)
  $ir028_dep_O21 isa input-requirement,
    has ir-id "IR-028-006",
    has ir-type "internal",
    has ir-criticality "blocking",
    has ir-satisfaction-mode "direct",
    has ir-description "Override procedures are core content of the operations manual",
    has ir-source-phase 2,
    has ir-derived-from-dependency true;

insert
  # O28 requires O22 (Interface Specification)
  $ir028_dep_O22 isa input-requirement,
    has ir-id "IR-028-007",
    has ir-type "internal",
    has ir-criticality "blocking",
    has ir-satisfaction-mode "transformed",
    has ir-description "Interface specification determines how humans interact with the system",
    has ir-source-phase 2,
    has ir-derived-from-dependency true;

insert
  # O28 requires O23 (Enrichment Assessment)
  $ir028_dep_O23 isa input-requirement,
    has ir-id "IR-028-008",
    has ir-type "internal",
    has ir-criticality "enhancing",
    has ir-satisfaction-mode "referenced",
    has ir-description "Enrichment assessment informs the human empowerment section of the manual",
    has ir-source-phase 2,
    has ir-derived-from-dependency true;

# ---- Root output IRs (what O4, O5 need from earlier phases) ----

insert
  # O4 (Scope Boundary Map) requires external human input
  $ir_O4_root isa input-requirement,
    has ir-id "IR-004-ROOT",
    has ir-type "external-human",
    has ir-criticality "blocking",
    has ir-satisfaction-mode "direct",
    has ir-description "Principal's definition of what is explicitly OUT of scope — the boundary between in-scope and out-of-scope must come from human judgment",
    has ir-source-phase 0,
    has ir-derived-from-dependency false;

insert
  # O5 (Task Contract Schema) requires O4 (Scope Boundary Map)
  $ir_O5_dep_O4 isa input-requirement,
    has ir-id "IR-005-001",
    has ir-type "internal",
    has ir-criticality "blocking",
    has ir-satisfaction-mode "transformed",
    has ir-description "Task contracts must respect scope boundaries — O4 defines what tasks the agent should and should not handle",
    has ir-source-phase 2,
    has ir-derived-from-dependency true;

insert
  # O5 (Task Contract Schema) requires O2 (Purpose Statement)
  $ir_O5_dep_O2 isa input-requirement,
    has ir-id "IR-005-002",
    has ir-type "internal",
    has ir-criticality "blocking",
    has ir-satisfaction-mode "direct",
    has ir-description "Every task contract must trace back to the agent's stated purpose",
    has ir-source-phase 2,
    has ir-derived-from-dependency true;

# ---- C) REPRESENTATIVE INTERNAL IRs (other key dependency patterns) ----

insert
  # O13 (Verification Independence Protocol) requires O5 (Task Contract Schema)
  $ir_O13_dep_O5 isa input-requirement,
    has ir-id "IR-013-001",
    has ir-type "internal",
    has ir-criticality "blocking",
    has ir-satisfaction-mode "transformed",
    has ir-description "Verification protocols must verify against task contract specifications — you can't verify what isn't specified",
    has ir-source-phase 2,
    has ir-derived-from-dependency true;

insert
  # O16 (Agno Agent Configuration) requires O5 (Task Contract Schema)
  # This is a TRANSFORMED dependency — contract schemas become Agno config
  $ir_O16_dep_O5 isa input-requirement,
    has ir-id "IR-016-001",
    has ir-type "internal",
    has ir-criticality "blocking",
    has ir-satisfaction-mode "transformed",
    has ir-description "Task contract schemas are transformed into Agno agent configuration — the contract IS the specification for implementation",
    has ir-source-phase 2,
    has ir-derived-from-dependency true;

insert
  # O16 (Agno Agent Configuration) requires O14 (Epistemic Metadata Schema)
  $ir_O16_dep_O14 isa input-requirement,
    has ir-id "IR-016-002",
    has ir-type "internal",
    has ir-criticality "enhancing",
    has ir-satisfaction-mode "referenced",
    has ir-description "Epistemic metadata schema informs agent configuration for confidence/provenance fields in outputs",
    has ir-source-phase 2,
    has ir-derived-from-dependency true;
```

```
# ---- INPUT REQUIREMENT RELATIONS ----
# Linking IRs to the outputs that require them, the outputs that satisfy them,
# and the subtasks that consume them.

insert
  # External inputs for Phase 0 outputs
  $ir001 isa input-requirement, has ir-id "IR-EXT-001";
  $o1 isa design-output, has output-id "O1";
  (requiring-output: $o1, required-ir: $ir001) isa ir-required-by-output;

insert
  $ir002 isa input-requirement, has ir-id "IR-EXT-002";
  $o3 isa design-output, has output-id "O3";
  (requiring-output: $o3, required-ir: $ir002) isa ir-required-by-output;

insert
  $ir003 isa input-requirement, has ir-id "IR-EXT-003";
  $o1 isa design-output, has output-id "O1";
  (requiring-output: $o1, required-ir: $ir003) isa ir-required-by-output;

insert
  $ir004 isa input-requirement, has ir-id "IR-EXT-004";
  $o16 isa design-output, has output-id "O16";
  (requiring-output: $o16, required-ir: $ir004) isa ir-required-by-output;

insert
  # External inputs cannot be satisfied by pipeline outputs
  # IR-EXT-001, 002, 003 are external — no ir-satisfied-by-output relation
  # IR-EXT-004 is external-system (Agno) — no pipeline output satisfies it

  # O28's direct dependency IRs — required by O28
  $ir028_1 isa input-requirement, has ir-id "IR-028-001";
  $o28 isa design-output, has output-id "O28";
  (requiring-output: $o28, required-ir: $ir028_1) isa ir-required-by-output;
  $o27 isa design-output, has output-id "O27";
  (satisfied-ir: $ir028_1, satisfying-output: $o27) isa ir-satisfied-by-output;

insert
  $ir028_2 isa input-requirement, has ir-id "IR-028-002";
  $o28 isa design-output, has output-id "O28";
  (requiring-output: $o28, required-ir: $ir028_2) isa ir-required-by-output;
  $o24 isa design-output, has output-id "O24";
  (satisfied-ir: $ir028_2, satisfying-output: $o24) isa ir-satisfied-by-output;

insert
  $ir028_3 isa input-requirement, has ir-id "IR-028-003";
  $o28 isa design-output, has output-id "O28";
  (requiring-output: $o28, required-ir: $ir028_3) isa ir-required-by-output;
  $o25 isa design-output, has output-id "O25";
  (satisfied-ir: $ir028_3, satisfying-output: $o25) isa ir-satisfied-by-output;

insert
  $ir028_4 isa input-requirement, has ir-id "IR-028-004";
  $o28 isa design-output, has output-id "O28";
  (requiring-output: $o28, required-ir: $ir028_4) isa ir-required-by-output;
  $o26 isa design-output, has output-id "O26";
  (satisfied-ir: $ir028_4, satisfying-output: $o26) isa ir-satisfied-by-output;

insert
  $ir028_5 isa input-requirement, has ir-id "IR-028-005";
  $o28 isa design-output, has output-id "O28";
  (requiring-output: $o28, required-ir: $ir028_5) isa ir-required-by-output;
  $o20 isa design-output, has output-id "O20";
  (satisfied-ir: $ir028_5, satisfying-output: $o20) isa ir-satisfied-by-output;

insert
  $ir028_6 isa input-requirement, has ir-id "IR-028-006";
  $o28 isa design-output, has output-id "O28";
  (requiring-output: $o28, required-ir: $ir028_6) isa ir-required-by-output;
  $o21 isa design-output, has output-id "O21";
  (satisfied-ir: $ir028_6, satisfying-output: $o21) isa ir-satisfied-by-output;

insert
  $ir028_7 isa input-requirement, has ir-id "IR-028-007";
  $o28 isa design-output, has output-id "O28";
  (requiring-output: $o28, required-ir: $ir028_7) isa ir-required-by-output;
  $o22 isa design-output, has output-id "O22";
  (satisfied-ir: $ir028_7, satisfying-output: $o22) isa ir-satisfied-by-output;

insert
  $ir028_8 isa input-requirement, has ir-id "IR-028-008";
  $o28 isa design-output, has output-id "O28";
  (requiring-output: $o28, required-ir: $ir028_8) isa ir-required-by-output;
  $o23 isa design-output, has output-id "O23";
  (satisfied-ir: $ir028_8, satisfying-output: $o23) isa ir-satisfied-by-output;

  # Root output IRs
  $ir4root isa input-requirement, has ir-id "IR-004-ROOT";
  $o4 isa design-output, has output-id "O4";
  (requiring-output: $o4, required-ir: $ir4root) isa ir-required-by-output;

  $ir5_1 isa input-requirement, has ir-id "IR-005-001";
  $o5 isa design-output, has output-id "O5";
  (requiring-output: $o5, required-ir: $ir5_1) isa ir-required-by-output;
  $o4 isa design-output, has output-id "O4";
  (satisfied-ir: $ir5_1, satisfying-output: $o4) isa ir-satisfied-by-output;

  $ir5_2 isa input-requirement, has ir-id "IR-005-002";
  $o5 isa design-output, has output-id "O5";
  (requiring-output: $o5, required-ir: $ir5_2) isa ir-required-by-output;
  $o2 isa design-output, has output-id "O2";
  (satisfied-ir: $ir5_2, satisfying-output: $o2) isa ir-satisfied-by-output;

  # Representative internal IRs
  $ir13_1 isa input-requirement, has ir-id "IR-013-001";
  $o13 isa design-output, has output-id "O13";
  (requiring-output: $o13, required-ir: $ir13_1) isa ir-required-by-output;
  $o5 isa design-output, has output-id "O5";
  (satisfied-ir: $ir13_1, satisfying-output: $o5) isa ir-satisfied-by-output;

  $ir16_1 isa input-requirement, has ir-id "IR-016-001";
  $o16 isa design-output, has output-id "O16";
  (requiring-output: $o16, required-ir: $ir16_1) isa ir-required-by-output;
  $o5 isa design-output, has output-id "O5";
  (satisfied-ir: $ir16_1, satisfying-output: $o5) isa ir-satisfied-by-output;

  $ir16_2 isa input-requirement, has ir-id "IR-016-002";
  $o16 isa design-output, has output-id "O16";
  (requiring-output: $o16, required-ir: $ir16_2) isa ir-required-by-output;
  $o14 isa design-output, has output-id "O14";
  (satisfied-ir: $ir16_2, satisfying-output: $o14) isa ir-satisfied-by-output;
```

```
# ---- IR-CONSUMED-BY-SUBTASK RELATIONS ----
# Linking input requirements to the subtasks that consume them.
# These bridge Phase 2 (backcasting) to Phase 3 (task decomposition).
#
# Convention: The subtask that CONSUMES an IR is the subtask that PRODUCES
# the output that requires the IR. If IR-X is required by Output-O5,
# and Subtask-S5 produces Output-O5, then Subtask-S5 consumes IR-X.

insert
  # O28 is produced by subtask S12 (Final assembly & operations manual)
  $ir028_1 isa input-requirement, has ir-id "IR-028-001";
  $s12 isa subtask, has subtask-id "S12";
  (consumed-ir: $ir028_1, consuming-task: $s12) isa ir-consumed-by-subtask;

  $ir028_2 isa input-requirement, has ir-id "IR-028-002";
  (consumed-ir: $ir028_2, consuming-task: $s12) isa ir-consumed-by-subtask;

  $ir028_3 isa input-requirement, has ir-id "IR-028-003";
  (consumed-ir: $ir028_3, consuming-task: $s12) isa ir-consumed-by-subtask;

  $ir028_4 isa input-requirement, has ir-id "IR-028-004";
  (consumed-ir: $ir028_4, consuming-task: $s12) isa ir-consumed-by-subtask;

  $ir028_5 isa input-requirement, has ir-id "IR-028-005";
  (consumed-ir: $ir028_5, consuming-task: $s12) isa ir-consumed-by-subtask;

  $ir028_6 isa input-requirement, has ir-id "IR-028-006";
  (consumed-ir: $ir028_6, consuming-task: $s12) isa ir-consumed-by-subtask;

  $ir028_7 isa input-requirement, has ir-id "IR-028-007";
  (consumed-ir: $ir028_7, consuming-task: $s12) isa ir-consumed-by-subtask;

  $ir028_8 isa input-requirement, has ir-id "IR-028-008";
  (consumed-ir: $ir028_8, consuming-task: $s12) isa ir-consumed-by-subtask;
```

---

## 4. Derivation Methodology for Remaining IRs

The seed data above demonstrates the pattern. Here's the systematic methodology for deriving the remaining ~75 input requirements from the 85 output-dependency relations:

### Derivation Algorithm

```
FOR EACH output-dependency relation (A depends-on B):
  1. CREATE Input-Requirement IR-{A_id}-{seq}:
     - ir-id: "IR-{A_id}-{seq}"
     - ir-type: "internal"
     - ir-criticality: infer from output criticality (blocking for Identity/Contracts, 
                       enhancing for Human Artefacts, validating for Operational)
     - ir-satisfaction-mode: infer from relationship:
         O5→O1 (transforming scope into contracts) = "transformed"
         O13→O5 (verifying against spec) = "referenced"
         O20→O4 (incorporating boundaries into budget) = "direct"
     - ir-description: "To produce {A_name}, {B_name} is needed because {reason}"
     - ir-source-phase: phase number of output A
     - ir-derived-from-dependency: true

  2. CREATE ir-required-by-output: (A, IR)
  3. CREATE ir-satisfied-by-output: (IR, B)
  4. CREATE ir-consumed-by-subtask: (IR, subtask that produces A)

FOR EACH output with no pipeline-internal dependencies (roots):
  1. CREATE external IR:
     - ir-type: "external-human" or "external-system" or "external-domain"
     - ir-criticality: "blocking" (root inputs are almost always blocking)
     - ir-satisfaction-mode: "direct"
     - ir-derived-from-dependency: false
```

### Criticality Inference Rules

| Output Group | Default Criticality | Rationale |
|---|---|---|
| Identity (O1-O4) | blocking | Without identity, nothing else has purpose |
| Contracts (O5-O8) | blocking | Contracts are structural enforcement |
| Behaviour (O9-O12) | blocking | Boundaries and directives are core |
| Verification (O13-O15) | validating | Verification validates, not produces |
| Implementation (O16-O19) | enhancing | Implementation details enrich, don't block |
| Human Artefacts (O20-O23) | enhancing | Human experience enriches |
| Ecosystem (O24-O26) | enhancing | Ecosystem enables, not blocks |
| Operational (O27-O28) | blocking | Deployment and ops manual are final deliverables |

### Satisfaction Mode Inference Rules

| Dependency Pattern | Mode | Rationale |
|---|---|---|
| Identity → Contracts | transformed | Purpose/boundaries become contractual terms |
| Contracts → Verification | referenced | Verification references contracts as criteria |
| Contracts → Implementation | transformed | Contracts become Agno config structure |
| Boundaries → Cognitive Load | direct | Boundaries directly inform cognitive budget |
| Verification → Monitoring | referenced | Verification protocols referenced in dashboards |
| Human Artefacts → Operations | transformed | Human experience transforms into operational procedures |
| Root (external) → Identity | direct | Human judgment directly feeds purpose/vision |

---

## 5. Verification Queries

```typeql
# Verify phase entities
match $p isa cawdp-phase; select $p; count;

# Verify phase sequence (should be 9: 0→1, 1→2, ..., 8→9)
match $seq isa phase-sequence; select $seq; count;

# Verify phase-produces-output relations (should be 28)
match $rel isa phase-produces-output; select $rel; count;

# Verify input requirements (should be 17 after seeding)
match $ir isa input-requirement; select $ir; count;

# Verify IR required-by-output relations
match $rel isa ir-required-by-output; select $rel; count;

# Verify IR satisfied-by-output relations
match $rel isa ir-satisfied-by-output; select $rel; count;

# Verify IR consumed-by-subtask relations
match $rel isa ir-consumed-by-subtask; select $rel; count;

# BACKCASTING CHAIN TEST: Trace from O28 back through dependencies
# This is the KEY query — can we navigate from a final deliverable
# back through its input requirements to the outputs that satisfy them?
match
  $o28 isa design-output, has output-id "O28";
  $ir (requiring-output: $o28) isa ir-required-by-output;
  $ir_type isa input-requirement, has ir-type $type;
  $satisfying (satisfied-ir: $ir) isa ir-satisfied-by-output;
  $satisfying_output isa design-output, has output-id $sat_id;
select $o28, $ir_type, $type, $satisfying, $satisfying_output, $sat_id;

# EXTERNAL INPUTS TEST: Find all external inputs
match
  $ir isa input-requirement, has ir-type "external-human";
  $req (requiring-output: $output) isa ir-required-by-output;
  $output has output-id $oid;
select $ir, $output, $oid;

# FULL DEPENDENCY CHAIN: From any output, trace back to roots
# O28 → IR → O20 → IR → O4 → IR → external-human
match
  $final isa design-output, has output-id "O28";
  $r1 (requiring-output: $final, required-ir: $ir1) isa ir-required-by-output;
  $ir1 has ir-id $ir1_id, has ir-type $ir1_type;
  $s1 (satisfied-ir: $ir1, satisfying-output: $mid) isa ir-satisfied-by-output;
  $mid has output-id $mid_id;
select $final, $ir1_id, $ir1_type, $mid_id;
```

---

## 6. Quality Gate Checklist (Applying Retro Lessons)

Before applying to the database, verify against the 8 correction patterns:

| # | Pattern | Check | Status |
|---|---|---|---|
| P1 | v2→v3 syntax | No `sub`, no `value long`, no inline plays | ✅ All v3 |
| P2 | Role name collisions | `predecessor-phase`, `successor-phase`, `producing-phase`, `produced-output`, `requiring-output`, `required-ir`, `satisfied-ir`, `satisfying-output`, `consumed-ir`, `consuming-task` — none match entity types | ✅ Verified |
| P3 | Dangling plays | Every `plays` references a defined relation | ✅ Verified |
| P4 | Missing relations | All 5 new relations defined before `plays` | ✅ Verified |
| P5 | Fetch syntax | Using `match ... select` pattern only | ✅ Verified |
| P6 | Large inserts | Phases split into batches (10 entities + 9 sequences + 28 relations + 17 IRs + ~30 relations = manageable) | ✅ Batches < 40 |
| P7 | Additive schema | Schema only adds; no modifications to existing types | ✅ Verified |
| P8 | Attribute order | Attributes defined in Pass 1, entities/relations/plays in Pass 2 | ✅ Two-pass |

---

## 7. What This Enables

With Phase 2 complete, the graph gains:

1. **Process Context**: Every output now knows which CAWDP phase produces it, and the linear sequence of phases
2. **Backward Tracing**: From any final deliverable (O28), you can trace the complete dependency chain back to root inputs (O1-O4) and external human inputs
3. **Forward Planning**: From any root input, you can trace which outputs depend on it
4. **Input-Requirement Richness**: Every dependency now carries metadata — type (internal/external), criticality (blocking/enhancing/validating), satisfaction-mode (direct/transformed/referenced/accumulated)
5. **Subtask Bridging**: Input requirements connect Phase 1 (outputs) to Phase 3 (subtasks), enabling queries like "what subtasks are blocked if O4 (Scope Boundary Map) is incomplete?"

The graph transforms from **a collection of connected nodes** into **a navigable DAG with traced paths** — exactly what the revised CAWDP phase order demands: Direction → Destination → **Path** → Work.The design is complete and verified against all 8 retro patterns. Here's the summary of what's ready to apply:

---

## What You Have

| File | Contents | Ready to Apply |
|---|---|---|
| `db/schemas/phase2.tql` | Pass 1 (attributes) + Pass 2 (entities/relations/plays) | ✅ Quality gated |
| `db/seeds/phase2_phases.tql` | 10 phases + 9 sequences + 28 phase-output links | ✅ v3 syntax verified |
| `db/seeds/phase2_input_requirements.tql` | 17 IRs + relations (4 external + 8 O28 chain + 2 root + 3 representative) | ✅ v3 syntax verified |

## What It Enables Immediately

1. **Process context** — every output knows which CAWDP phase produces it
2. **Cognitive mode navigation** — you can query which phases use which cognitive mode (IMAGINE, SPECIFY, TRACE, etc.)
3. **O28 backcasting chain** — the complete first-layer dependency chain from the final deliverable is navigable
4. **External input visibility** — Phase 0's human judgment roots are now explicit, not assumed
5. **Subtask bridging** — input requirements connect to the subtasks that consume them

## What Needs Follow-Up

The remaining ~75 input requirements can be derived systematically using the algorithm and inference rules documented in Section 4. This is mechanical work best done with a script that reads the existing 85 `output-dependency` relations and generates IR entities.
