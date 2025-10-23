/**
 * Example: Compare Multiple Training Strategies
 * 
 * This example demonstrates how to run multiple strategies and compare results.
 */

import {
  createModelConfig,
  createTrainingConfig,
  createFineTuningConfig,
  createRLHFConfig,
  PretrainingStrategy,
  FineTuningStrategy,
  RLHFStrategy,
  LabOrchestrator,
} from '../index.js';

async function main() {
  console.log('🧪 Strategy Comparison Example\n');

  // Create model configuration
  const modelConfig = createModelConfig('openai', 'gpt-3.5-turbo');

  // Create strategies
  const pretrainingConfig = createTrainingConfig(modelConfig, {
    epochs: 1,
    batchSize: 64,
  });

  const finetuningConfig = createFineTuningConfig(modelConfig, {
    epochs: 3,
    batchSize: 16,
    loraRank: 8,
  });

  const rlhfConfig = createRLHFConfig(modelConfig, {
    ppoEpochs: 4,
    clipRatio: 0.2,
  });

  // Create strategies
  const pretrainingStrategy = new PretrainingStrategy(pretrainingConfig);
  const finetuningStrategy = new FineTuningStrategy(finetuningConfig);
  const rlhfStrategy = new RLHFStrategy(rlhfConfig);

  // Add data to pretraining
  pretrainingStrategy.addTrainingData([
    {
      id: '1',
      text: 'Machine learning is a subset of artificial intelligence that enables systems to learn from data.',
    },
    {
      id: '2',
      text: 'Deep learning uses neural networks with multiple layers to learn hierarchical representations.',
    },
  ]);

  // Add data to fine-tuning
  finetuningStrategy.addTrainingPairs([
    {
      prompt: 'What is ML?',
      response: 'Machine learning enables systems to learn from data.',
    },
    {
      prompt: 'What is DL?',
      response: 'Deep learning uses neural networks with multiple layers.',
    },
  ]);

  // Add data to RLHF
  rlhfStrategy.addPreferenceData([
    {
      prompt: 'Explain AI',
      preferred: 'AI is the simulation of human intelligence by machines.',
      rejected: 'AI is just algorithms.',
    },
    {
      prompt: 'What is ML?',
      preferred: 'ML enables systems to learn from data without explicit programming.',
      rejected: 'ML is machine learning.',
    },
  ]);

  // Create orchestrator
  const lab = new LabOrchestrator();

  // Create experiment
  lab.createExperiment({
    name: 'LLM Training Strategies Comparison',
    description: 'Comparing pretraining, fine-tuning, and RLHF approaches',
    strategies: [pretrainingStrategy, finetuningStrategy, rlhfStrategy],
  });

  // Run experiment
  await lab.runExperiment();

  // Compare strategies
  lab.compareStrategies('LLM Training Strategies Comparison');

  // Export results
  const exportedResults = lab.exportResults('LLM Training Strategies Comparison');
  console.log('\n📄 Exported Results (JSON):');
  console.log(exportedResults);
}

main().catch(console.error);

