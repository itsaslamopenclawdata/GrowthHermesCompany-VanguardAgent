# EXPERIMENTS — Hypotheses, Tests, Results, and Learnings

## Experiment Template

| Field | Description |
|-------|-------------|
| Hypothesis | What we believe will happen |
| Assumption | What must be true for it to matter |
| Test | What we will do to validate |
| Expected Result | What success looks like |
| Success Criteria | Concrete thresholds |
| Time Limit | How long we will run it |
| Cost Limit | Maximum resource spend |
| Actual Result | What happened |
| Learning | What we learned |
| Next Decision | Continue, pivot, or kill |

---

## Active Experiments

### EXP-001: LangGraph Research Agent v1

- **Hypothesis:** We can build an autonomous research agent using LangGraph + DuckDuckGo search that outputs structured reports to Obsidian.
- **Assumption:** Search quality and LLM summarization are good enough for useful reports.
- **Test:** Build the agent, run 5 end-to-end research queries, and evaluate output quality.
- **Expected Result:** Each query produces a structured, readable Obsidian note.
- **Success Criteria:** 4/5 outputs are useful without heavy manual editing.
- **Time Limit:** 7 days
- **Cost Limit:** Free-tier APIs and local compute
- **Actual Result:** Built and operational. First agent writes to Obsidian vault successfully.
- **Learning:** LangGraph state management + tool binding works well; output templates need refinement.
- **Next Decision:** Continue. Build 4 more agents and standardize templates.

### EXP-002: Validate Demand for AI Research Reports

- **Hypothesis:** Busy professionals will pay for autonomous, high-quality research reports on demand.
- **Assumption:** There is a segment willing to pay for curated AI-generated intelligence.
- **Test:** Create a simple landing page or offer, share in 3 relevant communities, measure sign-ups or pre-sales.
- **Expected Result:** 10+ qualified leads or 1+ paid pre-order.
- **Success Criteria:** 5+ email sign-ups or 1 paid commitment.
- **Time Limit:** 14 days
- **Cost Limit:** $0
- **Actual Result:** (pending)
- **Learning:** (pending)
- **Next Decision:** (pending)

---

## Completed Experiments

| ID | Name | Result | Key Learning |
|----|------|--------|--------------|
| EXP-001 | LangGraph Research Agent v1 | Success | Agent-to-Obsidian pipeline works; template standardization needed |

---

## Experiment Backlog

| ID | Name | Hypothesis | Priority |
|----|------|------------|----------|
| EXP-003 | Agent orchestration with multiple specialists | Multi-agent workflows outperform single agents | Medium |
| EXP-004 | Autonomous content generation pipeline | Agents can produce publishable content with minimal editing | Medium |
| EXP-005 | B2B lead research agent | Agent can identify and qualify ideal prospects automatically | High |
