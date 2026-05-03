# TypeDB Schema — Phase 0: Target State Vision

This extends the existing PRISM schema. Only the new types needed for agent design.

```typeql
# ─── PHASE 0: TARGET STATE VISION ───

# The design project itself — one per agent being designed
define

agent-design-project sub entity,
    owns project-name,
    owns project-description,
    owns created-at,
    owns status,
    plays project-owner,
    plays project-dimension,
    plays project-target;

# Four dimensions from Phase 0
target-dimension sub entity,
    owns dimension-name,          # "Agent", "Specification", "Human", "Ecosystem"
    owns dimension-description,
    plays dimension-of-project,
    plays dimension-has-target;

# Each characteristic in Phase 0
target-characteristic sub entity,
    owns characteristic-id,        # e.g., "A1", "S3", "H4"
    owns characteristic-name,     # e.g., "Boundary-Locked", "Typed Throughout", "Enriching"
    owns characteristic-statement,# One sentence defining the target state
    owns testable-criterion,      # How to verify it's been achieved
    plays target-of-dimension,
    plays target-served-by-phase,
    plays target-served-by-output;

# Links: which CAWDP phase primarily serves which target
phase-service sub relation,
    relates serving-phase,         # e.g., "Phase 4: Agent Design"
    relates served-target,
    owns service-strength;        # "primary" | "contributing"

# Links: which output (from Phase 1) serves which target
output-service sub relation,
    relates serving-output,       # e.g., "O4: Quasi-Smart Contract"
    relates served-target,
    owns service-strength;

# ─── ROLE PLAYERS ───

project-owner sub attribute, value string;
project-description sub attribute, value string;
created-at sub attribute, value datetime;
status sub attribute, value string;
dimension-name sub attribute, value string;
dimension-description sub attribute, value string;
characteristic-id sub attribute, value string;
characteristic-name sub attribute, value string;
characteristic-statement sub attribute, value string;
testable-criterion sub attribute, value string;
service-strength sub attribute, value string;
```

---

## What This Enables

With Phase 0 in the database, you can query things like:

**"Which targets does Phase 4 serve?"**
```
match $t (serving-phase: $phase, served-target: $target); 
$phase "Phase 4: Agent Design";
```

**"Which targets have no outputs yet?"**
```
match $target (target-served-by-output); not; get $target;
```

**"Give me all Specification targets"**
```
match $dim owns dimension-name "Specification"; 
($dim, $target); get $target;
```

---

## Phase 0 Data — Ready to Insert

Here's the data as a compact reference you can query later, not a wall of text to read now:

| ID | Dim | Name | Statement | Testable |
|----|-----|------|-----------|----------|
| A1 | Agent | Purpose-Faithful | Achieves mission within designed scope, every time | Self-reports performance against specification |
| A2 | Agent | Boundary-Locked | Authority boundaries enforced at contract membrane | Every boundary passes speed-limiter test |
| A3 | Agent | Epistemically Honest | Carries epistemic metadata on every output | Every output includes confidence, provenance, assumptions |
| A4 | Agent | Identity-Preserving | Purpose, principal, authority survive every session | Agent recreatable from TypeDB graph alone |
| A5 | Agent | Cost-Predictable | Cost per invocation/task/pipeline known and bounded | Overruns trigger contract halt, not warning |
| A6 | Agent | Composable | Authority boundaries legible to other actors | Other agents can query scope without reading prompt |
| A7 | Agent | Relationally Intelligent | Collaborative agents build rapport serving purpose | Personality-purpose link justifies every tone parameter |
| S1 | Spec | Contract-Native | Every subtask produces quasi-smart contract | Spec and enforcement are one artifact |
| S2 | Spec | Graph-Native | All artefacts in TypeDB, only code as files | Query graph → get any artefact; doc ≠ source of truth |
| S3 | Spec | Typed Throughout | Type collision resolved at every layer | No undifferentiated prose blobs anywhere |
| S4 | Spec | Template-Complete | All 8 template contracts filled and validated | Each template passes its own validation |
| S5 | Spec | Design-to-Code Traceable | Every code element traces to design decision | Every line has provenance chain back to phase artefact |
| S6 | Spec | Dual-Parseable | Specs work for agents, humans, and code generation | Same spec serves three audiences without translation |
| S7 | Spec | Semantic by Name | Name encodes role, authority class, domain | Stranger reads name → knows what it does |
| H1 | Human | Guided Not Blank | Never a blank page, every step has context | Vision Mirror reflects user's words at Phase 0 |
| H2 | Human | Discovery-Driven | Process surfaces what human didn't know they needed | At least 3 decisions that user says "I wouldn't have thought of that" |
| H3 | Human | Ownership-Producing | Human can explain agent in 5 min using boundary map | Boundary map exists and is non-technical-readable |
| H4 | Human | Enriching | Human is more capable after design than before | System Empowerment Index shows Amplifying or Liberating |
| H5 | Human | Recoverable | Every decision revisable without starting over | Graph supports targeted modification, not rebuild |
| H6 | Human | Rapport-Aware | Collaborative agents capture human communication prefs | Relational profile exists for collaborative agents |
| E1 | Eco | Compound-Knowledge | Every design feeds artefact graph | Meta-agent queryable on patterns from prior designs |
| E2 | Eco | Pattern-Crystallising | Similar agents take 1/Nth design time | Template library grows from practice |
| E3 | Eco | Trust-Measured | Class-level trust scores with statistical backing | "Measurer-class: 96.2% pass rate, N=1247" |
| E4 | Eco | Specification-Portable | Design transferable across orgs/LLMs | Same job description deploys anywhere |
| E5 | Eco | Curriculum-Producing | Every design is a teachable artifact | Curriculum module draft produced per design |
| E6 | Eco | Self-Improving | Process improves with every agent | Meta-agent captures improvement signals automatically |

---

**Next step:** When you're ready for Phase 1 (Output Specification), we'd add new entity types for each output group and insert O1-O28 as typed nodes with their schemas, dependencies, and quality gates. Each output links to the targets it serves via the `output-service` relation.

The chat becomes a *discussion space* for reasoning. The database becomes the *single source of truth*. That's S2 Graph-Native applied to our own process.

Want me to write the insert queries for this Phase 0 data, or move straight to the Phase 1 schema additions?