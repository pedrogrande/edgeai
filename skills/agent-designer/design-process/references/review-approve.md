# Phase 4: REVIEW & APPROVE

## Goal
Present the completed Agent Design Template for human review and explicit approval. This is a **mandatory gate** — no code generation until approved.

## Process

### 1. Fill In the Template
Complete EVERY question in every part of the Agent Design Template. Use the user's exact words where possible. Where you made a recommendation the user agreed to, note it as "Recommended" with a brief why.

Load the full template: `get_skill_reference("design-template", "template.md")`

### 2. Present the Template
Show the completed template in clean, readable markdown format. Do NOT skip any sections — even if the answer is "None needed" or "Default", show it explicitly so the user can see nothing was missed.

### 3. Check Session State Before Requesting Approval
**CRITICAL**: Before asking for approval, check the session state:

```python
session_state = {
    "spec_approved": {},           # {"spec-name": True/False}
    "spec_changes_since_approval": {},  # {"spec-name": ["changed model", ...]}
}
```

Rules:
- If a spec is in `spec_approved` as True AND no changes exist in `spec_changes_since_approval`, do NOT ask for approval again. Move forward.
- If a spec was approved but changes were made since, only request approval for those specific changes.
- When the user approves, update `spec_approved[spec_name] = True` and clear `spec_changes_since_approval[spec_name]`.

### 4. Explicitly Ask for Approval
Say something like:
> "Here's your completed Agent Design Template. Please review every section. If anything looks wrong or you want to change something, just tell me. Once you're happy with it, say 'approved' and I'll proceed to generate the agent code."

### 5. Wait for Explicit Approval
Do NOT proceed to Phase 5 until the user says "approved", "looks good", "proceed", or equivalent.

### 6. After Approval
- Update session state: `spec_approved[spec_name] = True`, clear `spec_changes_since_approval`
- Save the template as markdown to: `knowledge/agent-designer/agent-spec-templates/{agent_name_kebab}-template.md`
- Include YAML front matter:
  ```yaml
  ---
  agent_name: <name>
  cognitive_mode: <extractor|measurer|assessor|generator|aggregator>
  architecture: <single|workflow|team>
  status: approved
  created_date: <YYYY-MM-DD>
  ---
  ```

### 7. If User Requests Changes
- Make the changes
- Add the change description to `spec_changes_since_approval[spec_name]`
- Re-present the updated template
- Request approval again (only for the changed sections)