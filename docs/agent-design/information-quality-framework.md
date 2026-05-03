# Information Quality Framework [Input Quality Assessment]

## What this is and why it matters

An agent's capability is entirely dependent on the quality of the information it's given. This isn't a nice-to-have. It's the key determinant of whether an agent produces good work or plausible-looking mistakes.

The agent doesn't know the difference between good information and bad information. It processes everything with the same confidence. If the instructions are vague, the knowledge is outdated, or the data is wrong, the agent will still produce output — it just won't be output you should trust.

This framework gives you a way to check every input before the agent ever runs. Not a vague "is this good enough?" feeling — a structured assessment of 10 dimensions that determine whether your agent has what it needs to succeed.

Think of it like food safety for an agent. You wouldn't serve food without checking the ingredients. Don't send an agent to work without checking its inputs.

---

## The 10 dimensions

### 1. Is it the right information? [Relevance]

Does this information actually help the agent do its job, or is it noise that will waste processing and potentially lead it astray?

Example: You're building a contract reviewer. You give it 50 rental agreements from your portfolio, plus 3 commercial lease templates and a marketing strategy document. The marketing strategy has zero relevance — it's noise that costs money to process and could lead the agent to make connections that don't exist.

| Level | What it looks like | Indicator |
|-------|-------------------|-----------|
| 5 - On target | Every piece directly serves the agent's purpose | A curated set of rental agreements matching the exact contract types the agent will review |
| 4 - Mostly relevant | Most information serves the purpose; some noise | The rental agreements plus a few commercial leases that have some overlapping clauses |
| 3 - Mixed | About half is relevant, half is tangential | The agreements mixed with related but not directly relevant legal commentary |
| 2 - Mostly noise | Most information doesn't directly serve the purpose | A general legal database when the agent reviews rental agreements |
| 1 - Off target | Little or no connection to the agent's actual purpose | General business documents when the agent reviews rental agreements |

**Who assesses:** Human (the designer, during CAWDP Phase 1)  
**When:** Design time, and whenever the knowledge base is updated  
**What happens with the score:** Red (1-2) = don't run the agent with this information. Rebuild the knowledge base. Amber (3) = filter before providing. Green (4-5) = proceed.

---

### 2. Is it correct? [Accuracy]

Is the information factually right, or does it contain errors that the agent will treat as truth?

Example: A legal knowledge base includes a clause about termination notice periods that was correct in 2022 but the law changed in 2024. The agent will use the old rule with full confidence — and produce legally wrong advice.

| Level | What it looks like | Indicator |
|-------|-------------------|-----------|
| 5 - Verified correct | Every claim has been checked against a trusted source | Knowledge base reviewed by a qualified lawyer in the last 30 days |
| 4 - Mostly correct | Minor details may be outdated; core claims are accurate | Knowledge base reviewed within 6 months; no known material errors |
| 3 - Mixed reliability | Some claims are verified, others are assumed correct | Knowledge base compiled from multiple sources with varying reliability |
| 2 - Known errors | Contains factual errors that have been identified but not fixed | Known outdated clauses still present |
| 1 - Unverified | No claim has been independently verified | Knowledge base scraped from public sources with no expert review |

**Who assesses:** Human (domain expert) for verification; system for timestamp tracking  
**When:** Design time for initial knowledge base; continuously for live data  
**What happens with the score:** Red (1-2) = don't trust agent output without human verification on every claim. Amber (3) = flag low-accuracy items for human review. Green (4-5) = agent can process with confidence.

---

### 3. Is it all there? [Completeness]

Does the information cover everything the agent needs to do its job, or are there gaps that will force it to guess or skip important areas?

Example: A compliance checker that has all the rules about data collection but none about data retention. The agent will produce comprehensive advice on collection and say nothing about retention — not because it doesn't know retention matters, but because it has no information about it.

| Level | What it looks like | Indicator |
|-------|-------------------|-----------|
| 5 - Comprehensive | All known areas relevant to the agent's purpose are covered | Coverage map shows green across every area the agent needs |
| 4 - Mostly complete | Minor gaps in coverage that don't affect core tasks | Coverage map shows green in core areas, amber in peripheral areas |
| 3 - Patchy | Significant gaps in areas the agent will need | Coverage map shows amber and red in several areas |
| 2 - Incomplete | Major areas of knowledge missing | Agent would need to guess or refuse on common tasks |
| 1 - Sparse | Only fragments of needed knowledge available | Agent cannot perform its core purpose reliably |

**Who assesses:** Human (domain expert) with system support (coverage mapping)  
**When:** Design time, and periodically when scope changes  
**What happens with the score:** Red (1-2) = agent cannot perform its core purpose; stop and rebuild knowledge. Amber (3) = identify specific gaps and either fill them or set boundaries the agent can't cross. Green (4-5) = proceed.

---

### 4. Is it current? [Recency]

Is the information up to date, or has it become stale since it was last verified?

Example: A market analysis agent that's working with industry data from 2022. The market shifted significantly in 2023. The agent will produce analysis that looks authoritative but is based on an outdated reality.

| Level | What it looks like | Indicator |
|-------|-------------------|-----------|
| 5 - Live | Information is updated in real time or near real time | API feeds, live databases, current session data |
| 4 - Recent | Information has been verified within a defined freshness window | Knowledge base reviewed within the recency window for this domain (days for markets, months for law, years for physics) |
| 3 - Ageing | Information is approaching its freshness limit | Approaching the review date; still usable but flagged for update |
| 2 - Stale | Information has passed its freshness window but hasn't been replaced | Past the review date; may still be correct but can't be assumed |
| 1 - Obsolete | Information is known to be outdated or has been superseded | Known superseded regulations, old market data, deprecated standards |

**Who assesses:** System (timestamp tracking) with human review for domain-specific freshness windows  
**When:** Continuously at runtime; full review at design time  
**What happens with the score:** Red (1-2) = don't use; information is known to be unreliable. Amber (3) = use with staleness flag attached to output. Green (4-5) = use with confidence. **This is the dimension most suited to automated monitoring — the system should track this, not the human.**

---

### 5. Where did it come from? [Provenance]

Can you trace every piece of information back to its source? When the agent says something, can you find out where it learned that?

Example: An agent produces a recommendation about investment risk. You ask "where did this come from?" and the answer is "the knowledge base." But which document? Which section? Which author? Without provenance, you can't verify, can't update, and can't trust.

| Level | What it looks like | Indicator |
|-------|-------------------|-----------|
| 5 - Fully traced | Every claim traces to a specific source, author, and date | Each unit of information has source, author, date, and verification status attached |
| 4 - Source identified | The document or dataset is known; specific claims within it may not be individually traced | You know which document a claim came from but not which page or which version |
| 3 - Generally sourced | The broad source category is known | "This came from industry reports" but not which specific report |
| 2 - Unclear origin | Information exists in the system but its source is unknown | "This is in the knowledge base" but no record of how it got there |
| 1 - No provenance | Information has no identifiable source | Agent-generated content, hallucinated claims, or data that was pasted in without attribution |

**Who assesses:** System (automated provenance tracking) with human verification  
**When:** Design time for knowledge base setup; continuously for runtime inputs  
**What happens with the score:** Red (1-2) = information cannot be verified; treat agent output as unverified. Amber (3) = provenance exists but is vague; human should spot-check claims. Green (4-5) = provenance supports trust in the output.

---

### 6. How sure is the agent? [Confidence]

Does the information come with an indication of how certain it is, or is everything presented with equal confidence regardless of how solid it is?

Example: A medical information agent has two claims: "aspirin reduces fever" (extremely well-established) and "this new compound may reduce inflammation" (early-stage research). If both are presented with equal confidence, the human can't tell which to trust more. Confidence signals let the human allocate their trust appropriately.

| Level | What it looks like | Indicator |
|-------|-------------------|-----------|
| 5 - Calibrated | Every claim has a confidence level that matches its actual reliability | High-confidence claims are well-established; low-confidence claims are flagged as uncertain |
| 4 - Mostly calibrated | Major claims are confidence-scored; minor claims may not be | Core information has confidence; peripheral information is unscored |
| 3 - Roughly scored | Broad confidence categories are applied | Information is marked "established," "emerging," or "speculative" |
| 2 - Uniform confidence | Everything is presented as equally certain, regardless of actual reliability | No distinction between well-established and speculative claims |
| 1 - False confidence | Uncertain information is presented with high confidence | Speculation presented as fact; early research presented as established knowledge |

**Who assesses:** Human (domain expert) at design time; system (confidence scoring) at runtime where possible  
**When:** Design time for knowledge base; continuously for agent-generated confidence  
**What happens with the score:** Red (1-2) = dangerous — the human cannot trust the confidence level; flag all output for human verification. Amber (3) = confidence exists but is imprecise; use as guidance, not gospel. Green (4-5) = confidence levels are reliable; human can allocate trust based on confidence signals.

---

### 7. Is it specific enough? [Specificity]

Is the information precise enough for the agent's purpose, or is it too general to be useful?

Example: An agent that reviews contracts needs to know that "termination clauses in commercial leases in Victoria typically require 30 days notice" — not just "termination clauses exist." The first is specific enough to work with. The second is too vague to be useful.

| Level | What it looks like | Indicator |
|-------|-------------------|-----------|
| 5 - Precisely scoped | Information is specific to the agent's exact domain, jurisdiction, and purpose | "Commercial lease termination in Victoria, 30-day notice standard" |
| 4 - Well-targeted | Information is specific to the domain but may include some broader context | "Australian commercial lease termination, 30-day notice in most states" |
| 3 - Adequately specific | Information covers the domain at a general level | "Lease termination in Australia, notice periods vary by state" |
| 2 | Too general to be directly useful without significant interpretation | "Tenancy law varies by jurisdiction" |
| 1 - Vague | Information is so general it could apply to anything | "Contracts have terms" |

**Who assesses:** Human (domain expert and designer)  
**When:** Design time, when selecting and curating knowledge  
**What happens with the score:** Red (1-2) = information is too vague for the agent to make specific judgments; it will produce generic output. Amber (3) = agent can work at a general level but will need human interpretation for specific cases. Green (4-5) = information is specific enough for the agent to produce targeted, useful output.

---

### 8. Is it structured? [Structure]

Is the information in a format the agent can use directly, or does it need significant processing before it's useful?

Example: An agent that extracts key terms from contracts receives scanned PDFs with headers, footers, page numbers, and watermarks mixed into the text. The information is there, but it's buried in noise that the agent has to process through before it can do its real job. Compare that to receiving the same contracts as structured data with fields already separated.

| Level | What it looks like | Indicator |
|-------|-------------------|-----------|
| 5 - Typed and structured | Information is in typed, structured format with clear fields and schemas | JSON/XML/database records with defined schemas |
| 4 - Well-formatted | Information has clear formatting and consistent structure | Clean markdown, well-organized documents with headers and sections |
| 3 | Information is present but requires extraction and interpretation | PDFs, web pages, documents with consistent but unmarked structure |
| 2 - Poorly formatted | Information is buried in noise and inconsistent formatting | Scanned documents, emails with mixed formatting, copy-pasted content |
| 1 - Raw or unstructured | Information has no discernible structure | Raw text dumps, transcribed audio, chat logs |

**Who assesses:** System (automated structure analysis) with human review  
**When:** Design time for knowledge base format decisions; continuously for runtime inputs  
**What happens with the score:** Red (1-2) = significant processing needed before agent can use information; processing cost and error risk are both high. Amber (3) = agent can process but with higher error risk and cost. Green (4-5) = information is in a format the agent can use efficiently.

---

### 9. Is it enough? [Sufficiency]

Is there enough information for the agent to make a judgment, or does it have to guess because critical pieces are missing?

Example: A compliance checker has the data protection regulation but not the industry-specific code of practice that interprets the regulation for this sector. It can tell you what the regulation says, but it can't tell you how to comply in your specific context. The information is accurate, relevant, and current — but it's insufficient for the task.

| Level | What it looks like | Indicator |
|-------|-------------------|-----------|
| 5 - Sufficient | The agent has everything it needs to produce a complete output | No known gaps that would force guessing or skipping |
| 4 - Mostly sufficient | Minor gaps that don't prevent core tasks | The agent can handle most cases; edge cases may need human input |
| 3 - Adequate | Enough for basic tasks but not for comprehensive judgment | The agent can handle routine cases but will miss nuance |
| 2 - Insufficient | Major gaps force the agent to guess or refuse on common tasks | The agent would need to say "I don't have enough information" frequently |
| 1 - Severely insufficient | The agent cannot perform its core purpose | Missing fundamental information that the task requires |

**Who assesses:** Human (domain expert), validated by testing the agent with representative inputs  
**When:** Design time; re-assessed when scope or task changes  
**What happens with the score:** Red (1-2) = agent cannot perform; don't deploy until sufficiency is addressed. Amber (3) = agent can handle routine cases; flag edge cases for human review. Green (4-5) = agent has enough information to produce comprehensive output.

**Note on completeness vs sufficiency:** Completeness asks "is every area covered?" Sufficiency asks "is there enough information to make a judgment?" A complete knowledge base can still be insufficient if each area has only surface-level coverage. A sufficient knowledge base can still have completeness gaps in areas that rarely matter. Both need to be checked.

---

### 10. Does it agree with itself? [Consistency]

Is the information internally consistent, or does it contradict itself? When the agent encounters conflicting information, can it tell which is right?

Example: A legal knowledge base contains two interpretations of the same clause — one from a 2022 case summary and one from a 2024 court decision that overturned the earlier interpretation. If the agent can't tell which is current, it might cite the overruled interpretation with the same confidence as the current one.

| Level | What it looks like | Indicator |
|-------|-------------------|-----------|
| 5 - Consistent | No contradictions; conflicting information is clearly marked with dates and sources | All information agrees, or disagreements are explicitly noted with recency and source |
| 4 - Mostly consistent | Minor inconsistencies that don't affect core judgments | A few points of disagreement, none on critical matters |
| 3 - Some contradictions | Conflicting information exists on important points | The agent will encounter disagreements and must decide which to follow |
| 2 | Significant contradictions that could lead to wrong conclusions | The agent might cite contradictory information with equal confidence |
| 1 - Contradictory | Fundamental contradictions on core topics | The knowledge base actively conflicts with itself on critical matters |

**Who assesses:** System (contradiction detection) with human review  
**When:** Design time for knowledge base setup; continuously for updates and additions  
**What happens with the score:** Red (1-2) = agent will produce contradictory output; don't trust. Amber (3) = agent needs human guidance on conflicting points. Green (4-5) = information is reliable and non-contradictory.

---

## How to use this framework

### The unit of assessment question

The framework can be applied at two levels:

**Package level:** "Is this document good enough to give the agent?" This is the quick, practical assessment. You score the whole document or knowledge base on each dimension. Fast, useful, but imprecise — a document can be mostly accurate but contain one critical error.

**Unit level:** "Within this package, which parts are high quality and which need attention?" This is the decomposability insight. A contract with 50 clauses might be mostly accurate (level 4) but contain two clauses that are outdated (recency level 2) and one that's ambiguous (specificity level 2). The package-level score hides these unit-level problems.

**When to use each:** Start with package-level assessment to catch obvious problems. If the package scores 4-5 on most dimensions, it's probably good enough for most purposes. If any dimension scores 1-3, drill down to unit level on that dimension.

**For high-stakes domains** (legal, medical, financial, regulatory): always assess at the unit level for accuracy, completeness, and sufficiency. A single clause error in a contract can be catastrophic.

---

### What to do with the scores

The traffic light model:

| Overall | Meaning | Action |
|---------|---------|--------|
| Mostly green (4-5) | Information is good enough for the agent to work with | Proceed with confidence. Attach confidence metadata to output. |
| Mixed green and amber | Information is usable with caveats | Proceed with human verification on amber dimensions. Flag these in agent output. |
| Mostly amber (3) | Information has significant limitations | Proceed only with human verification on every output. Agent should flag low-confidence areas. |
| Any red (1-2) | Information is not good enough for the agent to work with | Stop. Fix the information problem before running the agent. |

**Hard stops:** Red on accuracy or sufficiency means don't run the agent. Period. No amount of clever prompting fixes fundamentally wrong or insufficient information.

**Flags, not fixes:** An amber score doesn't mean "don't run the agent." It means "run the agent but attach a flag to the output saying this dimension is uncertain." The human allocates more attention to flagged dimensions.

---

### Who does what

| Dimension | Primary Assessor | Can be Automated? |
|-----------|------------------|-------------------|
| Relevance | Human (designer) | Partially — system can flag clearly irrelevant items |
| Accuracy | Human (domain expert) | Partially — system can cross-reference, but verification needs a human |
| Completeness | Human (domain expert) | Partially — system can check coverage against a known taxonomy |
| Recency | System (timestamps) | Fully — timestamps and freshness windows can be automated |
| Provenance | System (tracking) | Fully — source tracking can and should be automated |
| Confidence | Human (domain expert) with system scoring | Partially — system can estimate from source reliability; human calibrates |
| Specificity | Human (designer + domain expert) | Partially — system can detect vagueness patterns |
| Structure | System (format analysis) | Fully — format and schema analysis is mechanical |
| Sufficiency | Human (domain expert) validated by testing | Partially — system can detect gaps against a known task list |
| Consistency | System (contradiction detection) with human review | Partially — system can flag contradictions; human resolves them |

**Principle:** Automate what can be automated. Reserve human judgment for dimensions that require domain expertise (accuracy, completeness, sufficiency, confidence, specificity). Let the system handle what the system does well (recency, provenance, structure, consistency).

---

### Where this fits in CAWDP

**Phase 1 (Task Intelligence):** After you know what the agent needs to know, assess every input source on these 10 dimensions before proceeding.

**Phase 4 (Agent Design):** The 10 dimensions inform the agent's knowledge configuration. Low-scoring dimensions should be reflected in the agent's instructions — "the knowledge base may have gaps in X; flag uncertainty in this area rather than guessing."

**CC-3 (Epistemic Metadata Contracts):** At runtime, the scores become metadata that travels with the information. Every output carries confidence, provenance, recency, and consistency flags based on the input quality assessment.

**Phase 9 (Validation):** When testing the agent, check whether the quality assessment was accurate. If the agent produces poor output in an area that scored green, the assessment was wrong and needs updating.

---

### The connection to type collision

This framework is type collision resolution at the input layer. The same principle that says "different types of information need different containers" also says "different quality dimensions need different assessment scales." You can't assess accuracy with the same tool you assess structure. You can't fix recency with the same approach you fix specificity.

And the decomposability insight applies here too: a single knowledge base doesn't have one quality score. It has quality scores per unit. The overall assessment is the starting point, not the final word.That's the information quality framework. 10 dimensions, each with a concrete 5-level scale, who assesses it, when, and what to do with the score.

Three things I want to flag:

**The completeness vs sufficiency distinction** is one that took me a moment to separate, and I think it's genuinely important. "Is every area covered?" and "Is there enough information to make a judgment?" are different questions. A knowledge base that has every topic but only surface-level coverage is complete but insufficient. A knowledge base that has deep coverage of the 5 things that matter most is incomplete but sufficient. Both need checking.

**The hard stops** are deliberate. Red on accuracy or sufficiency means don't run the agent. Not "run it and add a disclaimer." Not "run it and verify afterward." Don't run it. The agent doesn't know its information is wrong. It will produce output with the same confidence whether the input is accurate or not. Running an agent on inaccurate information is worse than not running it at all — because the output looks authoritative.

**The automation allocation** is a practical decision, not a theoretical one. System should handle recency, provenance, structure, and consistency because these are mechanical checks. Human should handle accuracy, completeness, sufficiency, confidence, and specificity because these require domain expertise. Relevance is a human decision that the system can support.

