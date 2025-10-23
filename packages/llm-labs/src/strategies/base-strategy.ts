/**
 * Base strategy class for all LLM training approaches
 */

import { TrainingConfig, TrainingResult, StrategyMetrics } from '../types.js';

export abstract class BaseStrategy {
  protected config: TrainingConfig;
  protected metrics: StrategyMetrics[] = [];
  protected strategyMetrics: StrategyMetrics[] = [];

  constructor(config: TrainingConfig) {
    this.config = config;
  }

  /**
   * Execute the training strategy
   */
  abstract train(): Promise<TrainingResult>;

  /**
   * Validate the training configuration
   */
  protected validateConfig(): void {
    if (!this.config.model) {
      throw new Error('Model configuration is required');
    }
    if (!this.config.model.modelId) {
      throw new Error('Model ID is required');
    }
  }

  /**
   * Record metrics for this strategy
   */
  protected recordMetrics(metrics: Record<string, number | string>): void {
    this.metrics.push({
      strategy: this.constructor.name,
      timestamp: new Date(),
      metrics,
      duration: 0,
    });
  }

  /**
   * Get all recorded metrics
   */
  getMetrics(): StrategyMetrics[] {
    return this.metrics;
  }

  /**
   * Clear recorded metrics
   */
  clearMetrics(): void {
    this.metrics = [];
  }

  /**
   * Get the strategy name
   */
  getStrategyName(): string {
    return this.constructor.name;
  }
}

