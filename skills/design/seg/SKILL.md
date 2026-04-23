Identify under-served customer segments based on outcome satisfaction patterns.

Usage: /seg [product_name] OR provide opportunity data interactively.

1. If $ARGUMENTS provided, use as product context; otherwise ask:
   - What product are you working on?
   - Do you have the opportunity scores from /opp? (paste or describe)
   - What customer groups or roles exist in your target market?
2. Execute segmentation:
   STEP 1 -- Qualitative segmentation: identify 3-5 distinct segments by:
     - Role (e.g., front-line infantry vs training command vs logistics unit)
     - Context/use-case (combat deployment vs training range vs static defense)
     - Constraint profile (budget level, procurement authority, supply chain access)
   STEP 2 -- Score each segment (0-10) on: Market Size, Urgency, Access, Strategic Fit, Local Content potential
   STEP 3 -- Weighted score: Size*0.2 + Urgency*0.3 + Access*0.2 + StrategicFit*0.2 + LocalContent*0.1
   STEP 4 -- Classify: Primary (top scorer) / Secondary / Defer / Ignore
   STEP 5 -- VN_context check: which segment aligns with MoD procurement authority?
   HITL CHECKPOINT: Present segment rankings -> ask "Which primary segment should we target?"
3. Output: Segment ranking table + primary segment recommendation -> feed into Phase 1 requirements

HITL RULE: Do NOT select primary segment without explicit user confirmation.
VN CONTEXT: Always include procurement/operational role analysis, not just geography.
