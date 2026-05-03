# Progressive Autonomy: Design vs. Execution

**The plan is designed in Phase 7. The execution happens during validation and deployment.**

This is the same pattern as building codes: you specify the inspection criteria before construction starts, but the actual inspections happen during and after construction.

| What | Where it lives | When it happens |
|------|---------------|-----------------|
| Autonomy thresholds (shadow/advisory/supervised/autonomous) | Phase 7 — agent job description | Specified now |
| What changes at each level (which fields reviewed, which tools available, which decisions the agent can make) | Phase 7 — agent job description | Specified now |
| Actually running the agent in shadow mode and observing | S5 Validation + S9 Monitoring | Executed during use |
| Promoting from one level to the next based on observed performance | S9 Monitoring (specification aging + override rate data) | Executed during use |

So progressive autonomy is **not** pre-deployment testing. It's a deployment strategy with criteria designed before deployment and execution measured after deployment. The job description specifies the map; validation and monitoring walk the territory.

## Rationale — Why Progressive Autonomy Exists At All

Three reasons, none of which is "be cautious for caution's sake":

**1. The failure mode stakes change with autonomy level.**

A Generator that fabricates an import at shadow level — human catches it on the first field review. Zero harm. The same fabrication at autonomous level — human never sees it until it breaks in production. The same failure mode, different stakes. Progressive autonomy is a cost-effective risk management strategy: validate the agent's failure modes at the level where they're cheapest to catch, then promote when evidence supports it.

**2. The system learns the agent's actual performance boundaries, not its declared ones.**

The Job Drafter says "I produce high-quality job descriptions." Progressive autonomy asks: prove it. At shadow level, the system collects data on: how often does the human override? Which fields get corrected? What confidence scores does the agent assign vs. what quality actually materializes? This data feeds specification aging (CC-5) — the agent's spec gets revised based on observed performance, not assumed competence.

**3. For this meta-application specifically — you're trusting an agent to help design agents.**

The user is building their own trust trajectory with a tool that shapes how they design other tools. If the Vision Mirror over-identifies with the user's stated purpose and the human can't see it happening, the entire agent design is compromised at the foundation. Shadow mode on the first 3 designs means the human reviews every field of every Vision Mirror output — including the fields that look fine but carry the agent's bias. That's not caution. That's verification independence (CC-1) applied to the trust-building process itself.

---

**The alternative is what 77% of pilot-stuck organizations do: deploy at full autonomy, discover failures in production, lose trust, cancel the project.** Progressive autonomy is the structural antidote to that pattern. It replaces "trust the agent completely or don't use it at all" with "earn trust incrementally with evidence."
