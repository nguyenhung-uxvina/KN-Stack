---
name: forge-library
description: Manage the Workshop X AI model library — catalog validated models, track cross-product transfers, and activate R5 compound loop. This skill should be used when the user asks about "model library", "reuse model", "transfer learning", "catalog model", "thu vien mo hinh", "cross-product AI", or "R5 compound". Stage 3 of FORGE lifecycle.
---

# Forge Library — Model Library & Reuse Management

Catalog validated AI models into the Workshop X model library. Track cross-product transfer opportunities and execute transfers. This is the mechanism that activates R5 (Model Reuse Compound) — every library entry is a potential multiplier across the portfolio.

## When to Use

- After forge-validate Stage 1+ produces a validated model
- When forge-scout identifies reuse potential across products
- Monthly library inventory review
- When a new product needs AI and library might have a match

## Model ID Convention

```
WX-[TYPE]-[NUMBER]
Types: DET (Detection), CLS (Classification), TRK (Tracking),
       PRD (Prediction), CTL (Control), SEG (Segmentation)
Example: WX-DET-001 (first detection model)
```

## Workflow

### Step 1: Catalog Model

For each validated model, create a library entry:

```
MODEL LIBRARY ENTRY — {{model_id}}
Date: {{today}}

## METADATA
| Field | Value |
|-------|-------|
| Model ID | WX-{{TYPE}}-{{NNN}} |
| Name | {{descriptive name}} |
| Type | Detection / Classification / Tracking / Prediction / Control |
| Source product | {{which product created this model}} |
| Created | {{date}} |
| Last validated | {{date}} |
| Validation stage | Lab / Field Sim / Operational / Continuous |

## SPECIFICATIONS
| Spec | Value |
|------|-------|
| Input | {{sensor type, resolution, format}} |
| Output | {{data format, classes/values}} |
| Latency | {{ms}} |
| Accuracy | {{metric @ conditions}} |
| Model size | {{MB}} |
| Compute requirement | {{platform: CM4/Jetson/etc}} |

## PERFORMANCE ENVELOPE (from forge-validate)
| Condition | Performance | Category |
|-----------|------------|----------|
| {{good conditions}} | {{metric}} | WORKS WELL |
| {{edge conditions}} | {{metric}} | DEGRADED |
| {{bad conditions}} | {{metric}} | FAILS |

## TRAINING DATA
| Dataset | Size | Source | Availability |
|---------|------|--------|-------------|

## REUSE POTENTIAL
| Target Product | Sub-function Match | Transfer Effort | Readiness (1-5) |
|---------------|-------------------|----------------|:---------------:|
| | | Direct / Fine-tune / Retrain | |
```

### Step 2: Cross-Product Matching

Scan portfolio for products with sub-functions matching this model:

```
CROSS-PRODUCT MATCH REPORT — {{model_id}}

Matches found: {{N}}
| Product | Sub-function | Similarity | Transfer Effort | Value |
|---------|-------------|:----------:|----------------|-------|
| | | HIGH/MED | Direct/Fine-tune/Retrain | |

Transfer effort guide:
- Direct: same input/output, deploy as-is
- Fine-tune: same architecture, new training data needed
- Retrain: same concept, significant new development
```

### Step 3: CEO Transfer Decision (Core)

Present matches. CEO decides:
- "Worth the effort?" (team capacity, timeline)
- "Receiving product ready?" (HELIX phase check)
- "Customer would accept transferred model?"
- Decision: Transfer approved / Defer / Not applicable

### Step 4: Execute Transfer (if approved)

Generate:
1. Fine-tuning plan (data, compute, timeline)
2. Validation plan for new context (forge-validate)
3. Integration spec for receiving product's HELIX ICD
4. Track: time saved, cost saved, performance delta

### Step 5: Library Dashboard

```
MODEL LIBRARY DASHBOARD — Workshop X
Date: {{today}}

| Model ID | Type | Source | Validated | Products Using | Transfers |
|----------|------|--------|-----------|:-------------:|:---------:|
| | | | Stage N | N | N |

TOTALS:
- Library size: {{N}} models ({{production}} + {{experimental}})
- Total transfers: {{N}} this quarter (target: 1)
- Utilization: {{%}} products using library models
- Compound multiplier: {{total products served / total models}}

R5 STATUS: {{ACTIVE / DORMANT}}
- Active: >=1 transfer in last 90 days
- Dormant: 0 transfers → flag in forge-portfolio
```

## HELIX Integration

```
forge-library READS FROM HELIX:
  - Function structures → which functions need AI models?
  - Concept evaluation → library models should be options
  - Integration debt → model interface matches ICD?
  - Quality gate → validation passed? (prerequisite for entry)

forge-library WRITES TO HELIX:
  - "Model WX-DET-001 available" → concept options expanded
  - "Model requires input X, output Y" → ICD spec
  - "Transfer to Product B" → new project-init
  - "Performance Envelope" → requirements calibration
```

### Step 6: Component Reuse Matrix (from Pattern Library D2)

Beyond AI models, track HARDWARE component reuse across the portfolio. This activates platform economics — shared components reduce per-unit development cost.

```
COMPONENT REUSE MATRIX — Workshop X Portfolio
Date: {{today}}

CATEGORIES:
  1. Compute    (SBC, AI accelerator, MCU)
  2. Sensing    (cameras, microphones, radar, IMU, depth, pressure)
  3. Comms      (WiFi, LoRa, BLE, 4G, Ethernet, Iridium)
  4. Power      (battery chemistry, DC-DC, BMS, solar, charging)
  5. Enclosure  (materials, sealing, mounting, thermal management)
  6. Software   (OS, middleware, frameworks, protocols)

REUSE ANALYSIS — {{product_A}} × {{product_B}}
| Category | Component | Product A | Product B | Reuse | Notes |
|----------|-----------|-----------|-----------|:-----:|-------|
| Compute  | Pixhawk 6X | VN-USV-SS | VN-XUONG | 100% | Same autopilot |
| Comms    | LoRa 433MHz | VN-USV-SS | BB-01 | 100% | Same module |
| Sensing  | IMU (MPU-6050) | VN-USV-SS | VN-12.7MM | 80% | Same chip, diff config |
| Power    | LiFePO4 48V | VN-USV-SS | — | 0% | Unique to marine |
| Enclosure| HDPE hull | VN-USV-SS | VN-AST | 60% | Same material, diff form |
| Software | ArduSub/ROS2 | VN-USV-SS | VN-XUONG | 70% | Shared nav stack |

SUMMARY:
  Overall reuse: __% (target: ≥50% across portfolio)
  Per-category: Compute __% | Sensing __% | Comms __% | Power __% | Enclosure __% | SW __%
  Development amortization: shared component dev cost ÷ N products
  Unique components: __ items (0% reuse — custom or product-specific)

RECOMMENDATIONS:
  1. {{Standardize component X across products Y and Z}}
  2. {{Replace product-specific component with platform-common alternative}}
  3. {{Create shared component spec for next procurement cycle}}
```

**When to run:** Monthly (with forge-portfolio), or when a new product enters Phase 2 (concept selection should consider platform reuse).

**Integration with AI model library:** Component reuse is the HARDWARE analog of model reuse. Combined view: "What % of this product is shared with the platform?"

## Rules

- Only VALIDATED models enter the library (forge-validate Stage 1+ minimum)
- Performance Envelope is MANDATORY for every entry
- Track transfer metrics obsessively — this is where compound value lives
- 0 transfers in 90 days = R5 Dormant → flag in forge-portfolio
- Model versioning: increment on retrain, maintain compatibility notes
- Component reuse matrix: update when new product enters Phase 2 or portfolio review
- Do NOT force reuse where requirements fundamentally differ (Pattern Library D2 rule)
- Reuse % target: ≥50% across portfolio — flag if below in forge-portfolio

## COD Classification

- Model cataloging: Offload (O1) — AI creates library entry
- Cross-product matching: Offload (O2) — AI identifies matches
- Transfer decision: **Core (C)** — CEO decides resource allocation
- Transfer execution plan: Offload (O2) — AI generates plan
