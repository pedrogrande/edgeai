# Agent [Autonomous Agent]

An agent is a program that doesn't need to be coded because it is powered by an LLM.

Think of it like this: a regular program is a recipe. Follow each step exactly, get the same result every time. An agent is more like giving someone a goal and some guidelines, then letting them figure out how to get there.

An agent reviews 50 rental contracts and flags the ones with unusual termination clauses. A regular program can't do this, it would need someone to write a rule for every possible clause. The agent uses its understanding of language to find what's unusual, even if it's never seen that particular clause before.

**Agents are not beings.** They don't have thoughts, feelings, or opinions. They are specifications, written instructions that, when invoked, produce work. An agent "lives" only from the moment it's started to the moment it finishes. It doesn't exist between uses. The specification persists. The agent is temporary.

**An agent's capability is entirely dependent on what it's been given.** Give it clear instructions and good information, it produces good work. Give it vague instructions or bad information, it produces plausible-looking mistakes. The agent doesn't know the difference. That's the human's job.

---

## What an agent needs to exist

### Someone to start it [Invocation / Trigger]

An agent doesn't start itself. Something has to set it going, a person clicking a button, a schedule running every hour, or another system sending it a signal.

Like a tool in a workshop, it sits there until someone picks it up and uses it. The agent doesn't decide "I should check those contracts now." It waits to be told.

### A meaningful goal [Purpose / Intent]

An agent needs to know what it's trying to achieve. Not just a task ("process this document") but a reason ("find clauses that could cost the client money"). The better the goal, the better the agent's judgment about what matters and what doesn't.

A goal without meaning is just a program. "Find all paragraphs longer than 200 words" is a program. "Find paragraphs where the landlord might be hiding something" is a goal that requires judgment.

### The ability to receive and understand information [Perception / Input Processing]

An agent takes in information, text, data, signals, and makes sense of it. It reads a contract and understands that "termination without cause upon 30 days notice" means something different from "termination for breach upon 7 days notice."

The quality of what the agent produces depends directly on the quality of what it receives. Feed it a blurry scan instead of clear text, and it will misread clauses. Feed it a contract with outdated clauses mixed in with current ones, and it might flag the wrong things.

### The ability to figure out how to achieve its goal [Reasoning / Decision-Making]

An agent works out its own path to the goal. It considers options, picks the one most likely to succeed, and adjusts if new information comes in. You give it the "what" and enough guidance on the "how", but not step-by-step instructions. If you're giving step-by-step instructions, you've written a program, not an agent.

This is what makes agents feel magical. They don't just follow rules, they work things out. But it's not magic. The model inside the agent has seen millions of examples of how humans reason through problems, and it reproduces those patterns. It looks like thinking. Whether it IS thinking is a philosophical question. For practical purposes: the output resembles reasoning, and the reliability of that reasoning depends on the quality of what the agent was given.

### A way to make something happen [Action / Means of Causing Change]

An agent needs to be able to do something that changes the world, even if that change is just "a record now exists that this was done." An agent that reads a contract but can't flag the risky clauses, write a summary, or notify anyone, that agent hasn't done anything useful.

Some of what the agent does comes from inside: it can think, write, summarize, and recommend. These are part of what the agent IS. Some of what it does comes from the environment it's been given access to: it can search a database, send an email, or update a file. These are part of where the agent WORKS. Both matter.

### A world to work in [Environment / Operating Context]

An agent exists within an environment that gives it both capability and limits. The environment provides the tools the agent can access, the information it can reach, and the boundaries of what it's allowed to do. The same agent specification in a locked-down environment with no database access is fundamentally different from that same specification in an environment with full access.

The environment gives the agent its agency. It also constrains it. An agent with access to a legal database can check whether a clause is standard. Without that access, it can only guess based on what it already knows.

---

## What an agent is made of

### A point of view [Identity / Role]

An agent needs to know who it IS. Not just what it does, but what kind of worker it is. A reviewer looks for problems. A researcher finds information. A writer creates content. A coordinator brings things together. The identity shapes how the agent approaches every task.

An agent without identity is just ChatGPT, helpful but generic. An agent with identity is like a specialist: it brings a perspective, a philosophy, an approach. It knows what it's for, and, just as importantly, it knows what it's NOT for.

### High-level guidance [Instructions / Directives]

An agent needs instructions on how to approach its goal. But these must be high-level: "Look for clauses that shift risk to the tenant" not "Read paragraph 3, check if it contains the word 'indemnify', if yes then..." Low-level, step-by-step instructions are a program. The agent should be given the intention, not the procedure.

The instructions are not binding in the way program code is. An agent might interpret them differently than you expected. That's the trade-off: you get flexibility and judgment, but you also get the possibility of surprise.

### Relevant knowledge [Knowledge / Context]

An agent needs information to work with. But more is not always better. The goal is the minimum sufficient information, enough for the agent to make smart decisions, not so much that it gets confused or wastes processing on irrelevance.

With humans, we can trust that more knowledge is usually better because we naturally filter out what's irrelevant. Agents don't. Every piece of information they're given gets processed, costs money, and can potentially lead them in the wrong direction.

### A way to learn from experience [Memory / Persistent State]

An agent can be given the ability to remember things from one use to the next. This memory lets it improve: "Last time I flagged this clause, the human said it was fine, I should adjust." Memory is how the agent's specification gets smarter over time.

But memory needs curation, not just accumulation. The agent remembers everything it's told, including mistakes and outdated information. Without curation, memory becomes a liability, the agent repeats errors from the past with confidence.

### An intelligence engine [Reasoning Substrate / LLM Model]

The model is what makes an agent an agent instead of a program. It's the engine that takes instructions, knowledge, and information, and turns them into decisions and actions. Without the model, nothing else works, the agent can't even understand the goal it's been given.

Different models have different strengths. Some are better at reasoning, some at creative generation, some at following precise instructions. The model is part of the agent's identity: it shapes what the agent is naturally good at and where it's naturally weaker.

---

## The most important thing

**Agents are ephemeral.** Their capabilities, and the likelihood of their success, are entirely dependent on the quality of the information provided to them, whether that information was given when they started, while they were working, or was stored by a previous run of the same specification.

You don't design an agent. You design what goes into it. The agent is what comes out.