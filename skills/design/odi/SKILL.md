Run the full ODI (Outcome-Driven Innovation) process for a product.

Usage: /odi [product_name] OR provide details interactively.

1. If $ARGUMENTS provided, use as product_domain; otherwise ask:
   - What product/system are you analyzing? (product_domain)
   - Who is the target customer segment?
   - What do they use today (existing solutions)?
   - Which domain: training / surveillance / engagement / logistics / maritime
2. Read project artifacts if they exist:
   - `1_Projects/{{project}}/Status.md`
   - `1_Projects/{{project}}/_Project_Brief.md`
3. Execute the ODI workflow in full:
   - SECTION 1: Job-to-be-Done (core + emotional + consumption chain)
   - SECTION 2: Job Map (8 steps minimum)
   - SECTION 3: Desired Outcomes table (>=10 outcomes, DIM format)
   - SECTION 4: Opportunity Scores (formula: Importance + max(I-S, 0))
   - SECTION 5: Strategic Recommendation
   - HITL CHECKPOINT: Present top 5 opportunities -> wait for strategic direction before Phase 1
4. Save output to:
   `1_Projects/{{project}}/Phase1-Task/{{PROJECT_NAME}}_ODI_Report_v1.0.md`
   Include YAML frontmatter: project, phase (0a), type (ODI-report), version, created, status, data_confidence

HITL RULE: After opportunity scores calculated, STOP and present top 5. Wait for user to confirm strategic direction.
NAMING RULE: Always prefix filename with project/product name (e.g. VN-12.7MM-SIM_ODI_Report_v1.0.md)
