# TypeDB Schema — Phase 6: System Architecture

```typeql
define

# ─── PHASE 6: SYSTEM ARCHITECTURE ───

# ── PIPELINE ARCHITECTURE ──

pipeline-stage sub entity,
    owns stage-id,                # "S1" through "S9"
    owns stage-name,
    owns stage-description,
    owns stage-ordinal,           # Execution order
    owns stage-gate-ref,          # Quality gate ID
    owns stage-entry-event,       # What event allows entry
    owns stage-exit-event,        # What event marks completion
    owns stage-parallel,          # boolean — can this stage run alongside others?
    plays stage-contains-subtask,
    plays stage-precedes-stage,
    plays stage-follows-stage;

stage-contains sub relation,
    relates stage-containing,
    relates stage-contained-subtask;

stage-sequence sub relation,
    relates preceding-stage,
    relates succeeding-stage;

# ── ORCHESTRATION ──

orchestration-config sub entity,
    owns oc-id,
    owns oc-composition-type,     # "workflow" | "team" | "single_agent"
    owns oc-orchestration-pattern,# "sequential" | "parallel" | "conditional" | "loop"
    owns oc-session-model,        # "persistent" | "ephemeral" | "session-linked"
    owns oc-state-sharing,        # "session_state" | "shared_db" | "event_stream"
    owns oc-fallback-tier-limit,  # Max fallback depth before halt
    plays oc-defines-orchestration;

orchestration-decision sub entity,
    owns od-id,
    owns od-question,
    owns od-chosen,
    owns od-reason,
    owns od-alternatives,        # JSON: alternatives not chosen with reasons
    plays od-for-orchestration;

orchestration-has-decision sub relation,
    relates od-orchestration,
    relates orchestration-decision;

# ── FMEA ──

fmea-entry sub entity,
    owns fmea-id,
    owns fmea-subtask-ref,
    owns fmea-failure-ref,        # Links to failure-mode from Phase 3
    owns fmea-event-ref,          # Links to failure event from Phase 5
    owns fmea-effect,             # What happens downstream
    owns fmea-severity,           # 1-10 (10 = catastrophic)
    owns fmea-occurrence,         # 1-10 (10 = certain)
    owns fmea-detection,          # 1-10 (10 = undetectable)
    owns fmea-rpn,                # Risk Priority Number = S × O × D
    owns fmea-mitigation,         # What reduces the risk
    owns fmea-mitigation-type,    # "preventive" | "detective" | "corrective"
    owns fmea-residual-rpn,       # RPN after mitigation
    plays fmea-for-subtask;

# ── TEMPLATE ARCHITECTURE ──

template-type sub entity,
    owns tt-id,
    owns tt-name,                 # "input" | "output" | "handoff" | "verification" | "decision" | "feedback" | "escalation"
    owns tt-description,
    owns tt-schema-ref,           # Links to schema_registry entry
    owns tt-usage-count,          # How many subtasks use this template type
    plays tt-instances;

template-instance sub entity,
    owns ti-id,
    owns ti-template-type-ref,
    owns ti-subtask-ref,
    owns ti-specialisation,       # What makes this instance specific to its subtask
    owns ti-schema,               # The specialised schema
    plays ti-of-type,
    plays ti-for-subtask;

template-has-instance sub relation,
    relates tt-type,
    relates template-instance;

# ── COMPOSITION ──

composition-config sub entity,
    owns cc-id,
    owns cc-type,                 # "workflow" | "team" | "single_agent"
    owns cc-justification,
    owns cc-agno-mapping,         # How this maps to Agno constructs
    owns cc-steps,                # JSON: ordered step definitions
    owns cc-step-choices,         # JSON: conditional routing logic
    owns cc-session-config,       # Agno session configuration
    plays cc-defines-composition;

# ── FALLBACK MODEL ──

fallback-tier sub entity,
    owns ft-id,
    owns ft-tier,                 # 1, 2, 3, 4
    owns ft-name,                 # "retry_same_agent" | "retry_restricted" | "escalate_human" | "halt"
    owns ft-trigger,              # What condition activates this tier
    owns ft-action,
    owns ft-max-attempts,
    owns ft-preserve-state,       # boolean — does this tier keep artefact graph state?
    plays ft-for-subtask;

subtask-has-fallback sub relation,
    relates fallback-subtask,
    relates fallback-tier;

# Attribute types
stage-id sub attribute, value string;
stage-name sub attribute, value string;
stage-description sub attribute, value string;
stage-ordinal sub attribute, value long;
stage-gate-ref sub attribute, value string;
stage-entry-event sub attribute, value string;
stage-exit-event sub attribute, value string;
stage-parallel sub attribute, value boolean;
oc-id sub attribute, value string;
oc-composition-type sub attribute, value string;
oc-orchestration-pattern sub attribute, value string;
oc-session-model sub attribute, value string;
oc-state-sharing sub attribute, value string;
oc-fallback-tier-limit sub attribute, value long;
od-id sub attribute, value string;
od-question sub attribute, value string;
od-chosen sub attribute, value string;
od-reason sub attribute, value string;
od-alternatives sub attribute, value string;
fmea-id sub attribute, value string;
fmea-subtask-ref sub attribute, value string;
fmea-failure-ref sub attribute, value string;
fmea-event-ref sub attribute, value string;
fmea-effect sub attribute, value string;
fmea-severity sub attribute, value long;
fmea-occurrence sub attribute, value long;
fmea-detection sub attribute, value long;
fmea-rpn sub attribute, value long;
fmea-mitigation sub attribute, value string;
fmea-mitigation-type sub attribute, value string;
fmea-residual-rpn sub attribute, value long;
tt-id sub attribute, value string;
tt-name sub attribute, value string;
tt-description sub attribute, value string;
tt-schema-ref sub attribute, value string;
tt-usage-count sub attribute, value long;
ti-id sub attribute, value string;
ti-template-type-ref sub attribute, value string;
ti-subtask-ref sub attribute, value string;
ti-specialisation sub attribute, value string;
ti-schema sub attribute, value string;
cc-id sub attribute, value string;
cc-type sub attribute, value string;
cc-justification sub attribute, value string;
cc-agno-mapping sub attribute, value string;
cc-steps sub attribute, value string;
cc-step-choices sub attribute, value string;
cc-session-config sub attribute, value string;
ft-id sub attribute, value string;
ft-tier sub attribute, value long;
ft-name sub attribute, value string;
ft-trigger sub attribute, value string;
ft-action sub attribute, value string;
ft-max-attempts sub attribute, value long;
ft-preserve-state sub attribute, value string;
```

---

## Pipeline Architecture — 9 Stages, 9 Waves

Each stage is a gated checkpoint. You don't proceed until the quality gate passes. Stages 4-7 run partially in parallel where dependencies allow.

| Stage | Name | Subtasks | Entry Event | Exit Event | Gate | Parallel? |
|-------|------|----------|-------------|------------|------|-----------|
| S1 | Purpose | T1.1, T1.2 | E1 `session_started` | E3 `authority_class_selected` | G1 | No |
| S2 | Scope | T1.3, T8.1 | E3 | E4 `scope_boundary_drawn` | G2 | Yes (T1.3 ∥ T8.1) |
| S3 | Specification | T1.4, T1.5, T3.1 | E4, E5 | E6 `contract_architecture_approved` | G3 | Yes (T1.4 ∥ T3.1 after E5) |
| S4 | Templating | T2.1, T4.2, T8.2 | E6 | E8 `template_cascade_complete` | G4 | Yes (T2.1 ∥ T4.2 ∥ T8.2) |
| S5 | Validation | T2.2, T3.2, T4.1, T8.3, T8.4 | E8 | E9 `templates_validated` | G5 | Yes (all five parallel) |
| S6 | Generation | T5.1, T5.2, T6.1, T6.2, T6.3, T8.5 | E9 | E13 `code_generation_complete` | G6 | Yes (T5.1→T5.2 seq; T6.x ∥ T8.5) |
| S7 | Integration | T5.3, T7.1, T7.2 | E13 | E15 `integration_passed` | G7 | Yes (T5.3 first, then T7.x) |
| S8 | Completion | — | E15 | E16 `agent_design_complete` | G8 | No |
| S9 | Monitoring | F12, F13, F14 | E16 | Ongoing | G9 | Continuous |

---

## Quality Gates — Executable Assertions

Each gate queries the artefact graph. Transition happens when ALL assertions pass, not when the user clicks "Next."

### G1: Purpose Gate (S1 → S2)

```
ASSERT purpose_statement EXISTS AND length > 20
ASSERT anti_goals COUNT >= 1
ASSERT authority_class IN {extractor, measurer, assessor, generator, aggregator}
ASSERT authority_class VALIDATED_AGAINST 5-class_taxonomy_definitions
ASSERT principal_declared EXISTS
```

### G2: Scope Gate (S2 → S3)

```
ASSERT inside_scope COUNT >= 1
ASSERT outside_scope COUNT >= 1
ASSERT escalation_triggers COUNT >= 1
ASSERT tool_audit_complete EXISTS
ASSERT no_tool_grants_access_beyond_scope
```

### G3: Specification Gate (S3 → S4)

```
ASSERT job_description "Agno dev can implement" = TRUE
ASSERT contract_architecture EXISTS
ASSERT enforcement_regime IN {declare, detect, prevent}
ASSERT ALL guards HAVE assertion_schema
ASSERT personality_purpose_link EXISTS
```

### G4: Templating Gate (S4 → S5)

```
ASSERT template_cascade_count = 8
ASSERT cross_template_consistency_check = PASS
ASSERT aging_schedule EXISTS
ASSERT context_protocol_design EXISTS
ASSERT context_budget_kb > 0
```

### G5: Validation Gate (S5 → S6)

```
ASSERT template_validation_pass = TRUE
ASSERT trust_ledger_3_axis_queryable = TRUE
ASSERT autonomy_plan_thresholds QUANTITATIVE
ASSERT kb_scope CONTAINED_IN agent_scope
ASSERT memory_retention_policy EXISTS
ASSERT memory_human_deletable = TRUE
```

### G6: Generation Gate (S6 → S7)

```
ASSERT agent_code_schema_compliance = PASS
ASSERT test_suite_coverage_pct >= 80
ASSERT boundary_map_5min_readable = TRUE
ASSERT ops_manual_insurer_readable = TRUE
ASSERT decision_log_why_field_populated = TRUE
ASSERT all_outputs_schema_validated = TRUE
```

### G7: Integration Gate (S7 → S8)

```
ASSERT integration_test_pass = TRUE
ASSERT edge_cases RESOLVED
ASSERT human_sign_off EXISTS
ASSERT pattern_identification COMPLETE
ASSERT curriculum_module_teachable = TRUE
```

### G8: Completion Gate (S8 → S9)

```
ASSERT output_count = 28
ASSERT ALL outputs HAVE epistemic_metadata
ASSERT ALL outputs HAVE provenance
ASSERT artefact_graph_navigable = TRUE
ASSERT design_to_code_traceable = TRUE
```

### G9: Monitoring Gate (S9, continuous)

```
ASSERT spec_aging_check LAST_RUN < refresh_cadence_days
ASSERT memory_entries ALL WITHIN retention_policy
ASSERT override_rate < boundary_drift_threshold
```

---

## Orchestration — 5 Key Decisions

| OD | Question | Chosen | Reason | Rejected Alternatives |
|----|----------|--------|--------|----------------------|
| OD1 | Composition type? | **Workflow** | Stages are sequential and gated; subtasks within stages can parallelise; state flows forward through defined outputs | Team (no persistent roles — agents specialise per subtask, not per stage); Single agent (too many subtasks for one context window) |
| OD2 | Orchestration pattern? | **Sequential with conditional parallelism** | Stages run sequentially (gate dependencies); subtasks within stages parallelise where Phase 4 dependencies allow | Pure sequential (wastes parallelism opportunity); Event-driven (over-engineered for 9 stages) |
| OD3 | Session model? | **Persistent, session-linked** | Agent design spans hours/days; artefact graph must persist between sessions; user returns to continue where they left off | Ephemeral (loses context); Single-session (unrealistic for non-trivial agents) |
| OD4 | State sharing? | **Session state + shared TypeDB** | Session state for orchestration metadata (current stage, active subtasks); TypeDB for artefact graph (the real state); session metadata holds fragment IDs, TypeDB holds fragments | Session state only (can't query artefact graph); Event stream only (no direct query) |
| OD5 | Fallback depth? | **3 tiers max** | Tier 1 (retry), Tier 2 (restricted retry), Tier 3 (escalate human). Tier 4 (halt) is emergency only. Prevents infinite fallback loops | Unlimited (dangerous); 1 tier only (too aggressive) |

---

## Agno Mapping — Concrete Implementation

```python
from agno.workflow import Workflow
from agno.session import Session
from agno.models.ollama import Ollama
from agno.agent import Agent
from agno.storage.postgres import PostgresDb

# ── Model ──
model = Ollama(id="glm-5.1:cloud")

# ── Storage ──
storage = PostgresDb(table_name="agent_design_sessions", db_url=DB_URL)

# ── Workflow ──
class AgentDesignWorkflow(Workflow):
    name: str = "agent-design-workflow"
    
    # Stages map to workflow steps
    # Session state tracks: current_stage, completed_subtasks[], artefact_ids[]
    # TypeDB stores: all artefacts as typed PRISM entities
    
    # Step 1: S1 Purpose
    #   - Vision Mirror agent (human-primary, agent reflects)
    #   - Authority Validator agent (collaborative, 5-class check)
    #   - Gate: G1 assertions query TypeDB
    
    # Step 2: S2 Scope  
    #   - Scope Boundary agent (human-primary, agent stress-tests)
    #   - Tool Auditor agent (collaborative)
    #   - step_choices: after G2, route to S3
    #   - Gate: G2 assertions
    
    # Step 3: S3 Specification
    #   - Job Drafter agent (agent-primary, human approves)
    #   - Contract Architect agent (collaborative)
    #   - Profile Designer agent (collaborative)
    #   - Gate: G3 assertions
    
    # Step 4: S4 Templating
    #   - Template Cascade agent (agent-primary, generates 8 templates)
    #   - Aging Designer agent (collaborative)
    #   - Context Protocol agent (agent-primary)
    #   - Gate: G4 assertions
    
    # Step 5: S5 Validation
    #   - Template Validator agent (collaborative)
    #   - Trust Ledger agent (agent-primary)
    #   - Autonomy Planner agent (collaborative)
    #   - KB Spec agent (collaborative)
    #   - Memory Architect agent (collaborative)
    #   - Gate: G5 assertions
    
    # Step 6: S6 Generation
    #   - Code Generator agent (agent-primary)
    #   - Test Generator agent (agent-primary)
    #   - Artefact Renderer (system — no agent, just TypeDB queries → views)
    #   - Gate: G6 assertions
    
    # Step 7: S7 Integration
    #   - Integration Validator agent (collaborative)
    #   - Pattern Spotter agent (agent-primary)
    #   - Curriculum Drafter agent (collaborative)
    #   - Gate: G7 assertions
    
    # Step 8: S8 Completion
    #   - System assembles final artefact graph
    #   - Gate: G8 assertions
    
    # Step 9: S9 Monitoring (post-completion)
    #   - Specification Aging monitor (system-enforced)
    #   - Memory Governance monitor (system-enforced)  
    #   - Boundary Drift monitor (system-enforced)
    #   - Gate: G9 (continuous)
    
    def run(self, session_id: str):
        session = self.get_session(session_id)
        current_stage = session.metadata.get("current_stage", "S1")
        
        # Stage routing — resumes from wherever the user left off
        stage_map = {
            "S1": self.stage_purpose,
            "S2": self.stage_scope,
            "S3": self.stage_specification,
            "S4": self.stage_templating,
            "S5": self.stage_validation,
            "S6": self.stage_generation,
            "S7": self.stage_integration,
            "S8": self.stage_completion,
        }
        
        while current_stage in stage_map:
            next_stage = stage_map[current_stage](session)
            if next_stage is None:
                break  # Halt or escalate
            current_stage = next_stage
        
        # S9 monitoring starts after S8
        self.start_monitors(session)
```

---

## FMEA — Risk Priority Numbers

Severity × Occurrence × Detection = RPN. Scale 1-10 each. Max RPN = 1000. **Mitigation target: residual RPN < 100 for all entries.**

| FMEA | Subtask | Failure | Effect | S | O | D | RPN | Mitigation | Type | Residual |
|------|---------|---------|--------|---|---|---|-----|-----------|------|----------|
| FE1 | T1.1 | Purpose unclear — human can't articulate | Blocks all downstream; user abandons | 8 | 6 | 4 | **192** | Vision Mirror reflects back; "what if you had an agent that…" prompts | Preventive | 48 |
| FE2 | T1.1 | Multiple purposes tangled | Authority class ambiguous; contract covers wrong scope | 9 | 4 | 5 | **180** | Anti-goals field enforced; single-purpose check at G1 | Preventive | 36 |
| FE3 | T1.2 | Authority class mismatch | **KR9 cascade**: wrong class → wrong contract → wrong code → wrong agent | 10 | 3 | 2 | **60** | ST1 system gate + 5-class taxonomy check at G1 | Preventive | 15 |
| FE4 | T1.3 | Scope bloat | Agent tries to do too much; hallucination surface expands | 7 | 5 | 3 | **105** | Outside_scope mandatory at G2; stress test each inside item | Preventive | 35 |
| FE5 | T1.3 | Scope void | Agent can't do anything meaningful | 8 | 2 | 4 | **64** | G2 requires inside_scope ≥ 1; escalate if scope too narrow | Detective | 16 |
| FE6 | T1.5 | Contract untestable | Enforcement is decorative; guard exists but can't verify | 9 | 3 | 3 | **81** | ST3 system gate: every guard must have assertion_schema | Preventive | 18 |
| FE7 | T2.1 | Template inconsistency | Downstream code conflicts between templates | 6 | 4 | 2 | **48** | Cross-template consistency check at G4 | Detective | 12 |
| FE8 | T3.1 | Personality-purpose mismatch | User distrusts agent tone; e.g., Genial Assessor | 5 | 5 | 5 | **125** | Personality-purpose link mandatory at G3 | Detective | 25 |
| FE9 | T5.1 | Schema validation failure | Generated code won't run | 7 | 3 | 1 | **21** | ST5 system gate: schema_registry validation | Preventive | 7 |
| FE10 | T5.3 | Integration test failure | Agent doesn't work end-to-end | 8 | 3 | 2 | **48** | FMEA-driven test design covers edge cases | Preventive | 16 |
| FE11 | T8.2 | Context budget exceeded | Hallucination risk; cost overrun | 8 | 4 | 2 | **64** | ST7 hard ceiling enforced by system | Preventive | 16 |
| FE12 | — | Stale specification | Agent operates on outdated design | 6 | 7 | 3 | **126** | ST9 aging trigger + human review queue | Detective | 42 |
| FE13 | — | Memory governance breach | Silent assumption accumulation | 8 | 3 | 2 | **48** | ST8 retention enforcement + purge | Corrective | 12 |
| FE14 | — | Boundary drift | Agent exceeding authority | 7 | 5 | 3 | **105** | ST10 override rate monitor + autonomy review | Detective | 35 |

### FMEA Summary

| Category | Pre-Mitigation RPN > 100 | Post-Mitigation RPN > 100 | Max Residual |
|----------|--------------------------|---------------------------|-------------|
| Foundation (FE1-FE5) | 4 of 5 | **0** | 48 |
| Architecture (FE6-FE8) | 1 of 3 | **0** | 25 |
| Implementation (FE9-FE11) | 0 of 3 | **0** | 16 |
| Governance (FE12-FE14) | 2 of 3 | **0** | 42 |

**All residual RPNs < 100.** The system-enforced triggers (ST1-ST10) are the primary risk reduction mechanism — they convert high-detection-difficulty failures into low-detection-difficulty by making the system detect instead of relying on human or agent attention.

**Highest residual risk: FE12 (stale specification, RPN 42).** Specification aging is inherently ongoing and can't be fully prevented — only detected. This validates CC-5 as a continuous concern, not a one-time check.

---

## Template Architecture — 7 Types, 12 Instances

| Template Type | Description | Instances | Used By |
|---------------|-------------|-----------|---------|
| **Input** | Standardised input schema for a subtask | TI-01: Purpose Input (human), TI-02: Scope Input (human), TI-03: Authority Class Input (human) | T1.1, T1.3, T1.2 |
| **Output** | Standardised output schema (the 28 design outputs) | TI-04: Agent Identity Card (O1), TI-05: Job Description (O3), TI-06: Contract Schema (O5), TI-07: Boundary Map View (O19), TI-08: Ops Manual View (O20) | T1.1-T1.4, T1.5, T6.1, T6.2 |
| **Handoff** | Interface contract between subtasks or stages | TI-09: Stage Handoff (purpose → scope), TI-10: Subtask Handoff (job desc → contract) | All stage transitions, T1.4→T1.5 |
| **Verification** | Quality gate assertion template | TI-11: Gate Assertion (parameterised per gate G1-G9) | All quality gates |
| **Decision** | Decision capture template with "why" field | TI-12: Decision Record (decision, options, chosen, reasoning, authority) | DA1-DA10, T6.3 |
| **Feedback** | User feedback capture for progressive autonomy | — (deferred to Phase 8) | — |
| **Escalation** | Escalation protocol template | — (deferred to Phase 8; system triggers ST1-ST10 handle most escalations structurally) | — |

**5 of 7 types instantiated now.** Feedback and Escalation templates are deferred to Phase 8 (Human Experience Design) because they depend on interface specifications not yet designed.

---

## Composition — Workflow Validated

| Factor | Workflow ✅ | Team ❌ | Single Agent ❌ |
|--------|-----------|---------|----------------|
| Subtask count | 22 subtasks — too many for one agent; workflow stages them naturally | Agents don't have persistent roles — specialisation is per-subtask, not per-agent | Context window overflow guaranteed |
| Gating | Quality gates between stages = sequential step flow with conditional parallelism | No native gate mechanism; would need custom orchestration | No gate mechanism |
| State | Artefact graph in TypeDB + session metadata = natural session-linked model | Team session model designed for conversation, not staged production | Single session can't persist across days |
| Parallelism | Subtasks within stages parallelise naturally (T1.3 ∥ T8.1, T4.1 ∥ T4.2 ∥ T8.2) | Team parallelism is conversational, not production | No parallelism |
| Resumption | User returns to same stage after break | Team conversations don't resume gracefully | Single conversation context degrades |

**Decision: Workflow.** The Agno `Workflow` construct with `step_choices` for conditional routing and `Session` for persistence is the correct composition.

---

## Fallback Model — 4 Tiers

### Tier 1: Retry Same Agent (Same Inputs + Constraint)

| Subtask | Trigger | Constraint Added | Max Attempts |
|---------|---------|-----------------|-------------|
| T1.1 | Purpose unclear | Add reflection prompt, "what if you had…" | 3 |
| T2.1 | Template inconsistency | Add cross-template consistency constraint | 3 |
| T5.1 | Schema validation failure | Add schema_registry schema as strict constraint | 3 |
| T5.2 | Test coverage < 80% | Add FMEA failure scenarios as required test cases | 3 |

### Tier 2: Retry Restricted (Reduced Scope + Stricter Guard)

| Subtask | Trigger | Restriction | Max Attempts |
|---------|---------|-------------|-------------|
| T1.2 | Class still ambiguous | Restrict to 2 most likely classes; human picks | 2 |
| T2.2 | Validation ambiguous | Restrict to structural checks only; defer semantic | 2 |
| T5.3 | Integration failure | Restrict to critical path only; defer edge cases | 2 |
| T8.2 | Context budget exceeded | Reduce budget by 30%; simplify protocol | 2 |

### Tier 3: Escalate Human

| Subtask | Trigger | What Human Decides | Max Attempts |
|---------|---------|-------------------|-------------|
| T1.1 (after Tier 1) | Purpose still unclear after 3 attempts | Whether to continue, reframe, or abandon | 1 |
| T1.3 | Scope void — is agent needed? | Whether agent is the right solution | 1 |
| T1.5 | Contract regime disagreement | Which enforcement regime (declare/detect/prevent) | 1 |
| T3.1 | Personality can't be resolved | Override personality-purpose link with explicit decision | 1 |
| T5.3 (after Tier 2) | Critical path still failing | Whether to redesign or halt | 1 |
| T8.4 | Memory policy deadlock | Set retention policy manually | 1 |

### Tier 4: Halt

| Trigger | Action | State Preserved |
|---------|--------|----------------|
| Tier 3 human says "halt" | Stop pipeline. Preserve artefact graph. Log halt event. | All artefacts saved in TypeDB. Session can resume at this stage later. |
| Memory governance breach (F13) | Halt + purge to policy. | Policy-violating entries purged. All others preserved. |
| Context budget hard ceiling exceeded (ST7) on 2nd Tier 1 attempt | Halt + flag for redesign. | Context protocol artefact preserved for diagnosis. |
| Any 3 Tier 3 escalations in same stage | System halts stage. | Full artefact graph. System suggests design may need restructuring. |

**State preservation on halt:** Every halt preserves the artefact graph. No work is lost. The user can resume from the halted stage after resolving the blocking condition. This is the accretive model applied to failure — nothing is deleted, everything can be revisited.

---

## The Key Finding from System Architecture

**System-enforced quality gates are the primary risk reduction mechanism.** The FMEA shows that preventive system gates (ST1-ST10) reduce RPNs by 60-75% across all failure modes. Without them, 7 of 14 failures have RPN > 100. With them, **0 of 14** have residual RPN > 100.

**The gates replace trust in agents with trust in the system.** This is the enforcement regime inversion: the agent doesn't need to be trusted to correctly classify authority (ST1 catches it). The agent doesn't need to be trusted to stay within scope (ST2 catches it). The agent doesn't need to be trusted to produce valid schemas (ST5 catches it). **Trust shifts from the agent to the system — exactly as the quasi-smart contract model predicts.**

**5 of 7 template types are instantiated now.** The remaining 2 (Feedback, Escalation) depend on Phase 8 (Human Experience) interface design. This is the right dependency — you design the interface before you design how users give feedback through it.

---
