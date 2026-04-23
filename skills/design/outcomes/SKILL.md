Map desired outcomes (DIM format) for each step in a Job Map.

Usage: /outcomes [product_name] OR provide job map interactively.

1. If $ARGUMENTS provided, use as product/domain context; otherwise ask:
   - What product are you working on?
   - Do you have a completed job map? (if yes, paste it; if no, run /jobs first)
   - Who is the target customer segment?
2. Execute outcome mapping:
   - For EACH job step: generate 2-4 desired outcomes
   - Format: "Minimize/Maximize the [metric] of [subject] when [context]"
   - Add Importance (1-10), Satisfaction (1-10), Stability (H/M/L), Source
   - Validate: outcomes must be measurable, solution-neutral, customer-language
   - Minimum: >=10 outcomes total across all steps
   - GATE: Present outcome table -> ask user to review and adjust scores
3. Output: Desired outcomes table ready to feed into /opp

DIM FORMAT: Every outcome must be Desired (Minimize/Maximize) + Important + Measurable.
EVIDENCE RULE: Rate confidence: [FIELD-VALIDATED] > [EXPERT-ESTIMATE] > [ASSUMPTION] -- flag assumptions.
