/**
 * Tests for LabOrchestrator
 */

import { describe, it, expect, beforeEach } from 'vitest';
import {
  createModelConfig,
  createTrainingConfig,
  createFineTuningConfig,
  PretrainingStrategy,
  FineTuningStrategy,
  LabOrchestrator,
} from '../index.js';

describe('LabOrchestrator', () => {
  let orchestrator: LabOrchestrator;
  let modelConfig = createModelConfig('openai', 'gpt-3.5-turbo');

  beforeEach(() => {
    orchestrator = new LabOrchestrator();
    modelConfig = createModelConfig('openai', 'gpt-3.5-turbo');
  });

  it('should initialize', () => {
    expect(orchestrator).toBeDefined();
  });

  it('should create an experiment', () => {
    const config = createTrainingConfig(modelConfig);
    const strategy = new PretrainingStrategy(config);

    orchestrator.createExperiment({
      name: 'Test Experiment',
      description: 'A test experiment',
      strategies: [strategy],
    });

    expect(orchestrator).toBeDefined();
  });

  it('should run an experiment', async () => {
    const config = createTrainingConfig(modelConfig);
    const strategy = new PretrainingStrategy(config);

    strategy.addTrainingData([{ id: '1', text: 'Sample text' }]);

    orchestrator.createExperiment({
      name: 'Test Experiment',
      strategies: [strategy],
    });

    const results = await orchestrator.runExperiment();

    expect(results).toBeDefined();
    expect(results.experimentName).toBe('Test Experiment');
    expect(results.results.size).toBeGreaterThan(0);
  });

  it('should retrieve experiment results', async () => {
    const config = createTrainingConfig(modelConfig);
    const strategy = new PretrainingStrategy(config);

    strategy.addTrainingData([{ id: '1', text: 'Sample text' }]);

    orchestrator.createExperiment({
      name: 'Test Experiment',
      strategies: [strategy],
    });

    await orchestrator.runExperiment();

    const results = orchestrator.getExperimentResults('Test Experiment');
    expect(results).toBeDefined();
    expect(results?.experimentName).toBe('Test Experiment');
  });

  it('should get all experiments', async () => {
    const config1 = createTrainingConfig(modelConfig);
    const strategy1 = new PretrainingStrategy(config1);
    strategy1.addTrainingData([{ id: '1', text: 'Sample text' }]);

    orchestrator.createExperiment({
      name: 'Experiment 1',
      strategies: [strategy1],
    });

    await orchestrator.runExperiment();

    const config2 = createFineTuningConfig(modelConfig);
    const strategy2 = new FineTuningStrategy(config2);
    strategy2.addTrainingPairs([
      { prompt: 'What is AI?', response: 'AI is artificial intelligence' },
    ]);

    orchestrator.createExperiment({
      name: 'Experiment 2',
      strategies: [strategy2],
    });

    await orchestrator.runExperiment();

    const allExperiments = orchestrator.getAllExperiments();
    expect(allExperiments.length).toBe(2);
  });

  it('should export results as JSON', async () => {
    const config = createTrainingConfig(modelConfig);
    const strategy = new PretrainingStrategy(config);

    strategy.addTrainingData([{ id: '1', text: 'Sample text' }]);

    orchestrator.createExperiment({
      name: 'Test Experiment',
      strategies: [strategy],
    });

    await orchestrator.runExperiment();

    const json = orchestrator.exportResults('Test Experiment');
    const parsed = JSON.parse(json);

    expect(parsed.experimentName).toBe('Test Experiment');
    expect(parsed.results).toBeDefined();
    expect(Array.isArray(parsed.results)).toBe(true);
  });

  it('should throw error when running without experiment', async () => {
    try {
      await orchestrator.runExperiment();
      expect.fail('Should have thrown an error');
    } catch (error) {
      expect(error).toBeDefined();
    }
  });

  it('should throw error when exporting non-existent experiment', () => {
    try {
      orchestrator.exportResults('Non-existent');
      expect.fail('Should have thrown an error');
    } catch (error) {
      expect(error).toBeDefined();
    }
  });
});

