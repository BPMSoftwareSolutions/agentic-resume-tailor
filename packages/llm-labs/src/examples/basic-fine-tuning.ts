/**
 * Example: Basic Fine-Tuning
 * 
 * This example demonstrates how to fine-tune a model on custom instruction data.
 */

import {
  createModelConfig,
  createFineTuningConfig,
  FineTuningStrategy,
} from '../index.js';

async function main() {
  console.log('🚀 Fine-Tuning Example\n');

  // Create model configuration
  const modelConfig = createModelConfig('openai', 'gpt-3.5-turbo', {
    temperature: 0.7,
    maxTokens: 1024,
  });

  // Create fine-tuning configuration with LoRA
  const trainingConfig = createFineTuningConfig(modelConfig, {
    epochs: 3,
    batchSize: 16,
    loraRank: 8,
    loraAlpha: 16,
  });

  // Create strategy
  const strategy = new FineTuningStrategy(trainingConfig);

  // Add training data
  const trainingPairs = [
    {
      prompt: 'What is machine learning?',
      response:
        'Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed.',
    },
    {
      prompt: 'Explain neural networks',
      response:
        'Neural networks are computing systems inspired by biological neural networks. They consist of interconnected nodes that process information.',
    },
    {
      prompt: 'What is deep learning?',
      response:
        'Deep learning is a subset of machine learning that uses neural networks with multiple layers to learn hierarchical representations of data.',
    },
  ];

  strategy.addTrainingPairs(trainingPairs);

  // Add validation data
  const validationPairs = [
    {
      prompt: 'Define artificial intelligence',
      response:
        'Artificial intelligence refers to computer systems designed to perform tasks that typically require human intelligence.',
    },
  ];

  strategy.addValidationPairs(validationPairs);

  console.log(`📊 Training Configuration:`);
  console.log(`   Model: ${modelConfig.modelId}`);
  console.log(`   Epochs: ${trainingConfig.epochs}`);
  console.log(`   Batch Size: ${trainingConfig.batchSize}`);
  console.log(`   LoRA Rank: ${trainingConfig.loraRank}`);
  console.log(`   Training Pairs: ${trainingPairs.length}`);
  console.log(`   Validation Pairs: ${validationPairs.length}\n`);

  // Train
  console.log('⏳ Starting training...\n');
  const result = await strategy.train();

  // Display results
  console.log('✅ Training Complete!\n');
  console.log(`📈 Results:`);
  console.log(`   Success: ${result.success}`);
  console.log(`   Training Time: ${(result.trainingTime / 1000).toFixed(2)}s`);
  console.log(`   Loss: ${result.metrics.loss?.toFixed(4)}`);
  console.log(`   Accuracy: ${result.metrics.accuracy?.toFixed(4)}`);
  console.log(`   Checkpoint: ${result.checkpointPath}\n`);

  // Display metrics
  const metrics = strategy.getMetrics();
  console.log('📊 Detailed Metrics:');
  metrics.forEach((m) => {
    console.log(`   ${m.strategy}:`);
    Object.entries(m.metrics).forEach(([key, value]) => {
      console.log(`      ${key}: ${value}`);
    });
  });
}

main().catch(console.error);

