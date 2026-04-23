Calculate Opportunity Scores and prioritize underserved customer outcomes.

Usage: /opp [product_name] OR provide outcomes table interactively.

1. If $ARGUMENTS provided, use as product context; otherwise ask:
   - What product are you working on?
   - Do you have a desired outcomes table with Importance + Satisfaction scores? (paste or provide)
2. Execute opportunity scoring:
   - Calculate: Opportunity = Importance + max(Importance - Satisfaction, 0)
   - Classify: >=10 = UNDERSERVED | 8-9 = SLIGHTLY UNDERSERVED | 6-7 = SERVED | <6 = OVERSERVED
   - EXCEPTION: HITL/safety-critical outcomes score OVERSERVED only if satisfaction >=9 -- never reduce safety requirements
   - Rank all outcomes by Opportunity Score
   - Add Investment Type column: S=Structural (hardware/architecture) vs SW=Software (algorithm/UX)
   - Identify top 5 opportunities with strategic rationale
   - Plot strategic quadrant: Importance vs Satisfaction
   - Recommend strategy: DOMINATE / DISRUPT / IMPROVE / RETREAT
   - HITL CHECKPOINT: Present ranked table + recommendation -> WAIT for strategic direction
3. Output: Ranked opportunity table + strategy recommendation ready to feed into /seg or Phase 1

HITL RULE: STOP after presenting opportunity scores. Wait for user to confirm strategic direction before proceeding.
SAFETY RULE: Never classify HITL-mandatory outcomes as OVERSERVED unless satisfaction >=9.
