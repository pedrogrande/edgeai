# TypeDB Schema — Phase 4: Capability Allocation

```typeql
define

# ─── PHASE 4: CAPABILITY ALLOCATION ───

allocation sub entity,
    owns alloc-id,
    owns subtask-ref,             # Links to subtask-id
    owns judgment-demand,         # 0-10: How much human judgment
    owns pattern-capacity,        # 0-10: How well agent handles this
    owns determinism-fit,         # 0-10: Can System handle mechanically
    owns complementarity-gap,     # judgment-demand - pattern-capacity
    owns primary-actor,           # "human" | "agent" | "system"
    owns allocation-mode,         # "human_primary" | "agent_primary" | "system_primary" | "collaborative"
    owns human-role,              # What human does specifically
    owns agent-role,              # What agent does specifically
    owns system-role,             # What system does specifically
    owns reversibility,           # "high" | "medium" | "low"
    owns confidence-class,        # "high" | "medium" | "low"
    owns cr-class,                # C×R quadrant assignment
    plays alloc-for-subtask;

# Who decides what — the key question
decision-authority sub entity,
    owns da-id,
    owns da-description,          # The specific decision point
    owns da-authority,            # "human_only" | "human_decides_agent_prepares" | "agent_decides_human_verifies" | "system_enforces"
    owns da-trigger,              # When this decision is needed
    owns da-escalation,           # What happens if wrong decision
    plays authority-in-subtask;

subtask-has-allocation sub relation,
    relates allocated-subtask,
    relates allocation;

subtask-has-authority sub relation,
    relates authority-holding-subtask,
    relates decision-authority;

# Attribute types
alloc-id sub attribute, value string;
subtask-ref sub attribute, value string;
judgment-demand sub attribute, value long;
pattern-capacity sub attribute, value long;
determinism-fit sub attribute, value long;
complementarity-gap sub attribute, value long;
primary-actor sub attribute, value string;
allocation-mode sub attribute, value string;
human-role sub attribute, value string;
agent-role sub attribute, value string;
system-role sub attribute, value string;
reversibility sub attribute, value string;
confidence-class sub attribute, value string;
cr-class sub attribute, value string;
da-id sub attribute, value string;
da-description sub attribute, value string;
da-authority sub attribute, value string;
da-trigger sub attribute, value string;
da-escalation sub attribute, value string;
```

---

## Complementarity Matrix — All 22 Subtasks

Scored 0-10. Gap = Judgment Demand − Pattern Capacity. **Gap ≥ 6 → Human-primary.** System assigned when Determinism Fit ≥ 8.

### SG1: Identity

| ID | Subtask | J | P | D | Gap | Revers | Conf | C×R | Mode | Human | Agent | System |
|----|---------|---|---|---|-----|--------|------|-----|------|-------|-------|--------|
| T1.1 | Purpose Discovery | 9 | 2 | 0 | **+7** | Low | Low | ⚠️ Low/Low | **human_primary** | Articulates purpose, names anti-goals | Reflects words back, surfaces tensions | — |
| T1.2 | Authority Class Validation | 8 | 4 | 2 | +4 | Low | Med | ⚠️ Med/Low | **collaborative** | Decides class from 5 options | Presents taxonomy with evidence for each | Validates classification is complete |
| T1.3 | Scope Boundary Workshop | 9 | 3 | 1 | **+6** | Med | Low | ⚠️ Low/Med | **human_primary** | Draws inside/outside line | Surfaces edge cases, stress-tests boundaries | — |
| T1.4 | Job Description Drafting | 4 | 8 | 2 | −4 | High | Med | ✅ Med/High | **agent_primary** | Reviews, approves | Drafts from O1-O3 + schema_registry | Validates schema compliance |
| T1.5 | Contract Architecture | 7 | 6 | 4 | +1 | Low | Med | ⚠️ Med/Low | **collaborative** | Decides enforcement regime, revert granularity | Drafts contract from job description + authority class | Validates guard testability |

### SG2: Contracts

| ID | Subtask | J | P | D | Gap | Revers | Conf | C×R | Mode | Human | Agent | System |
|----|---------|---|---|---|-----|--------|------|-----|------|-------|-------|--------|
| T2.1 | Template Cascade | 2 | 9 | 6 | −7 | High | High | ✅ High/High | **agent_primary** | Spot-checks 2-3 templates | Generates all 8 from O4 specialisation | Validates cross-template consistency |
| T2.2 | Template Validation | 6 | 6 | 4 | 0 | Med | Med | ⚠️ Med/Med | **collaborative** | Judges edge cases, ambiguous validations | Runs structural checks, reports pass/fail | Enforces quality gate assertion |

### SG3: Behaviour

| ID | Subtask | J | P | D | Gap | Revers | Conf | C×R | Mode | Human | Agent | System |
|----|---------|---|---|---|-----|--------|------|-----|------|-------|-------|--------|
| T3.1 | Relational Profile Design | 8 | 4 | 1 | +4 | Med | Low | ⚠️ Low/Med | **collaborative** | Decides personality traits, tone | Drafts profile, surfaces tone-purpose tensions | — |
| T3.2 | Autonomy Plan Design | 7 | 6 | 3 | +1 | Low | Med | ⚠️ Med/Low | **collaborative** | Sets promotion thresholds, demotion triggers | Proposes quantitative metrics per level | Enforces threshold as guard |

### SG4: Verification

| ID | Subtask | J | P | D | Gap | Revers | Conf | C×R | Mode | Human | Agent | System |
|----|---------|---|---|---|-----|--------|------|-----|------|-------|-------|--------|
| T4.1 | Trust Ledger Design | 3 | 8 | 7 | −5 | High | High | ✅ High/High | **agent_primary** | Reviews query dimensions | Designs schema, query patterns | Validates 3-axis queryability |
| T4.2 | Aging Schedule Design | 5 | 7 | 4 | −2 | Med | Med | ⚠️ Med/Med | **collaborative** | Sets cadence for human-judgment specs | Proposes staleness scoring algorithm | Enforces calendar triggers as events |

### SG5: Implementation

| ID | Subtask | J | P | D | Gap | Revers | Conf | C×R | Mode | Human | Agent | System |
|----|---------|---|---|---|-----|--------|------|-----|------|-------|-------|--------|
| T5.1 | Agent Code Generation | 2 | 9 | 7 | −7 | High | High | ✅ High/High | **agent_primary** | Reviews generated code | Generates Agno agent from O3+O4+O5-O12 | Validates against schema_registry |
| T5.2 | Test Suite Generation | 2 | 9 | 7 | −7 | High | High | ✅ High/High | **agent_primary** | Reviews test coverage | Generates tests from FMEA + contract templates | Validates test schemas |
| T5.3 | Integration Validation | 7 | 5 | 6 | +2 | Low | Med | ⚠️ Med/Low | **collaborative** | Judges pass/fail on edge cases, non-deterministic output | Runs test suite, reports results | Enforces quality gate |

### SG6: Human Artefacts

| ID | Subtask | J | P | D | Gap | Revers | Conf | C×R | Mode | Human | Agent | System |
|----|---------|---|---|---|-----|--------|------|-----|------|-------|-------|--------|
| T6.1 | Boundary Map Render | 1 | 2 | **9** | −1 | High | High | ✅ High/High | **system_primary** | Spot-checks readability | — | Renders O2 → one-page view |
| T6.2 | Ops Manual Render | 1 | 2 | **9** | −1 | High | High | ✅ High/High | **system_primary** | Spot-checks insurer readability | — | Renders O1-O16 → structured doc |
| T6.3 | Decision Log Capture | 2 | 5 | **8** | −3 | Med | High | ✅ High/Med | **system_primary** | — | Classifies decision type | Captures, timestamps, stores in TypeDB |

### SG7: Ecosystem

| ID | Subtask | J | P | D | Gap | Revers | Conf | C×R | Mode | Human | Agent | System |
|----|---------|---|---|---|-----|--------|------|-----|------|-------|-------|--------|
| T7.1 | Pattern Identification | 4 | 8 | 3 | −4 | Med | Med | ⚠️ Med/Med | **agent_primary** | Validates genuine novelty | Scans design artefacts for repeatable patterns | — |
| T7.2 | Curriculum Module Draft | 5 | 7 | 2 | −2 | Med | Med | ⚠️ Med/Med | **collaborative** | Judges teachability | Drafts from decision log + patterns | — |

### SG8: Operational Environment

| ID | Subtask | J | P | D | Gap | Revers | Conf | C×R | Mode | Human | Agent | System |
|----|---------|---|---|---|-----|--------|------|-----|------|-------|-------|--------|
| T8.1 | Tool Audit & Spec | 6 | 7 | 4 | −1 | Med | Med | ⚠️ Med/Med | **collaborative** | Judges tool-scope alignment | Audits tool capabilities vs scope | Enforces information_boundary per tool |
| T8.2 | Context Protocol Design | 3 | 8 | 7 | −5 | Med | High | ✅ High/Med | **agent_primary** | Reviews budget allocation | Designs SELECT→ENRICH→CALIBRATE protocol | Enforces budget ceiling |
| T8.3 | Knowledge Base Spec | 5 | 7 | 4 | −2 | Med | Med | ⚠️ Med/Med | **collaborative** | Judges KB scope match to agent scope | Designs 12-characteristic KB schema | Validates scope containment |
| T8.4 | Memory Architecture | 6 | 6 | 5 | 0 | Low | Med | ⚠️ Med/Low | **collaborative** | Decides retention policy, human-deletable scope | Proposes architecture matching authority class | Enforces max_entries, max_age |
| T8.5 | Storage Specification | 1 | 4 | **9** | −3 | High | High | ✅ High/High | **system_primary** | — | Defines output schemas | Validates every output against schema_registry |

---

## Allocation Summary

| Mode | Count | Subtasks | % of Work |
|------|-------|----------|-----------|
| **Human-primary** | 2 | T1.1, T1.3 | 9% |
| **Collaborative** | 9 | T1.2, T1.5, T2.2, T3.1, T3.2, T4.2, T5.3, T7.2, T8.1, T8.3, T8.4 | 41% |
| **Agent-primary** | 7 | T1.4, T2.1, T4.1, T5.1, T5.2, T7.1, T8.2 | 32% |
| **System-primary** | 4 | T6.1, T6.2, T6.3, T8.5 | 18% |

---

## C×R Governor — What This Means for Agent Behaviour

| C×R Quadrant | Subtasks | Agent Behaviour | Human Role |
|--------------|----------|-----------------|------------|
| ⚠️ **Low Conf / Low Rev** | T1.1, T1.3 | Proposes, never decides. Surfaces tensions. Captures reasoning. | Decides. Reviews reasoning. Authorises. |
| ⚠️ **Med Conf / Low Rev** | T1.5, T3.2, T5.3, T8.4 | Drafts options with evidence. Stops at boundaries. | Picks option. Sets thresholds. Judges edge cases. |
| ⚠️ **Low Conf / Med Rev** | T1.2, T3.1, T7.2 | Presents structured choices. Names trade-offs. | Chooses. Validates personality-purpose link. |
| ⚠️ **Med / Med** | T2.2, T4.2, T8.1, T8.3 | Runs checks, reports, proposes. | Judges ambiguous results. Aligns scope. |
| ✅ **High Conf / High Rev** | T1.4, T2.1, T4.1, T5.1, T5.2, T6.1-T6.3, T8.2, T8.5 | Executes. Generates. Validates structurally. | Spot-checks. Approves. Reviews readability. |

**The governor is silent but total.** In Low/Low, the agent proposes and the human decides. In High/High, the agent executes and the human reviews. The human never loses decision authority — it just activates at different points.

---

## Decision Authority Register — 10 Critical Decision Points

| DA | Decision Point | Authority | Trigger | Escalation |
|----|---------------|-----------|---------|------------|
| DA1 | What is this agent's purpose? | **human_only** | Start of Phase 0 | Cannot proceed without answer |
| DA2 | What authority class? | **human_decides** | After purpose stated | Wrong class → rebuild contracts |
| DA3 | What's inside/outside scope? | **human_only** | After authority class | Scope miss → wrong boundaries everywhere |
| DA4 | What enforcement regime? | **human_decides** | During contract architecture | Wrong regime → false enforcement |
| DA5 | What revert granularity? | **human_decides** | During contract architecture | Too coarse → over-rollback; too fine → leaky |
| DA6 | What personality/tone? | **human_decides** | During relational profile | Mismatch → user distrust |
| DA7 | Autonomy promotion threshold? | **human_decides** | During autonomy plan | Too low → premature autonomy |
| DA8 | Integration pass/fail? | **human_decides** | During integration validation | False pass → production failure |
| DA9 | Memory retention policy? | **human_decides** | During memory architecture | Too long → governance drift |
| DA10 | KB scope containment? | **human_decides** | During KB specification | Scope leak → hallucination surface |

**Pattern: 0 agent-only decisions.** The agent prepares every decision input. The human makes every decision that has Low or Medium confidence, and reviews every decision in High confidence. This is the "agent prepares judgment; human makes judgment" principle at the subtask level.

---

## The Key Finding from Allocation

**2 human-primary subtasks gate 85% of downstream work.** T1.1 (Purpose Discovery) and T1.3 (Scope Boundary) are the only human-only tasks, but their outputs are the foundation for everything. If they're wrong, nothing downstream is right.

**9 collaborative subtasks** are where the highest-value work happens — the agent and human co-producing judgment preparation and judgment making. This is the design sweet spot.

**4 system-primary subtasks** are pure rendering and validation — deterministic work that should never touch an LLM. The system actor earns its place by eliminating hallucination risk from mechanical operations.

**0 decisions are agent-only.** Every decision point either requires human judgment or human review. The agent never operates without human authority for this meta-agent.

---

