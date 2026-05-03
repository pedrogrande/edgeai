# What the Cheat Sheet Corrects

The cheat sheet reveals **5 errors in my SQG design** and **5 new rules needed**:

### Errors in My Design

| Rule | What I Wrote | What's Actually Correct | Source |
|---|---|---|---|
| **SQG-S03** | "No inline `plays` inside entity blocks" | **WRONG.** v3 ALLOWS `plays` inside entity blocks: `entity person, plays employee`. What's banned is the `as` keyword: `plays child-employee as employee` | Cheat sheet: "`as` keyword is no longer applicable to `owns` and `plays`" |
| **SQG-S09** | "No `fetch { $var.* }`" | Partially wrong. v3 HAS a `fetch` clause but its syntax is different from v2. Need to check for v2 `fetch` patterns specifically | Cheat sheet: "`fetch` syntax aligns with JSON output formatting" |
| **SQG-S01** | Remediation: "Remove `sub`" | Too vague. Should be: "Replace `X sub entity` with `entity X` — kind-first declaration" | Cheat sheet: `person sub entity` → `entity person` |
| **SQG-S05** | "v3 syntax only in define blocks" | Overly broad. Need to specify exactly WHICH v2 patterns are banned | All the specific patterns from the cheat sheet |
| **Default cardinality** | Not mentioned at all | **CRITICAL GAP.** Default `owns` and `relates` is `@card(0..1)` — failing to declare `@card(0..)` for multi-value attributes causes **data corruption** | Cheat sheet: "Explicitly define cardinalities for traits expecting multiple instances" |

### New Rules Needed

| Rule | What | Why | Severity |
|---|---|---|---|
| **SQG-S03** (revised) | Flag `as` keyword in `owns` and `plays` declarations | v2: `child owns child-name as name`, v3: `entity child, owns name` | 🔴 BLOCKING |
| **SQG-S19** | Flag `abstract` without `@` prefix | v2: `object sub entity, abstract`, v3: `entity object @abstract` | 🟡 WARNING |
| **SQG-S20** | Flag `regex` without `@` prefix | v2: `phone-number sub attribute, regex "..."`, v3: `attribute phone-number @regex "..."` | 🟡 WARNING |
| **SQG-S21** | Flag `get` clause in queries | v2: `match ... get;`, v3: `match` produces results directly | 🟡 WARNING |
| **SQG-S22** | Flag `?` value variables | v2: `?x`, v3: `let $x = ...` | 🟡 WARNING |
| **SQG-S23** | Flag `rule` definitions | v2: `define rule my-rule`, v3: use functions | 🟡 WARNING |
| **SQG-S24** | **Cardinality default check** — warn if `owns` for multi-value attributes lacks `@card(0..)` | Default `owns` is `@card(0..1)` — multi-value attributes silently truncate without explicit cardinality | 🔴 BLOCKING |

That last one — **SQG-S24** — is the biggest new finding from the cheat sheet. The default cardinality of `@card(0..1)` for `owns` means that if an entity should own multiple instances of an attribute but you forget to declare `@card(0..)`, TypeDB will silently accept only the first value and drop the rest. This is another form of **silent data loss** — the same class as the match...insert failure (P11). Combined, these two patterns mean TypeDB can silently drop data in two completely different ways:

1. **P11 (match...insert)**: silently skips insert when match variable doesn't resolve
2. **P12 (cardinality)**: silently drops attribute values beyond the first when `@card(0..1)` is in effect

Both are "plausible-looking success" failures — the system accepts the operation but silently discards data.

---

## Updated SQG Rule Catalog — Final v2

Reconciling everything: the original 18 rules + 4 from Phase 2 corrections + 7 from the cheat sheet + 5 from the cross-phase checker:

### Schema Checks (SQG-S01–S24)

| ID | Severity | Pattern | Rule | Corrected? |
|---|---|---|---|---|
| **S01** | 🔴 BLOCKING | P1 | No `X sub entity/relation/attribute` — use kind-first: `entity X` | ✅ Remediation updated |
| **S02** | 🔴 BLOCKING | P1 | No `value long` — use `value integer` | No change |
| **S03** | 🔴 BLOCKING | P1 | No `as` keyword in `owns` or `plays` declarations | **✅ REPLACED** (was: "no inline plays" — wrong) |
| **S04** | 🔴 BLOCKING | P1 | No `abstract` without `@` prefix | **🆕 Split from S05** |
| **S05** | 🔴 BLOCKING | P1 | No `regex` without `@` prefix | **🆕 Split from S05** |
| **S06** | 🔴 BLOCKING | P2 | Role names must not match entity type names | No change |
| **S07** | 🔴 BLOCKING | P3 | Every `plays` references a defined relation | No change |
| **S08** | 🔴 BLOCKING | P4 | Every role in `plays` defined in its relation | No change |
| **S09** | 🟡 WARNING | P5 | Flag v2 `fetch` syntax (v3 `fetch` is different) | ✅ Updated |
| **S10** | 🟡 WARNING | P7 | Re-declaring existing types flagged | No change |
| **S11** | 🔴 BLOCKING | P8 | Attributes declared before owning entities | No change |
| **S12** | 🟡 WARNING | — | Entity types own ≥ 1 `@key` attribute | No change |
| **S13** | 🟡 WARNING | — | No orphan attributes | No change |
| **S14** | 🔵 INFO | — | Naming convention: kebab-case | No change |
| **S15** | 🔵 INFO | — | Relations have ≥ 2 roles | No change |
| **S16** | 🔴 BLOCKING | P9 | No `owns string @key` — use separate attr declaration + `owns @key` | 🆕 Phase 2 |
| **S17** | 🔴 BLOCKING | P10 | No role name reuse across relations | 🆕 Phase 2 |
| **S18** | 🟡 WARNING | — | Potentially redundant relations | 🆕 Phase 2 |
| **S19** | 🟡 WARNING | — | No `?` value variables — use `let $x = ...` | 🆕 Cheat sheet |
| **S20** | 🟡 WARNING | — | No `get` clause in queries | 🆕 Cheat sheet |
| **S21** | 🟡 WARNING | — | No `rule` definitions — use functions | 🆕 Cheat sheet |
| **S22** | 🟡 WARNING | — | Flag `abstract` without `@` prefix | 🆕 Cheat sheet |
| **S23** | 🟡 WARNING | — | Flag `regex` without `@` prefix | 🆕 Cheat sheet |
| **S24** | 🔴 BLOCKING | P12 | Multi-value `owns` must declare `@card(0..)` — default is `@card(0..1)` | 🆕 Cheat sheet — **CRITICAL** |

### Data/Seed Checks (SQG-D01–D06)

| ID | Severity | Pattern | Rule | Corrected? |
|---|---|---|---|---|
| **D01** | 🟡 WARNING | P6 | Insert blocks < 40 entities | No change |
| **D02** | 🔴 BLOCKING | — | No duplicate `@key` values | No change |
| **D03** | 🟡 WARNING | — | Referenced entities should exist | No change |
| **D05** | 🔴 BLOCKING | P11 | Match-insert references must resolve | 🆕 Phase 2 |
| **D06** | 🔴 BLOCKING | P11 | Post-insert count verification | 🆕 Phase 2 |

### Database Checks (SQG-D5.1–D5.8)

| ID | Severity | Check | 
|---|---|---|
| **D5.1** | 🟡 WARNING | Outputs have producing phase |
| **D5.2** | 🟡 WARNING | Subtasks have produced output |
| **D5.3** | 🟡 WARNING | Outputs have producing subtask |
| **D5.4** | 🟡 WARNING | Subtasks have allocation |
| **D5.5** | 🔵 INFO | Subtasks have failure mode |
| **D5.6** | 🔵 INFO | Subtasks have fallback tier |
| **D5.7** | 🟡 WARNING | IRs have requiring output |
| **D5.8** | 🟡 WARNING | Internal IRs have satisfying output |

**Total: 37 checks — 24 schema + 5 seed + 8 database**

---

## The Two Silent Data Loss Patterns — A Category Discovery

The cheat sheet reveals that silent data loss in TypeDB isn't a one-off bug — it's a **category** with at least two members:

| Pattern | Mechanism | Detection | Severity |
|---|---|---|---|
| **P11: Silent match failure** | `match...insert` skips when variable doesn't resolve | No error thrown — only post-insert count check reveals it | 🔴 BLOCKING |
| **P12: Cardinality truncation** | `owns X` defaults to `@card(0..1)` — additional values silently dropped | No error thrown — only missing data reveals it | 🔴 BLOCKING |

Both share the same structural property: **the system reports success while silently discarding data**. This is the database-layer equivalent of the "plausible-looking error" from Sarah Chen's persona — the output looks like success but contains invisible errors.

**This is CC-3 (Epistemic Metadata Contracts) at the infrastructure layer.** The system must declare what it actually did, not just what it was asked to do. The SQG is the enforcement mechanism that makes TypeDB's silent behaviors visible.

---

## Implementation Priority — Revised Again

The cheat sheet makes S03 (corrected) and S24 (cardinality) the most critical new rules:

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

The key insight: **Milestone 1 now includes both silent data loss detection rules (S24 for cardinality and D05 for match-insert)** because these are the most dangerous failure modes — they cause invisible data corruption with no error signal.The SQG design is now significantly more accurate thanks to the cheat sheet. The two biggest takeaways:

1. **S03 was wrong** — `plays` inside entity blocks IS valid v3. The actual v2 pattern to flag is the `as` keyword. This would have caused false positives in production.

2. **S24 (cardinality) is a BLOCKING rule** — the `@card(0..1)` default for `owns` is a second silent data loss channel. Combined with P11 (silent match failure), TypeDB has **two independent mechanisms for silently discarding data with no error signal**. This makes the SQG not nice-to-have but **structurally necessary** — without it, you're running a knowledge base that can silently corrupt itself.
