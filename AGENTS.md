# AGENTS — Available Hermes Agents and Their Capabilities

## Founder's Ecosystem

| Agent | Primary Role | Best Used For |
|-------|--------------|---------------|
| **default** | General assistant | Broad tasks, coordination, default execution |
| **commander** | Operations / orchestration | Complex multi-step missions, cross-agent coordination |
| **quantum-developer** | Engineering / coding | Python, LangGraph, agents, APIs, infrastructure |
| **quantum-ml-engineer** | ML / data science | Model design, RAG, evaluation, ML pipelines |
| **youtube-learning** | Learning / content | Research, summaries, learning paths, content |
| **vanguard** | Strategy / founder intelligence | Strategic thinking, prioritization, business decisions |

## Agent Handoff Rules

1. **Use the right specialist.** Don't ask youtube-learning to write production code. Don't ask quantum-developer to do market strategy.
2. **Provide context.** When handing off, include the goal, constraints, expected output, and why it matters.
3. **Set success criteria.** Make the deliverable measurable.
4. **Verify output.** VANGUARD should review high-stakes deliverables before they are treated as done.
5. **Capture learnings.** Agent outputs that produce reusable knowledge should be recorded in this repo or the Obsidian vault.

## When to Message Each Agent

- **commander:** When a task spans multiple agents or requires mission-level coordination.
- **quantum-developer:** When building, refactoring, or debugging agents, code, APIs, or infrastructure.
- **quantum-ml-engineer:** When designing RAG systems, evaluating models, or building ML/data pipelines.
- **youtube-learning:** When researching a topic, summarizing content, or planning a learning path.
- **vanguard:** When making strategic decisions, prioritizing opportunities, or reviewing company direction.

## Agent Infrastructure

- Bot mode is active. Each agent has a canonical "Bot Chat" conversation.
- Handoff command: `hermes -p <agent-name> chat --in ~ -c "Bot Chat" --create-if-missing -Q -q "Message from 🤖 vanguard (@vanguard): <message>"`
- Always open with the "Message from 🤖 vanguard (@vanguard):" prefix so the recipient knows the source.

## Capability Gaps

| Gap | Impact | Plan |
|-----|--------|------|
| No dedicated sales/lead-gen agent | Limits outbound validation | Consider building or assigning a research agent to prospect qualification |
| No dedicated design/UI agent | Slows frontend work | Use templates and no-code tools until specialist is needed |
| No dedicated DevOps agent | Infrastructure bottlenecks | Delegate to quantum-developer initially; document reusable patterns |
