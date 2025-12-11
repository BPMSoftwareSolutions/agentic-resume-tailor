# 🎼 Fractal Orchestration: Domain Registry & Code Analysis Overview

**Date**: November 28, 2025  
**Status**: ✅ Active & Experimental  
**Version**: 0.1.0

---

## 📚 Table of Contents

1. [Core Concepts](#core-concepts)
2. [Domain Registry Architecture](#domain-registry-architecture)
3. [Fractal Patterns](#fractal-patterns)
4. [Code Analysis Pipeline](#code-analysis-pipeline)
5. [Key Files & Tools](#key-files--tools)
6. [Getting Started](#getting-started)

---

## Core Concepts

### What is Fractal Orchestration?

Fractal orchestration encodes a **recursive pattern** where:

```
Domain → Orchestrated Domain → System → Subsystem → Higher-Level Domain → Meta-System → ...
```

Each level repeats the same structural pattern:
- **Domains** are static collections of related concerns
- **Orchestrated Domains** gain behavior through musical sequences (movements, beats, handlers)
- **Systems** emerge when orchestrated domains exhibit flow, telemetry, and feedback
- **Subsystems** are systems packaged as reusable black-box capabilities
- **Higher-Level Domains** promote subsystems to first-class governance entities
- **Meta-Systems** coordinate many orchestrated domains into a unified whole

### Key Principle: **"Domain as System, System as Domain"**

At every scale, the architecture looks the same. A domain can be:
- A **system** when viewed from below (composed of handlers and beats)
- A **domain** when viewed from above (as a first-class citizen in governance)
- Both simultaneously in the **meta-system** level

---

## Domain Registry Architecture

### DOMAIN_REGISTRY.json

**Location**: `DOMAIN_REGISTRY.json` (root)  
**Purpose**: Global domain registration index for lineage, link resolution, and validation

**Key Features**:

#### Registry Principles
```json
{
  "registry_principles": [
    "Registry is append-only for active domains (mutations via lifecycle changes)",
    "All domain_ids are globally unique",
    "Lineage hashes are recomputed at validation time",
    "Deprecation retains record but marks domain non-linkable unless migration",
    "Handler scope/kind is immutable per beat (tracks system vs feature logic)"
  ]
}
```

#### Handler Layer Introduction (Active since Nov 27, 2025)

Each beat now includes **handler-level scope/kind metadata** that distinguishes:
- **`plugin`** handlers - Feature logic and business rules
- **`orchestration`** handlers - System logic and governance
- **`infra`** handlers - Infrastructure and platform concerns

This enables:
- Per-scope metrics in symphonic code analysis
- Registry audit to identify missing orchestration handlers
- Self-healing domain to target fixes by scope
- Clear separation: feature logic vs system logic

### orchestration-domains.json

**Location**: `orchestration-domains.json` (root)  
**Purpose**: Registry of all orchestration domains and their sequences

**Structure**:
```json
{
  "domains": [
    {
      "id": "fractal-orchestration-domain-symphony",
      "name": "Fractal Orchestration Domain",
      "type": "orchestration",
      "status": "experimental",
      "sequenceFile": "packages/orchestration/json-sequences/fractal-orchestration-domain-symphony.json",
      "orchestration": {
        "movements": 5,
        "beats": 10,
        "handlers": ["fractalNarrator"]
      }
    }
  ]
}
```

### Domain Registration Structure

Each domain in `DOMAIN_REGISTRY.json` contains:

```json
{
  "domain_id": "orchestration-core",
  "domain_type": "orchestration",
  "status": "active",
  "root_ref": "docs/governance/UNIFIED_GOVERNANCE_AUTHORITY.json",
  "parent_refs": [],
  "checksum": "cc6785471d80179e9e78637bde4c56dc7437b1715c3fd42231c3ea425461d20d",
  "supersedes": [],
  "deprecated": false,
  "ownership": "Platform-Orchestration",
  "orchestration": {
    "schema_ref": "docs/schemas/musical-sequence.schema.json",
    "interface": {
      "name": "MusicalSequence",
      "source": "packages/musical-conductor/modules/communication/sequences/SequenceTypes.ts"
    },
    "registry_ref": {
      "file": "orchestration-domains.json",
      "id": "orchestration-domains-registry"
    }
  }
}
```

**Key Fields**:
- `domain_id`: Globally unique identifier
- `domain_type`: `orchestration`, `workflow`, `capability`, `plugin`, etc.
- `status`: `active`, `deprecated`, `experimental`, `planned`
- `parent_refs`: Array of parent domains in the hierarchy
- `checksum`: Immutable hash for validation
- `ownership`: Responsible team/platform

---

## Fractal Patterns

### The Fractal Orchestration Domain Symphony

**File**: `packages/orchestration/json-sequences/fractal-orchestration-domain-symphony.json`

This is a **didactic symphony** that demonstrates fractal behavior in 5 movements:

#### Movement 1: From Domain to Orchestrated Domain
```
Event: fractal:domain:identified
└─ Recognize a cohesive domain with clear boundaries

Event: fractal:domain:orchestrated
└─ Bind the domain to a MusicalSequence (movements, beats, handlers, rules)
```

#### Movement 2: Domain Becomes System
```
Event: fractal:system:emerges
└─ The orchestrated domain now has flow, telemetry, and self-awareness hooks

Event: fractal:system:stabilized
└─ Feedback loops and governance beats keep the system within safe bounds
```

#### Movement 3: System Becomes Subsystem
```
Event: fractal:subsystem:packaged
└─ Treat the system as a black-box capability with manifest and contracts

Event: fractal:subsystem:composed
└─ Compose this subsystem alongside others inside a higher-order sequence
```

#### Movement 4: Subsystem Becomes Higher-Level Domain
```
Event: fractal:domain:promoted
└─ Promote the subsystem to a first-class domain in the global registry

Event: fractal:domain:linked
└─ Link the new domain into orchestration registries and governance symphonies
```

#### Movement 5: Meta-System and Fractal Ecosystem
```
Event: fractal:metasystem:formed
└─ Multiple orchestration domains now function as a coordinated meta-system

Event: fractal:ecosystem:self-similar
└─ Every level repeats the same pattern: domain as system, system as domain
```

### Events in the Fractal Pattern

All 10 events are tracked in the pipeline:

```
fractal:domain:identified
fractal:domain:orchestrated
fractal:system:emerges
fractal:system:stabilized
fractal:subsystem:packaged
fractal:subsystem:composed
fractal:domain:promoted
fractal:domain:linked
fractal:metasystem:formed
fractal:ecosystem:self-similar
```

---

## Code Analysis Pipeline

### Symphonic Code Analysis Pipeline

**File**: `packages/orchestration/json-sequences/symphonic-code-analysis-pipeline.json`

This is a comprehensive **4-movement analysis pipeline** that measures orchestration code quality and fractal architecture participation.

#### Pipeline Structure

```json
{
  "id": "symphonic-code-analysis-pipeline",
  "name": "Symphonic Code Analysis Pipeline",
  "status": "active",
  "movements": 4,
  "beats": 16,
  "tempo": 120
}
```

#### 4 Movements

##### Movement 1: Code Discovery & Beat Mapping (4 beats)
**Purpose**: Discover all source files, map them to orchestration beats, establish baseline

- Beat 1: Scan orchestration files and identify beat definitions
- Beat 2: Map source code files to beat handlers
- Beat 3: Extract handler signatures and dependencies
- Beat 4: Identify analysis coverage gaps

##### Movement 2: Code Metrics Analysis (4 beats)
**Purpose**: Calculate LOC, complexity, duplication, maintainability metrics

- Beat 1: Calculate lines of code per beat
- Beat 2: Analyze cyclomatic complexity
- Beat 3: Detect code duplication
- Beat 4: Calculate maintainability index

##### Movement 3: Test Coverage Analysis (4 beats)
**Purpose**: Measure statement, branch, function, line coverage

- Beat 1: Collect statement coverage metrics
- Beat 2: Analyze branch coverage
- Beat 3: Calculate function coverage
- Beat 4: Correlate coverage to beats

##### Movement 4: Architecture Conformity & Reporting (4 beats)
**Purpose**: Validate handler-to-beat mapping, calculate conformity, generate reports

- Beat 1: Validate orchestration conformity
- Beat 2: Analyze handler implementation completeness
- **Beat 3: Analyze fractal architecture** ⭐
- Beat 4: Generate report and trend analysis

### Conformity Metrics

The pipeline measures several key metrics:

```json
{
  "metrics": [
    "Lines of code per beat",
    "Lines of code per movement",
    "Test coverage percentage (statement, branch, function, line)",
    "Cyclomatic complexity per beat",
    "Code duplication percentage",
    "Handler implementation completeness",
    "Test assertion count per beat",
    "Architecture conformity score",
    "Dependency coupling metrics",
    "Debt score (technical debt estimate)",
    "Maintainability index per module"
  ],
  "conformityMetrics": {
    "fractalArchitecture": {
      "description": "Fractal architecture participation of orchestration domains (domains-as-systems and systems-as-domains)",
      "benchmark": "≥ 0.50 fractalScore (50%+ orchestration domains acting as systems-of-systems)",
      "impact": "High - Indicates architecture follows recursive self-similar patterns"
    }
  }
}
```

### Key Analysis Events

```
analysis:initiated
movement-1:discovery:started
movement-1:beat:files:collected
movement-1:beat:handlers:identified
movement-1:discovery:complete
movement-2:metrics:started
movement-2:loc:calculated
movement-2:complexity:analyzed
movement-2:duplication:detected
movement-2:metrics:complete
movement-3:coverage:started
movement-3:statement:coverage:calculated
movement-3:branch:coverage:calculated
movement-3:coverage:complete
movement-4:conformity:started
movement-4:architecture:validated
movement-4:fractal:analyzed        ⭐ FRACTAL EVENT
movement-4:trend:analyzed
movement-4:report:generated
analysis:complete
```

---

## Key Files & Tools

### Domain Registry Files

| File | Purpose | Location |
|------|---------|----------|
| `DOMAIN_REGISTRY.json` | Global domain index, lineage, validation | Root |
| `orchestration-domains.json` | Orchestration domain registry | Root |
| `DOMAIN_REGISTRY_QUERY_TOOLS.md` | Query and analysis tools documentation | Root |
| `DOMAIN_REGISTRY_REPRESENTATION.md` | Domain registry data model | Root |

### Orchestration Sequences

| File | Purpose | Location |
|------|---------|----------|
| `fractal-orchestration-domain-symphony.json` | Didactic fractal pattern demo | `packages/orchestration/json-sequences/` |
| `symphonic-code-analysis-pipeline.json` | Code analysis and conformity pipeline | `packages/orchestration/json-sequences/` |

### Analysis Scripts

| Script | Purpose | Location |
|--------|---------|----------|
| `analyze-fractal-architecture.cjs` | Compute fractal metrics from registries | `scripts/` |
| `symphonic-metrics-envelope.cjs` | Wire metrics into symphonic envelope | `scripts/` |
| `validate-orchestration-registry.js` | Validate registry against catalog | `scripts/` |
| `query-lineage.js` | Query data lineage and audit trail | `scripts/` |

### Test Files

| Test | Purpose | Location |
|------|---------|----------|
| `symphonic-fractal-architecture.spec.ts` | Test fractal metrics computation | `scripts/__tests__/` |
| `symphonic-code-analysis-fractal.spec.ts` | Test code analysis fractal encoding | `tests/` |

### Documentation

| Document | Focus | Location |
|----------|-------|----------|
| `SYMPHONIA_ORCHESTRATION_MASTER_REFERENCE.md` | Complete orchestration framework | Root |
| `SYMPHONY_ORCHESTRATION_FRAMEWORK_GUIDE.md` | Orchestration patterns and practices | Root |
| `SYMPHONIC_CODE_ANALYSIS_PIPELINE_DESIGN.md` | Code analysis architecture | Root |
| `ARCHITECTURE_GOVERNANCE_SYMPHONY_GUIDE.md` | Governance frameworks | Root |

---

## Getting Started

### 1. Understanding the Domain Registry

**Quick Tour**:

```bash
# View the domain registry structure
cat DOMAIN_REGISTRY.json | head -100

# Query a specific domain
node scripts/query-lineage.js trace orchestration-core

# Validate the registry
node scripts/validate-orchestration-registry.js
```

### 2. Exploring Fractal Patterns

**Key Concepts**:
- Open `packages/orchestration/json-sequences/fractal-orchestration-domain-symphony.json`
- Read the 5 movements to understand domain → system → domain recursion
- Note the 10 events that track the fractal lifecycle

### 3. Running Code Analysis

**Full Analysis**:
```bash
# Run the symphonic code analysis pipeline
npm run analyze:symphonic:code

# Run specific tests
npx vitest run scripts/__tests__/symphonic-fractal-architecture.spec.ts tests/symphonic-code-analysis-fractal.spec.ts
```

### 4. Analyzing Fractal Architecture

**Key Test Files**:

**`scripts/__tests__/symphonic-fractal-architecture.spec.ts`**:
- Tests fractal metrics computation
- Validates registry alignment
- Checks domain linkage across registries
- Verifies fractal score normalization (0-1)

**Key Assertions**:
```typescript
// All orchestration domains that appear only in projection should be empty
expect(result.summary.projectionOnly).toEqual([]);

// Fractal domain must be in both registries
expect(result.fractalDomain.inOrchestrationRegistry).toBe(true);
expect(result.fractalDomain.inDomainRegistry).toBe(true);

// Fractal score normalizes between 0 and 1
expect(result.summary.fractalScore).toBeGreaterThanOrEqual(0);
expect(result.summary.fractalScore).toBeLessThanOrEqual(1);
```

**`tests/symphonic-code-analysis-fractal.spec.ts`**:
- Tests that pipeline declares fractal architecture as metric
- Verifies `movement-4:fractal:analyzed` event exists
- Confirms fractal work is described in movement 4 beats

### 5. Understanding Handler Scopes

Each beat handler now has:
- **Scope**: `plugin` | `orchestration` | `infra`
- **Kind**: Matches the scope (e.g., `plugin`, `orchestration`, `infrastructure`)

This allows:
- Separate metrics for system vs feature logic
- Targeted governance for orchestration handlers
- Self-healing domain to fix by scope

**Example**:
```json
{
  "beat": 1,
  "event": "fractal:domain:identified",
  "handler": "fractalNarrator",
  "handler_scope": "orchestration",
  "handler_kind": "orchestration"
}
```

### 6. Key Commands

```bash
# Analyze fractal architecture
npm run analyze:symphonic:code

# Run all tests
npm run test

# Run specific test
npx vitest run scripts/__tests__/symphonic-fractal-architecture.spec.ts

# Validate registry
node scripts/validate-orchestration-registry.js

# Query domain lineage
node scripts/query-lineage.js trace orchestration-core
```

---

## Architecture Summary

```
┌────────────────────────────────────────────────────────────────┐
│        Fractal Orchestration Domain Architecture               │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  DOMAIN REGISTRY LAYER                                         │
│  ├─ DOMAIN_REGISTRY.json (global index)                       │
│  ├─ orchestration-domains.json (orchestration index)          │
│  └─ Handler scope/kind metadata (plugin|orch|infra)          │
│                                                                │
│  FRACTAL PATTERN LAYER                                         │
│  └─ fractal-orchestration-domain-symphony.json                │
│     ├─ Movement 1: Domain → Orchestrated Domain              │
│     ├─ Movement 2: Orchestrated Domain → System              │
│     ├─ Movement 3: System → Subsystem                        │
│     ├─ Movement 4: Subsystem → Domain (Promoted)            │
│     └─ Movement 5: Meta-System (Ecosystem)                   │
│                                                                │
│  CODE ANALYSIS LAYER                                           │
│  └─ symphonic-code-analysis-pipeline.json                     │
│     ├─ Movement 1: Discovery & Beat Mapping                  │
│     ├─ Movement 2: Code Metrics                              │
│     ├─ Movement 3: Test Coverage                             │
│     └─ Movement 4: Conformity & Fractal Analysis ⭐          │
│                                                                │
│  METRICS LAYER                                                 │
│  ├─ Per-beat code metrics (LOC, complexity, coverage)        │
│  ├─ Per-scope handler metrics (plugin vs orchestration)      │
│  ├─ Fractal architecture score (0-1)                         │
│  └─ Conformity score (0-100)                                 │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## Next Steps

1. **Explore the Domain Registry**: Open `DOMAIN_REGISTRY.json` and understand the global domain index
2. **Study Fractal Patterns**: Review the 5 movements in `fractal-orchestration-domain-symphony.json`
3. **Run Code Analysis**: Execute `npm run analyze:symphonic:code` to see metrics
4. **Review Test Coverage**: Check the fractal and analysis test files
5. **Understand Handler Scopes**: See how orchestration vs plugin handlers are distinguished

---

**Last Updated**: November 28, 2025  
**Framework Version**: 1.0  
**Status**: ✅ Active & Experimental
