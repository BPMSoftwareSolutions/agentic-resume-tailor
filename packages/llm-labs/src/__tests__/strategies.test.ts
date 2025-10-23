/**
 * Tests for training strategies
 */

import { describe, it, expect, beforeEach } from 'vitest';
import {
  createModelConfig,
  createTrainingConfig,
  createFineTuningConfig,
  createRLHFConfig,
  createRAGConfig,
  PretrainingStrategy,
  FineTuningStrategy,
  RLHFStrategy,
  RAGStrategy,
} from '../index.js';

describe('Training Strategies', () => {
  let modelConfig = createModelConfig('openai', 'gpt-3.5-turbo');

  beforeEach(() => {
    modelConfig = createModelConfig('openai', 'gpt-3.5-turbo');
  });

  describe('PretrainingStrategy', () => {
    it('should initialize with config', () => {
      const config = createTrainingConfig(modelConfig);
      const strategy = new PretrainingStrategy(config);
      expect(strategy).toBeDefined();
      expect(strategy.getStrategyName()).toBe('PretrainingStrategy');
    });

    it('should add training data', () => {
      const config = createTrainingConfig(modelConfig);
      const strategy = new PretrainingStrategy(config);

      const data = [
        { id: '1', text: 'Sample text 1' },
        { id: '2', text: 'Sample text 2' },
      ];

      strategy.addTrainingData(data);
      expect(strategy.getTrainingData()).toHaveLength(2);
    });

    it('should train successfully with data', async () => {
      const config = createTrainingConfig(modelConfig);
      const strategy = new PretrainingStrategy(config);

      strategy.addTrainingData([{ id: '1', text: 'Sample training text' }]);

      const result = await strategy.train();
      expect(result.success).toBe(true);
      expect(result.modelId).toBe('gpt-3.5-turbo');
      expect(result.metrics.loss).toBeDefined();
      expect(result.metrics.perplexity).toBeDefined();
    });

    it('should fail without training data', async () => {
      const config = createTrainingConfig(modelConfig);
      const strategy = new PretrainingStrategy(config);

      const result = await strategy.train();
      expect(result.success).toBe(false);
      expect(result.error).toContain('No training data');
    });
  });

  describe('FineTuningStrategy', () => {
    it('should initialize with config', () => {
      const config = createFineTuningConfig(modelConfig);
      const strategy = new FineTuningStrategy(config);
      expect(strategy).toBeDefined();
      expect(strategy.getStrategyName()).toBe('FineTuningStrategy');
    });

    it('should add training pairs', () => {
      const config = createFineTuningConfig(modelConfig);
      const strategy = new FineTuningStrategy(config);

      const pairs = [
        { prompt: 'What is AI?', response: 'AI is artificial intelligence' },
      ];

      strategy.addTrainingPairs(pairs);
      expect(strategy.getTrainingPairs()).toHaveLength(1);
    });

    it('should train successfully with pairs', async () => {
      const config = createFineTuningConfig(modelConfig);
      const strategy = new FineTuningStrategy(config);

      strategy.addTrainingPairs([
        { prompt: 'What is AI?', response: 'AI is artificial intelligence' },
      ]);

      const result = await strategy.train();
      expect(result.success).toBe(true);
      expect(result.metrics.loss).toBeDefined();
      expect(result.metrics.accuracy).toBeDefined();
    });

    it('should support LoRA configuration', () => {
      const config = createFineTuningConfig(modelConfig, {
        loraRank: 16,
        loraAlpha: 32,
      });

      expect(config.loraRank).toBe(16);
      expect(config.loraAlpha).toBe(32);
    });
  });

  describe('RLHFStrategy', () => {
    it('should initialize with config', () => {
      const config = createRLHFConfig(modelConfig);
      const strategy = new RLHFStrategy(config);
      expect(strategy).toBeDefined();
      expect(strategy.getStrategyName()).toBe('RLHFStrategy');
    });

    it('should add preference data', () => {
      const config = createRLHFConfig(modelConfig);
      const strategy = new RLHFStrategy(config);

      const preferences = [
        {
          prompt: 'What is AI?',
          preferred: 'AI is artificial intelligence',
          rejected: 'AI is just algorithms',
        },
      ];

      strategy.addPreferenceData(preferences);
      expect(strategy.getPreferenceData()).toHaveLength(1);
    });

    it('should train successfully with preferences', async () => {
      const config = createRLHFConfig(modelConfig);
      const strategy = new RLHFStrategy(config);

      strategy.addPreferenceData([
        {
          prompt: 'What is AI?',
          preferred: 'AI is artificial intelligence',
          rejected: 'AI is just algorithms',
        },
      ]);

      const result = await strategy.train();
      expect(result.success).toBe(true);
      expect(result.metrics.rewardModelAccuracy).toBeDefined();
      expect(result.metrics.averageReward).toBeDefined();
    });
  });

  describe('RAGStrategy', () => {
    it('should initialize with config', () => {
      const trainingConfig = createTrainingConfig(modelConfig);
      const ragConfig = createRAGConfig('local');
      const strategy = new RAGStrategy(trainingConfig, ragConfig);
      expect(strategy).toBeDefined();
      expect(strategy.getStrategyName()).toBe('RAGStrategy');
    });

    it('should add documents', () => {
      const trainingConfig = createTrainingConfig(modelConfig);
      const ragConfig = createRAGConfig('local');
      const strategy = new RAGStrategy(trainingConfig, ragConfig);

      const docs = [
        { id: '1', content: 'Document 1' },
        { id: '2', content: 'Document 2' },
      ];

      strategy.addDocuments(docs);
      expect(strategy.getDocuments()).toHaveLength(2);
    });

    it('should retrieve documents', async () => {
      const trainingConfig = createTrainingConfig(modelConfig);
      const ragConfig = createRAGConfig('local');
      const strategy = new RAGStrategy(trainingConfig, ragConfig);

      strategy.addDocuments([
        { id: '1', content: 'Machine learning is AI' },
        { id: '2', content: 'Deep learning uses neural networks' },
      ]);

      await strategy.train();

      const results = await strategy.retrieve({
        query: 'What is machine learning?',
        topK: 1,
      });

      expect(results.documents.length).toBeGreaterThan(0);
      expect(results.scores.length).toBeGreaterThan(0);
    });
  });

  describe('Metrics Recording', () => {
    it('should record metrics', async () => {
      const config = createTrainingConfig(modelConfig);
      const strategy = new PretrainingStrategy(config);

      strategy.addTrainingData([{ id: '1', text: 'Sample text' }]);
      await strategy.train();

      const metrics = strategy.getMetrics();
      expect(metrics.length).toBeGreaterThan(0);
      expect(metrics[0].strategy).toBe('PretrainingStrategy');
      expect(metrics[0].metrics).toBeDefined();
    });

    it('should clear metrics', async () => {
      const config = createTrainingConfig(modelConfig);
      const strategy = new PretrainingStrategy(config);

      strategy.addTrainingData([{ id: '1', text: 'Sample text' }]);
      await strategy.train();

      let metrics = strategy.getMetrics();
      expect(metrics.length).toBeGreaterThan(0);

      strategy.clearMetrics();
      metrics = strategy.getMetrics();
      expect(metrics).toHaveLength(0);
    });
  });
});

