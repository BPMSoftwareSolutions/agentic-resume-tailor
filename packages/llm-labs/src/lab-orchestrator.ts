/**
 * Lab Orchestrator: Manages multiple training strategies and experiments
 */

import { BaseStrategy } from './strategies/base-strategy.js';
import { TrainingResult } from './types.js';

export interface ExperimentConfig {
  name: string;
  description?: string;
  strategies: BaseStrategy[];
}

export interface ExperimentResult {
  experimentName: string;
  timestamp: Date;
  results: Map<string, TrainingResult>;
  totalDuration: number;
}

export class LabOrchestrator {
  private experiments: Map<string, ExperimentResult> = new Map();
  private currentExperiment?: ExperimentConfig;

  /**
   * Create a new experiment
   */
  createExperiment(config: ExperimentConfig): void {
    this.currentExperiment = config;
  }

  /**
   * Run the current experiment
   */
  async runExperiment(): Promise<ExperimentResult> {
    if (!this.currentExperiment) {
      throw new Error('No experiment configured');
    }

    const startTime = Date.now();
    const results = new Map<string, TrainingResult>();

    console.log(`\n🚀 Starting experiment: ${this.currentExperiment.name}`);
    if (this.currentExperiment.description) {
      console.log(`   ${this.currentExperiment.description}`);
    }

    for (const strategy of this.currentExperiment.strategies) {
      const strategyName = strategy.getStrategyName();
      console.log(`\n   ⏳ Running ${strategyName}...`);

      try {
        const result = await strategy.train();
        results.set(strategyName, result);

        if (result.success) {
          console.log(`   ✅ ${strategyName} completed successfully`);
          console.log(`      Loss: ${result.metrics.loss?.toFixed(4)}`);
        } else {
          console.log(`   ❌ ${strategyName} failed: ${result.error}`);
        }
      } catch (error) {
        console.log(
          `   ❌ ${strategyName} error: ${error instanceof Error ? error.message : 'Unknown error'}`
        );
      }
    }

    const totalDuration = Date.now() - startTime;
    const experimentResult: ExperimentResult = {
      experimentName: this.currentExperiment.name,
      timestamp: new Date(),
      results,
      totalDuration,
    };

    this.experiments.set(this.currentExperiment.name, experimentResult);

    console.log(`\n✨ Experiment completed in ${(totalDuration / 1000).toFixed(2)}s`);

    return experimentResult;
  }

  /**
   * Get experiment results
   */
  getExperimentResults(name: string): ExperimentResult | undefined {
    return this.experiments.get(name);
  }

  /**
   * Get all experiments
   */
  getAllExperiments(): ExperimentResult[] {
    return Array.from(this.experiments.values());
  }

  /**
   * Compare strategies from an experiment
   */
  compareStrategies(experimentName: string): void {
    const experiment = this.experiments.get(experimentName);
    if (!experiment) {
      console.log(`Experiment "${experimentName}" not found`);
      return;
    }

    console.log(`\n📊 Comparison for experiment: ${experimentName}`);
    console.log('─'.repeat(80));

    const rows: string[] = [];
    experiment.results.forEach((result, strategyName) => {
      const status = result.success ? '✅' : '❌';
      const loss = result.metrics.loss?.toFixed(4) || 'N/A';
      const accuracy = result.metrics.accuracy?.toFixed(4) || 'N/A';
      rows.push(
        `${status} ${strategyName.padEnd(25)} | Loss: ${loss.padEnd(8)} | Accuracy: ${accuracy}`
      );
    });

    rows.forEach((row) => console.log(row));
    console.log('─'.repeat(80));
  }

  /**
   * Export experiment results as JSON
   */
  exportResults(experimentName: string): string {
    const experiment = this.experiments.get(experimentName);
    if (!experiment) {
      throw new Error(`Experiment "${experimentName}" not found`);
    }

    const resultsObj = {
      experimentName: experiment.experimentName,
      timestamp: experiment.timestamp,
      totalDuration: experiment.totalDuration,
      results: Array.from(experiment.results.entries()).map(([name, result]) => ({
        strategy: name,
        ...result,
      })),
    };

    return JSON.stringify(resultsObj, null, 2);
  }
}

