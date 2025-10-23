# 📦 @bpm/llm-labs Package Summary

## Overview

A comprehensive TypeScript framework for experimenting with different LLM training strategies and optimization techniques. This package provides a modular, extensible architecture for implementing and comparing various approaches to training and fine-tuning large language models.

## Package Structure

```
packages/llm-labs/
├── src/
│   ├── __tests__/
│   │   ├── strategies.test.ts      # Tests for all training strategies
│   │   └── orchestrator.test.ts    # Tests for experiment orchestration
│   ├── examples/
│   │   ├── basic-fine-tuning.ts    # Fine-tuning example
│   │   ├── compare-strategies.ts   # Multi-strategy comparison
│   │   └── rag-example.ts          # RAG implementation example
│   ├── strategies/
│   │   ├── base-strategy.ts        # Abstract base class
│   │   ├── pretraining.ts          # Pretraining strategy
│   │   ├── fine-tuning.ts          # Fine-tuning with LoRA support
│   │   ├── rlhf.ts                 # RLHF strategy
│   │   └── rag.ts                  # RAG strategy
│   ├── utils/
│   │   └── config-builder.ts       # Configuration utilities
│   ├── types.ts                    # TypeScript type definitions
│   ├── lab-orchestrator.ts         # Experiment orchestration
│   └── index.ts                    # Main entry point
├── package.json
├── tsconfig.json
├── vitest.config.ts
├── README.md
├── GETTING_STARTED.md
├── LICENSE
└── .gitignore
```

## Core Components

### 1. **Training Strategies**

#### PretrainingStrategy
- **Purpose**: Train models from scratch on raw text corpora
- **Use Case**: Building foundation models or domain-specific models
- **Compute**: Massive (thousands of GPUs/TPUs)
- **Duration**: Weeks to months
- **Key Methods**:
  - `addTrainingData()` - Add raw text data
  - `train()` - Execute pretraining

#### FineTuningStrategy
- **Purpose**: Supervised instruction tuning on prompt-response pairs
- **Use Case**: Teaching models to follow specific instructions
- **Compute**: Moderate (single GPU or small cluster)
- **Duration**: Hours to days
- **Features**: LoRA/QLoRA support for parameter-efficient training
- **Key Methods**:
  - `addTrainingPairs()` - Add instruction data
  - `addValidationPairs()` - Add validation data
  - `train()` - Execute fine-tuning

#### RLHFStrategy
- **Purpose**: Reinforcement Learning from Human Feedback
- **Use Case**: Aligning models with human preferences
- **Compute**: High (requires reward model + PPO)
- **Duration**: Days to weeks
- **Key Methods**:
  - `addPreferenceData()` - Add human preference rankings
  - `train()` - Execute RLHF training

#### RAGStrategy
- **Purpose**: Retrieval-Augmented Generation
- **Use Case**: Dynamic knowledge injection without retraining
- **Compute**: Low (no model training)
- **Duration**: Real-time
- **Key Methods**:
  - `addDocuments()` - Add documents to vector store
  - `retrieve()` - Query and retrieve relevant documents
  - `train()` - Index documents

### 2. **LabOrchestrator**

Manages and orchestrates multiple training experiments:

- `createExperiment()` - Define an experiment with multiple strategies
- `runExperiment()` - Execute all strategies in parallel
- `compareStrategies()` - Display side-by-side comparison
- `exportResults()` - Export results as JSON
- `getExperimentResults()` - Retrieve specific experiment
- `getAllExperiments()` - Get all completed experiments

### 3. **Configuration Builders**

Utility functions for creating configurations:

- `createModelConfig()` - Create model configuration with API keys
- `createTrainingConfig()` - Create basic training configuration
- `createFineTuningConfig()` - Create fine-tuning config with LoRA
- `createRLHFConfig()` - Create RLHF configuration
- `createRAGConfig()` - Create RAG configuration

## Type System

### Core Types

```typescript
// Model configuration
interface ModelConfig {
  provider: 'openai' | 'anthropic' | 'local';
  modelId: string;
  apiKey?: string;
  temperature?: number;
  maxTokens?: number;
}

// Training data
interface TrainingData {
  id: string;
  text: string;
  metadata?: Record<string, unknown>;
}

// Prompt-response pairs
interface PromptResponsePair {
  prompt: string;
  response: string;
  metadata?: Record<string, unknown>;
}

// Preference examples
interface PreferenceExample {
  prompt: string;
  preferred: string;
  rejected: string;
  metadata?: Record<string, unknown>;
}

// Training results
interface TrainingResult {
  success: boolean;
  modelId: string;
  trainingTime: number;
  metrics: Record<string, number | undefined>;
  checkpointPath?: string;
  error?: string;
}

// RAG documents
interface RAGDocument {
  id: string;
  content: string;
  metadata?: Record<string, unknown>;
  embedding?: number[];
}
```

## Testing

### Test Coverage

- **24 tests** across 2 test files
- **100% pass rate**
- Tests cover:
  - Strategy initialization and configuration
  - Data addition and retrieval
  - Training execution and error handling
  - Metrics recording and retrieval
  - Experiment orchestration
  - Results export and comparison

### Running Tests

```bash
npm test              # Run all tests
npm test:ui          # Interactive UI
npm run type-check   # Type checking
npm run lint         # Linting
```

## API Keys

The package supports multiple LLM providers:

### OpenAI
```bash
export OPENAI_API_KEY=sk-...
```

### Anthropic Claude
```bash
export CLAUDE_API_KEY=sk-ant-...
```

### Local Models
No API key required for local models.

## Examples

Three comprehensive examples are included:

1. **basic-fine-tuning.ts** - Simple fine-tuning workflow
2. **compare-strategies.ts** - Running multiple strategies
3. **rag-example.ts** - RAG implementation

Run examples:
```bash
npx ts-node src/examples/basic-fine-tuning.ts
npx ts-node src/examples/compare-strategies.ts
npx ts-node src/examples/rag-example.ts
```

## Key Features

✅ **Modular Architecture** - Easy to extend with new strategies
✅ **Type-Safe** - Full TypeScript support with strict mode
✅ **Comprehensive Testing** - 24 unit tests with 100% pass rate
✅ **Configuration Builders** - Simplified configuration creation
✅ **Metrics Tracking** - Built-in metrics recording and analysis
✅ **Experiment Orchestration** - Run and compare multiple strategies
✅ **RAG Support** - Vector store integration for knowledge injection
✅ **LoRA Support** - Parameter-efficient fine-tuning
✅ **Environment Variables** - Automatic API key loading
✅ **Well Documented** - Comprehensive README and examples

## Dependencies

- **axios** - HTTP client for API calls
- **dotenv** - Environment variable management
- **TypeScript** - Type safety
- **Vitest** - Testing framework

## Build & Distribution

```bash
npm run build        # Compile TypeScript to dist/
npm run dev         # Watch mode
npm run type-check  # Type checking
npm run lint        # ESLint
```

## License

MIT - See LICENSE file

## Next Steps

1. Install the package: `npm install @bpm/llm-labs`
2. Set up API keys in environment variables
3. Review GETTING_STARTED.md for quick start
4. Explore examples in src/examples/
5. Run tests to verify setup: `npm test`
6. Start experimenting with different strategies!

