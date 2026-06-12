---
name: jobs
description: Analyzes the Job-to-be-Done (JTBD) for a product or customer segment by defining the core functional job (solution-neutral), emotional jobs, consumption chain jobs, and an 8-step Job Map. Output feeds directly into /outcomes for outcome-driven innovation. Triggers on: "jobs to be done", "JTBD", "job map", "what job does this do", "công việc cần hoàn thành", "phân tích nhu cầu khách hàng".
---
Analyze the Job-to-be-Done for a product or customer segment.

Usage: /jobs [product_name] OR provide details interactively.

1. If $ARGUMENTS provided, use as product/domain context; otherwise ask:
   - What product or system are you analyzing?
   - Who is the target customer?
   - What are they trying to accomplish (initial hypothesis)?
2. Execute the JTBD analysis:
   - Define core functional job (verb + object + context, solution-neutral)
   - Identify emotional jobs (personal + social)
   - Map consumption chain jobs (Before / During / After)
   - Construct 8-step Job Map
   - GATE: Present completed job map -> ask "Does this capture what customers are really trying to do?"
   - Wait for user confirmation before passing to /outcomes
3. Output: Job map table + JTBD statement ready to feed into /outcomes

HITL RULE: Present job map and wait for explicit confirmation before proceeding to outcome mapping.
SOLUTION-NEUTRAL RULE: Never name specific products in job statements -- describe results, not means.
