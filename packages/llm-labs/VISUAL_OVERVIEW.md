# 📊 @bpm/llm-labs Visual Overview

## Package Structure

```
@bpm/llm-labs
│
├── 📚 Documentation
│   ├── README.md                    # Main documentation
│   ├── GETTING_STARTED.md          # Quick start guide
│   ├── PACKAGE_SUMMARY.md          # Package overview
│   ├── ARCHITECTURE.md             # Architecture deep dive
│   └── VISUAL_OVERVIEW.md          # This file
│
├── 🔧 Configuration
│   ├── package.json                # NPM package config
│   ├── tsconfig.json               # TypeScript config
│   ├── vitest.config.ts            # Test config
│   └── .gitignore                  # Git ignore rules
│
└── 📦 Source Code
    └── src/
        ├── index.ts                # Main entry point
        ├── types.ts                # Type definitions
        ├── lab-orchestrator.ts     # Experiment orchestrator
        │
        ├── strategies/             # Training strategies
        │   ├── base-strategy.ts    # Abstract base
        │   ├── pretraining.ts      # Pretraining
        │   ├── fine-tuning.ts      # Fine-tuning + LoRA
        │   ├── rlhf.ts             # RLHF
        │   └── rag.ts              # RAG
        │
        ├── utils/                  # Utilities
        │   └── config-builder.ts   # Config builders
        │
        ├── examples/               # Examples
        │   ├── basic-fine-tuning.ts
        │   ├── compare-strategies.ts
        │   └── rag-example.ts
        │
        └── __tests__/              # Tests
            ├── strategies.test.ts   # 16 tests
            └── orchestrator.test.ts # 8 tests
```

## Training Strategies Comparison

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        TRAINING STRATEGIES                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  🧩 PRETRAINING          🎯 FINE-TUNING        ⚙️ RLHF              🔍 RAG
│  ─────────────────       ──────────────────    ──────────────────    ──────
│                                                                         │
│  • Train from scratch    • Instruction tuning  • Human feedback      • Knowledge
│  • Raw text corpus       • Prompt-response     • Reward model        • Injection
│  • Foundation models     • LoRA/QLoRA          • PPO training        • No training
│                          • Parameter efficient • Alignment           • Real-time
│                                                                         │
│  Compute: Massive        Compute: Moderate    Compute: High         Compute: Low
│  Duration: Weeks-Months  Duration: Hours-Days Duration: Days-Weeks  Duration: Real-time
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Data Flow Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                         USER CODE                                │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
        ┌──────────────────┐    ┌──────────────────┐
        │ Create Strategy  │    │ Create Config    │
        │                  │    │                  │
        │ • Pretraining    │    │ • Model Config   │
        │ • Fine-tuning    │    │ • Training Params│
        │ • RLHF           │    │ • LoRA Settings  │
        │ • RAG            │    │ • RAG Config     │
        └────────┬─────────┘    └────────┬─────────┘
                 │                       │
                 └───────────┬───────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Add Training    │
                    │  Data            │
                    │                  │
                    │ • TrainingData   │
                    │ • Prompt-Response│
                    │ • Preferences    │
                    │ • Documents      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Call train()    │
                    │                  │
                    │ • Validate config│
                    │ • Execute logic  │
                    │ • Record metrics │
                    │ • Return result  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ TrainingResult   │
                    │                  │
                    │ • success        │
                    │ • metrics        │
                    │ • checkpoint     │
                    │ • error (if any) │
                    └──────────────────┘
```

## Orchestrator Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR WORKFLOW                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Create Orchestrator                                         │
│     └─► new LabOrchestrator()                                   │
│                                                                 │
│  2. Define Experiment                                           │
│     └─► createExperiment({                                      │
│           name: "My Experiment",                                │
│           strategies: [strategy1, strategy2, ...]               │
│         })                                                       │
│                                                                 │
│  3. Run Experiment                                              │
│     └─► runExperiment()                                         │
│         ├─► For each strategy:                                  │
│         │   ├─► Validate config                                 │
│         │   ├─► Execute train()                                 │
│         │   └─► Collect results                                 │
│         └─► Return ExperimentResult                             │
│                                                                 │
│  4. Analyze Results                                             │
│     ├─► compareStrategies()  ─► Display comparison table        │
│     ├─► exportResults()      ─► Export as JSON                  │
│     └─► getMetrics()         ─► Access detailed metrics         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Type System Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│                      TYPE HIERARCHY                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Configuration Types                                            │
│  ├─ ModelConfig                                                 │
│  ├─ TrainingConfig                                              │
│  ├─ FineTuningConfig (extends TrainingConfig)                   │
│  ├─ RLHFConfig (extends TrainingConfig)                         │
│  └─ RAGConfig                                                   │
│                                                                 │
│  Data Types                                                     │
│  ├─ TrainingData                                                │
│  ├─ PromptResponsePair                                          │
│  ├─ PreferenceExample                                           │
│  └─ RAGDocument                                                 │
│                                                                 │
│  Result Types                                                   │
│  ├─ TrainingResult                                              │
│  ├─ RAGResult                                                   │
│  ├─ StrategyMetrics                                             │
│  └─ ExperimentResult                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Feature Matrix

```
┌──────────────────┬──────────┬──────────┬──────┬─────┐
│ Feature          │ Pretrain │ FineTune │ RLHF │ RAG │
├──────────────────┼──────────┼──────────┼──────┼─────┤
│ Raw text data    │    ✅    │    ❌    │  ❌  │  ❌ │
│ Instruction data │    ❌    │    ✅    │  ❌  │  ❌ │
│ Preference data  │    ❌    │    ❌    │  ✅  │  ❌ │
│ Documents        │    ❌    │    ❌    │  ❌  │  ✅ │
│ LoRA support     │    ❌    │    ✅    │  ❌  │  ❌ │
│ Reward model     │    ❌    │    ❌    │  ✅  │  ❌ │
│ Vector store     │    ❌    │    ❌    │  ❌  │  ✅ │
│ Metrics tracking │    ✅    │    ✅    │  ✅  │  ✅ │
│ Error handling   │    ✅    │    ✅    │  ✅  │  ✅ │
└──────────────────┴──────────┴──────────┴──────┴─────┘
```

## Configuration Builder Functions

```
┌─────────────────────────────────────────────────────────────────┐
│              CONFIGURATION BUILDER FUNCTIONS                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  createModelConfig(provider, modelId, options?)                 │
│  └─► Returns: ModelConfig                                       │
│      • Loads API keys from environment                          │
│      • Sets temperature, maxTokens                              │
│                                                                 │
│  createTrainingConfig(model, options?)                          │
│  └─► Returns: TrainingConfig                                    │
│      • Sets learning rate, batch size, epochs                   │
│      • Configures validation split                              │
│                                                                 │
│  createFineTuningConfig(model, options?)                        │
│  └─► Returns: FineTuningConfig                                  │
│      • Extends TrainingConfig                                   │
│      • Adds LoRA rank, alpha, target modules                    │
│      • Supports QLoRA                                           │
│                                                                 │
│  createRLHFConfig(model, options?)                              │
│  └─► Returns: RLHFConfig                                        │
│      • Extends TrainingConfig                                   │
│      • Configures PPO epochs, clip ratio                        │
│      • Sets reward model path                                   │
│                                                                 │
│  createRAGConfig(vectorStoreType, options?)                     │
│  └─► Returns: RAGConfig                                         │
│      • Selects vector store (local, pinecone, etc.)             │
│      • Sets embedding model, retrieval top-k                    │
│      • Configures similarity threshold                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Test Coverage

```
┌─────────────────────────────────────────────────────────────────┐
│                      TEST COVERAGE                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  strategies.test.ts (16 tests)                                  │
│  ├─ PretrainingStrategy (4 tests)                               │
│  ├─ FineTuningStrategy (4 tests)                                │
│  ├─ RLHFStrategy (3 tests)                                      │
│  ├─ RAGStrategy (3 tests)                                       │
│  └─ Metrics Recording (2 tests)                                 │
│                                                                 │
│  orchestrator.test.ts (8 tests)                                 │
│  ├─ Initialization (1 test)                                     │
│  ├─ Experiment Creation (1 test)                                │
│  ├─ Experiment Execution (1 test)                               │
│  ├─ Results Retrieval (2 tests)                                 │
│  ├─ Results Export (1 test)                                     │
│  └─ Error Handling (2 tests)                                    │
│                                                                 │
│  Total: 24 tests, 100% pass rate ✅                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Reference

### Import Everything

```typescript
import {
  // Types
  ModelConfig,
  TrainingConfig,
  TrainingResult,
  
  // Strategies
  PretrainingStrategy,
  FineTuningStrategy,
  RLHFStrategy,
  RAGStrategy,
  
  // Orchestrator
  LabOrchestrator,
  
  // Config Builders
  createModelConfig,
  createTrainingConfig,
  createFineTuningConfig,
  createRLHFConfig,
  createRAGConfig,
} from '@bpm/llm-labs';
```

### Common Patterns

```typescript
// 1. Create and train a strategy
const config = createFineTuningConfig(modelConfig);
const strategy = new FineTuningStrategy(config);
strategy.addTrainingPairs([...]);
const result = await strategy.train();

// 2. Run multiple strategies
const lab = new LabOrchestrator();
lab.createExperiment({ name: 'Test', strategies: [...] });
await lab.runExperiment();
lab.compareStrategies('Test');

// 3. Access metrics
const metrics = strategy.getMetrics();
const results = lab.exportResults('Test');
```

## Performance Characteristics

```
┌──────────────────┬──────────┬──────────┬──────┬─────┐
│ Metric           │ Pretrain │ FineTune │ RLHF │ RAG │
├──────────────────┼──────────┼──────────┼──────┼─────┤
│ Compute          │ Massive  │ Moderate │ High │ Low │
│ Duration         │ Weeks    │ Hours    │ Days │ Real│
│ Memory           │ Huge     │ Moderate │ High │ Low │
│ Scalability      │ Excellent│ Good     │ Good │ Exc │
│ Customization    │ Limited  │ High     │ High │ High│
└──────────────────┴──────────┴──────────┴──────┴─────┘
```

---

**For more details, see:**
- README.md - Main documentation
- GETTING_STARTED.md - Quick start guide
- ARCHITECTURE.md - Architecture deep dive

