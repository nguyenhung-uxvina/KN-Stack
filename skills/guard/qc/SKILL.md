---
name: qc
description: >-
  Run the Defense AI QC Gate — 10-check validation framework for any
  AI-generated defense output covering physics plausibility, HITL safety,
  TCVN/regulatory compliance, ROE context boundary, environmental qualification,
  AI confidence calibration, fallback protocol, detection dual-error rate,
  power/logistics budget, and local content. Gate result is PROCEED / HUMAN
  REVIEW REQUIRED / BLOCKED. Check 02 (HITL) fail = immediate halt. Triggers
  on: "qc", "QC gate", "defense AI check", "kiểm tra AI", "validate output",
  "safety check", "HITL", "AI gate defense".
---

Run the Defense AI QC Gate on any AI-generated output before acting on it.

Usage: /qc [product_name] -- then paste or describe the AI output to review.

1. Collect inputs:
   - Product name (from $ARGUMENTS, or ask)
   - Output type: requirements / design / analysis / recommendation / firing_solution / architecture / training_report / other
   - Domain: engagement / training / surveillance / maritime / logistics
   - Design phase: ODI / Phase1 / Phase2 / Phase3 / Phase4 / deployment / operations
   - The AI-generated content to review (ask user to paste it, or describe key claims)
2. Run all 10 checks against the provided content:
   01 Physics Plausibility
   02 HITL Safety Enforcement
   03 TCVN / Regulatory Compliance
   04 ROE Context Boundary
   05 Environmental Qualification
   06 AI Confidence Calibration
   07 Fallback Protocol Completeness
   08 Detection Dual-Error Rate
   09 Power / Logistics Budget
   10 Local Content / Supply Chain
3. Produce the structured QC Gate Report with gate decision:
   PROCEED / HUMAN REVIEW REQUIRED / BLOCKED
4. If any check returns FAIL: STOP. Do not proceed further until resolved.
   Surface the FAIL to the user with specific required action.

SAFETY RULE: Check 02 (HITL) FAIL = immediate halt. No further processing until KN manual review.
GATE LOGIC: FAIL present -> BLOCKED. FLAG only -> HUMAN REVIEW. All PASS -> PROCEED.
CALIBRATION: After each run, note any issues the gate MISSED -> suggest updates.
