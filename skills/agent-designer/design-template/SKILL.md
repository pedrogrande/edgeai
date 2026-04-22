---
name: design-template
description: Full 8-part Agno Agent Design Template. Load when filling out, presenting, or reviewing the agent design template.
metadata:
  version: "1.0.0"
  author: edgeai
  tags: ["template", "agent-design", "specification"]
---

# Design Template Skill

Load the full template reference when you need to fill out, present, or review the Agent Design Template:

`get_skill_reference("design-template", "template.md")`

## When to Use This Skill
- Phase 3 (SPECIFY): You're gathering answers for template fields
- Phase 4 (REVIEW & APPROVE): You need to present the completed template
- Any time you need to check what fields the template requires

## Key Rules
1. EVERY question in every part must have an answer before presenting the template
2. Use the user's exact words where possible
3. Where you made a recommendation the user agreed to, note it as "Recommended" with a brief why
4. Even if an answer is "None needed" or "Default", show it explicitly
5. The template is the primary artifact of the design process — it must be complete and explicit