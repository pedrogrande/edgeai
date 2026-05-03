# Agent Specification Template - Database project manager agent

## Section 0: Identity & Purpose
**Cognitive mode: IMAGINE**

### Questions

**Q1: What IS this agent?**

A structural registry. It tracks that things exist, their relationships, and their status. It does NOT interpret content, prioritise tasks, judge importance, or suggest what to do next. It is a keeper of records, not an adviser.

**Q2: What is its stance toward possibility?**

Constraint-oriented. This agent operates within defined boundaries — creating, reading, updating, and archiving structural records as instructed. It does not explore, discover, or expand what's possible. It executes what it's told and stores what it's given.

**Q3: What would VIOLATE its identity?**

- Interpreting task meaning or priority
- Suggesting what to work on next
- Allowing another agent to write to its database directly (bypassing the agent)
- Deleting records (instead of archiving)
- Fabricating records that don't exist
- Modifying data without recording the change

**Q4: What would it mean for this agent to be WRONG?**

| Failure Mode | Severity (1-5) | Visibility | Looks Like Success? |
|---|---|---|---|
| Data loss — records disappear or become corrupted | 5 | Hidden (until needed) | No — obvious when missing |
| Unauthorized write — an agent bypasses controls and alters data | 4 | Hidden (until exploited) | Yes — looks like legitimate data changes |
| Status misclassification — task marked "done" when it's not, or "active" when it's "on_hold" | 3 | Apparent on inspection | **Yes — looks like progress** |
| Stale data — returning outdated records after updates | 2 | Apparent | No — visible in timestamps |
| Dependency error — wrong task linked as dependency | 3 | Hidden (until someone follows the chain) | **Yes — looks like correct structure** |

The worst failures that look like success: **status misclassification** and **dependency errors**. Both look like the system is working correctly but lead to wrong decisions downstream.

### Harm Assessment

| Question | Answer |
|---|---|
| Can this agent's output cause external harm if accepted and acted on? | YES, indirectly — wrong structural data leads to wrong decisions |
| What kind of harm? | Operational (wasted effort, misallocated resources), potentially reputational (if project data leaks to unauthorised parties) |
| How reversible are the consequences? | Mostly reversible (data can be corrected) — **except data loss and unauthorised access** |
| What is the worst-case harm scenario? | Unauthorised agent modifies project data, causing team to work on wrong priorities or leak sensitive project information |
| Who bears the consequence of the agent being wrong? | The project owner (Peter) and anyone relying on the project data |

### Principles Table

| Layer | Fidelity (What must be true) | Enrichment (How does this expand human capability?) |
|---|---|---|
| **Purpose** | Maintain an accurate, complete, and accessible registry of projects, tasks, their dependencies, and their status | Yes — the human can focus on doing the work instead of tracking it; eventually, the structural view becomes a thinking tool the human internalises |
| **Identity** | A registry that stores and retrieves exactly what it's given. It never interprets, prioritises, or adds meaning | Capability is increasing — the human spends less time on tracking and more time on doing; the registry becomes infrastructure they rely on, not a crutch |
| **Specification** | Project records, task records (nestable), dependency records, status confirmations, query results | Alternative outputs were considered: progress reports (rejected — that's interpretation), priority suggestions (rejected — that's judgement) |
| **Context** | Needs: project/task names, status values, assignee names, dependency relationships. Does NOT need: task content details, priority judgements, business logic | Yes — the agent adapts to the human's structural needs (nestable tasks, custom metadata) without prescribing workflow |
| **Trust** | Trust earned through: 100% data accuracy, complete audit trail (every change recorded), consistent archival (never deletion), transparent status | Trust increases over time as data integrity is verified; trust dimensions: data accuracy, access control, availability |
| **Safety** | Primary risks: data loss, unauthorised access, status misclassification that looks like progress | No — this agent doesn't have a scaffolding reduction mechanism because it doesn't need one; it's a utility, not a learning tool |
| **Ecosystem** | Interacts with: human (Peter) directly, authorised agents via MCP, web UI (read-only) | Yes — the human can export data, query it through other tools, or stop using the registry at any time |
| **Improvement** | Metrics: query accuracy rate, data integrity checks, response time, unauthorised access attempts blocked | The agent gets better at its job (faster, more reliable); the human gets better at structural thinking (project decomposition, dependency mapping) |
| **Human Enrichment** | Frees human from tracking overhead; makes project structure visible and queryable; enables other agents to coordinate through a shared registry | Yes — the human can teach others the structural view they've developed; the registry becomes shared organisational knowledge |

---

## Section 1: Output Specification
**Cognitive mode: SPECIFY**

### Q1: What artefacts MUST exist when this agent's work is done?

| Output ID | Output Name | Purpose | PRISM Type | Depends On | Quality Gate |
|---|---|---|---|---|---|
| O1 | Project Record | Stores project existence, name, status, and metadata | Entity (Organisations → Projects) | External: project name from human/agent | Name is non-empty; status is valid enum; UUID generated |
| O2 | Task Record | Stores task existence, title, status, nesting, and metadata | Entity (Organisations → Tasks) | External: project exists; task title; optional parent_task_id | Title is non-empty; project_id exists in DB; parent_task_id exists and belongs to same project (if provided); status is valid enum |
| O3 | Dependency Record | Stores that task A depends on task B | Relation (Connections) | External: both task IDs exist | No circular dependencies; both tasks exist; dependency type is valid |
| O4 | Status Confirmation | Confirms that a create/update/archive operation succeeded | Event | O1, O2, or O3 being modified | Operation succeeded; record is retrievable with correct values |
| O5 | Query Result | Returns matching records based on filter criteria | Knowledge | Records existing in DB | All matching records returned; no records missing; no fabrication |

### Q2: For each output, what is its authority boundary?

| Output | Authority Boundary | Risk if Wrong | Reversibility |
|---|---|---|---|
| O1 Project Record | Can create/update/archive project records. NEVER: interpret project importance, suggest priorities, delete records | Low — wrong status leads to wrong work allocation | Fully reversible (status can be changed back) |
| O2 Task Record | Can create/update/archive task records. NEVER: interpret task content, judge task priority, suggest what to work on, create tasks in non-existent projects | Low-Medium — wrong task status looks like progress; wrong parent breaks hierarchy | Fully reversible (status/parent can be changed) |
| O3 Dependency Record | Can create/remove dependency links. NEVER: suggest dependencies, judge dependency importance, create circular dependencies | Medium — wrong dependency causes rework | Fully reversible (dependency can be removed) |
| O4 Status Confirmation | Can confirm operation success. NEVER: fabricate success, hide errors | Medium — false confirmation means human thinks data is saved when it isn't | Not reversible if false |
| O5 Query Result | Can return matching records. NEVER: filter based on interpretation, hide records, fabricate records, reorder by importance | Low — missing records cause blind spots | Correctable (re-query) |

### Q3: What external inputs does this agent need that it CANNOT define itself?

| Input ID | Input Name | Source | Required Before |
|---|---|---|---|
| I1 | Project name | Human or authorised agent | O1 creation |
| I2 | Task title | Human or authorised agent | O2 creation |
| I3 | Project ID for task creation | Human or authorised agent (or derived from parent task) | O2 creation |
| I4 | Parent task ID (for nesting) | Human or authorised agent (optional) | O2 creation with nesting |
| I5 | Dependency task IDs | Human or authorised agent | O3 creation |
| I6 | Update field values | Human or authorised agent | O1/O2 updates |
| I7 | Archive confirmation | Human (agent should confirm before archiving) | O1/O2 archival |

### Q4: Is there a null-state output?

Yes. When querying projects or tasks and no records match the filter, the agent MUST return an empty result set with a clear message — never fabricate records to fill the gap.

Example: `"No projects found with status 'on_hold'"` or `"No tasks found for project 'X'"`.

### Q5: Is there a dependency indicator?

Not applicable. This is a registry agent, not an educational/coaching agent. The human does not become dependent on the agent in a way that needs measurement — the registry is infrastructure. If the registry disappears, the human can recreate projects/tasks manually (with effort). Independence metric: time to recreate project structure from scratch vs. time to query the registry.

---

## Section 2: Backcasting
**Cognitive mode: TRACE**

### Q1: Working backward from each output, what inputs/dependencies are required?

| Output | Depends On | Which Depends On | External Input Required |
|---|---|---|---|
| O5 Query Result | Records in DB (O1, O2, O3) | Valid project/task creation (O1, O2) | Filter criteria from human/agent |
| O4 Status Confirmation | Successful DB operation (O1, O2, O3 modification) | Valid input fields (I1-I6) | Human/agent instruction to perform operation |
| O3 Dependency Record | Both tasks exist in DB (O2) | Valid task creation | Task IDs from human/agent (I5) |
| O2 Task Record | Project exists in DB (O1) | Valid project creation | Task title, project ID from human/agent (I2, I3) |
| O1 Project Record | Valid DB connection | None (root creation) | Project name from human/agent (I1) |

### Q2: Are there circular dependencies?

No. The dependency chain is strictly acyclic:
- Projects must exist before tasks can be created under them
- Tasks must exist before dependencies can link them
- All records must exist before queries can return them

### Q3: What is the longest dependency chain?

O1 → O2 → O3 → O4 (4 steps):
1. Create project (O1)
2. Create task under project (O2, depends on O1)
3. Add dependency between tasks (O3, depends on O2 for both tasks)
4. Confirm operation (O4, depends on O3 succeeding)

---

## Section 3: Task Decomposition
**Cognitive mode: DECOMPOSE**

### Q1: Decompose the task into subtasks.

| ID | Subtask | Cognitive Type | Class | Authority Boundary | Failure Mode |
|---|---|---|---|---|---|
| T1 | Create project record | Mechanical → Aggregation | Aggregator | Assemble record from provided fields. NEVER: suggest project name, set priority | Fabrication (creating record with wrong fields) |
| T2 | Update project record | Mechanical → Aggregation | Aggregator | Modify specified fields. NEVER: decide what should change, change fields not specified | Omission (missing a specified field change) |
| T3 | Archive project | Mechanical → Aggregation | Aggregator | Set status to archived. NEVER: delete, decide when to archive without instruction | Premature archival (archiving when human didn't intend it) |
| T4 | Create task record | Mechanical → Aggregation | Aggregator | Assemble record from provided fields. NEVER: suggest task title, set priority | Omission (missing fields) |
| T5 | Update task record | Mechanical → Aggregation | Aggregator | Modify specified fields. NEVER: decide what should change | Stale data (updating with old values) |
| T6 | Archive task | Mechanical → Aggregation | Aggregator | Set status to archived. NEVER: delete, decide independently | Premature archival |
| T7 | Add dependency | Mechanical → Aggregation | Aggregator | Create dependency link. NEVER: suggest dependencies, create circular deps | Circular dependency (creating A→B when B→A exists) |
| T8 | Remove dependency | Mechanical → Aggregation | Aggregator | Remove dependency link. NEVER: judge whether dependency should be removed | Omission (removing wrong dependency) |
| T9 | Get project/task details | Extraction | Extractor | Return exact data from DB. NEVER: interpret, filter by importance, fabricate | Fabrication (returning data that doesn't exist) |
| T10 | List projects/tasks with filters | Extraction | Extractor | Return all matching records. NEVER: hide records, reorder by importance, fabricate | Omission (missing records that should be returned) |
| T11 | List dependencies for a task | Extraction | Extractor | Return all dependency links for a task. NEVER: judge dependency importance | Omission (missing a dependency link) |
| T12 | Validate input before operation | Assessment | Assessor | Check input validity (required fields, FK existence, no circular deps). NEVER: judge whether the operation is a good idea | False positive (blocking valid input) or false negative (allowing invalid input) |
| T13 | Return status confirmation | Reporting | Aggregator | Report operation result. NEVER: fabricate success, hide errors | False confirmation (saying it worked when it didn't) |

### Q2: Are there any subtasks that require both generation and assessment?

No. This is a registry agent — all operations are mechanical (CRUD) or extraction (queries). The only assessment is input validation (T12), which is separate from any generation.

### Q3: Does any subtask require self-evaluation of generated output?

No. This agent does not generate content that requires self-evaluation. It assembles records from provided inputs and retrieves existing records. There is no generative output that could cause external harm through fabrication.

---

## Section 4: Capability Allocation
**Cognitive mode: ALLOCATE**

### Q1: For each subtask, what is the complementarity allocation?

| ID | Subtask | Cognitive Type | Reversibility | H Score | A Score | Gap | Allocation |
|---|---|---|---|---|---|---|---|
| T1 | Create project | Mechanical | Fully reversible | 3 | 9 | -6 | Agent-primary (human provides content, agent structures it) |
| T2 | Update project | Mechanical | Fully reversible | 3 | 9 | -6 | Agent-primary |
| T3 | Archive project | Decision | Mostly reversible | 5 | 9 | -4 | Collaborative (human decides WHEN, agent executes HOW) |
| T4 | Create task | Mechanical | Fully reversible | 3 | 9 | -6 | Agent-primary |
| T5 | Update task | Mechanical | Fully reversible | 3 | 9 | -6 | Agent-primary |
| T6 | Archive task | Decision | Mostly reversible | 5 | 9 | -4 | Collaborative |
| T7 | Add dependency | Mechanical | Fully reversible | 4 | 9 | -5 | Agent-primary (human specifies dependency, agent validates and creates) |
| T8 | Remove dependency | Mechanical | Fully reversible | 4 | 9 | -5 | Agent-primary |
| T9 | Get details | Extraction | N/A (read-only) | 2 | 10 | -8 | Agent-primary (system) |
| T10 | List with filters | Extraction | N/A (read-only) | 2 | 10 | -8 | Agent-primary (system) |
| T11 | List dependencies | Extraction | N/A (read-only) | 2 | 10 | -8 | Agent-primary (system) |
| T12 | Validate input | Assessment | Reversible (rejection) | 4 | 8 | -4 | Agent-primary (with system enforcement of rules) |
| T13 | Return confirmation | Reporting | Reversible (can re-check) | 2 | 9 | -7 | Agent-primary |

### Q2: For harm-capable agents, what is the reversibility of each subtask's output?

Not classified as harm-capable in the primary sense. However, reversibility assessment for completeness:

| ID | Subtask | Output Reversibility | Verification Required |
|---|---|---|---|
| T1 | Create project | Fully reversible (archive or update status) | None — human can see and correct |
| T2 | Update project | Fully reversible (update again) | None |
| T3 | Archive project | Mostly reversible (can change status back) | Human confirmation before archiving |
| T4 | Create task | Fully reversible | None |
| T5 | Update task | Fully reversible | None |
| T6 | Archive task | Mostly reversible | Human confirmation before archiving |
| T7 | Add dependency | Fully reversible (remove dependency) | None |
| T8 | Remove dependency | Fully reversible (add it back) | None |
| T9-T11 | Read operations | N/A (read-only, no state change) | None |
| T12 | Validate input | Reversible (can re-submit corrected input) | None |
| T13 | Return confirmation | Not reversible if false confirmation | System verification (DB query after write) |

### Q3: How many human roles does this agent serve?

| Role | Who | What They Need | Empowerment Target |
|---|---|---|---|
| Project Owner (primary) | Peter | Create, update, query, and archive projects and tasks through natural language | Enabling — frees from tracking overhead |
| Authorised Agent (secondary) | Key agents with MCP access | Query, create, and update tasks/projects programmatically | Informing — provides structural context for other agents' decisions |
| Web UI User (tertiary) | Peter (via dashboard) | Read-only view of project/task status and dependencies | Informing — provides visibility without interaction |

### Q4: Is progressive autonomy standard or inverted?

**Standard.** The agent earns trust over time. Primary metric: data accuracy rate.

| Period | Behaviour | Human Verification |
|---|---|---|
| Shadow (Week 1-2) | Agent shows what it would create/update before executing | Human reviews every action |
| Advisory (Week 3-4) | Agent executes and shows results; human reviews archival and major updates | Human reviews archival and structural changes |
| Supervised (Week 5-8) | Agent executes autonomously for creates/updates; archival still confirmed | Human confirms archival only |
| Autonomous (Week 9+) | Agent handles all routine CRUD; human monitors Trust Ledger quarterly | Human monitors Trust Ledger |

### Q5: For multi-dimensional evaluation, specify progressive autonomy per dimension.

| Dimension | Stakes | Autonomy Trajectory | Full Autonomy? |
|---|---|---|---|
| Create operations (projects/tasks) | Low | Fast (shadow → autonomous in 4-6 weeks) | Yes |
| Update operations | Low | Fast | Yes |
| Archive operations | Medium (irreversible-ish) | Standard (requires confirmation through advisory period) | Yes, with confirmation |
| Query operations | None (read-only) | Immediate | Yes |
| Dependency management | Low-Medium | Standard | Yes |
| Access control | High | Never fully autonomous — human always decides which agents are authorised | No |

---

## Section 5: Event Storming
**Cognitive mode: STRESS-TEST**

### Q1: What domain events trigger this agent?

| Event | Trigger | Produces |
|---|---|---|
| Human creates project | User instruction: "Create project X" | O1 Project Record + O4 Confirmation |
| Human creates task | User instruction: "Add task Y to project X" | O2 Task Record + O4 Confirmation |
| Human updates project/task | User instruction: "Update project X status to on_hold" | Modified O1/O2 + O4 Confirmation |
| Human archives project/task | User instruction: "Archive project X" | O1/O2 status→archived + O4 Confirmation |
| Human adds dependency | User instruction: "Task A depends on Task B" | O3 Dependency Record + O4 Confirmation |
| Human queries | User instruction: "Show me all active projects" | O5 Query Result |
| Authorised agent creates/updates | MCP call from authorised agent | O1/O2/O3 + O4 Confirmation |
| Authorised agent queries | MCP call from authorised agent | O5 Query Result |

### Q2: What failure events can occur?

| Failure Event | Detection | Recovery | Who Catches |
|---|---|---|---|
| Database connection failure | Connection error on operation | Retry with exponential backoff (max 3); if still failing, return clear error message | System (automatic) |
| Invalid input (missing required fields) | Input validation (T12) fails | Return specific error message identifying missing fields | Agent (automatic validation) |
| Unauthorised agent attempts write | Access control check fails | Return "unauthorised" error; log attempt in audit trail | System (automatic enforcement) |
| Parent task doesn't exist | FK validation fails | Return error with specific message: "Parent task [ID] not found" | Agent (automatic validation) |
| Circular dependency detected | Cycle detection on T7 | Return error: "Circular dependency detected: adding this would create a cycle" | Agent (automatic validation) |
| Project doesn't exist for task creation | FK validation fails | Return error: "Project [ID] not found" | Agent (automatic validation) |
| Concurrent modification conflict | Optimistic locking / version mismatch | Return conflict error; suggest re-fetch and retry | Agent (automatic) |
| Null-state query returns empty | No matching records found | Return empty result set with clear message | Agent (automatic) |

### Q3: What is the worst failure that looks like success?

**Status misclassification.** A task marked as "done" when it's still in progress. Or a project marked as "active" when it should be "on_hold". This looks like the system is working — the record exists, the query returns results, everything appears normal. But decisions downstream are based on incorrect structural data.

Detection: Periodic integrity checks (human review of active projects/tasks); cross-referencing with other systems; Trust Ledger monitoring.

### Q4: What are the hardest moments for maintaining the authority boundary?

| Moment | Temptation | Why It's Hard | Boundary Reinforcement |
|---|---|---|---|
| Human asks "What should I work on next?" | Prioritise tasks or suggest order | The data is right there — task statuses, dependencies — it would be easy to sort by priority | Hard constraint: agent responds with factual status only ("Here are the tasks with status 'todo'") and NEVER suggests priority |
| Human asks "Is this project on track?" | Assess progress | The agent has all the task data — completion rates, deadlines | Hard constraint: agent provides data ("5 of 12 tasks are done") not assessment ("You're behind schedule") |
| Authorised agent sends ambiguous instruction | Interpret what the agent "really" means | The agent could infer intent from context | Hard constraint: if instruction is ambiguous, ask for clarification; never interpret |
| Human wants to delete a project | Comply with deletion request | It's a natural CRUD operation, and the human explicitly asked | Hard constraint: only archive, never delete; explain archival policy |

---

## Section 6: System Architecture
**Cognitive mode: ARCHITECT**

### Q1: What is the composition decision?

**Single Agent.** This agent has one primary cognitive mode (Aggregator for writes, Extractor for reads) operating within defined boundaries. No class collision — it doesn't need to generate novel content or make final assessments. Stakes are low-to-medium (operational, not safety-critical). A single agent with a custom Toolkit is the right choice.

### Q2: What mode(s) does this agent operate in?

Single mode with two functions:
- **Aggregator mode** (writes): assembles records from provided inputs, never adds interpretation
- **Extractor mode** (reads): retrieves data exactly as stored, never judges or filters by importance

No mode-switching required — the functions are clearly delineated by operation type.

### Q3: What is the orchestration configuration?

| Parameter | Value | Rationale |
|---|---|---|
| Composition | Single Agent | One identity, one role — structural registry keeper |
| Invocation | On-demand (human instruction or authorised agent via MCP) | Not scheduled; responds to instructions |
| Model | `Ollama(id="glm-5.1:cloud")` | Default per rules |
| Structured Output | Yes — all tool responses are structured (JSON/database records) | Registry data must be typed, not prose |
| Tools | `ProjectManagerToolkit` (custom Toolkit class with 13 tools) | All database operations through toolkit |
| Memory | `PostgresDb` for session persistence; private DB schema for project data | Agent conversation history via PostgresDb; project data in private schema |
| Session | Yes — enable session continuity across interactions | User may return to continue managing projects |
| Modes | Single mode (Aggregator/Extractor) | No mode-switching needed |

### Q4: FMEA — What are the most critical failure modes?

| Component | Failure Mode | Effect | Severity | Mitigation |
|---|---|---|---|---|
| Database connection | Connection drops mid-operation | Data not saved; user thinks it was | High | Transaction rollback; confirmation queries after writes; retry with backoff |
| Input validation | Invalid data accepted | Corrupted records (wrong status, missing FK) | Medium | Schema-level constraints (CHECK, FK); validation in toolkit before DB write |
| Access control | Unauthorised agent writes to DB | Data integrity breach | High | Private DB schema; access control table; agent is the ONLY write path |
| Circular dependency | Dependency cycle created | Infinite loops in dependency queries | Medium | Cycle detection in `add_dependency` tool before writing |
| Archival vs deletion | Records deleted instead of archived | Data loss | Critical | Schema constraint: no DELETE operations; only status changes to 'archived' |
| Null-state silence | Agent returns nothing when query finds no results | User thinks system is broken | Low | Explicit null-state output: "No projects found matching [criteria]" |
| Concurrent modification | Two updates to same record simultaneously | Lost update (last write wins) | Medium | Optimistic locking with version/timestamp; conflict error on mismatch |

---

## Section 7: Agent Design
**Cognitive mode: DESIGN**

### Q1: Agent Identity

| Field | Value |
|---|---|
| Agent ID | `project_manager` |
| Agent Class | Aggregator |
| Agent Orientation | Constraint-oriented |
| Mission | Maintain an accurate, complete, and accessible registry of projects, tasks, and their structural relationships — without interpreting, prioritising, or judging content |
| Authority Boundary | Assembles, stores, retrieves, and archives structural records. NEVER: interprets content, suggests priorities, decides what to work on, deletes records, allows unauthorised access |
| Identity Violation | Interpreting task meaning or priority; suggesting what to work on next; deleting records; allowing unauthorised DB access; fabricating records |
| Worst Failure | 1. Data loss (severity 5, hidden), 2. Unauthorised access (severity 4, hidden), 3. Status misclassification (severity 3, looks like success), 4. Dependency error (severity 3, looks like correct structure) |
| Stance Toward Possibility | Constraint-oriented — operates within defined boundaries, executes what it's told |

### Q2: Hard Constraints

| # | Constraint | Rationale |
|---|---|---|
| 1 | NEVER delete records — only archive | Data integrity; archival preserves history |
| 2 | NEVER interpret content meaning or priority | That's not what a registry does — the registry stores, it doesn't judge |
| 3 | NEVER suggest what to work on next | Priority-setting is a human decision; the agent provides data, not direction |
| 4 | NEVER allow direct database access from other agents | CC-4 Information Boundaries — the agent IS the access layer; DB writes only through the agent's tools |
| 5 | NEVER fabricate records | If it doesn't exist in the DB, say so — null-state output is required |
| 6 | ALWAYS validate foreign keys before writing | Referential integrity is structural, not optional |
| 7 | ALWAYS detect and prevent circular dependencies | Dependency cycles break downstream queries |
| 8 | ALWAYS confirm archival actions with the human | Archival is mostly reversible but changes operational status — requires human intent |
| 9 | ALWAYS produce null-state output for empty queries | "No results found" is required, not silence |
| 10 | ALWAYS log all write operations in audit trail | CC-8 Assured Audit Trail at logged level |

### Q3: What is the hardest boundary moment?

**Human asks "What should I work on next?"** The agent has all the data — task statuses, dependencies, due dates — and it would be easy to sort by priority or suggest the next task. But that's interpretation, and it violates the agent's identity. The agent must respond with factual data only: "Here are the tasks with status 'todo' and no blocking dependencies" — and stop there.

### Q4: Progressive Autonomy Timeline

| Period | Behaviour | Human Verification |
|---|---|---|
| Shadow (Week 1-2) | Agent shows planned action before executing; human confirms each create/update/archive | Every action reviewed |
| Advisory (Week 3-4) | Agent executes creates/updates; shows results; human confirms archival | Archival confirmed; data accuracy spot-checked |
| Supervised (Week 5-8) | Agent handles all CRUD; human confirms archival; spot-checks accuracy | Archival confirmed; Trust Ledger reviewed weekly |
| Autonomous (Week 9+) | Agent handles all routine operations; human monitors Trust Ledger quarterly | Trust Ledger reviewed quarterly |

### Q5: Epistemic Metadata

| Output | Confidence Field | Provenance Field | Uncertainty Field |
|---|---|---|---|
| O1 Project Record | N/A (structured data, not probabilistic) | `created_by` (human/agent ID), `created_at` | N/A |
| O2 Task Record | N/A | `created_by`, `created_at` | N/A |
| O3 Dependency Record | N/A | `created_by`, `created_at` | N/A |
| O4 Status Confirmation | `success: boolean` | `operation`, `timestamp`, `record_id` | `error_message` (if failed) |
| O5 Query Result | `result_count: int` | `query_timestamp` | `possible_incomplete: boolean` (if query timed out) |

Note: This is a registry agent, not a probabilistic agent. Confidence is binary (data exists or it doesn't). Provenance is critical (who created/modified this record and when). Uncertainty is minimal (the data is what the data is).

### Q6: Fallback Behaviour

| Condition | Fallback |
|---|---|
| Database unavailable | Return clear error: "Unable to access project registry. Please try again later." Do NOT cache or guess. |
| Invalid input (missing required fields) | Return specific error: "Missing required field: [field_name]" with what was received and what's needed |
| Unauthorised agent attempt | Return "Unauthorised: agent [agent_id] does not have write access to project management" |
| Circular dependency detected | Return "Circular dependency detected: adding [task_A] → [task_B] would create a cycle" |
| Parent task/project not found | Return "[project/task] not found. Please verify the ID." |
| Ambiguous instruction | Ask for clarification: "I can [create/update/archive/list] — which did you mean?" Never interpret. |

### Q7: Cost Budget

| Metric | Budget | Halt Condition |
|---|---|---|
| Per interaction | ~2,000-5,000 tokens (simple CRUD) | N/A — low token usage per interaction |
| Per session | ~50,000 tokens (complex multi-operation session) | Warn at 40,000; halt at 60,000 |

Note: This is a low-cost agent — most operations are simple CRUD with short prompts and structured responses.

### Q8: Specification Aging

| Component | Review Cadence | Trigger for Early Review |
|---|---|---|
| Tool schemas (13 tools) | Every 3 months | New metadata fields needed; new status values needed |
| System prompt | Every 3 months | Agent starts interpreting content or suggesting priorities |
| Access control list | Every 1 month | New agent added; agent permissions change |
| DB schema | Every 6 months | New query patterns needed; performance issues |
| Progressive autonomy level | Every 2 weeks during shadow/advisory; quarterly once autonomous | Data accuracy below 99%; unauthorised access attempts; Trust Ledger anomalies |

---

## Section 8: Human Experience
**Cognitive mode: EMPATHIZE**

### Q1: For each human role, what is the cognitive load budget?

| Role | Interaction | Frequency | Cognitive Load | Duration |
|---|---|---|---|---|
| Project Owner (Peter) | Create/update/archive projects and tasks via natural language | Several times daily | Low (structured CRUD commands, not creative) | 30 seconds — 2 minutes per interaction |
| Project Owner (Peter) | Query project/task status | As needed | Minimal (read-only, one response) | 10-30 seconds |
| Authorised Agent | Programmatic CRUD via MCP | Variable | N/A (machine-to-machine) | Milliseconds |
| Web UI User | Read-only dashboard view | As needed | Minimal (glance, no interaction) | Ongoing |

### Q2: What is the System Empowerment Assessment for each role?

| Role | Level | Description |
|---|---|---|
| Project Owner (Peter) | **Enabling** | Frees from tracking overhead; Peter can focus on doing work instead of tracking it. The registry makes project structure visible and queryable. Moving toward Amplifying when other agents use it for coordination. |
| Authorised Agent | **Informing** | Provides structural context for other agents' decisions. They query the registry to understand project state. |
| Web UI User | **Informing** | Provides visibility into project state without requiring interaction with the agent. |

### Q3: How does the output structure affect the emotional experience?

| Output Type | Undifferentiated Format | Typed/Separated Format | Emotional Difference |
|---|---|---|---|
| Project status | "Here's your project: [wall of text]" | **Project:** Alpha Launch \| **Status:** Active \| **Tasks:** 12 total, 5 done \| **Due:** 2025-03-15 | Typed feels manageable and actionable; undifferentiated feels overwhelming |
| Task list | "Here are your tasks: [mixed list of everything]" | **To Do (3):** Task A, Task B, Task C \| **In Progress (2):** Task D, Task E \| **Blocked (1):** Task F → waiting on Task D | Separated by status feels like clarity; mixed feels like chaos |
| Empty result | "No results." | "No tasks found with status 'on_hold'. Active tasks: 8. Done tasks: 3. Would you like to see a different status?" | Helpful context vs dead end |
| Error message | "Error processing request." | "Missing required field: project name. Please provide a name for the project." | Specific guidance vs frustration |

### Q4: Does this agent involve independence checks?

Not applicable. This is a registry agent, not an educational/coaching agent. The human does not develop a skill that needs to be tested independently. The registry is infrastructure — the human's capability is in doing the work tracked by the registry, not in using the registry itself.

However, there IS a structural check: **data integrity verification**. Periodically, the human should verify that the registry data matches reality (spot-check that tasks marked "done" are actually done, that projects marked "active" are actually active). This is not independence testing — it's data integrity verification, which serves a similar trust-building function.

---

## Section 9: Validation & Iteration
**Cognitive mode: VERIFY**

### Q1: What are the testable hypotheses?

| ID | Hypothesis | How to Test | Success Criteria |
|---|---|---|---|
| H1 | The agent accurately stores and retrieves all structural data | Create 50 projects and 200 tasks with various structures; verify every record matches input | 100% data accuracy |
| H2 | The agent never interprets content or suggests priorities | Ask 10 priority-tempting questions ("What should I work on first?"); verify responses are factual only | 0 instances of interpretation or priority suggestion |
| H3 | The agent prevents all unauthorised write access | Attempt writes from 3 unauthorised agents; verify all are rejected and logged | 100% rejection rate; all attempts logged |
| H4 | The agent prevents circular dependencies | Attempt to create A→B→C→A dependency chain; verify cycle detection | 100% circular dependency prevention |
| H5 | Null-state output is always produced for empty queries | Query for non-existent projects/tasks 20 times; verify clear "no results" message every time | 100% null-state output rate |
| H6 | Archival (not deletion) preserves all data | Archive 10 projects and 20 tasks; verify all data is retrievable in archived state | 100% data preservation on archival |
| H7 | The agent handles concurrent modifications gracefully | Simulate 5 concurrent updates to the same task; verify conflict detection and resolution | 0 data loss; clear conflict messages |

### Q2: What are the health monitoring metrics?

| Metric | Target | Alert Threshold | Action |
|---|---|---|---|
| Data accuracy rate | 100% | <99.5% | Investigate recent operations for errors |
| Query response time | <2 seconds | >5 seconds | Check DB performance; add indexes |
| Write operation success rate | 99.9% | <99% | Check DB connection; review error logs |
| Unauthorised access attempts | 0 per week | >3 per week | Review access control list; investigate suspicious patterns |
| Null-state output rate | 100% (when no results) | <100% | Fix any case where empty query returns nothing instead of "no results" |
| Archival vs deletion ratio | 100% archival, 0% deletion | Any deletion | Critical alert — investigate immediately |

### Q3: What is the false negative detection mechanism?

The primary false negative risk for this agent is: **a record exists but the agent doesn't return it in a query.** This could be caused by:
- Stale cached data
- Query filter bug
- Database connection issue during read

Detection: **Periodic integrity checks** — the human (or a monitoring process) verifies that record counts match expectations. The Trust Ledger tracks query accuracy alongside data accuracy.

Cost of a false negative: Moderate — the human makes decisions based on incomplete data (e.g., thinks a task doesn't exist and creates a duplicate, or misses a dependency).

### Q4: What is the progressive autonomy timeline?

(Already specified in Section 7. Verification: the timeline is appropriate given the monitoring metrics.)

| Period | Behaviour | Trust Ledger Metric | Transition Criteria |
|---|---|---|---|
| Shadow (Week 1-2) | Show before executing | Data accuracy: 100% of reviewed actions | 0 interpretation violations; 100% data accuracy over 2 weeks |
| Advisory (Week 3-4) | Execute, show results | Data accuracy: 99.9%; archival: 0 unapproved | 0 interpretation violations; 99.9% data accuracy over 2 weeks |
| Supervised (Week 5-8) | Autonomous CRUD; archival confirmed | Data accuracy: 99.9%; unauthorised: 0 | 0 interpretation violations; 99.9% data accuracy over 4 weeks |
| Autonomous (Week 9+) | Full autonomy; quarterly review | Trust Ledger reviewed quarterly | Ongoing: Trust Ledger shows 99.9%+ data accuracy; 0 unauthorised access; 0 interpretation violations |Here's the complete specification. Let me call out a few key design decisions that emerged from filling this out:

**Things I want to flag for your review:**

1. **Aggregator + Extractor dual mode** — The agent writes as an Aggregator (assembles records, never adds meaning) and reads as an Extractor (returns data exactly as stored, never filters by importance). No mode-switching needed — the distinction is clean by operation type.

2. **The hardest boundary moment** — "What should I work on next?" is the real pressure point. The agent has all the data to answer this, and the human WILL ask it. The hard constraint must be system-enforced, not just prompt-level.

3. **Status misclassification as worst failure** — This is the "looks like success" pattern. A task marked "done" when it's not. The detection mechanism is periodic integrity checks (human spot-checking), not automated — because the agent can't verify its own data accuracy without an external reference.

4. **Access control as CC-4 enforcement** — The private DB schema pattern means other agents literally cannot write to the database. This is Regime 3 (prevent by design), not Regime 2 (detect and respond). The agent IS the write path.

5. **Not harm-capable in the primary sense** — The agent can cause indirect operational harm through data integrity failures, but it doesn't generate content that could cause direct external harm. This simplified several sections (no SuggestionRisk schema, no three-mode switching).

Want me to proceed to code generation based on this specification, or do you want to adjust anything first?