# Schema Verification Diagnostic (SVD) — Implementation Specification

This is the post-insertion complement to the pre-insertion linter. Together they form the complete CC-1 pipeline:

| Level | Mechanism | Timing | What It Checks |
|---|---|---|---|
| CC-1 Level 1 (Structural) | **SQG Linter** | Before insertion | Files are syntactically valid, no naming collisions |
| CC-1 Level 2 (Semantic) | **SVD Verification** | After insertion | Database state matches design intent |
| CC-1 Level 3 (Authority) | **Human review** | After verification | Approves phase completion |

Let me design the Schema Verification Diagnostic — the IDS for the knowledge graph.

## Why This Exists

The SQG linter catches errors **before** they enter the knowledge base. But it can't verify that what you **intended** to insert is what actually **landed**. The SVD is the post-insertion complement — the **IDS (Intrusion Detection System)** for the knowledge graph. Together they form the complete CC-1 verification pipeline:

```
                    ┌──────────┐         ┌──────────┐         ┌──────────┐
   .tql files ───► │  SQG     │ ──PASS──►│  TypeDB  │ ───────►│  SVD     │ ──PASS──► Human review
   (static)        │  Linter  │         │  Insert  │         │  Verify  │         (CC-1 L3)
                    └──────────┘         └──────────┘         └──────────┘
                   CC-1 L1              Database              CC-1 L2
                   (structural)         state                 (semantic)
```

**The SQG asks: "Is this file syntactically valid?"**
**The SVD asks: "Is the database state semantically correct?"**

Different question, different timing, different method.

---