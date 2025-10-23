# 🚀 Getting Started with @bpm/llm-labs

## Installation

```bash
npm install @bpm/llm-labs
```

## Environment Setup

Set up your API keys as environment variables:

```bash
# For OpenAI models
export OPENAI_API_KEY=sk-...

# For Anthropic Claude models
export CLAUDE_API_KEY=sk-ant-...
```

## Quick Examples

### 1. Fine-Tune a Model

```typescript
import {
  createModelConfig,
  createFineTuningConfig,
  FineTuningStrategy,
} from '@bpm/llm-labs';

// Create configuration
const modelConfig = createModelConfig('openai', 'gpt-3.5-turbo');
const trainingConfig = createFineTuningConfig(modelConfig, {
  epochs: 3,
  batchSize: 16,
  loraRank: 8, // Use LoRA for efficiency
});

// Create strategy
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
console.log('Training complete:', result);
```

### 2. Compare Multiple Strategies

```typescript
import {
  createModelConfig,
  createTrainingConfig,
  createFineTuningConfig,
  PretrainingStrategy,
  FineTuningStrategy,
  LabOrchestrator,
} from '@bpm/llm-labs';

const lab = new LabOrchestrator();

// Create strategies
const pretraining = new PretrainingStrategy(pretrainingConfig);
const finetuning = new FineTuningStrategy(finetuningConfig);

// Add data
pretraining.addTrainingData([...]);
finetuning.addTrainingPairs([...]);

// Run experiment
lab.createExperiment({
  name: 'Strategy Comparison',
  strategies: [pretraining, finetuning],
});

const results = await lab.runExperiment();
lab.compareStrategies('Strategy Comparison');
```

### 3. Use RAG for Knowledge Injection

```typescript
import {
  createModelConfig,
  createTrainingConfig,
  createRAGConfig,
  RAGStrategy,
} from '@bpm/llm-labs';

const modelConfig = createModelConfig('openai', 'gpt-3.5-turbo');
const trainingConfig = createTrainingConfig(modelConfig);
const ragConfig = createRAGConfig('local', {
  embeddingModel: 'all-MiniLM-L6-v2',
  retrievalTopK: 5,
});

const rag = new RAGStrategy(trainingConfig, ragConfig);

// Add documents
rag.addDocuments([
  {
    id: 'doc1',
    content: 'Machine learning enables systems to learn from data...',
    metadata: { source: 'AI Basics' },
  },
  // ... more documents
]);

// Index documents
await rag.train();

// Retrieve relevant documents
const results = await rag.retrieve({
  query: 'What is machine learning?',
  topK: 3,
});

console.log('Retrieved documents:', results.documents);
```

### 4. RLHF Training

```typescript
import {
  createModelConfig,
  createRLHFConfig,
  RLHFStrategy,
} from '@bpm/llm-labs';

const modelConfig = createModelConfig('anthropic', 'claude-3-sonnet');
const rlhfConfig = createRLHFConfig(modelConfig, {
  ppoEpochs: 4,
  clipRatio: 0.2,
});

const rlhf = new RLHFStrategy(rlhfConfig);

// Add preference data
rlhf.addPreferenceData([
  {
    prompt: 'Explain AI',
    preferred: 'AI is the simulation of human intelligence...',
    rejected: 'AI is just algorithms.',
  },
  // ... more preferences
]);

// Train
const result = await rlhf.train();
console.log('RLHF training complete:', result);
```

## Configuration Options

### Model Configuration

```typescript
const config = createModelConfig('openai', 'gpt-3.5-turbo', {
  temperature: 0.7,
  maxTokens: 2048,
});
```

### Fine-Tuning with LoRA

```typescript
const config = createFineTuningConfig(modelConfig, {
  epochs: 3,
  batchSize: 16,
  loraRank: 8,        // Low-rank adapter rank
  loraAlpha: 16,      // Scaling factor
  targetModules: ['q_proj', 'v_proj'],
  useQLoRA: true,     // Quantized LoRA for memory efficiency
});
```

### RAG Configuration

```typescript
const ragConfig = createRAGConfig('local', {
  embeddingModel: 'all-MiniLM-L6-v2',
  retrievalTopK: 5,
  similarityThreshold: 0.3,
});
```

## Running Tests

```bash
npm test
npm test:ui  # Interactive UI
```

## Building

```bash
npm run build
npm run type-check
npm run lint
```

## Metrics & Monitoring

Each strategy tracks metrics during training:

```typescript
const strategy = new FineTuningStrategy(config);
await strategy.train();

const metrics = strategy.getMetrics();
console.log(metrics);
// Output: Array of StrategyMetrics with timestamp, duration, and metrics
```

## Exporting Results

```typescript
const lab = new LabOrchestrator();
// ... run experiment ...

const json = lab.exportResults('Experiment Name');
console.log(json);
```

## Next Steps

- Explore the `/src/examples` directory for more detailed examples
- Check the API reference in README.md
- Review test files in `/src/__tests__` for usage patterns
- Experiment with different strategies and configurations

## Troubleshooting

### API Key Issues

Make sure your environment variables are set correctly:

```bash
echo $OPENAI_API_KEY
echo $CLAUDE_API_KEY
```

### Build Errors

Clear node_modules and reinstall:

```bash
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
npm run build
```

### Test Failures

Run tests with verbose output:

```bash
npm test -- --reporter=verbose
```

## Support

For issues or questions, please refer to the main repository documentation.

