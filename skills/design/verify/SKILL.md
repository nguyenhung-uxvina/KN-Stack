Generate a verification plan mapping requirements to test and inspection methods.

Usage: /verify [project_name] OR provide requirements list interactively.

1. If $ARGUMENTS provided, use as project name; otherwise ask:
   - What project is this for?
   - Do you have the requirements list from Phase 1? (paste or reference file path)
   - Are there any safety-critical or HITL requirements in the list?
2. Read project artifacts:
   - `1_Projects/{{project}}/Status.md`
   - Phase 1 requirements list
3. Execute verification plan:
   - For each requirement: map to verification method using A/I/T/D taxonomy:
     A = Analysis (calculation/simulation)
     I = Inspection (visual check / measurement)
     T = Test (functional/environmental test)
     D = Demonstration (live operational demo)
   - SAFETY RULE: Safety-critical requirements must use T or D. A alone = NOT ACCEPTABLE.
   - HITL requirements must be verified by D (live demonstration with human-in-loop)
   - For each test: specify method, pass/fail criteria, environment, responsible party
   - Group by: Unit test | Integration test | System test | Acceptance test
   - Flag any requirements that cannot be verified with current resources -> escalate
4. Save output to:
   `1_Projects/{{project}}/VnV/{{PROJECT_NAME}}_Verification_Plan_v1.0.md`

SAFETY RULE: T or D required for safety-critical requirements. Never accept A-only for HITL or lethal system requirements.
HITL RULE: Present plan -> get explicit sign-off before proceeding to production.
