/**
 * @bpm/llm-labs - LLM Training and Fine-tuning Lab
 * 
 * A comprehensive framework for experimenting with different LLM training strategies:
 * - Pretraining: Training from scratch on raw text corpora
 * - Fine-tuning: Supervised instruction tuning with optional LoRA
 * - RLHF: Reinforcement Learning from Human Feedback
 * - RAG: Retrieval-Augmented Generation for knowledge injection
 */

// Export types
export * from './types.js';

// Export strategies
export { BaseStrategy } from './strategies/base-strategy.js';
export { PretrainingStrategy } from './strategies/pretraining.js';
export { FineTuningStrategy } from './strategies/fine-tuning.js';
export { RLHFStrategy } from './strategies/rlhf.js';
export { RAGStrategy } from './strategies/rag.js';

// Export orchestrator
export { LabOrchestrator, type ExperimentConfig, type ExperimentResult } from './lab-orchestrator.js';

// Export utilities
export {
  createModelConfig,
  createTrainingConfig,
  createFineTuningConfig,
  createRLHFConfig,
  createRAGConfig,
} from './utils/config-builder.js';

