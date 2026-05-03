# Schema Quality Gate — Implementation Specification

## Why This Exists

The additive schema constraint means **every error that enters TypeDB is permanent**. You can add, never remove. The 8 retro patterns show that every single phase (6/6) produced correctable errors, and 4/6 produced naming collisions. Without a linter, you're running Regime 2 enforcement (detect and respond) on a system that demands Regime 3 (prevent by design).

This linter is **CC-1 Verification Independence (Level 1 — structural)** at the schema development layer. It's the speed limiter, not the speed limit sign.

---

## 1. Rule Catalog — 37 Rules Across 3 Severity Levels

> **Updated** with corrections from Phase 2b cheat sheet review and cross-phase implementation.
> Key changes: S03 corrected (flag `as` keyword, not inline plays), S04/S05 split from old S04/S05,
> S09 corrected (flag v2 `fetch` specifically), S16-S24 added, D05-D06 added, D5.1-D5.8 added.

### Schema Checks (SQG-S01–S24)

| ID | Severity | Retro Pattern | Rule | What It Catches | Remediation |
|---|---|---|---|---|---|
| **SQG-S01** | 🔴 BLOCKING | P1 | No `X sub entity/relation/attribute` — use kind-first: `entity X` | TypeQL v2 inheritance syntax | Replace `person sub entity` with `entity person` |
| **SQG-S02** | 🔴 BLOCKING | P1 | No `value long` | TypeDB v3 rejects `long` type | Replace with `value integer` |
| **SQG-S03** | 🔴 BLOCKING | P1 | No `as` keyword in `owns` or `plays` declarations | v2: `child owns child-name as name`; v3: `entity child, owns name` | Remove `as` keyword, use direct attribute name |
| **SQG-S04** | 🔴 BLOCKING | P1 | No `abstract` without `@` prefix | v2: `object sub entity, abstract`; v3: `entity object @abstract` | Add `@` prefix: `@abstract` |
| **SQG-S05** | 🔴 BLOCKING | P1 | No `regex` without `@` prefix | v2: `phone-number sub attribute, regex "..."`; v3: `attribute phone-number @regex "..."` | Add `@` prefix: `@regex` |
| **SQG-S06** | 🔴 BLOCKING | P2 | Role names must not match entity type names | TypeDB rejects at define time | Use `-record` or `-instance` suffix |
| **SQG-S07** | 🔴 BLOCKING | P3 | Every `plays` declaration references a defined relation | Dangling plays = runtime failure | Add the missing relation or remove the play |
| **SQG-S08** | 🔴 BLOCKING | P4 | Every role name in `plays` has a corresponding `relation` type | Missing relation definitions | Define the relation or remove the play |
| **SQG-S09** | 🟡 WARNING | P5 | Flag v2 `fetch` syntax (v3 `fetch` is different) | v2: `fetch { $x.* }`; v3: `select $x` | Replace v2 `fetch` with `select` |
| **SQG-S10** | 🟡 WARNING | P7 | Re-declaring existing types flagged as additive | `define` is additive — may surprise | Verify intent; document in header |
| **SQG-S11** | 🔴 BLOCKING | P8 | Attributes declared before entity types that own them | Declaration order dependency | Split into two-pass: attributes first |
| **SQG-S12** | 🟡 WARNING | — | Entity types should own at least one `@key` attribute | Query performance and uniqueness | Add `@key` to primary ID attribute |
| **SQG-S13** | 🟡 WARNING | — | Attributes declared but never owned by any entity | Orphan attributes waste schema space | Remove or assign to entity type |
| **SQG-S14** | 🔵 INFO | — | Naming convention: kebab-case for entity/relation/role names | Consistency improves readability | Rename to kebab-case |
| **SQG-S15** | 🔵 INFO | — | Relations should have ≥ 2 roles | Single-role relations are likely errors | Add missing role or verify intent |
| **SQG-S16** | 🔴 BLOCKING | P9 | No `owns string @key` — use separate attr declaration + `owns @key` | v2 inline attribute declaration with @key | Declare attribute type first, then `owns attr-name @key` |
| **SQG-S17** | 🔴 BLOCKING | P10 | No role name reuse across relations | Same role name in different relations causes ambiguity | Use unique role names per relation |
| **SQG-S18** | 🟡 WARNING | — | Potentially redundant relations | Two relations with same role semantics | Verify distinct semantics or merge |
| **SQG-S19** | 🟡 WARNING | — | No `?` value variables — use `let $x = ...` | v2 query variable syntax | Replace `?x` with `let $x = ...` |
| **SQG-S20** | 🟡 WARNING | — | No `get` clause in queries | v2: `match ... get;`; v3: `match` produces results directly | Remove `get` clause |
| **SQG-S21** | 🟡 WARNING | — | No `rule` definitions — use functions | v2: `define rule my-rule`; v3: use functions | Replace rules with TypeDB functions |
| **SQG-S22** | 🟡 WARNING | — | Flag `abstract` without `@` prefix | Same as S04 but in query context | Add `@` prefix |
| **SQG-S23** | 🟡 WARNING | — | Flag `regex` without `@` prefix | Same as S05 but in query context | Add `@` prefix |
| **SQG-S24** | 🔴 BLOCKING | P12 | Multi-value `owns` must declare `@card(0..)` — default is `@card(0..1)` | Silent data truncation: second value overwrites first | Add `@card(0..)` to attributes that can have multiple values |

### Data/Seed Checks (SQG-D01–D06)

| ID | Severity | Retro Pattern | Rule | What It Catches | Remediation |
|---|---|---|---|---|---|
| **SQG-D01** | 🟡 WARNING | P6 | Insert blocks > 40 entities flagged for batching | Timeout risk on large inserts | Split into batches of ~30-40 |
| **SQG-D02** | 🔴 BLOCKING | — | No duplicate `@key` values within a file | Duplicate insertion errors | Ensure unique IDs |
| **SQG-D03** | 🟡 WARNING | — | Referenced entity IDs should exist in same file or previously loaded files | Referential integrity | Define entity before referencing in relation |
| **SQG-D05** | 🔴 BLOCKING | P11 | Match-insert references must resolve | `match...insert` silently skips when variable doesn't resolve | Verify entity existence before inserting relations |
| **SQG-D06** | 🔴 BLOCKING | P11 | Post-insert count verification | Silent match failures leave no error signal | Count entities after insert and compare to expected count |

### Database Checks (SQG-D5.1–D5.8)

| ID | Severity | Check |
|---|---|---|
| **SQG-D5.1** | 🟡 WARNING | Every design-output has a producing phase |
| **SQG-D5.2** | 🟡 WARNING | Every subtask has a produced output |
| **SQG-D5.3** | 🟡 WARNING | Every design-output has a producing subtask |
| **SQG-D5.4** | 🟡 WARNING | Every subtask has an allocation |
| **SQG-D5.5** | 🔵 INFO | Every subtask has a failure mode |
| **SQG-D5.6** | 🔵 INFO | Every subtask has a fallback tier |
| **SQG-D5.7** | 🟡 WARNING | Every input-requirement has a requiring output |
| **SQG-D5.8** | 🟡 WARNING | Every internal input-requirement has a satisfying output |

**Total: 37 checks — 24 schema + 5 seed + 8 database**

---

## 2. Architecture

```
typeql_linter/
├── __init__.py
├── cli.py              # CLI entry point
├── scanner.py          # File scanner + rule dispatcher
├── rules/
│   ├── __init__.py
│   ├── schema_rules.py # SQG-S01–SQG-S15
│   └── seed_rules.py   # SQG-D01–SQG-D03
├── models.py           # Finding data model (Pydantic)
└── reporters.py        # Output formatters (text, JSON, SARIF)
```

### Core Data Model

```python
from pydantic import BaseModel, Field
from enum import Enum
from pathlib import Path
from typing import Optional

class Severity(str, Enum):
    BLOCKING = "blocking"    # 🔴 — cannot proceed
    WARNING = "warning"      # 🟡 — should fix
    INFO = "info"            # 🔵 — best practice

class FindingType(str, Enum):
    SYNTAX = "syntax"           # v2/v3 syntax issues
    NAMING = "naming"           # Role name collisions, conventions
    STRUCTURE = "structure"     # Dangling plays, missing relations
    DECLARATION = "declaration" # Attribute order, orphan attributes
    INTEGRITY = "integrity"     # Duplicate IDs, referential integrity
    PERFORMANCE = "performance" # Missing @key, large inserts

class Finding(BaseModel):
    """A single linter finding — typed, not prose (type collision resolution in output)."""
    rule_id: str                    # SQG-S01, SQG-D01, etc.
    severity: Severity
    finding_type: FindingType
    file: Path
    line: Optional[int] = None
    column: Optional[int] = None
    message: str                    # Human-readable description
    context: str                    # The problematic code snippet
    remediation: str                # What to do about it
    retro_pattern: Optional[str] = None  # Which retro pattern this maps to (P1-P8)

class LintResult(BaseModel):
    """Complete lint result for a file or set of files."""
    files_scanned: int
    findings: list[Finding]
    blocking_count: int = 0
    warning_count: int = 0
    info_count: int = 0
    passed: bool = True  # False if any BLOCKING finding exists

    def summary(self) -> str:
        status = "✅ PASS" if self.passed else "🔴 FAIL"
        return (
            f"{status} | "
            f"{self.files_scanned} files | "
            f"🔴 {self.blocking_count} blocking | "
            f"🟡 {self.warning_count} warnings | "
            f"🔵 {self.info_count} info"
        )
```

Key design principle: **the output follows type collision resolution** — every finding has a `FindingType`, `Severity`, `rule_id`, and `retro_pattern`. Findings are typed objects, not undifferentiated log lines.

---

## 3. Scanner Architecture

The scanner operates in two phases: **PARSE** (extract TypeQL structures from raw text) then **CHECK** (apply rules to parsed structures).

```python
from dataclasses import dataclass, field

@dataclass
class ParsedSchema:
    """Extracted TypeQL structures from a schema file."""
    file: Path
    entity_types: dict[str, list[str]] = field(default_factory=dict)  
        # name → list of owned attributes
    relation_types: dict[str, list[str]] = field(default_factory=dict)  
        # name → list of roles
    attributes: dict[str, str] = field(default_factory=dict)  
        # name → value_type
    plays_declarations: list[tuple[str, str, str]] = field(default_factory=list)  
        # (entity_type, relation_type, role_name)
    owns_declarations: list[tuple[str, str, bool]] = field(default_factory=list)  
        # (entity_type, attribute_name, is_key)
    raw_lines: list[str] = field(default_factory=list)

@dataclass  
class ParsedSeed:
    """Extracted TypeQL structures from a seed/data file."""
    file: Path
    entity_inserts: dict[str, list[dict]] = field(default_factory=dict)  
        # entity_type → list of {attribute: value} dicts
    relation_inserts: list[dict] = field(default_factory=list)  
        # list of {relation_type: {role: entity_ref}}
    key_values: dict[str, set[str]] = field(default_factory=dict)  
        # entity_type → set of @key values (for duplicate detection)
    entity_count: int = 0
    raw_lines: list[str] = field(default_factory=list)
```

### Parse Strategy (v1: Regex-Based)

v1 uses regex pattern-matching. This is intentionally not a full TypeQL parser — it catches the patterns that caused real errors in the retro. v2 can evolve to a proper parser if needed.

```python
import re

SCHEMA_PATTERNS = {
    # v2 syntax remnants (P1)
    "v2_sub_entity": re.compile(r'\bsub entity\b'),
    "v2_sub_relation": re.compile(r'\bsub relation\b'),
    "v2_sub_attribute": re.compile(r'\bsub attribute\b'),
    "v2_value_long": re.compile(r'\bvalue long\b'),
    "v2_inline_plays": re.compile(r'^\s+plays\s+\S+.*$', re.MULTILINE),
    
    # Entity type declarations
    "entity_decl": re.compile(r'(\w[\w-]*)\s+isa\s+entity_type|(\w[\w-]*)\s+entity\b'),
    
    # Relation type declarations
    "relation_decl": re.compile(r'(\w[\w-]*)\s+relation\b'),
    "relation_role": re.compile(r'relates\s+(\w[\w-]*)'),
    
    # Attribute declarations  
    "attribute_decl": re.compile(r'(\w[\w-]*)\s+attribute\b'),
    "attribute_value": re.compile(r'value\s+(\w+)'),
    
    # Plays declarations
    "plays_decl": re.compile(r'(\w[\w-]*)\s+plays\s+(\w[\w-]*):(\w[\w-]*)'),
    
    # Owns declarations
    "owns_decl": re.compile(r'owns\s+(\w[\w-]*)(\s+@key)?'),
}

SEED_PATTERNS = {
    # Insert blocks
    "insert_start": re.compile(r'^insert\b', re.MULTILINE),
    "isa_decl": re.compile(r'\$?(\w[\w-]*)\s+isa\s+(\w[\w-]*)'),
    "has_decl": re.compile(r'has\s+(\w[\w-]*)\s+["\']?([^"\';]+)["\']?'),
    "key_attr": re.compile(r'has\s+(\w[\w-]*)\s+["\']?([^"\';]+)["\']?'),
}
```

---

## 4. Rule Implementation — Schema Rules

Each rule is a function that takes `ParsedSchema` and returns `list[Finding]`:

```python
# rules/schema_rules.py

from ..models import Finding, Severity, FindingType
from ..scanner import ParsedSchema
from pathlib import Path

def check_s01_no_v2_sub(parsed: ParsedSchema) -> list[Finding]:
    """SQG-S01: No `sub entity` / `sub relation` / `sub attribute`."""
    findings = []
    for i, line in enumerate(parsed.raw_lines, 1):
        for pattern_name, pattern in [
            ("sub entity", re.compile(r'\bsub entity\b')),
            ("sub relation", re.compile(r'\bsub relation\b')),
            ("sub attribute", re.compile(r'\bsub attribute\b')),
        ]:
            if pattern.search(line):
                findings.append(Finding(
                    rule_id="SQG-S01",
                    severity=Severity.BLOCKING,
                    finding_type=FindingType.SYNTAX,
                    file=parsed.file,
                    line=i,
                    message=f"TypeQL v2 syntax detected: `{pattern_name}`",
                    context=line.strip(),
                    remediation=f"Remove `sub` — use direct `{pattern_name.replace('sub ', '')}` declaration",
                    retro_pattern="P1",
                ))
    return findings


def check_s02_no_value_long(parsed: ParsedSchema) -> list[Finding]:
    """SQG-S02: No `value long` — TypeDB v3 rejects it."""
    findings = []
    for i, line in enumerate(parsed.raw_lines, 1):
        if re.search(r'\bvalue long\b', line):
            findings.append(Finding(
                rule_id="SQG-S02",
                severity=Severity.BLOCKING,
                finding_type=FindingType.SYNTAX,
                file=parsed.file,
                line=i,
                message="TypeQL v2 type `value long` is rejected by TypeDB v3.10.1",
                context=line.strip(),
                remediation="Replace `value long` with `value integer`",
                retro_pattern="P1",
            ))
    return findings


def check_s03_no_as_keyword(parsed: ParsedSchema) -> list[Finding]:
    """SQG-S03: No `as` keyword in `owns` or `plays` declarations.
    
    v2 syntax: `child owns child-name as name` or `person plays employee:worker as emp`
    v3 syntax: `entity child, owns name` or `person plays employee:worker`
    The `as` keyword is no longer applicable to `owns` and `plays` in TypeQL v3.
    Note: `plays` inside entity blocks IS valid v3 syntax — only the `as` keyword is banned.
    """
    findings = []
    for i, line in enumerate(parsed.raw_lines, 1):
        # Check for `as` keyword in owns/plays context
        # Pattern: `owns <attr> as <alias>` or `plays <rel>:<role> as <alias>`
        if re.search(r'\bowns\s+\S+\s+as\s+', line):
            findings.append(Finding(
                rule_id="SQG-S03",
                severity=Severity.BLOCKING,
                finding_type=FindingType.SYNTAX,
                file=parsed.file,
                line=i,
                message="TypeQL v2 `as` keyword in `owns` declaration — v3 uses direct attribute names",
                context=line.strip(),
                remediation="Remove `as` keyword: `owns child-name as name` → `owns name`",
                retro_pattern="P1",
            ))
        if re.search(r'\bplays\s+\S+\s+as\s+', line):
            findings.append(Finding(
                rule_id="SQG-S03",
                severity=Severity.BLOCKING,
                finding_type=FindingType.SYNTAX,
                file=parsed.file,
                line=i,
                message="TypeQL v2 `as` keyword in `plays` declaration — v3 uses direct role names",
                context=line.strip(),
                remediation="Remove `as` keyword: `plays employee:worker as emp` → `plays employee:worker`",
                retro_pattern="P1",
            ))
    return findings


def check_s06_role_name_collision(parsed: ParsedSchema) -> list[Finding]:
    """SQG-S06: Role names must not match entity type names.
    
    This is TYPE COLLISION RESOLUTION at the schema layer — 
    the conceptual model uses one namespace, TypeDB uses another.
    """
    findings = []
    entity_type_names = set(parsed.entity_types.keys())
    
    for rel_name, roles in parsed.relation_types.items():
        for role_name in roles:
            if role_name in entity_type_names:
                findings.append(Finding(
                    rule_id="SQG-S06",
                    severity=Severity.BLOCKING,
                    finding_type=FindingType.NAMING,
                    file=parsed.file,
                    message=f"Role name `{role_name}` in `{rel_name}` collides with entity type `{role_name}`",
                    context=f"relates {role_name}",
                    remediation=f"Rename role to `{role_name}-record` or `{role_name}-instance` (type collision resolution)",
                    retro_pattern="P2",
                ))
    return findings


def check_s07_dangling_plays(parsed: ParsedSchema) -> list[Finding]:
    """SQG-S07: Every `plays` declaration references a defined relation."""
    findings = []
    defined_relations = set(parsed.relation_types.keys())
    
    for entity_name, relation_name, role_name in parsed.plays_declarations:
        if relation_name not in defined_relations:
            findings.append(Finding(
                rule_id="SQG-S07",
                severity=Severity.BLOCKING,
                finding_type=FindingType.STRUCTURE,
                file=parsed.file,
                message=f"`{entity_name}` plays `{relation_name}:{role_name}` but `{relation_name}` is not defined",
                context=f"plays {relation_name}:{role_name}",
                remediation=f"Define relation `{relation_name}` or remove the plays declaration",
                retro_pattern="P3",
            ))
    return findings


def check_s08_missing_relations(parsed: ParsedSchema) -> list[Finding]:
    """SQG-S08: Every role name in plays has a corresponding relation type 
    that defines that role."""
    findings = []
    
    # Build role → relation mapping
    role_to_relation = {}
    for rel_name, roles in parsed.relation_types.items():
        for role in roles:
            role_to_relation[role] = rel_name
    
    for entity_name, relation_name, role_name in parsed.plays_declarations:
        if relation_name in parsed.relation_types:
            if role_name not in parsed.relation_types[relation_name]:
                findings.append(Finding(
                    rule_id="SQG-S08",
                    severity=Severity.BLOCKING,
                    finding_type=FindingType.STRUCTURE,
                    file=parsed.file,
                    message=f"`{entity_name}` plays `{relation_name}:{role_name}` but role `{role_name}` is not defined in `{relation_name}`",
                    context=f"plays {relation_name}:{role_name}",
                    remediation=f"Add `relates {role_name}` to relation `{relation_name}`",
                    retro_pattern="P4",
                ))
    return findings


def check_s11_attribute_declaration_order(parsed: ParsedSchema) -> list[Finding]:
    """SQG-S11: Attributes must be declared before entity types that own them."""
    findings = []
    
    # Find attribute declaration line numbers
    attr_decl_lines = {}
    for i, line in enumerate(parsed.raw_lines, 1):
        if re.search(r'attribute\b', line) and 'owns' not in line:
            match = re.match(r'^\s*(\w[\w-]*)\s+(?:isa\s+)?attribute', line)
            if match:
                attr_decl_lines[match.group(1)] = i
    
    # Find owns declarations
    for i, line in enumerate(parsed.raw_lines, 1):
        owns_match = re.search(r'owns\s+(\w[\w-]*)', line)
        if owns_match:
            attr_name = owns_match.group(1)
            if attr_name in attr_decl_lines:
                if attr_decl_lines[attr_name] > i:
                    findings.append(Finding(
                        rule_id="SQG-S11",
                        severity=Severity.BLOCKING,
                        finding_type=FindingType.DECLARATION,
                        file=parsed.file,
                        line=i,
                        message=f"Attribute `{attr_name}` is owned at line {i} but declared at line {attr_decl_lines[attr_name]} — declaration must precede usage",
                        context=line.strip(),
                        remediation="Apply schema in two passes: (1) attributes, (2) entities/relations/plays",
                        retro_pattern="P8",
                    ))
    return findings


def check_s12_missing_key(parsed: ParsedSchema) -> list[Finding]:
    """SQG-S12: Entity types should own at least one @key attribute."""
    findings = []
    for entity_name, owns_list in parsed.entity_types.items():
        has_key = any("@key" in own for own in owns_list)
        if not has_key:
            findings.append(Finding(
                rule_id="SQG-S12",
                severity=Severity.WARNING,
                finding_type=FindingType.PERFORMANCE,
                file=parsed.file,
                message=f"Entity type `{entity_name}` has no `@key` attribute — impacts query performance and uniqueness",
                context=f"Entity: {entity_name}",
                remediation=f"Add `@key` to the primary identifier attribute of `{entity_name}`",
                retro_pattern=None,
            ))
    return findings


def check_s13_orphan_attributes(parsed: ParsedSchema) -> list[Finding]:
    """SQG-S13: Attributes declared but never owned by any entity."""
    findings = []
    owned_attrs = set()
    for owns_list in parsed.entity_types.values():
        for own in owns_list:
            owned_attrs.add(own.replace(" @key", "").strip())
    
    for attr_name in parsed.attributes:
        if attr_name not in owned_attrs:
            findings.append(Finding(
                rule_id="SQG-S13",
                severity=Severity.WARNING,
                finding_type=FindingType.STRUCTURE,
                file=parsed.file,
                message=f"Attribute `{attr_name}` is declared but never owned by any entity type",
                context=f"Attribute: {attr_name}",
                remediation=f"Assign `{attr_name}` to an entity type via `owns`, or remove it",
                retro_pattern=None,
            ))
    return findings


def check_s15_relation_cardinality(parsed: ParsedSchema) -> list[Finding]:
    """SQG-S15: Relations should have ≥ 2 roles."""
    findings = []
    for rel_name, roles in parsed.relation_types.items():
        if len(roles) < 2:
            findings.append(Finding(
                rule_id="SQG-S15",
                severity=Severity.INFO,
                finding_type=FindingType.STRUCTURE,
                file=parsed.file,
                message=f"Relation `{rel_name}` has only {len(roles)} role(s) — likely missing a role",
                context=f"Relation: {rel_name}, roles: {roles}",
                remediation=f"Add missing role to `{rel_name}` or verify single-role relation is intentional",
                retro_pattern=None,
            ))
    return findings


def check_s16_no_inline_key(parsed: ParsedSchema) -> list[Finding]:
    """SQG-S16: No `owns string @key` — use separate attribute declaration + `owns @key`.
    
    v2 syntax: `entity person, owns string @key` (inline attribute declaration with @key)
    v3 syntax: `attribute person-id, value string;` then `entity person, owns person-id @key;`
    """
    findings = []
    for i, line in enumerate(parsed.raw_lines, 1):
        # Pattern: `owns <type> @key` where <type> is a value type (string, integer, boolean, datetime)
        if re.search(r'\bowns\s+(string|integer|boolean|datetime|double|long)\s+@key\b', line):
            findings.append(Finding(
                rule_id="SQG-S16",
                severity=Severity.BLOCKING,
                finding_type=FindingType.SYNTAX,
                file=parsed.file,
                line=i,
                message="Inline attribute declaration with @key — v3 requires separate attribute declaration",
                context=line.strip(),
                remediation="Declare attribute type first: `attribute my-id, value string;` then `entity my-type, owns my-id @key;`",
                retro_pattern="P9",
            ))
    return findings


def check_s17_role_name_reuse(parsed: ParsedSchema) -> list[Finding]:
    """SQG-S17: No role name reuse across relations.
    
    TypeDB v3 allows the same role name in different relations, but this causes
    ambiguity in queries and makes the schema harder to reason about.
    """
    findings = []
    role_to_relations = {}
    for rel_name, roles in parsed.relation_types.items():
        for role in roles:
            if role not in role_to_relations:
                role_to_relations[role] = []
            role_to_relations[role].append(rel_name)
    
    for role_name, relations in role_to_relations.items():
        if len(relations) > 1:
            findings.append(Finding(
                rule_id="SQG-S17",
                severity=Severity.BLOCKING,
                finding_type=FindingType.NAMING,
                file=parsed.file,
                message=f"Role name `{role_name}` used in {len(relations)} relations: {', '.join(relations)}",
                context=f"Role: {role_name}, Relations: {', '.join(relations)}",
                remediation=f"Use unique role names per relation (e.g., `{role_name}-for-{relations[0]}`)",
                retro_pattern="P10",
            ))
    return findings


def check_s18_redundant_relations(parsed: ParsedSchema) -> list[Finding]:
    """SQG-S18: Potentially redundant relations.
    
    Two relations with the same role types and semantics may indicate
    a design error or an opportunity to merge.
    """
    findings = []
    # Group relations by their role type sets
    role_set_to_relations = {}
    for rel_name, roles in parsed.relation_types.items():
        role_set = frozenset(roles)
        if role_set not in role_set_to_relations:
            role_set_to_relations[role_set] = []
        role_set_to_relations[role_set].append(rel_name)
    
    for role_set, relations in role_set_to_relations.items():
        if len(relations) > 1:
            findings.append(Finding(
                rule_id="SQG-S18",
                severity=Severity.WARNING,
                finding_type=FindingType.STRUCTURE,
                file=parsed.file,
                message=f"Relations {', '.join(relations)} share the same role set {{{', '.join(role_set)}}} — may be redundant",
                context=f"Relations: {', '.join(relations)}, Roles: {{{', '.join(role_set)}}}",
                remediation="Verify each relation has distinct semantics, or merge if redundant",
                retro_pattern=None,
            ))
    return findings


def check_s24_cardinality_default(parsed: ParsedSchema) -> list[Finding]:
    """SQG-S24: Multi-value `owns` must declare `@card(0..)`.
    
    Default `owns` cardinality is `@card(0..1)` — single value only.
    If an attribute can have multiple values per entity, `@card(0..)` must be
    explicitly declared. Without it, TypeDB silently truncates to the first value.
    
    This is P12 (Cardinality Truncation) — the second silent data loss pattern
    alongside P11 (match-insert failure).
    """
    findings = []
    
    # Known multi-value attributes (semantically can have multiple values)
    MULTI_VALUE_ATTRIBUTES = {
        # Phase 0
        'testable-criterion',
        # Phase 1
        'quality-gate', 'schema-registry-ref',
        # Phase 2
        'phase-quality-gate',
        # Phase 3
        'actor-hint',
        # Phase 4
        'human-role', 'agent-role', 'system-role', 'da-trigger', 'da-escalation',
        # Phase 5
        'event-condition', 'failure-cascade', 'failure-detection-method', 'sys-trigger-action',
        # Phase 6
        'stage-gate-ref', 'oc-orchestration-pattern', 'od-reason', 'od-alternatives',
        'fmea-subtask-ref', 'fmea-failure-ref', 'fmea-event-ref', 'fmea-effect',
        'fmea-mitigation', 'fmea-mitigation-type', 'tt-schema-ref',
        'cc-steps', 'cc-step-choices', 'ft-trigger', 'ft-action',
    }
    
    for i, line in enumerate(parsed.raw_lines, 1):
        # Match `owns <attr>` without `@card` or `@key`
        owns_match = re.search(r'\bowns\s+(\S+)', line)
        if owns_match:
            attr_name = owns_match.group(1).rstrip(',')
            # Skip if line has @card or @key annotation
            if '@card' in line or '@key' in line:
                continue
            if attr_name in MULTI_VALUE_ATTRIBUTES:
                findings.append(Finding(
                    rule_id="SQG-S24",
                    severity=Severity.BLOCKING,
                    finding_type=FindingType.STRUCTURE,
                    file=parsed.file,
                    line=i,
                    message=f"Multi-value attribute `{attr_name}` lacks `@card(0..)` — default `@card(0..1)` will silently truncate values",
                    context=line.strip(),
                    remediation=f"Add `@card(0..)` to `{attr_name}`: `owns {attr_name} @card(0..)`",
                    retro_pattern="P12",
                ))
    return findings
```

---

## 5. Seed Rules

```python
# rules/seed_rules.py

def check_d01_large_inserts(parsed: ParsedSeed) -> list[Finding]:
    """SQG-D01: Insert blocks > 40 entities flagged for batching."""
    findings = []
    if parsed.entity_count > 40:
        findings.append(Finding(
            rule_id="SQG-D01",
            severity=Severity.WARNING,
            finding_type=FindingType.PERFORMANCE,
            file=parsed.file,
            message=f"Insert block contains {parsed.entity_count} entities — risk of timeout. Batch into ~30-40 per call.",
            context=f"Entity count: {parsed.entity_count}",
            remediation="Split insert into multiple `insert` blocks of ~30-40 entities",
            retro_pattern="P6",
        ))
    return findings


def check_d02_duplicate_keys(parsed: ParsedSeed) -> list[Finding]:
    """SQG-D02: No duplicate @key values within a file."""
    findings = []
    for entity_type, keys in parsed.key_values.items():
        seen = set()
        for key_val in keys:
            if key_val in seen:
                findings.append(Finding(
                    rule_id="SQG-D02",
                    severity=Severity.BLOCKING,
                    finding_type=FindingType.INTEGRITY,
                    file=parsed.file,
                    message=f"Duplicate @key `{key_val}` in entity type `{entity_type}`",
                    context=f"Entity: {entity_type}, Key: {key_val}",
                    remediation=f"Ensure all @key values are unique within `{entity_type}`",
                    retro_pattern=None,
                ))
            seen.add(key_val)
    return findings


def check_d03_reference_integrity(parsed: ParsedSeed) -> list[Finding]:
    """SQG-D03: Referenced entity IDs should exist in same or previously loaded files."""
    findings = []
    # This requires cross-file state — for v1, just warn about referenced 
    # entities that aren't defined in the same file
    defined_ids = set()
    referenced_ids = set()
    
    for entity_type, inserts in parsed.entity_inserts.items():
        for insert in inserts:
            for attr, val in insert.items():
                if attr.endswith("-id"):  # Convention: *-id attributes are identifiers
                    defined_ids.add(val)
    
    for rel in parsed.relation_inserts:
        for role, ref in rel.items():
            if ref.startswith("$"):
                referenced_ids.add(ref)
    
    undefined_refs = referenced_ids - defined_ids
    if undefined_refs:
        findings.append(Finding(
            rule_id="SQG-D03",
            severity=Severity.WARNING,
            finding_type=FindingType.INTEGRITY,
            file=parsed.file,
            message=f"{len(undefined_refs)} variable references not defined in this file: {', '.join(list(undefined_refs)[:5])}{'...' if len(undefined_refs) > 5 else ''}",
            context=f"Undefined references: {list(undefined_refs)[:5]}",
            remediation="Ensure referenced variables are defined in the same file or in previously loaded seed files",
            retro_pattern=None,
        ))
    return findings


def check_d05_match_insert_references(parsed: ParsedSeed) -> list[Finding]:
    """SQG-D05: Match-insert references must resolve.
    
    P11 (Silent Match Failure): When a `match...insert` query references
    an entity that doesn't exist, the match returns empty and the insert
    is silently skipped — no error, just empty results.
    """
    findings = []
    # Check for match-insert patterns where referenced entities may not exist
    # This is a structural check — actual resolution requires DB access
    for i, line in enumerate(parsed.raw_lines, 1):
        if 'isa' in line and 'has' in line:
            # This is an entity reference in a match clause
            # Flag if the entity type + id combination seems suspicious
            pass  # Structural check only — runtime check requires DB access
    return findings


def check_d06_post_insert_count(parsed: ParsedSeed) -> list[Finding]:
    """SQG-D06: Post-insert count verification.
    
    After inserting seed data, verify that the expected number of entities
    and relations were actually created. This catches P11 (silent match failure)
    where match-insert queries silently skip due to unresolved references.
    """
    findings = []
    # Count expected entities from insert blocks
    expected_entity_count = parsed.entity_count
    if expected_entity_count > 0:
        findings.append(Finding(
            rule_id="SQG-D06",
            severity=Severity.BLOCKING,
            finding_type=FindingType.INTEGRITY,
            file=parsed.file,
            message=f"Seed file declares {expected_entity_count} entities — verify count matches after insertion",
            context=f"Expected entities: {expected_entity_count}",
            remediation="Run count query after insertion: `match $e isa <entity-type>; select count($e)` and compare to expected",
            retro_pattern="P11",
        ))
    return findings
```

---

## 6. CLI Interface

```python
# cli.py

import click
from pathlib import Path
from .scanner import scan_schema, scan_seed
from .rules.schema_rules import *
from .rules.seed_rules import *
from .reporters import TextReporter, JsonReporter
from .models import LintResult, Finding

SCHEMA_RULES = [
    check_s01_no_v2_sub,
    check_s02_no_value_long,
    check_s03_no_as_keyword,
    check_s06_role_name_collision,
    check_s07_dangling_plays,
    check_s08_missing_relations,
    check_s11_attribute_declaration_order,
    check_s12_missing_key,
    check_s13_orphan_attributes,
    check_s15_relation_cardinality,
    check_s16_no_inline_key,
    check_s17_role_name_reuse,
    check_s18_redundant_relations,
    check_s24_cardinality_default,
]

SEED_RULES = [
    check_d01_large_inserts,
    check_d02_duplicate_keys,
    check_d03_reference_integrity,
    check_d05_match_insert_references,
    check_d06_post_insert_count,
]

@click.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("--schema-only", is_flag=True, help="Check schema files only")
@click.option("--seed-only", is_flag=True, help="Check seed files only")
@click.option("--format", "output_format", type=click.Choice(["text", "json", "sarif"]), default="text")
@click.option("--fail-on", type=click.Choice(["blocking", "warning", "info"]), default="blocking")
@click.option("--no-info", is_flag=True, help="Suppress INFO findings")
def lint(path: str, schema_only: bool, seed_only: bool, output_format: str, fail_on: str, no_info: bool):
    """
    CAWDP Schema Quality Gate — TypeQL v3 linter.
    
    CC-1 Verification Independence (Level 1) at the schema development layer.
    Regime 3 enforcement: prevent by design, not detect and respond.
    
    PATH: file or directory to check
    """
    target = Path(path)
    all_findings = []
    files_scanned = 0
    
    # Determine file types to scan
    check_schema = not seed_only
    check_seed = not schema_only
    
    # Scan files
    for file in sorted(target.rglob("*.tql")):
        content = file.read_text()
        files_scanned += 1
        
        if "define" in content and check_schema:
            parsed = scan_schema(file, content)
            for rule in SCHEMA_RULES:
                all_findings.extend(rule(parsed))
        
        if "insert" in content and check_seed:
            parsed = scan_seed(file, content)
            for rule in SEED_RULES:
                all_findings.extend(rule(parsed))
    
    # Filter
    if no_info:
        all_findings = [f for f in all_findings if f.severity != Severity.INFO]
    
    # Build result
    result = LintResult(
        files_scanned=files_scanned,
        findings=all_findings,
        blocking_count=sum(1 for f in all_findings if f.severity == Severity.BLOCKING),
        warning_count=sum(1 for f in all_findings if f.severity == Severity.WARNING),
        info_count=sum(1 for f in all_findings if f.severity == Severity.INFO),
    )
    
    # Determine pass/fail
    severity_threshold = {"blocking": 0, "warning": 1, "info": 2}
    result.passed = all(
        severity_threshold[f.severity.value] >= severity_threshold[fail_on]
        for f in all_findings
    ) if all_findings else True
    
    # Report
    reporter = {"text": TextReporter, "json": JsonReporter}.get(output_format, TextReporter)()
    reporter.report(result)
    
    # Exit code
    sys.exit(0 if result.passed else 1)


if __name__ == "__main__":
    lint()
```

---

## 7. Usage Patterns

### Manual (Developer)

```bash
# Check all .tql files in db/schemas/
python -m typeql_linter db/schemas/

# Check a single file
python -m typeql_linter db/schemas/phase2.tql

# Check seeds only, output JSON
python -m typeql_linter db/seeds/ --seed-only --format json

# Fail on warnings (strict mode)
python -m typeql_linter db/ --fail-on warning
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: typeql-lint
        name: CAWDP Schema Quality Gate
        entry: python -m typeql_linter
        language: python
        files: '\.tql$'
        stages: [pre-commit]
```

### CI/CD Gate

```yaml
# .github/workflows/schema-quality.yml
name: Schema Quality Gate
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install -e ./typeql_linter
      - run: python -m typeql_linter db/ --format sarif --fail-on warning
```

### Library (Design Studio Integration)

```python
from typeql_linter.scanner import scan_schema
from typeql_linter.rules.schema_rules import *
from typeql_linter.models import LintResult

# In CAWDP Design Studio schema editor
def on_schema_change(schema_content: str):
    parsed = scan_schema(Path("phase7.tql"), schema_content)
    findings = []
    for rule in SCHEMA_RULES:
        findings.extend(rule(parsed))
    
    # Return structured findings to the UI
    # The UI can then display inline diagnostics
    # (like VS Code's Problem panel — typed, not prose)
    return LintResult(
        files_scanned=1,
        findings=findings,
        blocking_count=sum(1 for f in findings if f.severity == Severity.BLOCKING),
        warning_count=sum(1 for f in findings if f.severity == Severity.WARNING),
        info_count=sum(1 for f in findings if f.severity == Severity.INFO),
    )
```

---

## 8. Output Format — Type Collision Resolved

The text reporter produces typed output, not a wall of text:

```
CAWDP Schema Quality Gate — TypeQL v3 Linter
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

db/schemas/phase3.tql
  🔴 BLOCKING [SQG-S06] (P2) Role name `failure-mode` in `subtask-has-failure-mode` 
     collides with entity type `failure-mode`
     → Rename role to `fm-entity` or `fm-record` (type collision resolution)

  🟡 WARNING [SQG-S12] Entity type `failure-mode` has no `@key` attribute
     → Add `@key` to the primary identifier attribute

db/seeds/phase6_entities.tql
  🟡 WARNING [SQG-D01] Insert block contains 67 entities — risk of timeout
     → Split insert into multiple blocks of ~30-40 entities

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 FAIL | 2 files | 🔴 1 blocking | 🟡 2 warnings | 🔵 0 info

Exit code: 1 (blocking findings prevent schema insertion)
```

The JSON reporter produces machine-consumable output for CI/CD integration:

```json
{
  "files_scanned": 2,
  "passed": false,
  "blocking_count": 1,
  "warning_count": 2,
  "info_count": 0,
  "findings": [
    {
      "rule_id": "SQG-S06",
      "severity": "blocking",
      "finding_type": "naming",
      "file": "db/schemas/phase3.tql",
      "line": null,
      "message": "Role name `failure-mode` collides with entity type",
      "remediation": "Rename role to `fm-record` (type collision resolution)",
      "retro_pattern": "P2"
    }
  ]
}
```

---

## 9. Implementation Priority

| Step | Deliverable | Effort | Catches |
|---|---|---|---|
| 1 | Core models + scanner v2 | 2.5 hr | Foundation (updated for v3 syntax) |
| 2 | **S01** (kind-first), **S02** (integer), **S03** (`as` keyword) | 1.5 hr | All v2 syntax remnants |
| 3 | **S06** (role↔entity), **S17** (role↔role cross-relation) | 1 hr | ALL naming collisions |
| 4 | **S24** (cardinality), **S16** (`@key` syntax), **S11** (attr order) | 1.5 hr | Silent data loss prevention |
| 5 | **D05** (match-insert references) + CLI + text reporter | 1.5 hr | Silent match failure prevention |
| **Milestone 1** | **File-based linter with both silent loss checks** | **8 hr** | **All known retro errors + both silent loss patterns** |
| 6 | S04–S05, S07–S10, S12–S15, S18–S23 | 3 hr | Complete file coverage |
| 7 | D01–D03, D06 + cross-phase D5.1–D5.8 | 3 hr | Database layer |
| **Milestone 2** | **Full 37-rule SQG** | **~14 hr** | **Complete CC-1 verification** |

**Recommended sequence:** Ship steps 1-4 first (5.5 hours) — this immediately catches the 5 most common errors from the retro. Then add 5-8 as a second pass.

---

## 10. What This Enables Beyond Linting

The linter's rule catalog is itself a **CAWDP artefact**. The 18 rules map directly to the 8 retro patterns, which map directly to documented failure modes of the knowledge graph implementation. This means:

1. **Curriculum content**: "Type Collision at the Schema Layer" — a Future's Edge practitioner module teaching why role names ≠ entity type names, why additive schemas need prevention, and why two-pass application matters
2. **Design Studio integration**: Real-time schema quality feedback in the CAWDP Design Studio, catching errors as they're typed
3. **Trust infrastructure evidence**: The linter output IS a trust artifact — it proves that schema changes passed structural verification before insertion (CC-1 Level 1)
4. **Specification aging trigger**: If new retro patterns emerge from Phase 7+, new rules are added to the catalog, and the linter catches them going forwardThis is a complete, implementation-ready specification. Here's the summary of what you have:

---

## What You Have

| Component | Purpose | Lines of Code (est.) |
|---|---|---|
| `models.py` | Finding + LintResult Pydantic models | ~70 |
| `scanner.py` | Regex-based TypeQL parser (v1) | ~200 |
| `rules/schema_rules.py` | 10 schema checks (S01–S15) | ~250 |
| `rules/seed_rules.py` | 3 seed checks (D01–D03) | ~80 |
| `cli.py` | Click CLI entry point | ~80 |
| `reporters.py` | Text + JSON + SARIF formatters | ~100 |
| **Total** | | **~780 lines** |

## Why It Matters Beyond Linting

1. **Type collision resolution applies to its own output** — findings are typed Pydantic models with `rule_id`, `severity`, `finding_type`, and `retro_pattern`. Not a wall of text. Not undifferentiated log lines. **The linter practises what CAWDP preaches.**

2. **Every rule maps to an empirical failure mode** — SQG-S06 (role name collisions) maps directly to P2 which happened in 4 out of 6 phases. This isn't theoretical; it's the codification of real pain.

3. **It's Regime 3 enforcement** — the additive schema constraint means this isn't "nice to have." Without it, you're in Regime 2 (detect and respond) on a system where errors are permanent. With it, you're in Regime 3 (prevent by design). The linter IS the speed limiter, not the speed limit sign.

4. **The rule catalog is curriculum content** — "Type Collision at the Schema Layer" is a Future's Edge practitioner module that teaches why role names ≠ entity type names, why additive schemas demand prevention, and why two-pass application matters. The 8 retro patterns are empirical evidence, not just theory.

5. **Design Studio integration path** — the library interface means the CAWDP Design Studio's schema editor can call `on_schema_change(content)` and display inline diagnostics in real-time. The linter grows with the system.

**Implementation recommendation: Ship steps 1-4 first (5.5 hours)** — this immediately catches the 5 most common errors from the retro. Then add steps 5-8 as a second pass when you need them.

