# 🏗️ @bpm/llm-labs Architecture

## Design Philosophy

The @bpm/llm-labs package is built on a **strategy pattern** architecture that allows for:

1. **Modularity** - Each training strategy is independent and self-contained
2. **Extensibility** - New strategies can be added without modifying existing code
3. **Composability** - Strategies can be combined and compared through the orchestrator
4. **Type Safety** - Full TypeScript support with strict type checking
5. **Testability** - Each component is independently testable

## Core Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    LabOrchestrator                          │
│  (Manages experiments, runs strategies, compares results)   │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┬──────────────┐
        │            │            │              │
        ▼            ▼            ▼              ▼
   ┌─────────┐ ┌──────────┐ ┌────────┐ ┌──────────┐
   │Pretraining│Fine-Tuning│ RLHF   │  RAG     │
   │Strategy │ Strategy   │Strategy│ Strategy │
   └────┬────┘ └────┬─────┘ └───┬──┘ └────┬────┘
        │           │           │         │
        └───────────┴───────────┴─────────┘
                    │
                    ▼
            ┌──────────────────┐
            │  BaseStrategy    │
            │  (Abstract)      │
            └──────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
    ┌────────┐ ┌────────┐ ┌──────────┐
    │ Types  │ │Metrics │ │ Config   │
    │        │ │        │ │ Builders │
    └────────┘ └────────┘ └──────────┘
```

## Component Breakdown

### 1. BaseStrategy (Abstract)

**Location**: `src/strategies/base-strategy.ts`

The foundation for all training strategies:

```typescript
abstract class BaseStrategy {
  protected config: TrainingConfig;
  protected metrics: StrategyMetrics[] = [];

  abstract train(): Promise<TrainingResult>;
  protected validateConfig(): void;
  protected recordMetrics(metrics: Record<string, number | string>): void;
  getMetrics(): StrategyMetrics[];
  getStrategyName(): string;
}
```

**Responsibilities**:
- Define the training interface
- Manage configuration validation
- Track metrics during training
- Provide common utilities

### 2. Concrete Strategies

#### PretrainingStrategy
- **File**: `src/strategies/pretraining.ts`
- **Purpose**: Train from scratch on raw text
- **Data Structure**: `TrainingData[]`
- **Metrics**: Loss, Perplexity, Token count

#### FineTuningStrategy
- **File**: `src/strategies/fine-tuning.ts`
- **Purpose**: Supervised instruction tuning
- **Data Structure**: `PromptResponsePair[]`
- **Features**: LoRA/QLoRA support
- **Metrics**: Loss, Accuracy, Validation Loss

#### RLHFStrategy
- **File**: `src/strategies/rlhf.ts`
- **Purpose**: Reinforcement learning from human feedback
- **Data Structure**: `PreferenceExample[]`
- **Process**: Reward model training + PPO
- **Metrics**: Reward accuracy, PPO loss, Average reward

#### RAGStrategy
- **File**: `src/strategies/rag.ts`
- **Purpose**: Retrieval-augmented generation
- **Data Structure**: `RAGDocument[]`
- **Features**: Vector store integration, similarity search
- **Metrics**: Documents indexed, retrieval performance

### 3. LabOrchestrator

**Location**: `src/lab-orchestrator.ts`

Orchestrates multiple strategies:

```typescript
class LabOrchestrator {
  createExperiment(config: ExperimentConfig): void;
  async runExperiment(): Promise<ExperimentResult>;
  compareStrategies(experimentName: string): void;
  exportResults(experimentName: string): string;
  getExperimentResults(name: string): ExperimentResult | undefined;
  getAllExperiments(): ExperimentResult[];
}
```

**Responsibilities**:
- Manage experiment lifecycle
- Execute strategies sequentially or in parallel
- Collect and aggregate results
- Provide comparison and export functionality

### 4. Type System

**Location**: `src/types.ts`

Core type definitions:

```typescript
// Configuration
interface ModelConfig { ... }
interface TrainingConfig { ... }
interface FineTuningConfig extends TrainingConfig { ... }
interface RLHFConfig extends TrainingConfig { ... }
interface RAGConfig { ... }

// Data
interface TrainingData { ... }
interface PromptResponsePair { ... }
interface PreferenceExample { ... }
interface RAGDocument { ... }

// Results
interface TrainingResult { ... }
interface RAGResult { ... }
interface StrategyMetrics { ... }
```

### 5. Configuration Builders

**Location**: `src/utils/config-builder.ts`

Factory functions for creating configurations:

```typescript
createModelConfig(provider, modelId, options?)
createTrainingConfig(model, options?)
createFineTuningConfig(model, options?)
createRLHFConfig(model, options?)
createRAGConfig(vectorStoreType, options?)
```

**Benefits**:
- Automatic API key loading from environment
- Sensible defaults
- Type-safe configuration creation

## Data Flow

### Training Flow

```
User Code
    │
    ├─► Create Strategy
    │       │
    │       ├─► Create Config
    │       │
    │       └─► Instantiate Strategy
    │
    ├─► Add Training Data
    │       │
    │       └─► Strategy stores data
    │
    ├─► Call train()
    │       │
    │       ├─► Validate config
    │       │
    │       ├─► Execute training logic
    │       │
    │       ├─► Record metrics
    │       │
    │       └─► Return TrainingResult
    │
    └─► Access Results
            │
            ├─► result.metrics
            │
            ├─► strategy.getMetrics()
            │
            └─► Export/Compare
```

### Experiment Flow

```
User Code
    │
    ├─► Create LabOrchestrator
    │
    ├─► Create multiple strategies
    │
    ├─► createExperiment()
    │       │
    │       └─► Store experiment config
    │
    ├─► runExperiment()
    │       │
    │       ├─► For each strategy:
    │       │   ├─► Call train()
    │       │   └─► Collect results
    │       │
    │       └─► Return ExperimentResult
    │
    └─► Analyze Results
            │
            ├─► compareStrategies()
            │
            ├─► exportResults()
            │
            └─► getExperimentResults()
```

## Extension Points

### Adding a New Strategy

1. Create a new file in `src/strategies/`
2. Extend `BaseStrategy`
3. Implement `train()` method
4. Add type definitions to `src/types.ts`
5. Export from `src/index.ts`
6. Add tests in `src/__tests__/`

Example:

```typescript
export class MyStrategy extends BaseStrategy {
  async train(): Promise<TrainingResult> {
    // Implementation
  }
}
```

### Adding New Metrics

Metrics are recorded via `recordMetrics()`:

```typescript
this.recordMetrics({
  customMetric1: value1,
  customMetric2: value2,
});
```

Metrics are automatically timestamped and associated with the strategy.

## Testing Strategy

### Unit Tests

- **File**: `src/__tests__/strategies.test.ts`
- **Coverage**: All strategies, configuration, data handling
- **Framework**: Vitest

### Integration Tests

- **File**: `src/__tests__/orchestrator.test.ts`
- **Coverage**: Experiment orchestration, result aggregation
- **Framework**: Vitest

### Test Patterns

```typescript
describe('Strategy', () => {
  it('should initialize', () => { ... });
  it('should add data', () => { ... });
  it('should train successfully', async () => { ... });
  it('should handle errors', async () => { ... });
  it('should record metrics', async () => { ... });
});
```

## Performance Considerations

1. **Metrics Storage** - Metrics are stored in memory; consider pagination for long experiments
2. **Parallel Execution** - Strategies run sequentially; can be parallelized in future
3. **Vector Store** - RAG uses in-memory embeddings; consider external stores for scale
4. **API Calls** - Simulated in current implementation; real API calls will add latency

## Future Enhancements

1. **Parallel Strategy Execution** - Run multiple strategies concurrently
2. **Persistent Storage** - Save experiments to database
3. **Real API Integration** - Connect to actual LLM APIs
4. **Advanced RAG** - Integration with Pinecone, Weaviate, Milvus
5. **Distributed Training** - Support for multi-GPU/multi-node training
6. **Custom Metrics** - User-defined metric collection
7. **Visualization** - Dashboard for experiment results
8. **Checkpointing** - Save and resume training

## Dependencies

- **axios** - HTTP client (for future API integration)
- **dotenv** - Environment variable management
- **TypeScript** - Type safety
- **Vitest** - Testing framework

## Code Quality

- **TypeScript Strict Mode** - Enabled
- **ESLint** - Code style enforcement
- **Type Checking** - Full type coverage
- **Test Coverage** - 24 tests, 100% pass rate
- **Documentation** - Comprehensive inline comments

## Deployment

The package is designed to be:

1. **Installable** - Via npm
2. **Importable** - ES modules with TypeScript support
3. **Extensible** - Easy to add new strategies
4. **Testable** - Full test suite included
5. **Documentable** - Clear API and examples

