# 🧠 @bpm/llm-labs

A comprehensive framework for experimenting with different LLM training strategies and optimization techniques.

## 📚 Training Strategies

### 1. **Pretraining** 🧩
Training from scratch on raw text corpora to teach language fundamentals.
- **Use case**: Building foundation models or domain-specific models
- **Compute**: Massive (thousands of GPUs/TPUs)
- **Duration**: Weeks to months

### 2. **Fine-Tuning** 🎯
Supervised instruction tuning on prompt-response pairs with optional LoRA.
- **Use case**: Teaching models to follow specific instructions and output formats
- **Compute**: Moderate (single GPU or small cluster)
- **Duration**: Hours to days
- **Features**: LoRA/QLoRA support for parameter-efficient training

### 3. **RLHF** ⚙️
Reinforcement Learning from Human Feedback using reward models and PPO.
- **Use case**: Aligning models with human preferences
- **Compute**: High (requires reward model + PPO)
- **Duration**: Days to weeks

### 4. **RAG** 🔍
Retrieval-Augmented Generation for dynamic knowledge injection.
- **Use case**: Adding external knowledge without retraining (legal, medical, financial)
- **Compute**: Low (no model training)
- **Duration**: Real-time

## 🚀 Quick Start

### Installation

```bash
npm install @bpm/llm-labs
```

### Basic Usage

```typescript
import {
  createModelConfig,
  createTrainingConfig,
  FineTuningStrategy,
  LabOrchestrator,
} from '@bpm/llm-labs';

// Create model configuration
const modelConfig = createModelConfig('openai', 'gpt-3.5-turbo', {
  apiKey: process.env.OPENAI_API_KEY,
});

// Create training configuration
const trainingConfig = createTrainingConfig(modelConfig, {
  epochs: 3,
  batchSize: 32,
});

// Create fine-tuning strategy
const strategy = new FineTuningStrategy(trainingConfig);

// Add training data
strategy.addTrainingPairs([
  {
    prompt: 'What is machine learning?',
    response: 'Machine learning is a subset of AI...',
  },
  // ... more pairs
]);

// Train
const result = await strategy.train();
console.log(result);
```

### Running Experiments

```typescript
import { LabOrchestrator, PretrainingStrategy, FineTuningStrategy } from '@bpm/llm-labs';

const lab = new LabOrchestrator();

lab.createExperiment({
  name: 'Compare Training Strategies',
  description: 'Testing pretraining vs fine-tuning',
  strategies: [
    new PretrainingStrategy(pretrainingConfig),
    new FineTuningStrategy(finetuningConfig),
  ],
});

const results = await lab.runExperiment();
lab.compareStrategies('Compare Training Strategies');
```

## 🔧 Configuration

### Model Configuration

```typescript
const modelConfig = createModelConfig('anthropic', 'claude-3-sonnet', {
  apiKey: process.env.CLAUDE_API_KEY,
  temperature: 0.7,
  maxTokens: 2048,
});
```

### Fine-Tuning with LoRA

```typescript
const ftConfig = createFineTuningConfig(modelConfig, {
  loraRank: 8,
  loraAlpha: 16,
  targetModules: ['q_proj', 'v_proj'],
  useQLoRA: true,
});
```

### RAG Configuration

```typescript
import { createRAGConfig, RAGStrategy } from '@bpm/llm-labs';

const ragConfig = createRAGConfig('local', {
  embeddingModel: 'all-MiniLM-L6-v2',
  retrievalTopK: 5,
  similarityThreshold: 0.3,
});

const ragStrategy = new RAGStrategy(trainingConfig, ragConfig);
```

## 📊 Metrics & Monitoring

Each strategy tracks metrics during training:

```typescript
const strategy = new FineTuningStrategy(config);
// ... train ...
const metrics = strategy.getMetrics();
console.log(metrics);
```

## 🧪 Testing

```bash
npm test
```

## 📖 API Reference

### Strategies

- `PretrainingStrategy` - Full model pretraining
- `FineTuningStrategy` - Instruction tuning with LoRA support
- `RLHFStrategy` - Reinforcement learning from human feedback
- `RAGStrategy` - Retrieval-augmented generation

### Orchestrator

- `LabOrchestrator` - Manage and run multiple experiments
- `createExperiment()` - Define an experiment
- `runExperiment()` - Execute all strategies
- `compareStrategies()` - Compare results
- `exportResults()` - Export as JSON

## 🔐 Environment Variables

```bash
OPENAI_API_KEY=sk-...
CLAUDE_API_KEY=sk-ant-...
```

## 📝 License

MIT

## 🤝 Contributing

Contributions welcome! Please follow the existing code style and add tests for new features.

