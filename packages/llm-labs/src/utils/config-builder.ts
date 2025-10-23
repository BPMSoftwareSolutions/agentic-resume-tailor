/**
 * Configuration builder utilities
 */

import { ModelConfig, TrainingConfig, FineTuningConfig, RLHFConfig, RAGConfig } from '../types.js';

/**
 * Create a model configuration from environment variables or parameters
 */
export function createModelConfig(
  provider: 'openai' | 'anthropic' | 'local',
  modelId: string,
  options?: {
    apiKey?: string;
    baseUrl?: string;
    temperature?: number;
    maxTokens?: number;
  }
): ModelConfig {
  let apiKey = options?.apiKey;

  // Try to get API key from environment if not provided
  if (!apiKey) {
    if (provider === 'openai') {
      apiKey = process.env.OPENAI_API_KEY;
    } else if (provider === 'anthropic') {
      apiKey = process.env.CLAUDE_API_KEY;
    }
  }

  if (!apiKey && provider !== 'local') {
    console.warn(
      `⚠️  No API key found for ${provider}. Set ${provider === 'openai' ? 'OPENAI_API_KEY' : 'CLAUDE_API_KEY'} environment variable.`
    );
  }

  return {
    provider,
    modelId,
    apiKey,
    baseUrl: options?.baseUrl,
    temperature: options?.temperature ?? 0.7,
    maxTokens: options?.maxTokens ?? 2048,
  };
}

/**
 * Create a basic training configuration
 */
export function createTrainingConfig(
  model: ModelConfig,
  options?: {
    learningRate?: number;
    batchSize?: number;
    epochs?: number;
    validationSplit?: number;
    seed?: number;
  }
): TrainingConfig {
  return {
    model,
    learningRate: options?.learningRate ?? 1e-4,
    batchSize: options?.batchSize ?? 32,
    epochs: options?.epochs ?? 3,
    validationSplit: options?.validationSplit ?? 0.1,
    seed: options?.seed ?? 42,
  };
}

/**
 * Create a fine-tuning configuration with LoRA support
 */
export function createFineTuningConfig(
  model: ModelConfig,
  options?: {
    learningRate?: number;
    batchSize?: number;
    epochs?: number;
    validationSplit?: number;
    seed?: number;
    loraRank?: number;
    loraAlpha?: number;
    targetModules?: string[];
    useQLoRA?: boolean;
  }
): FineTuningConfig {
  return {
    model,
    learningRate: options?.learningRate ?? 5e-5,
    batchSize: options?.batchSize ?? 16,
    epochs: options?.epochs ?? 3,
    validationSplit: options?.validationSplit ?? 0.1,
    seed: options?.seed ?? 42,
    loraRank: options?.loraRank ?? 8,
    loraAlpha: options?.loraAlpha ?? 16,
    targetModules: options?.targetModules ?? ['q_proj', 'v_proj'],
    useQLoRA: options?.useQLoRA ?? false,
  };
}

/**
 * Create an RLHF configuration
 */
export function createRLHFConfig(
  model: ModelConfig,
  options?: {
    learningRate?: number;
    batchSize?: number;
    epochs?: number;
    validationSplit?: number;
    seed?: number;
    rewardModelPath?: string;
    ppoEpochs?: number;
    clipRatio?: number;
  }
): RLHFConfig {
  return {
    model,
    learningRate: options?.learningRate ?? 1e-5,
    batchSize: options?.batchSize ?? 8,
    epochs: options?.epochs ?? 1,
    validationSplit: options?.validationSplit ?? 0.1,
    seed: options?.seed ?? 42,
    rewardModelPath: options?.rewardModelPath,
    ppoEpochs: options?.ppoEpochs ?? 4,
    clipRatio: options?.clipRatio ?? 0.2,
  };
}

/**
 * Create a RAG configuration
 */
export function createRAGConfig(
  vectorStoreType: 'pinecone' | 'weaviate' | 'milvus' | 'local' = 'local',
  options?: {
    embeddingModel?: string;
    retrievalTopK?: number;
    similarityThreshold?: number;
  }
): RAGConfig {
  return {
    vectorStoreType,
    embeddingModel: options?.embeddingModel ?? 'all-MiniLM-L6-v2',
    retrievalTopK: options?.retrievalTopK ?? 5,
    similarityThreshold: options?.similarityThreshold ?? 0.3,
  };
}

