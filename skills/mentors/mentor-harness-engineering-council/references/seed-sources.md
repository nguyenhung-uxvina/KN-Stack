# Seed Sources — mentor-harness-engineering-council

> Curated 2026-06-25. CEO-approved set = T1+T2 (14 selected → 13 live after deleting 1 Cloudflare-blocked OpenAI page; OpenAI/Codex story covered by InfoQ + framework).
> Notebook: 8c7dab78-fca9-4391-90ca-7b6ad3d91bed
> Persona purity verified across Q1-Q7 extraction (citations accurate, no fabrication).

## Tier 1 — Canonical / primary (originators + the anchor) — 9

| # | Source | URL | NLM source_id | Note |
|---|--------|-----|---------------|------|
| 1 ⭐ | KHUNG HARNESS ENGINEERING v1.0 (VN-SIM-TECH) | local: D:/Workshop_X/0_Inbox/Harness_Engineering_Framework_v1.0.docx → .md | 747dcea7 | THE anchor — defense lifecycle, VN vocabulary, harness vật lý, air-gapped |
| 2 | Mitchell Hashimoto — My AI Adoption Journey | mitchellh.com/writing/my-ai-adoption-journey | c3118dea | Naming essay 2/2026; "engineer the harness"; single-agent pragmatism |
| 3 | Anthropic — Effective harnesses for long-running agents | anthropic.com/engineering/effective-harnesses-for-long-running-agents | 96bbdeda | initializer+coding agent, claude-progress.txt, cross-session artifacts |
| 4 | Anthropic — Effective context engineering for AI agents | anthropic.com/engineering/effective-context-engineering-for-ai-agents | 402ba542 | context-as-bottleneck, sub-agent, "smarter models need less prescriptive eng" |
| 5 | Anthropic — Writing effective tools for AI agents | anthropic.com/engineering/writing-tools-for-agents | 8b5cc097 | tool = agent UX; namespacing; restrict tool count |
| 6 | LangChain — Improving Deep Agents with harness engineering | langchain.com/blog/improving-deep-agents-with-harness-engineering | 37e35b35 | +13.7pts fixing harness only; LoopDetection; "guardrails will dissolve" |
| 7 | Martin Fowler — Agentic Programming | martinfowler.spicytakes.org/post/2026-05-21-AgenticProgramming | ca0b9c7e | agentic programming as new mode; harness eng as core competency |
| 8 | Martin Fowler — Function calling using LLMs | martinfowler.com/articles/function-call-LLM.html | 98491eb9 | restrict action space; prompt-injection guardrails; manual gates |
| 9 | Martin Fowler — Expert Generalists | martinfowler.com/articles/expert-generalist.html | 20f20228 | humans on the loop; mechanical sympathy; EG value rises with LLMs |

## Tier 2 — Authoritative synthesis / practitioner — 4

| # | Source | URL | NLM source_id | Note |
|---|--------|-----|---------------|------|
| 10 | InfoQ — OpenAI Introduces Harness Engineering: Codex | infoq.com/news/2026/02/openai-harness-engineering-codex/ | e7a7f39d | Independent coverage of OpenAI Codex harness (1M lines / 1500 PR / Lopopolo) |
| 11 | SIG — What is harness engineering? | softwareimprovementgroup.com/blog/what-is-harness-engineering/ | 58b8ed0c | Clean 3-layer definition; "portfolio governance is the harness"; monitoring layer |
| 12 | Faros.ai — Harness Engineering: Making AI Coding Agents Work in 2026 | faros.ai/blog/harness-engineering | 5e50dfb4 | 3-phase maturity table; victory-declaration/context-anxiety failure modes; senior engineer tax |
| 13 | GitHub — awesome-harness-engineering | github.com/ai-boost/awesome-harness-engineering | de86d518 | Curated foundations/HITL/loop-architecture/eval list; computational vs inferential |

## Removed during ingest
- OpenAI — *Introducing Codex* (openai.com/index/introducing-codex/) — fetched as Cloudflare "Just a moment..." challenge page (no content). Deleted (was source c76a39af). OpenAI/Codex narrative retained via #10 InfoQ + #1 framework. Re-attempt with a non-Cloudflare mirror on next `--refresh` if a clean OpenAI primary is wanted.

## Added 2026-06-25 — `--refresh exa` (Exa semantic discovery, CEO approved 8, 5 live) — 5

### Tier 1 (4)
| # | Source | URL | NLM source_id | Note |
|---|--------|-----|---------------|------|
| 14 | Anthropic — Building Effective Agents | anthropic.com/engineering/building-effective-agents | f21c0247 | Foundational workflows-vs-agents taxonomy; 5 workflow patterns (chaining/routing/parallel/orchestrator-workers/evaluator-optimizer) |
| 15 | Anthropic — Demystifying evals for AI agents | anthropic.com/engineering/demystifying-evals-for-ai-agents | 2efdadc6 | ⭐ capability vs regression evals; pass@k vs pass^k metrics — feeds Mastery Module 4 |
| 16 | LangChain — The Anatomy of an Agent Harness | langchain.com/blog/the-anatomy-of-an-agent-harness | 8e8a13f8 | 5 harness primitives: filesystem / bash+code / sandbox / memory(AGENTS.md) / context-compaction+skills |
| 17 | Martin Fowler/Böckeler — Harness engineering for coding agent users | martinfowler.com/articles/harness-engineering.html | fb5fffec | ⭐ ORIGIN of Guides/Sensors + Computational/Inferential vocab; "harnessability / ambient affordances" |

### Tier 2 (1)
| # | Source | URL | NLM source_id | Note |
|---|--------|-----|---------------|------|
| 18 | Thoughtworks — Harness engineering & agent feedback: AI coding sensors | thoughtworks.com/insights/blog/generative-ai/harness-engineering-agent-feedback-exploring-ai-coding-sensors | 2207316b | Sensors deep-dive companion to Böckeler |

### Approved but NOT ingested (Cloudflare-gated — TRY1/2/3 failed)
- OpenAI *Harness engineering: leveraging Codex* (openai.com/index/harness-engineering/) — Cloudflare "Just a moment...". Doctrine covered by InfoQ #10 + framework #1.
- OpenAI *Unrolling the Codex agent loop* (openai.com/index/unrolling-the-codex-agent-loop/ + engineering.fyi mirror) — both Cloudflare-blocked.
- OpenAI *Unlocking the Codex harness: App Server* (openai.com/index/unlocking-the-codex-harness/) — Cloudflare-blocked.
- **Note:** all openai.com/index/* + engineering.fyi mirror are JS-challenge gated → un-ingestable by NLM. Retry only if a clean text mirror appears.

## Tier classification (after 2026-06-25 refresh)
T1=13 (originators + anchor + refresh) · T2=5 (synthesis) · T3=0 · **Total live = 18.** Council ≥3 T1 rule satisfied (13).

## Refresh guidance
Lĩnh vực đặt tên 2/2026, phát triển rất nhanh. Khuyến nghị `--check-new` hàng tháng. Ứng viên T1 chưa nạp (cân nhắc khi refresh): OpenAI *Unrolling the Codex Agent Loop*, Anthropic *Building Effective Agents* + *Demystifying Evals*, LangChain *The Anatomy of an Agent Harness*, Birgitta Böckeler *Harness engineering for coding agent users*, Red Hat *Structured Workflows*.
