# 1. Check Categories — 5 Diagnostic Dimensions

### D1: Count Verification
Entity and relation counts match expected values from the design manifest. Drift from expected counts signals missing data, duplicate insertion, or failed batches.

### D2: Structural Integrity
No orphan entities (entities with zero relation connections). No isolated subgraphs (clusters of entities disconnected from the main graph). Every entity type is reachable.

### D3: Backcasting Integrity
Dependency chains are fully traceable. Every output can trace backward to root inputs. No broken chains. No circular dependencies. Phase 2's specific contribution.

### D4: Phase Connectivity
Phase sequence is complete (0→1→2→...→9). Every design-output is linked to a phase. Every phase produces at least one output. No orphan outputs without phase context.

### D5: Cross-Phase Consistency
Relations between phases are consistent. Subtask-produces references match actual design-output IDs. Allocations match subtasks. Events reference real subtasks. FMEA entries reference real pipeline stages.

---

## 2. Expected Counts Manifest

The single source of truth for what the database *should* contain. This is the design intent materialised as a queryable specification.

```python
# manifest.py

from dataclasses import dataclass, field
from enum import Enum

class CountSource(str, Enum):
    """Where does this expected count come from?"""
    DESIGN_SPEC = "design_spec"      # Directly from the CAWDP design specification
    RETRO_REPORT = "retro_report"     # From the implementation retrospective
    SEED_FILE = "seed_file"           # Counted from the seed data file

@dataclass
class ExpectedCount:
    entity_type: str
    expected: int
    phase: int
    source: CountSource
    tolerance: int = 0  # Allow ± tolerance for evolving data
    note: str = ""

# Phase 0
PHASE0_COUNTS = [
    ExpectedCount("target-dimension", 4, 0, CountSource.DESIGN_SPEC),
    ExpectedCount("target-characteristic", 26, 0, CountSource.DESIGN_SPEC),
    ExpectedCount("cawdp-phase", 0, 0, CountSource.RETRO_REPORT, note="Stub only, no seed data"),
    ExpectedCount("input-requirement", 0, 0, CountSource.RETRO_REPORT, note="Stub only, no seed data"),
]

# Phase 1
PHASE1_COUNTS = [
    ExpectedCount("design-output", 28, 1, CountSource.DESIGN_SPEC),
    ExpectedCount("output-group", 8, 1, CountSource.DESIGN_SPEC),
]

PHASE1_RELATION_COUNTS = [
    ExpectedCount("output-group-membership", 28, 1, CountSource.RETRO_REPORT),
    ExpectedCount("output-dependency", 85, 1, CountSource.DESIGN_SPEC),
    ExpectedCount("phase-service", 28, 1, CountSource.RETRO_REPORT),
    ExpectedCount("output-service", 28, 1, CountSource.RETRO_REPORT),
]

# Phase 2 (after full seeding — update after Phase 2 is applied)
PHASE2_COUNTS = [
    ExpectedCount("cawdp-phase", 10, 2, CountSource.DESIGN_SPEC, note="After Phase 2 seeding"),
    ExpectedCount("input-requirement", 17, 2, CountSource.SEED_FILE, tolerance=70, 
                  note="17 seeded, ~85 after full derivation"),
]

PHASE2_RELATION_COUNTS = [
    ExpectedCount("phase-sequence", 9, 2, CountSource.DESIGN_SPEC),
    ExpectedCount("phase-produces-output", 28, 2, CountSource.DESIGN_SPEC),
    ExpectedCount("ir-required-by-output", 17, 2, CountSource.SEED_FILE, tolerance=70),
    ExpectedCount("ir-satisfied-by-output", 13, 2, CountSource.SEED_FILE, tolerance=70,
                  note="External IRs have no satisfied-by"),
    ExpectedCount("ir-consumed-by-subtask", 8, 2, CountSource.SEED_FILE, tolerance=70),
]

# Phase 3
PHASE3_COUNTS = [
    ExpectedCount("subtask", 24, 3, CountSource.DESIGN_SPEC),
    ExpectedCount("subtask-group", 8, 3, CountSource.DESIGN_SPEC),
    ExpectedCount("failure-mode", 24, 3, CountSource.DESIGN_SPEC),
]

PHASE3_RELATION_COUNTS = [
    ExpectedCount("subtask-group-membership", 24, 3, CountSource.RETRO_REPORT),
    ExpectedCount("subtask-produces", 24, 3, CountSource.RETRO_REPORT),
    ExpectedCount("subtask-has-fm", 24, 3, CountSource.RETRO_REPORT),
]

# Phase 4
PHASE4_COUNTS = [
    ExpectedCount("allocation", 24, 4, CountSource.DESIGN_SPEC),
    ExpectedCount("decision-authority", 10, 4, CountSource.DESIGN_SPEC),
]

PHASE4_RELATION_COUNTS = [
    ExpectedCount("subtask-has-allocation", 24, 4, CountSource.RETRO_REPORT),
    ExpectedCount("subtask-has-authority", 10, 4, CountSource.RETRO_REPORT),
]

# Phase 5
PHASE5_COUNTS = [
    ExpectedCount("domain-event", 16, 5, CountSource.DESIGN_SPEC),
    ExpectedCount("failure-event", 14, 5, CountSource.DESIGN_SPEC),
    ExpectedCount("recovery-path", 14, 5, CountSource.DESIGN_SPEC),
    ExpectedCount("system-trigger", 10, 5, CountSource.DESIGN_SPEC),
]

PHASE5_RELATION_COUNTS = [
    ExpectedCount("subtask-trigger", 24, 5, CountSource.RETRO_REPORT),
    ExpectedCount("subtask-emits", 16, 5, CountSource.RETRO_REPORT),
    ExpectedCount("event-sequence", 13, 5, CountSource.RETRO_REPORT),
    ExpectedCount("failure-interrupts", 14, 5, CountSource.RETRO_REPORT),
    ExpectedCount("failure-recovery", 14, 5, CountSource.RETRO_REPORT),
    ExpectedCount("failure-system-trigger", 14, 5, CountSource.RETRO_REPORT),
]

# Phase 6
PHASE6_COUNTS = [
    ExpectedCount("pipeline-stage", 9, 6, CountSource.DESIGN_SPEC),
    ExpectedCount("orchestration-config", 1, 6, CountSource.DESIGN_SPEC),
    ExpectedCount("orchestration-decision", 5, 6, CountSource.DESIGN_SPEC),
    ExpectedCount("fmea-entry", 14, 6, CountSource.DESIGN_SPEC),
    ExpectedCount("template-type", 7, 6, CountSource.DESIGN_SPEC),
    ExpectedCount("template-instance", 12, 6, CountSource.DESIGN_SPEC),
    ExpectedCount("composition-config", 1, 6, CountSource.DESIGN_SPEC),
    ExpectedCount("fallback-tier", 18, 6, CountSource.DESIGN_SPEC),
]

PHASE6_RELATION_COUNTS = [
    ExpectedCount("stage-contains", 21, 6, CountSource.RETRO_REPORT,
                  note="24 minus 3 — S9 subtasks are failure-events, not subtask entities"),
    ExpectedCount("stage-sequence", 8, 6, CountSource.RETRO_REPORT),
    ExpectedCount("orchestration-has-decision", 5, 6, CountSource.RETRO_REPORT),
    ExpectedCount("template-has-instance", 12, 6, CountSource.RETRO_REPORT),
    ExpectedCount("subtask-has-fallback", 15, 6, CountSource.RETRO_REPORT,
                  note="Varies — Tier 4 fallbacks have no subtask link"),
]

# Aggregate
ALL_ENTITY_COUNTS = (
    PHASE0_COUNTS + PHASE1_COUNTS + PHASE2_COUNTS + 
    PHASE3_COUNTS + PHASE4_COUNTS + PHASE5_COUNTS + PHASE6_COUNTS
)

ALL_RELATION_COUNTS = (
    PHASE1_RELATION_COUNTS + PHASE2_RELATION_COUNTS + PHASE3_RELATION_COUNTS +
    PHASE4_RELATION_COUNTS + PHASE5_RELATION_COUNTS + PHASE6_RELATION_COUNTS
)
```

---

## 3. TypeQL Verification Queries

These queries run against the **live database** (not files). They use `match ... select` pattern (TypeQL v3, not `fetch`).

### D1: Count Verification Queries

```python
# queries.py — TypeQL v3 compatible

# Count all entities of a given type
COUNT_ENTITY_TYPE = """
match $x isa {entity_type}; select $x; count;
"""

# Count all relations of a given type
COUNT_RELATION_TYPE = """
match $x isa {relation_type}; select $x; count;
"""

# Count ALL entities (total)
COUNT_ALL_ENTITIES = """
match $x isa entity; select $x; count;
"""

# Count ALL relations (total)
COUNT_ALL_RELATIONS = """
match $x isa relation; select $x; count;
"""
```

### D2: Structural Integrity Queries

```python
# Find orphan entities — entities with NO relation connections
FIND_ORPHANS = """
match
  $e isa entity;
  not { $r ($e); isa relation; };
  $e has output-id $id;  # generic: replace with appropriate ID attribute
select $e, $id;
"""

# More specific: find design-outputs with no dependencies (should have at least
# output-group-membership or output-dependency)
FIND_ISOLATED_OUTPUTS = """
match
  $o isa design-output, has output-id $oid;
  not { $g isa output-group; (grouped-output: $o) isa output-group-membership; };
select $o, $oid;
"""

# Find subtasks with no allocation
FIND_UNALLOCATED_SUBTASKS = """
match
  $s isa subtask, has subtask-id $sid;
  not { $a isa allocation; (fm-subtask: $s) isa subtask-has-allocation; };
select $s, $sid;
"""

# Find subtasks with no failure mode
FIND_UNTESTED_SUBTASKS = """
match
  $s isa subtask, has subtask-id $sid;
  not { $fm isa failure-mode; (fm-subtask: $s) isa subtask-has-fm; };
select $s, $sid;
"""
```

### D3: Backcasting Integrity Queries

```python
# Verify O28 backcasting chain exists
TRACE_O28_CHAIN = """
match
  $o28 isa design-output, has output-id "O28";
  $r1 (requiring-output: $o28) isa ir-required-by-output;
  $ir1 has ir-id $ir1_id;
  $r2 (satisfied-ir: $ir1, satisfying-output: $sat) isa ir-satisfied-by-output;
  $sat has output-id $sat_id;
select $ir1_id, $sat_id;
"""

# Find outputs with NO input requirements (roots — should only be O1-O4 or externals)
FIND_ROOT_OUTPUTS = """
match
  $o isa design-output, has output-id $oid;
  not { (requiring-output: $o) isa ir-required-by-output; };
select $o, $oid;
"""

# Find input requirements with no satisfying output (unsatisfied IRs — 
# should only be external-type)
FIND_UNSATISFIED_IRS = """
match
  $ir isa input-requirement, has ir-id $irid, has ir-type $type;
  not { (satisfied-ir: $ir) isa ir-satisfied-by-output; };
select $ir, $irid, $type;
"""

# Detect circular dependencies (A → B → ... → A)
# This is a hard query in TypeDB — v1 checks for direct cycles only
FIND_DIRECT_CYCLES = """
match
  $a isa design-output, has output-id $aid;
  $b isa design-output, has output-id $bid;
  (dependent: $a, depended-upon: $b) isa output-dependency;
  (dependent: $b, depended-upon: $a) isa output-dependency;
select $a, $aid, $b, $bid;
"""
```

### D4: Phase Connectivity Queries

```python
# Verify phase sequence is complete (0-9, no gaps)
FIND_PHASE_GAPS = """
match
  $p isa cawdp-phase, has phase-number $n;
  select $p, $n;
"""

# Find outputs with no phase link
FIND_UNPHASED_OUTPUTS = """
match
  $o isa design-output, has output-id $oid;
  not { (produced-output: $o) isa phase-produces-output; };
select $o, $oid;
"""

# Find phases with no output
FIND_EMPTY_PHASES = """
match
  $p isa cawdp-phase, has phase-id $pid, has phase-name $pname;
  not { (producing-phase: $p) isa phase-produces-output; };
select $p, $pid, $pname;
"""

# Verify phase sequence completeness (should be 9 relations for 10 phases)
COUNT_PHASE_SEQUENCE = """
match $seq isa phase-sequence; select $seq; count;
"""
```

### D5: Cross-Phase Consistency Queries

```python
# Every subtask should produce at least one output
FIND_IDLE_SUBTASKS = """
match
  $s isa subtask, has subtask-id $sid;
  not { (fm-subtask: $s) isa subtask-produces; };
select $s, $sid;
"""

# Every pipeline stage should contain subtasks
FIND_EMPTY_STAGES = """
match
  $stg isa pipeline-stage, has stage-id $stgid;
  not { (stage: $stg) isa stage-contains; };
select $stg, $stgid;
"""

# Every failure event should have a recovery path
FIND_UNRECOVERABLE_FAILURES = """
match
  $fe isa failure-event, has event-id $feid;
  not { (failed-event: $fe) isa failure-recovery; };
select $fe, $feid;
"""

# Every template type should have at least one instance
FIND_ABSTRACT_TEMPLATES = """
match
  $tt isa template-type, has template-type-id $ttid;
  not { (type: $tt) isa template-has-instance; };
select $tt, $ttid;
"""
```

---

## 4. Architecture

```
svd/
├── __init__.py
├── cli.py              # CLI entry point
├── runner.py            # Orchestrates all checks against live DB
├── manifest.py         # Expected counts (from Section 2)
├── queries.py          # TypeQL query templates (from Section 3)
├── checks/
│   ├── __init__.py
│   ├── count_check.py   # D1: Count verification
│   ├── structure.py     # D2: Structural integrity
│   ├── backcasting.py   # D3: Backcasting integrity
│   ├── phase_conn.py    # D4: Phase connectivity
│   └── consistency.py   # D5: Cross-phase consistency
├── models.py           # HealthReport data model (Pydantic)
└── reporters.py        # Output formatters (text, JSON)
```

### Core Data Model

```python
# models.py

from pydantic import BaseModel, Field
from enum import Enum
from pathlib import Path
from typing import Optional

class CheckSeverity(str, Enum):
    CRITICAL = "critical"    # Data is missing or corrupt — must fix
    WARNING = "warning"      # Data may be incomplete — should investigate
    HEALTHY = "healthy"      # All checks pass for this dimension

class CheckDimension(str, Enum):
    COUNT = "D1_count"              # Entity/relation counts
    STRUCTURE = "D2_structure"      # No orphans, connected graph
    BACKCASTING = "D3_backcasting"  # Dependency chains traceable
    PHASE = "D4_phase"             # Phase connectivity
    CONSISTENCY = "D5_consistency"  # Cross-phase consistency

class CountVariance(BaseModel):
    """Single count discrepancy between expected and actual."""
    type_name: str
    expected: int
    actual: int
    delta: int
    phase: int
    tolerance: int = 0
    severity: CheckSeverity
    note: str = ""

class StructuralFinding(BaseModel):
    """A single structural issue found in the database."""
    dimension: CheckDimension
    severity: CheckSeverity
    description: str
    entity_id: Optional[str] = None
    entity_type: Optional[str] = None
    query_used: str         # Which TypeQL query found this
    remediation: str

class PhaseHealth(BaseModel):
    """Health status for a single CAWDP phase."""
    phase_number: int
    phase_name: str
    entity_types: list[str]
    total_entities: int = 0
    total_relations: int = 0
    count_variances: list[CountVariance] = []
    structural_findings: list[StructuralFinding] = []
    status: CheckSeverity = CheckSeverity.HEALTHY

class HealthReport(BaseModel):
    """Complete health report for the CAWDP knowledge graph."""
    database: str
    timestamp: str
    total_entities: int = 0
    total_relations: int = 0
    phase_health: dict[int, PhaseHealth] = {}
    cross_phase_findings: list[StructuralFinding] = []
    
    # Summary metrics
    critical_count: int = 0
    warning_count: int = 0
    healthy_phases: int = 0
    
    @property
    def status(self) -> CheckSeverity:
        if self.critical_count > 0:
            return CheckSeverity.CRITICAL
        elif self.warning_count > 0:
            return CheckSeverity.WARNING
        return CheckSeverity.HEALTHY
    
    def summary(self) -> str:
        status_icon = {"critical": "🔴", "warning": "🟡", "healthy": "🟢"}
        icon = status_icon[self.status.value]
        return (
            f"{icon} {self.status.value.upper()} | "
            f"{self.total_entities} entities | {self.total_relations} relations | "
            f"🔴 {self.critical_count} critical | 🟡 {self.warning_count} warnings | "
            f"🟢 {self.healthy_phases}/7 phases healthy"
        )
```

---

## 5. Check Runner

```python
# runner.py

from typedb.driver import TypeDB, SessionType, TransactionType
from .manifest import ALL_ENTITY_COUNTS, ALL_RELATION_COUNTS
from .models import *
from .queries import *

class SVDRunner:
    """Schema Verification Diagnostic runner.
    
    The IDS (Intrusion Detection System) for the CAWDP knowledge graph.
    Post-insertion complement to the pre-insertion SQG linter.
    """
    
    def __init__(self, host: str = "localhost", port: int = 1729, 
                 database: str = "edgeai"):
        self.host = host
        self.port = port
        self.database = database
    
    def run_full_diagnostic(self) -> HealthReport:
        """Run all 5 diagnostic dimensions."""
        with TypeDB.core_driver(f"{self.host}:{self.port}") as driver:
            with driver.session(self.database, SessionType.DATA) as session:
                report = HealthReport(
                    database=self.database,
                    timestamp=datetime.now().isoformat(),
                )
                
                # D1: Count verification
                self._run_count_checks(session, report)
                
                # D2: Structural integrity
                self._run_structure_checks(session, report)
                
                # D3: Backcasting integrity
                self._run_backcasting_checks(session, report)
                
                # D4: Phase connectivity
                self._run_phase_checks(session, report)
                
                # D5: Cross-phase consistency
                self._run_consistency_checks(session, report)
                
                # Compute summaries
                self._compute_summaries(report)
                
                return report
    
    def _query_count(self, session, query: str) -> int:
        """Execute a count query and return the integer result."""
        with session.transaction(TransactionType.READ) as tx:
            result = tx.query().match_aggregate(query)
            # Parse TypeQL aggregate result
            for answer in result:
                return int(answer.get("count", 0))
            return 0
    
    def _query_match(self, session, query: str) -> list[dict]:
        """Execute a match query and return results as list of dicts."""
        with session.transaction(TransactionType.READ) as tx:
            results = []
            for answer in tx.query().match(query):
                results.append(answer)
            return results
    
    # ---- D1: COUNT VERIFICATION ----
    
    def _run_count_checks(self, session, report: HealthReport):
        """Verify entity and relation counts match expected values."""
        for expected in ALL_ENTITY_COUNTS:
            actual = self._query_count(
                session, COUNT_ENTITY_TYPE.format(entity_type=expected.entity_type)
            )
            delta = actual - expected.expected
            abs_delta = abs(delta)
            
            if abs_delta > expected.tolerance:
                severity = CheckSeverity.CRITICAL if abs_delta > max(1, expected.tolerance * 2) else CheckSeverity.WARNING
            else:
                severity = CheckSeverity.HEALTHY
            
            if severity != CheckSeverity.HEALTHY:
                variance = CountVariance(
                    type_name=expected.entity_type,
                    expected=expected.expected,
                    actual=actual,
                    delta=delta,
                    phase=expected.phase,
                    tolerance=expected.tolerance,
                    severity=severity,
                    note=expected.note,
                )
                # Add to appropriate phase health
                if expected.phase not in report.phase_health:
                    report.phase_health[expected.phase] = PhaseHealth(
                        phase_number=expected.phase,
                        phase_name=f"Phase {expected.phase}",
                    )
                report.phase_health[expected.phase].count_variances.append(variance)
            
            # Track totals
            report.total_entities += actual
        
        # Same for relation counts
        for expected in ALL_RELATION_COUNTS:
            actual = self._query_count(
                session, COUNT_RELATION_TYPE.format(relation_type=expected.entity_type)
            )
            delta = actual - expected.expected
            abs_delta = abs(delta)
            
            if abs_delta > expected.tolerance:
                severity = CheckSeverity.CRITICAL if abs_delta > max(1, expected.tolerance * 2) else CheckSeverity.WARNING
            else:
                severity = CheckSeverity.HEALTHY
            
            if severity != CheckSeverity.HEALTHY:
                variance = CountVariance(
                    type_name=expected.entity_type,
                    expected=expected.expected,
                    actual=actual,
                    delta=delta,
                    phase=expected.phase,
                    tolerance=expected.tolerance,
                    severity=severity,
                    note=expected.note,
                )
                if expected.phase not in report.phase_health:
                    report.phase_health[expected.phase] = PhaseHealth(
                        phase_number=expected.phase,
                        phase_name=f"Phase {expected.phase}",
                    )
                report.phase_health[expected.phase].count_variances.append(variance)
            
            report.total_relations += actual
    
    # ---- D2: STRUCTURAL INTEGRITY ----
    
    def _run_structure_checks(self, session, report: HealthReport):
        """Check for orphans, isolated subgraphs, disconnected entities."""
        checks = [
            (FIND_ISOLATED_OUTPUTS, "Design-output has no output-group membership"),
            (FIND_UNALLOCATED_SUBTASKS, "Subtask has no allocation"),
            (FIND_UNTESTED_SUBTASKS, "Subtask has no failure mode"),
        ]
        
        for query_template, description in checks:
            results = self._query_match(session, query_template)
            for result in results:
                finding = StructuralFinding(
                    dimension=CheckDimension.STRUCTURE,
                    severity=CheckSeverity.WARNING,
                    description=description,
                    entity_id=result.get("oid") or result.get("sid"),
                    entity_type="design-output" if "oid" in result else "subtask",
                    query_used=query_template[:50] + "...",
                    remediation="Check seed data — relation may have failed during insertion",
                )
                report.cross_phase_findings.append(finding)
    
    # ---- D3: BACKCASTING INTEGRITY ----
    
    def _run_backcasting_checks(self, session, report: HealthReport):
        """Verify dependency chains are traceable and complete."""
        # Check 1: Root outputs should only be O1-O4 or external-type IRs
        root_results = self._query_match(session, FIND_ROOT_OUTPUTS)
        # After Phase 2, roots should be O1-O4 (driven by external inputs)
        # Before Phase 2, ALL outputs are roots (no IR links yet)
        # So this check only runs meaningfully after Phase 2 is seeded
        
        # Check 2: Unsatisfied IRs should only be external type
        unsatisfied = self._query_match(session, FIND_UNSATISFIED_IRS)
        for result in unsatisfied:
            ir_type = result.get("type", "")
            if ir_type != "external-human" and ir_type != "external-system" and ir_type != "external-domain":
                finding = StructuralFinding(
                    dimension=CheckDimension.BACKCASTING,
                    severity=CheckSeverity.CRITICAL,
                    description=f"Internal input-requirement '{result.get('irid')}' has no satisfying output — broken dependency chain",
                    entity_id=result.get("irid"),
                    entity_type="input-requirement",
                    query_used="FIND_UNSATISFIED_IRS",
                    remediation="Check Phase 2 seed data — internal IRs must have ir-satisfied-by-output relations",
                )
                report.cross_phase_findings.append(finding)
        
        # Check 3: Direct circular dependencies
        cycles = self._query_match(session, FIND_DIRECT_CYCLES)
        for result in cycles:
            finding = StructuralFinding(
                dimension=CheckDimension.BACKCASTING,
                severity=CheckSeverity.CRITICAL,
                description=f"Circular dependency: {result.get('aid')} ↔ {result.get('bid')}",
                entity_id=result.get("aid"),
                entity_type="design-output",
                query_used="FIND_DIRECT_CYCLES",
                remediation="Break the circular dependency — one output must not depend on the other",
            )
            report.cross_phase_findings.append(finding)
    
    # ---- D4: PHASE CONNECTIVITY ----
    
    def _run_phase_checks(self, session, report: HealthReport):
        """Verify phase sequence and output-phase links."""
        # Check 1: Phase sequence count
        seq_count = self._query_count(session, COUNT_PHASE_SEQUENCE)
        if seq_count < 9:
            finding = StructuralFinding(
                dimension=CheckDimension.PHASE,
                severity=CheckSeverity.WARNING,
                description=f"Phase sequence has {seq_count} relations, expected 9 (10 phases → 9 sequences)",
                query_used="COUNT_PHASE_SEQUENCE",
                remediation="Check Phase 2 seed data for missing phase-sequence relations",
            )
            report.cross_phase_findings.append(finding)
        
        # Check 2: Outputs without phase links
        unphased = self._query_match(session, FIND_UNPHASED_OUTPUTS)
        for result in unphased:
            finding = StructuralFinding(
                dimension=CheckDimension.PHASE,
                severity=CheckSeverity.WARNING,
                description=f"Output {result.get('oid')} has no phase-produces-output link",
                entity_id=result.get("oid"),
                entity_type="design-output",
                query_used="FIND_UNPHASED_OUTPUTS",
                remediation="Add phase-produces-output relation in Phase 2 seed data",
            )
            report.cross_phase_findings.append(finding)
        
        # Check 3: Empty phases
        empty = self._query_match(session, FIND_EMPTY_PHASES)
        for result in empty:
            # P7, P8, P9 don't have outputs in Phase 1 spec yet — not errors
            phase_name = result.get("pname", "")
            phase_num = int(result.get("pid", "P0")[1:]) if result.get("pid") else 0
            if phase_num < 7:  # Phases 0-6 should have outputs
                finding = StructuralFinding(
                    dimension=CheckDimension.PHASE,
                    severity=CheckSeverity.WARNING,
                    description=f"Phase {phase_name} has no produced outputs",
                    entity_id=result.get("pid"),
                    entity_type="cawdp-phase",
                    query_used="FIND_EMPTY_PHASES",
                    remediation="Add phase-produces-output relations for this phase",
                )
                report.cross_phase_findings.append(finding)

# ---- D5: CROSS-PHASE INTEGRITY ----
# These checks query the live database to verify that relationships
# between phases are consistent. They require a TypeDB session.

FIND_ORPHAN_OUTPUTS = """
match
  $o isa design-output, has output-id $oid;
  not { ($phase, $o) isa phase-produces-output; };
  select $oid;
"""

FIND_ORPHAN_SUBTASKS = """
match
  $s isa subtask, has subtask-id $sid;
  not { ($s, $o) isa subtask-produces; };
  select $sid;
"""

FIND_UNPRODUCED_OUTPUTS = """
match
  $o isa design-output, has output-id $oid;
  not { ($s, $o) isa subtask-produces; };
  select $oid;
"""

FIND_MISSING_ALLOCATIONS = """
match
  $s isa subtask, has subtask-id $sid;
  not { ($s, $a) isa subtask-has-allocation; };
  select $sid;
"""

FIND_MISSING_FAILURE_MODES = """
match
  $s isa subtask, has subtask-id $sid;
  not { ($s, $fm) isa subtask-has-fm; };
  select $sid;
"""

FIND_MISSING_FALLBACKS = """
match
  $s isa subtask, has subtask-id $sid;
  not { ($s, $ft) isa subtask-has-fallback; };
  select $sid;
"""

FIND_ORPHAN_IRS = """
match
  $ir isa input-requirement, has ir-id $irid;
  not { ($o, $ir) isa ir-required-by-output; };
  select $irid;
"""

FIND_IRS_WITHOUT_SATISFACTION = """
match
  $ir isa input-requirement, has ir-id $irid;
  has ir-type "internal";
  not { ($ir, $o) isa ir-satisfied-by-output; };
  select $irid;
"""

    def check_cross_phase_integrity(self, session) -> list[CrossPhaseFinding]:
        """D5: Verify cross-phase relationship consistency in live database.
        
        These checks catch structural gaps that file-based linting cannot:
        - Outputs with no producing phase
        - Subtasks with no produced output
        - Outputs with no producing subtask
        - Subtasks with no allocation, failure mode, or fallback
        - Input requirements with no requiring output
        - Internal IRs with no satisfying output
        
        Returns a list of CrossPhaseFindings, not blocking errors — 
        some gaps are expected during incremental development.
        """
        findings = []
        
        # D5.1: Outputs with no producing phase
        orphans = self._query_match(session, FIND_ORPHAN_OUTPUTS)
        for result in orphans:
            findings.append(CrossPhaseFinding(
                check_id="D5.1",
                severity=CheckSeverity.WARNING,
                dimension=CheckDimension.PHASE,
                description=f"Output {result.get('oid')} has no producing phase via phase-produces-output",
                entity_id=result.get("oid"),
                entity_type="design-output",
                from_phase=None,
                to_phase=None,
                remediation="Add phase-produces-output relation linking this output to its CAWDP phase",
            ))
        
        # D5.2: Subtasks with no produced output
        orphan_subtasks = self._query_match(session, FIND_ORPHAN_SUBTASKS)
        for result in orphan_subtasks:
            findings.append(CrossPhaseFinding(
                check_id="D5.2",
                severity=CheckSeverity.WARNING,
                dimension=CheckDimension.TASK,
                description=f"Subtask {result.get('sid')} has no produced output via subtask-produces",
                entity_id=result.get("sid"),
                entity_type="subtask",
                from_phase=3,
                to_phase=1,
                remediation="Add subtask-produces relation linking this subtask to its output",
            ))
        
        # D5.3: Outputs with no producing subtask (backcasting gap)
        unproduced = self._query_match(session, FIND_UNPRODUCED_OUTPUTS)
        for result in unproduced:
            findings.append(CrossPhaseFinding(
                check_id="D5.3",
                severity=CheckSeverity.WARNING,
                dimension=CheckDimension.BACKCASTING,
                description=f"Output {result.get('oid')} has no producing subtask — backcasting chain is broken",
                entity_id=result.get("oid"),
                entity_type="design-output",
                from_phase=3,
                to_phase=1,
                remediation="Add subtask-produces relation, or verify this output is produced by a human-only task",
            ))
        
        # D5.4: Subtasks with no allocation (capability allocation gap)
        unallocated = self._query_match(session, FIND_MISSING_ALLOCATIONS)
        for result in unallocated:
            findings.append(CrossPhaseFinding(
                check_id="D5.4",
                severity=CheckSeverity.WARNING,
                dimension=CheckDimension.ALLOCATION,
                description=f"Subtask {result.get('sid')} has no capability allocation",
                entity_id=result.get("sid"),
                entity_type="subtask",
                from_phase=4,
                to_phase=3,
                remediation="Add subtask-has-allocation relation for this subtask",
            ))
        
        # D5.5: Subtasks with no failure modes (event storming gap)
        no_fm = self._query_match(session, FIND_MISSING_FAILURE_MODES)
        for result in no_fm:
            findings.append(CrossPhaseFinding(
                check_id="D5.5",
                severity=CheckSeverity.INFO,
                dimension=CheckDimension.EVENT,
                description=f"Subtask {result.get('sid')} has no associated failure mode",
                entity_id=result.get("sid"),
                entity_type="subtask",
                from_phase=5,
                to_phase=3,
                remediation="Add subtask-has-fm relation, or verify this subtask is simple enough to skip event storming",
            ))
        
        # D5.6: Subtasks with no fallback tiers (architecture gap)
        no_fallback = self._query_match(session, FIND_MISSING_FALLBACKS)
        for result in no_fallback:
            findings.append(CrossPhaseFinding(
                check_id="D5.6",
                severity=CheckSeverity.INFO,
                dimension=CheckDimension.ARCHITECTURE,
                description=f"Subtask {result.get('sid')} has no fallback tier defined",
                entity_id=result.get("sid"),
                entity_type="subtask",
                from_phase=6,
                to_phase=3,
                remediation="Add subtask-has-fallback relation, or verify this subtask uses the default fallback tier",
            ))
        
        # D5.7: Input requirements with no requiring output
        orphan_irs = self._query_match(session, FIND_ORPHAN_IRS)
        for result in orphan_irs:
            findings.append(CrossPhaseFinding(
                check_id="D5.7",
                severity=CheckSeverity.WARNING,
                dimension=CheckDimension.BACKCASTING,
                description=f"Input requirement {result.get('irid')} has no requiring output — disconnected IR",
                entity_id=result.get("irid"),
                entity_type="input-requirement",
                from_phase=2,
                to_phase=1,
                remediation="Add ir-required-by-output relation linking this IR to the output that needs it",
            ))
        
        # D5.8: Internal IRs with no satisfying output
        unsatisfied = self._query_match(session, FIND_IRS_WITHOUT_SATISFACTION)
        for result in unsatisfied:
            findings.append(CrossPhaseFinding(
                check_id="D5.8",
                severity=CheckSeverity.WARNING,
                dimension=CheckDimension.BACKCASTING,
                description=f"Internal input requirement {result.get('irid')} has no satisfying output — dependency chain broken",
                entity_id=result.get("irid"),
                entity_type="input-requirement",
                from_phase=2,
                to_phase=1,
                remediation="Add ir-satisfied-by-output relation, or change ir-type to external if this is an external dependency",
            ))
        
        return findings
```

---

## Full Cross-Phase Report Data Model

```python
@dataclass
class CheckDimension(str, Enum):
    """The CAWDP dimension being checked — maps to Phase 0 target characteristics."""
    PHASE = "phase"           # Phase completeness
    OUTPUT = "output"         # Output specification
    BACKCASTING = "backcast"  # Dependency chain integrity
    TASK = "task"             # Task decomposition
    ALLOCATION = "allocation"  # Capability allocation
    EVENT = "event"           # Event storming
    ARCHITECTURE = "arch"     # System architecture

@dataclass
class CrossPhaseFinding:
    """A structural gap found by querying the live database.
    
    Unlike file-based Findings (which catch syntax errors before insertion),
    CrossPhaseFindings catch relational gaps in the live graph.
    They are WARNING or INFO — not BLOCKING — because incremental 
    development naturally creates temporary gaps.
    """
    check_id: str               # D5.1–D5.8
    severity: CheckSeverity
    dimension: CheckDimension   # Which CAWDP dimension
    description: str
    entity_id: str
    entity_type: str
    from_phase: Optional[int]  # Phase that should provide the relation
    to_phase: Optional[int]    # Phase that contains the entity
    remediation: str

@dataclass
class CrossPhaseReport:
    """Complete cross-phase integrity report."""
    timestamp: datetime
    total_entities: int
    total_relations: int
    findings: list[CrossPhaseFinding]
    
    # Phase completion tracking
    phase_entity_counts: dict[int, dict[str, int]]  # phase_num → {entity_type: count}
    
    # Chain integrity tracking
    backcast_chains_complete: int = 0
    backcast_chains_broken: int = 0
    allocation_coverage: float = 0.0  # % of subtasks with allocations
    failure_mode_coverage: float = 0.0  # % of subtasks with failure modes
    fallback_coverage: float = 0.0  # % of subtasks with fallback tiers
    
    def summary(self) -> str:
        lines = [
            f"Cross-Phase Integrity Report — {self.timestamp.isoformat()}",
            f"Entities: {self.total_entities} | Relations: {self.total_relations}",
            f"Backcast chains: {self.backcast_chains_complete} complete, "
            f"{self.backcast_chains_broken} broken",
            f"Allocation coverage: {self.allocation_coverage:.0%}",
            f"Failure mode coverage: {self.failure_mode_coverage:.0%}",
            f"Fallback coverage: {self.fallback_coverage:.0%}",
            "",
            f"Findings: {len(self.findings)}",
        ]
        for f in self.findings:
            icon = {"blocking": "🔴", "warning": "🟡", "info": "🔵"}[f.severity.value]
            lines.append(f"  {icon} [{f.check_id}] {f.description}")
        lines.append("")
        status = "✅ PASS" if not any(
            f.severity == CheckSeverity.BLOCKING for f in self.findings
        ) else "🔴 FAIL"
        lines.append(f"{status} | {len(self.findings)} findings")
        return "\n".join(lines)
```

---

## Complete Architecture — Two-Layer Verification

The SQG now has **two layers** matching CC-1's three verification levels:

```
┌─────────────────────────────────────────────────────────────┐
│                SQG Architecture                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Layer 1: FILE-BASED (Regime 3 — Prevent by Design)        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Scanner → Rules → Findings                          │   │
│  │  Runs BEFORE database insertion                      │   │
│  │  Catches: syntax, naming, structure, declaration     │   │
│  │  18 rules (S01–S15, D01–D03)                        │   │
│  │  BLOCKING findings prevent insertion                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                           ↓ pass                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              TypeDB INSERT                             │   │
│  └─────────────────────────────────────────────────────┘   │
│                           ↓ after insert                    │
│  Layer 2: DATABASE-BASED (CC-1 Level 2 — Semantic)          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Cross-Phase Queries → CrossPhaseFindings             │   │
│  │  Runs AFTER database insertion                        │   │
│  │  Catches: relational gaps, broken chains, coverage   │   │
│  │  8 checks (D5.1–D5.8)                                │   │
│  │  WARNING/INFO only — incremental development expected │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Combined output: LintResult + CrossPhaseReport              │
│  = Complete CC-1 verification at schema layer               │
│                                                             │
│  Layer 3 (CC-1 Level 3 — Authority) = Human review of      │
│  WARNING/INFO findings before proceeding to next phase       │
└─────────────────────────────────────────────────────────────┘
```

This three-layer stack maps directly to CC-1:

| CC-1 Level | SQG Layer | What It Catches | When It Runs | Blocking? |
|---|---|---|---|---|
| **Level 1 — Structural** | File-based linter | Syntax, naming, declaration order | Before insertion | Yes |
| **Level 2 — Semantic** | Cross-phase queries | Relational gaps, broken chains | After insertion | No (WARNING/INFO) |
| **Level 3 — Authority** | Human review | Design intent, coverage adequacy | At phase gate | Human decision |

---

## Complete Rule Catalog — Final Count

| ID | Severity | Layer | Check | Retro Pattern |
|---|---|---|---|---|
| SQG-S01 | 🔴 BLOCKING | File | No `sub entity/relation/attribute` | P1 |
| SQG-S02 | 🔴 BLOCKING | File | No `value long` | P1 |
| SQG-S03 | 🔴 BLOCKING | File | No inline `plays` | P1 |
| SQG-S04 | 🔴 BLOCKING | File | No v2 keywords in `define` | P1 |
| SQG-S05 | 🔴 BLOCKING | File | v3 syntax only in `define` blocks | P1 |
| SQG-S06 | 🔴 BLOCKING | File | Role names ≠ entity type names | P2 |
| SQG-S07 | 🔴 BLOCKING | File | Every `plays` references defined relation | P3 |
| SQG-S08 | 🔴 BLOCKING | File | Every role in `plays` defined in relation | P4 |
| SQG-S09 | 🟡 WARNING | File | No `fetch { $var.* }` syntax | P5 |
| SQG-S10 | 🟡 WARNING | File | Re-declaring existing types flagged | P7 |
| SQG-S11 | 🔴 BLOCKING | File | Attributes declared before owning entities | P8 |
| SQG-S12 | 🟡 WARNING | File | Entity types own ≥ 1 `@key` | — |
| SQG-S13 | 🟡 WARNING | File | No orphan attributes | — |
| SQG-S14 | 🔵 INFO | File | Naming convention (kebab-case) | — |
| SQG-S15 | 🔵 INFO | File | Relations have ≥ 2 roles | — |
| SQG-D01 | 🟡 WARNING | File | Insert blocks < 40 entities | P6 |
| SQG-D02 | 🔴 BLOCKING | File | No duplicate `@key` values | — |
| SQG-D03 | 🟡 WARNING | File | Referenced entities exist | — |
| **SQG-D5.1** | 🟡 WARNING | **DB** | Outputs have producing phase | — |
| **SQG-D5.2** | 🟡 WARNING | **DB** | Subtasks have produced output | — |
| **SQG-D5.3** | 🟡 WARNING | **DB** | Outputs have producing subtask | — |
| **SQG-D5.4** | 🟡 WARNING | **DB** | Subtasks have allocation | — |
| **SQG-D5.5** | 🔵 INFO | **DB** | Subtasks have failure mode | — |
| **SQG-D5.6** | 🔵 INFO | **DB** | Subtasks have fallback tier | — |
| **SQG-D5.7** | 🟡 WARNING | **DB** | IRs have requiring output | — |
| **SQG-D5.8** | 🟡 WARNING | **DB** | Internal IRs have satisfying output | — |

**Total: 26 checks — 18 file-based + 8 database-based**

---

## Implementation Priority — Revised

| Step | Deliverable | Effort | Catches |
|---|---|---|---|
| 1 | Core models (`models.py`) | 30 min | Foundation |
| 2 | Scanner v1 (`scanner.py`) | 2 hr | File parsing |
| 3 | Top 5 blocking file rules (S01–S05, S06–S08, S11) | 2 hr | 90% of retro errors |
| 4 | CLI + text reporter | 1 hr | Manual use |
| **Milestone 1** | **File-based linter ships** | **5.5 hr** | **Blocking errors caught before insertion** |
| 5 | Remaining file rules (S09–S10, S12–S15) | 1.5 hr | Completes file coverage |
| 6 | Seed rules (D01–D03) | 1 hr | Data quality |
| 7 | Cross-phase checker (`cross_phase.py`) + 8 DB queries | 2 hr | Relational integrity |
| 8 | JSON/SARIF reporters + pre-commit config | 45 min | CI/CD integration |
| **Milestone 2** | **Full SQG with cross-phase** | **~11 hr total** | **Complete CC-1 verification** |

Ship Milestone 1 first. It immediately prevents the 5 most damaging error types from ever reaching the database. The cross-phase checker (Milestone 2) is for after Phase 2 is populated — it becomes meaningful when there are enough relations between phases to check.

---

## The Bigger Picture — Why This Matters

The SQG is **not just a linter**. It's the first operationalisation of CC-1 at the infrastructure layer of CAWDP's own knowledge graph. Three things make it significant:

**1. It's CAWDP eating its own cooking at the deepest level.**
The process for designing trustworthy agent workflows now has structural verification of its own data layer. The same principle — verify before trust, check before commit, prevent by design — is applied to the CAWDP knowledge graph itself.

**2. The two-layer architecture maps directly to CC-1's three levels.**
File-based (structural) → Database-based (semantic) → Human review (authority). This isn't an accident. It's the same enforcement regime pattern that appears in the quasi-smart contract model (Regime 1/2/3) and the verification independence principle (structural/semantic/authority).

**3. The rule catalog IS curriculum.**
Every rule traces to a retro pattern. Every retro pattern is a real failure mode that happened 4/6 times or more. "Type Collision at the Schema Layer" isn't abstract theory — it's the codification of actual pain, teachable as a Future's Edge module.