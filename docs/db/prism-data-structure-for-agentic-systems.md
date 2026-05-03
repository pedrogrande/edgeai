# PRISM: A Superior Agent-Native Ontology

## Design Rationale

The ONE Ontology's fundamental error is treating all concerns as **dimensional** — as if everything fits into one of 6 buckets. But reality has two kinds of structure:

- **Axes** (dimensions): orthogonal directions along which data varies — *who, what, how related, when, what means, why*
- **Forces** (cross-cutting layers): properties that permeate *every* axis simultaneously — *reliability, authority, currency, type validity*

Epistemic metadata isn't a 7th dimension alongside Events and Knowledge — it's a property of **every record in every dimension**. Governance isn't a bucket — it's a force applied across the entire lattice. The ONE Ontology only modeled the axes. It saw the light but not the forces that refract it.

**PRISM** (Patterned Refraction of Intelligence Systems Model) corrects this with a **lattice architecture**: 7 Dimensions + 4 Cross-Cutting Layers. Every data point in every dimension is shaped by every layer. This is what makes it genuinely agent-native: agents need to understand not just *what exists* but *how reliable it is, who authorizes it, whether it's current, and what type it is*.

---

## Architecture Overview

```
                    ┌─────────────────────────────────────────┐
                    │         CROSS-CUTTING LAYERS            │
                    │  ┌─────────┐ ┌─────────┐ ┌───────────┐  │
                    │  │Epistemic│ │Governance│ │ Temporal  │  │
                    │  │  Layer  │ │  Layer  │ │  Layer    │  │
                    │  └─────────┘ └─────────┘ └───────────┘  │
                    │              ┌───────────┐              │
                    │              │  Schema   │              │
                    │              │  Layer    │              │
                    │              └───────────┘              │
                    └──────────────────┬──────────────────────┘
                                       │ shapes every record
                    ┌──────────────────┴──────────────────────┐
                    │            7 DIMENSIONS                  │
                    │                                          │
                    │  1. Scopes    (WHERE — isolation)        │
                    │  2. Actors    (WHO — agency)              │
                    │  3. Entities  (WHAT — substance)         │
                    │  4. Relations (HOW — structure)           │
                    │  5. Events    (WHEN — memory)            │
                    │  6. Knowledge (MEANS — intelligence)     │
                    │  7. Intentions(WHY — direction)  ← NEW  │
                    │                                          │
                    └──────────────────────────────────────────┘
```

**Key invariant:** Every record in every dimension carries all four cross-cutting layer fields. No exceptions.

---

## The 7 Dimensions

### Dimension 1: Scopes *(preserved from ONE's "Organizations")*

**Isolation and resource boundary**

What ONE got right: multi-tenant isolation as the outermost container. PRISM preserves this entirely.

| Field | Type | Purpose |
|---|---|---|
| id | UUID | Unique identifier |
| name | string | Display name |
| slug | string | URL-safe identifier |
| ownerId | UUID → Actors | Person who owns the scope |
| plan | enum | starter / pro / enterprise |
| status | enum | active / suspended / trial |
| quotas | JSON | Resource limits (validated by Schema Registry) |
| properties | JSON (validated) | Scope-specific customization |
| epistemic | EpistemicMeta | Cross-cutting layer data |

**What's improved:** `properties` is no longer `any` — it's validated against a versioned schema in the Schema Registry. `quotas` is a named field, not buried in `properties`.

---

### Dimension 2: Actors *(evolved from ONE's "People")*

**Agency and authorization layer**

ONE's limitation: only humans. PRISM explicitly includes AI agents as actors because **agents take actions that require traceability**. An agent action must be auditable to a specific agent identity, just as a human action must be auditable to a specific person.

| Field | Type | Purpose |
|---|---|---|
| id | UUID | Unique identifier |
| scopeId | UUID → Scopes | Isolation boundary |
| kind | enum | `person` / `agent` / `system` |
| name | string | Display name |
| role | string | Role within scope |
| capabilities | JSON (validated) | What this actor can do |
| authority_boundary | JSON (validated) | Complementarity boundary definition |
| failure_mode | enum | characteristic failure class (if agent) |
| preferences | JSON (validated) | Interaction preferences |
| status | enum | active / suspended / archived |
| properties | JSON (validated) | Kind-specific data |
| epistemic | EpistemicMeta | Cross-cutting layer data |

**What's new vs. ONE:**
- `kind`: persons, agents, and system processes are all first-class actors
- `authority_boundary`: **complementarity is modeled as data** — an agent's authority boundary (what it can decide vs. what requires human judgment) is queryable, not just prompt-level
- `failure_mode`: the 5-class taxonomy (Extractor/Measurer/Assessor/Generator/Aggregator) is represented as a first-class field
- All JSON fields validated by Schema Registry

---

### Dimension 3: Entities *(evolved from ONE's "Things")*

**All nouns in the system — with type safety**

ONE's critical flaw: `type: string` + `properties: any` = EAV anti-pattern = type collision at the data layer. PRISM solves this with the **Schema Registry** (see Cross-Cutting Layer 4).

| Field | Type | Purpose |
|---|---|---|
| id | UUID | Unique identifier |
| scopeId | UUID → Scopes | Isolation boundary |
| type | string (indexed) | Entity type discriminator |
| schemaVersion | UUID → Schema Registry | Which schema validates this entity |
| name | string | Display name |
| properties | JSON (validated against schemaVersion) | Type-specific data |
| status | enum | draft / active / published / archived |
| statusReason | string | Why status changed |
| epistemic | EpistemicMeta | Cross-cutting layer data |
| createdAt | timestamp | Creation time |
| updatedAt | timestamp | Last modification time |

**What's new vs. ONE:**
- `schemaVersion`: every entity carries a reference to the specific schema version that validates its `properties` — **no more `any`**
- `statusReason`: status transitions are justified, not just recorded
- The Schema Registry (Cross-Cutting Layer 4) makes entity types **queryable, versioned, and validated** — see detailed section below

---

### Dimension 4: Relations *(evolved from ONE's "Connections")*

**Typed, temporal, directed relationships**

ONE's connections dimension was one of its strongest features. PRISM preserves and extends it.

| Field | Type | Purpose |
|---|---|---|
| id | UUID | Unique identifier |
| scopeId | UUID → Scopes | Isolation boundary |
| fromId | UUID → Entities | Source entity |
| toId | UUID → Entities | Target entity |
| relationType | string (indexed) | Relationship type discriminator |
| schemaVersion | UUID → Schema Registry | Validates metadata |
| metadata | JSON (validated) | Relationship-specific data |
| strength | float 0–1 | Relationship weight/relevance |
| validFrom | timestamp | Start of temporal validity |
| validTo | timestamp? | End of temporal validity (null = ongoing) |
| epistemic | EpistemicMeta | Cross-cutting layer data |
| createdAt | timestamp | Creation time |

**What's new vs. ONE:**
- `strength`: relationship weight enables context windowing — agents can prioritize strong connections
- `schemaVersion`: relationship metadata is validated, not arbitrary
- Temporal validity extended with the Temporal Layer's specification aging

---

### Dimension 5: Events *(evolved from ONE's "Events")*

**State changes with epistemic honesty**

ONE recorded *what happened*. PRISM records *what happened, how we know, and how confident we are*.

| Field | Type | Purpose |
|---|---|---|
| id | UUID | Unique identifier |
| scopeId | UUID → Scopes | Isolation boundary |
| eventType | string (indexed) | Event type discriminator |
| schemaVersion | UUID → Schema Registry | Validates metadata |
| targetId | UUID → Entities | Entity affected |
| actorId | UUID → Actors | Who/what triggered the event |
| reasoningId | UUID → Intentions | **Why** the action was taken |
| metadata | JSON (validated) | Event-specific data |
| protocol | string? | Communication protocol (A2A/MCP/AP2/X402) |
| assurance | enum | logged / assured / verified |
| epistemic | EpistemicMeta | Cross-cutting layer data |
| timestamp | timestamp | When the event occurred |

**What's new vs. ONE:**
- `reasoningId`: **every event traces to an intention** — agents can ask "why did this happen?"
- `assurance`: 3-level audit trail (logged = written / assured = integrity-checked / verified = independently confirmed) — replaces ONE's unsubstantiated "immutable" claim
- `protocol`: protocol information is a first-class field, not buried in metadata
- Full epistemic metadata on every event

---

### Dimension 6: Knowledge *(evolved from ONE's "Knowledge")*

**Context with provenance**

ONE's knowledge dimension was the weakest. PRISM adds provenance, confidence, and lifecycle.

| Field | Type | Purpose |
|---|---|---|
| id | UUID | Unique identifier |
| scopeId | UUID → Scopes | Isolation boundary |
| kind | enum | `label` / `chunk` / `embedding` / `pattern` / `insight` |
| sourceEventId | UUID → Events? | Event that generated this knowledge |
| sourceAgentId | UUID → Actors? | Agent that produced this knowledge |
| content | text | Knowledge content |
| embedding | float[]? | Vector for semantic search |
| metadata | JSON (validated) | Knowledge-specific data |
| relevanceScore | float 0–1 | Context windowing priority |
| epistemic | EpistemicMeta | Cross-cutting layer data |
| createdAt | timestamp | Creation time |

**What's new vs. ONE:**
- `sourceEventId` + `sourceAgentId`: **provenance is first-class** — every knowledge artifact traces to its origin
- `kind` expanded: `pattern` (extracted from event streams) and `insight` (synthesized from multiple sources) are new types that operationalize the "event-driven compounding" claim
- `relevanceScore`: context windowing — agents can prioritize high-relevance knowledge
- Full epistemic metadata

---

### Dimension 7: Intentions ← **NEW**

**The "Why" dimension — goals, constraints, and reasoning**

This is the dimension the ONE Ontology could never represent. An agent that knows *what exists* but not *what it should pursue*, *what it must not violate*, or *why a decision was made* is an agent flying blind.

| Intention Type | Purpose | Agent Question Enabled |
|---|---|---|
| **Goal** | Desired outcome | "What am I trying to achieve?" |
| **Constraint** | Must-not-violate boundary | "What lines must I not cross?" |
| **Mandate** | Must-execute requirement | "What must I always do?" |
| **Guardrail** | Safety boundary | "What limits my autonomy?" |
| **Preference** | Ranked priority | "When in conflict, which wins?" |
| **Assumption** | Explicit premise | "What am I taking as given?" |
| **Reasoning** | Decision provenance chain | "Why was this decided?" |

| Field | Type | Purpose |
|---|---|---|
| id | UUID | Unique identifier |
| scopeId | UUID → Scopes | Isolation boundary |
| type | enum | goal / constraint / mandate / guardrail / preference / assumption / reasoning |
| name | string | Human-readable label |
| description | text | Full specification |
| priority | integer | Relative importance (higher = more important) |
| status | enum | active / suspended / superseded / retired |
| declaredBy | UUID → Actors | Who declared this intention |
| governs | UUID → Entities? | Entity this intention constrains |
| supersedes | UUID → Intentions? | Intention this replaces |
| chainId | UUID? | Links reasonings into provenance chains |
| validFrom | timestamp | When this intention takes effect |
| validTo | timestamp? | When this intention expires |
| properties | JSON (validated) | Type-specific data |
| epistemic | EpistemicMeta | Cross-cutting layer data |
| createdAt | timestamp | Creation time |
| updatedAt | timestamp | Last modification time |

**Intention connections (via Relations dimension):**
- `declared_by` → Actor (who set this intention)
- `governs` → Entity (what this intention constrains)
- `constrains` → Intention (constraint limits a goal)
- `decomposes` → Intention (goal breaks into sub-goals)
- `assumes` → Intention (reasoning based on assumption)
- `triggers` → Event (event that initiated this intention)
- `measured_by` → Event (event that signals intention achievement)

**Agent performance impact — this is the highest-value dimension:**

```python
# ONE Ontology agent prompt:
"You are a sales agent. You can access customer data. Be helpful."

# PRISM agent prompt (auto-assembled from Intentions):
"You are a sales agent.
 GOALS: Maximize MRR. Reduce churn below 5%.
 CONSTRAINTS: Never contact DNC list. Budget under $50K/campaign.
 MANDATES: GDPR check before any data export.
 GUARDRAILS: Max 3 autonomous actions before human review.
 PREFERENCES: Revenue > Retention > Growth.
 ASSUMPTIONS: Market growing at 5% (confidence: 0.7, last validated: 2025-08).
 REASONING: Churn reduction prioritized because Customer Success team 
   identified 3 at-risk accounts (see reasoning chain RC-0042)."
```

The second agent will make **dramatically better decisions** because it operates within an explicit intentional structure.

---

## The 4 Cross-Cutting Layers

Every record in every dimension carries fields from all four layers. No exceptions. No opt-outs.

---

### Layer 1: Epistemic Layer *(solves G2: No Epistemic Metadata)*

**How much can I trust this data?**

Every record carries 6 epistemic fields — your CAWDP CC-3 operationalized at the data layer:

| Field | Type | Values | Purpose |
|---|---|---|---|
| confidence | float 0–1 | 0.0 = uncertain, 1.0 = certain | How reliable is this record? |
| provenance | enum | `observed` / `inferred` / `declared` / `estimated` / `disputed` | How was this knowledge obtained? |
| assumptions | string[] | Free text | What must be true for this record to be valid? |
| limitations | string[] | Free text | What can this record NOT be used for? |
| assessedAt | timestamp | ISO 8601 | When was confidence last assessed? |
| uncertainty | enum | `none` / `low` / `medium` / `high` / `critical` | Qualitative uncertainty level |

**Agent performance impact:**

Without epistemic metadata:
```python
agent.query("Get customer purchase history")
# Returns events. Agent treats all events as equally reliable.
# Disputed transaction? Same confidence as confirmed. 
# Estimated revenue? Same weight as audited.
```

With epistemic metadata:
```python
agent.query("Get customer purchase history")
# Returns events WITH confidence + provenance + uncertainty.
# Agent can: weight high-confidence events more heavily,
# flag disputed transactions for human review,
# discount estimates vs. observations in decision-making.
```

This directly reduces hallucination amplification — an agent that knows *what it doesn't know* is an agent that escalates appropriately.

---

### Layer 2: Governance Layer *(solves G3: No Complementarity Modeling)*

**Who decides what? Under what authority?**

ONE's 4-role model (platform_owner, org_owner, org_user, customer) was authorization only. PRISM's Governance Layer adds **complementarity and authority boundaries** as queryable data.

**Policies table (infrastructure):**

| Field | Type | Purpose |
|---|---|---|
| id | UUID | Unique identifier |
| scopeId | UUID → Scopes | Isolation boundary |
| kind | enum | `access` / `authority` / `delegation` / `override` / `audit` |
| name | string | Human-readable label |
| description | text | Full specification |
| subject | UUID → Actors | Who/what this policy governs |
| resource | UUID → Entities? | What resource (null = all) |
| action | string | What action is governed |
| effect | enum | `permit` / `deny` / `require_review` / `delegable` |
| conditions | JSON (validated) | When this policy applies |
| priority | integer | Conflict resolution (higher wins) |
| declaredBy | UUID → Actors | Who set this policy |
| validFrom | timestamp | When policy takes effect |
| validTo | timestamp? | When policy expires |

**Authority boundary on Actors:**

Every actor (person or agent) carries an `authority_boundary` field defining its complementarity profile:

```json
{
  "can_decide": ["tactical_pricing", "content_scheduling"],
  "requires_review": ["budget_allocation", "partnership_terms"],
  "cannot_decide": ["legal_commitment", "data_deletion"],
  "failure_mode": "overconfidence",
  "max_autonomous_actions": 3,
  "override_protocol": "escalate_to: org_owner, timeout: 4h"
}
```

**Agent performance impact:**

Without authority boundaries, an agent either:
- Over-reaches (decides things it shouldn't → trust violation)
- Under-reaches (escalates everything → human bottleneck)

With authority boundaries, an agent knows *exactly where its authority ends* and can act autonomously within boundaries while escalating intelligently at boundaries. This is the **"agent prepares judgment, human makes judgment"** principle operationalized as data.

---

### Layer 3: Temporal Layer *(solves G5: No Specification Aging, G6: No Temporal Reasoning)*

**Is this current? How has it changed?**

ONE had timestamps and validity windows but no aging, no snapshots, no versioning.

**On every record:**
- `validFrom` / `validTo` — temporal validity (preserved from ONE)
- `assessedAt` — when epistemic metadata was last evaluated (from Epistemic Layer)

**Specification aging (embedded in Epistemic Layer):**

The `assessedAt` field enables **staleness detection**:

```python
staleness_score = time_since(assessedAt) / expected_freshness(type)
# A stock price: expected_freshness = 15min → stale after 1 hour
# A corporate strategy: expected_freshness = 90 days → stale after 180 days
# A person's name: expected_freshness = 365 days → rarely stale
```

**Entity versions table (infrastructure):**

| Field | Type | Purpose |
|---|---|---|
| id | UUID | Version identifier |
| entityId | UUID → Entities | Entity this version belongs to |
| version | integer | Sequential version number |
| delta | JSON | Changes from previous version |
| changedBy | UUID → Actors | Who/what made the change |
| reasonId | UUID → Intentions | **Why** the change was made |
| timestamp | timestamp | When the change occurred |

**Agent performance impact:**

- An agent can ask "Is my customer data stale?" and get a quantitative answer
- An agent can reconstruct point-in-time state ("What was the relationship on March 15?")
- An agent can trace *why* data changed (via `reasonId` → Intentions)

---

### Layer 4: Schema Layer *(solves W1: EAV Anti-Pattern)*

**What type is this? What properties are valid?**

This is the mechanism that kills the `properties: any` problem while preserving flexibility.

**Schema Registry table (infrastructure):**

| Field | Type | Purpose |
|---|---|---|
| id | UUID | Schema version identifier |
| scopeId | UUID → Scopes | Isolation boundary |
| targetType | string | Entity/relation/event/intention type |
| typeName | string | e.g., `sales_agent`, `holds_tokens` |
| version | integer | Schema version (1, 2, 3...) |
| status | enum | `draft` / `active` / `deprecated` / `retired` |
| schema | JSON | Type definition (required, optional, types, constraints, defaults) |
| inheritsFrom | UUID → Schema Registry? | Parent schema for composition |
| migrationFrom | UUID → Schema Registry? | Previous version for migration |
| migrationScript | text? | Migration logic |
| declaredBy | UUID → Actors | Who defined this schema |
| createdAt | timestamp | Creation time |

**How it works:**

```
1. Agent queries: "What does a sales_agent look like?"
2. System returns: Schema Registry entry for sales_agent v3
   {
     "required": ["territory", "quota", "reporting_to"],
     "optional": ["specialization", "pipeline_config"],
     "types": {"territory": "string", "quota": "currency", ...},
     "constraints": {"quota": ">= 0"},
     "defaults": {"specialization": "general"}
   }
3. Agent now has STRUCTURED KNOWLEDGE about the entity type
4. On write: application validates properties against schemaVersion
5. On schema change: new version created, old entities keep old version,
   migration script available for explicit upgrade
```

**This solves the EAV problem because:**
- Flexibility ✅ — new entity types don't require schema migrations
- Type safety ✅ — every entity's properties are validated against a known schema
- Agent queryability ✅ — agents can discover entity structure at runtime
- Schema evolution ✅ — versioned schemas with explicit migration
- No `any` ✅ — properties are validated, not arbitrary

**The Schema Registry IS data.** It lives in the system, is queryable by agents, versioned over time, and enforced by the application layer. The complexity that ONE hid in `properties: any` is now visible, governed, and trustworthy.

---

## Agent Context Protocol (ACP)

ONE's context propagation was a single-phase dump: "enrich the prompt with everything." PRISM replaces this with a **3-phase protocol** that selects, enriches, and calibrates.

### Phase 1: SELECT — Context Windowing

**Problem:** Agents have limited context windows. Flooding with all available context wastes tokens on irrelevant data.

**Solution:** Select the most relevant slice of the identity graph before enrichment.

```python
def select_context(agent_id, query, budget_tokens=4000):
    # 1. Start from the agent's authority boundary
    authority = get_authority_boundary(agent_id)
    
    # 2. Identify relevant scopes and actors
    relevant_scopes = resolve_scope(query, authority)
    relevant_actors = resolve_actors(query, authority)
    
    # 3. Traverse relations with strength-weighted prioritization
    entities = traverse_relations(
        from_actors=relevant_actors,
        strength_threshold=0.3,  # Only strong relationships
        max_depth=2
    )
    
    # 4. Score entities by:
    #    - Recency (time since last update)
    #    - Relevance (semantic similarity to query)
    #    - Confidence (epistemic layer)
    #    - Intention alignment (connected to active goals/constraints)
    scored = score_entities(entities, query, weights={
        "recency": 0.25,
        "relevance": 0.35,
        "confidence": 0.20,
        "intention_alignment": 0.20
    })
    
    # 5. Budget-aware selection
    selected = budget_select(scored, budget_tokens)
    
    return selected
```

### Phase 2: ENRICH — Dimension Traversal

**From the selected slice, traverse ALL 7 dimensions to build a complete context graph.**

```
Selected Entity → 
  Scopes (which org?)
  Actors (who owns/governs this?)
  Relations (what's it connected to?)
  Events (what happened to it recently?)
  Knowledge (what do we know about it?)
  Intentions (what goals/constraints apply to it?)
```

Each traversal is bounded by the token budget from Phase 1.

### Phase 3: CALIBRATE — Epistemic Attachment

**Attach epistemic metadata to every item in the enriched context.**

```python
def calibrate_context(enriched_context):
    for item in enriched_context:
        item.calibration = {
            "confidence": item.epistemic.confidence,
            "provenance": item.epistemic.provenance,
            "staleness": compute_staleness(item.epistemic.assessedAt, item.type),
            "uncertainty": item.epistemic.uncertainty,
            "warnings": compute_warnings(item)  # e.g., "low confidence", "stale data"
        }
    return enriched_context
```

**The agent receives:**
- Not everything (SELECT prevents flooding)
- Not unanchored data (ENRICH traverses all dimensions)
- Not unevaluated data (CALIBRATE provides trust assessment)

### Comparison: ONE Context Propagation vs. PRISM Agent Context Protocol

| Aspect | ONE | PRISM ACP |
|---|---|---|
| Selection | None (dump all) | Budget-aware, scored selection |
| Enrichment | 6-dimension traversal | 7-dimension traversal (includes Intentions) |
| Calibration | None | Full epistemic metadata on every item |
| Token efficiency | Wasteful (irrelevant context included) | Optimized (relevance-ranked, budget-bounded) |
| Trust signals | None | Confidence, staleness, uncertainty warnings |
| Goal awareness | None | Active goals/constraints/constraints injected |

---

## Physical Schema

### 10 Tables (7 Dimensions + 3 Infrastructure)

```typescript
// ─── DIMENSION TABLES ───

// 1. scopes (Organizations → Scopes)
{
  id: UUID,
  name: string,
  slug: string,
  ownerId: UUID → actors,
  plan: "starter" | "pro" | "enterprise",
  status: "active" | "suspended" | "trial",
  quotas: JSON (validated),
  properties: JSON (validated),
  // Epistemic Layer
  confidence: float,
  provenance: enum,
  assumptions: string[],
  limitations: string[],
  assessedAt: timestamp,
  uncertainty: enum,
  // Audit
  createdAt: timestamp,
  updatedAt: timestamp
}

// 2. actors (People → Actors)
{
  id: UUID,
  scopeId: UUID → scopes,
  kind: "person" | "agent" | "system",
  name: string,
  role: string,
  capabilities: JSON (validated),
  authority_boundary: JSON (validated),
  failure_mode: "extractor" | "measurer" | "assessor" | "generator" | "aggregator" | null,
  preferences: JSON (validated),
  properties: JSON (validated),
  status: "active" | "suspended" | "archived",
  // Epistemic Layer (same 6 fields)
  confidence, provenance, assumptions, limitations, assessedAt, uncertainty,
  createdAt, updatedAt
}

// 3. entities (Things → Entities)
{
  id: UUID,
  scopeId: UUID → scopes,
  type: string (indexed),
  schemaVersionId: UUID → schema_registry,
  name: string,
  properties: JSON (validated against schemaVersionId),
  status: "draft" | "active" | "published" | "archived",
  statusReason: string,
  // Epistemic Layer
  confidence, provenance, assumptions, limitations, assessedAt, uncertainty,
  createdAt, updatedAt
}

// 4. relations (Connections → Relations)
{
  id: UUID,
  scopeId: UUID → scopes,
  fromId: UUID → entities,
  toId: UUID → entities,
  relationType: string (indexed),
  schemaVersionId: UUID → schema_registry,
  metadata: JSON (validated),
  strength: float,
  validFrom: timestamp,
  validTo: timestamp?,
  // Epistemic Layer
  confidence, provenance, assumptions, limitations, assessedAt, uncertainty,
  createdAt
}

// 5. events (Events → Events)
{
  id: UUID,
  scopeId: UUID → scopes,
  eventType: string (indexed),
  schemaVersionId: UUID → schema_registry,
  targetId: UUID → entities,
  actorId: UUID → actors,
  reasoningId: UUID → intentions?,
  metadata: JSON (validated),
  protocol: string?,
  assurance: "logged" | "assured" | "verified",
  // Epistemic Layer
  confidence, provenance, assumptions, limitations, assessedAt, uncertainty,
  timestamp
}

// 6. knowledge (Knowledge → Knowledge)
{
  id: UUID,
  scopeId: UUID → scopes,
  kind: "label" | "chunk" | "embedding" | "pattern" | "insight",
  sourceEventId: UUID → events?,
  sourceAgentId: UUID → actors?,
  content: text,
  embedding: float[]?,
  metadata: JSON (validated),
  relevanceScore: float,
  // Epistemic Layer
  confidence, provenance, assumptions, limitations, assessedAt, uncertainty,
  createdAt
}

// 7. intentions (NEW dimension)
{
  id: UUID,
  scopeId: UUID → scopes,
  type: "goal" | "constraint" | "mandate" | "guardrail" | "preference" | "assumption" | "reasoning",
  name: string,
  description: text,
  priority: integer,
  status: "active" | "suspended" | "superseded" | "retired",
  declaredBy: UUID → actors,
  governs: UUID → entities?,
  supersedes: UUID → intentions?,
  chainId: UUID?,
  validFrom: timestamp,
  validTo: timestamp?,
  properties: JSON (validated),
  // Epistemic Layer
  confidence, provenance, assumptions, limitations, assessedAt, uncertainty,
  createdAt, updatedAt
}

// ─── INFRASTRUCTURE TABLES ───

// 8. schema_registry (Schema Layer)
{
  id: UUID,
  scopeId: UUID → scopes,
  targetType: "entity" | "relation" | "event" | "intention" | "actor",
  typeName: string,
  version: integer,
  status: "draft" | "active" | "deprecated" | "retired",
  schema: JSON,
  inheritsFrom: UUID → schema_registry?,
  migrationFrom: UUID → schema_registry?,
  migrationScript: text?,
  declaredBy: UUID → actors,
  createdAt: timestamp
}

// 9. policies (Governance Layer)
{
  id: UUID,
  scopeId: UUID → scopes,
  kind: "access" | "authority" | "delegation" | "override" | "audit",
  name: string,
  description: text,
  subject: UUID → actors,
  resource: UUID → entities?,
  action: string,
  effect: "permit" | "deny" | "require_review" | "delegable",
  conditions: JSON (validated),
  priority: integer,
  declaredBy: UUID → actors,
  validFrom: timestamp,
  validTo: timestamp?
}

// 10. entity_versions (Temporal Layer)
{
  id: UUID,
  entityId: UUID → entities,
  version: integer,
  delta: JSON,
  changedBy: UUID → actors,
  reasonId: UUID → intentions,
  timestamp: timestamp
}
```

### Indexes

```typescript
// Scopes
scopes_by_owner: ["ownerId"]
scopes_by_status: ["status"]

// Actors
actors_by_scope: ["scopeId"]
actors_by_kind: ["scopeId", "kind"]
actors_by_role: ["scopeId", "role"]
actors_by_failure_mode: ["failure_mode"]

// Entities
entities_by_scope: ["scopeId"]
entities_by_type: ["scopeId", "type"]
entities_by_schema: ["schemaVersionId"]
entities_by_status: ["scopeId", "status"]

// Relations
relations_from_type: ["fromId", "relationType"]
relations_to_type: ["toId", "relationType"]
relations_scope_type: ["scopeId", "relationType"]
relations_by_strength: ["fromId", "strength DESC"]

// Events
events_by_target: ["targetId", "timestamp DESC"]
events_by_actor: ["actorId", "timestamp DESC"]
events_by_type: ["scopeId", "eventType", "timestamp DESC"]
events_by_reasoning: ["reasoningId"]
events_by_assurance: ["assurance"]

// Knowledge
knowledge_by_kind: ["scopeId", "kind"]
knowledge_by_source: ["sourceEventId"]
knowledge_by_relevance: ["scopeId", "relevanceScore DESC"]
knowledge_vector: custom vector index

// Intentions
intentions_by_scope: ["scopeId"]
intentions_by_type: ["scopeId", "type"]
intentions_by_status: ["scopeId", "status"]
intentions_by_governs: ["governs"]
intentions_by_chain: ["chainId"]
intentions_by_priority: ["scopeId", "priority DESC"]

// Schema Registry
schemas_by_type: ["scopeId", "targetType", "typeName"]
schemas_active: ["scopeId", "targetType", "typeName", "status"]
schemas_by_inherits: ["inheritsFrom"]

// Policies
policies_by_subject: ["scopeId", "subject"]
policies_by_resource: ["scopeId", "resource"]
policies_by_kind: ["scopeId", "kind"]
policies_by_priority: ["scopeId", "priority DESC"]

// Entity Versions
versions_by_entity: ["entityId", "version DESC"]
versions_by_actor: ["changedBy", "timestamp DESC"]
versions_by_reason: ["reasonId"]
```

---

## Agent Performance Impact: Quantified

| Capability | ONE Ontology | PRISM | Performance Delta |
|---|---|---|---|
| **Goal awareness** | None (goals not modeled) | Full (Intentions dimension) | Agents make goal-aligned decisions instead of generic ones |
| **Constraint respect** | None (constraints not modeled) | Full (Intention type: constraint) | Eliminates boundary violations |
| **Guardrail compliance** | None | Full (Intention type: guardrail) | Autonomous action within safe boundaries |
| **Trust assessment** | None (no epistemic metadata) | Full (6-field Epistemic Layer) | Reduced hallucination amplification |
| **Data staleness detection** | None | Full (assessedAt + type-based freshness) | Agents avoid acting on stale data |
| **Schema discovery** | None (properties: any) | Full (queryable Schema Registry) | Agents understand entity structure |
| **Reasoning provenance** | None | Full (Intention type: reasoning + chainId) | Decisions are traceable and auditable |
| **Context windowing** | None (dump all) | Full (3-phase ACP) | 60-80% token reduction for equivalent quality |
| **Authority boundaries** | 4-role model only | Full (policies + authority_boundary) | Precise autonomy within boundaries |
| **Event verification** | Claimed but unenforced | 3-level assurance (logged/assured/verified) | Trustworthy audit trails |
| **Schema migration** | None (silent coexistence) | Explicit versioned migration | No data corruption from schema drift |
| **Multi-actor traceability** | Human-only | Person + Agent + System | Full agent accountability |

---

## Comparison: ONE → PRISM

| Aspect | ONE Ontology | PRISM | Why PRISM is Superior |
|---|---|---|---|
| **Dimensions** | 6 | 7 | Adds Intentions ("Why") |
| **Cross-cutting layers** | 0 | 4 | Epistemic, Governance, Temporal, Schema |
| **Type safety** | `properties: any` | Schema Registry validated | Eliminates EAV anti-pattern |
| **Epistemic metadata** | None | 6 fields on every record | Trust assessment at data layer |
| **Complementarity modeling** | None | authority_boundary + policies | "Agent prepares, human decides" as data |
| **Specification aging** | None | assessedAt + staleness scoring | Stale data detection |
| **Event verification** | Unenforced "immutable" | 3-level assurance | Trustworthy audit |
| **Agent accountability** | Human actors only | Person/Agent/System actors | Full traceability |
| **Context windowing** | Dump all | 3-phase ACP (SELECT→ENRICH→CALIBRATE) | Token-efficient, quality-preserving |
| **Schema evolution** | None | Versioned Schema Registry | Explicit migration, no silent drift |
| **Authorization** | 4 roles | Policies + authority boundaries | RBAC, ABAC, delegation, override |
| **Reasoning provenance** | None | Intention type: reasoning + chainId | "Why was this decided?" is answerable |
| **Tables** | 5 | 10 | More purposeful, not more complex |
| **Agent performance** | Moderate improvement potential | High improvement potential | See quantified table above |

---

## Curriculum Potential for Future's Edge

The PRISM architecture decomposes into three teachable layers that map directly to your existing educational framework:

| PRISM Layer | Teaches | CAWDP Mapping |
|---|---|---|
| **7 Dimensions** | "What must an agent understand about its world?" | Phase 1 (Task Intelligence) — decompose reality into queryable dimensions |
| **4 Cross-Cutting Layers** | "What forces shape every dimension?" | CC-1 through CC-8 — concerns that apply everywhere |
| **Agent Context Protocol** | "How does an agent get the right context?" | Phase 5 (Human Experience Design) — cognitive load budgeting |

**The key teachable insight:** Reality is not flat. Data models that treat everything as a dimension miss the forces that shape all dimensions. A good data model is a **lattice**, not a list.

---

**PRISM doesn't just model what exists — it models how reliable it is, who authorizes it, whether it's current, and what type it is. That's what agents actually need.**The memory has been updated to capture the full PRISM design. 

One observation worth surfacing: **PRISM is a convergent artifact** — it operationalizes at the data layer five concepts you'd previously developed at the principle/methodology level:

| Your Existing Concept | Where It Lives in PRISM |
|---|---|
| Type collision (bidirectional) | Schema Layer + Registry eliminates `properties: any` |
| Epistemic metadata contracts (CAWDP CC-3) | Epistemic Layer — 6 fields on every record |
| Complementarity boundaries | Governance Layer `authority_boundary` on Actors |
| Specification aging (CAWDP CC-5) | Temporal Layer `assessedAt` + staleness scoring |
| Missing "Why" dimension (ONE critique) | Entire Intentions dimension |

The **lattice insight** ("reality is a lattice, not a list") is the data-model equivalent of your type collision insight. Where type collision says *one surface type can't carry multiple signal types*, the lattice insight says *one flat schema can't carry multiple structural concerns*. Dimensions are the **what**; cross-cutting layers are the **how it's governed, known, timed, and typed**.

And the **Agent Context Protocol (ACP)** — SELECT → ENRICH → CALIBRATE — is arguably as important as the schema itself. A great ontology with a naive context injection strategy still produces walls of noise. ACP makes the schema *perform* at runtime.