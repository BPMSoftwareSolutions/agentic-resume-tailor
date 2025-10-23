/**
 * Core types and interfaces for LLM training strategies
 */

export type ModelProvider = 'openai' | 'anthropic' | 'local';

export interface ModelConfig {
  provider: ModelProvider;
  modelId: string;
  apiKey?: string;
  baseUrl?: string;
  temperature?: number;
  maxTokens?: number;
}

export interface TrainingData {
  id: string;
  text: string;
  metadata?: Record<string, unknown>;
}

export interface PromptResponsePair {
  prompt: string;
  response: string;
  metadata?: Record<string, unknown>;
}

export interface PreferenceExample {
  prompt: string;
  preferred: string;
  rejected: string;
  metadata?: Record<string, unknown>;
}

export interface TrainingConfig {
  model: ModelConfig;
  learningRate?: number;
  batchSize?: number;
  epochs?: number;
  validationSplit?: number;
  seed?: number;
}

export interface TrainingResult {
  success: boolean;
  modelId: string;
  trainingTime: number;
  metrics: {
    loss?: number;
    accuracy?: number;
    perplexity?: number;
    [key: string]: number | undefined;
  };
  checkpointPath?: string;
  error?: string;
}

export interface RAGConfig {
  vectorStoreType: 'pinecone' | 'weaviate' | 'milvus' | 'local';
  embeddingModel: string;
  retrievalTopK?: number;
  similarityThreshold?: number;
}

export interface RAGDocument {
  id: string;
  content: string;
  metadata?: Record<string, unknown>;
  embedding?: number[];
}

export interface RAGQuery {
  query: string;
  topK?: number;
  filters?: Record<string, unknown>;
}

export interface RAGResult {
  query: string;
  documents: RAGDocument[];
  scores: number[];
}

export interface RLHFConfig extends TrainingConfig {
  rewardModelPath?: string;
  ppoEpochs?: number;
  clipRatio?: number;
}

export interface RLHFTrainingData {
  prompt: string;
  responses: string[];
  rankings: number[];
}

export interface FineTuningConfig extends TrainingConfig {
  loraRank?: number;
  loraAlpha?: number;
  targetModules?: string[];
  useQLoRA?: boolean;
}

export interface StrategyMetrics {
  strategy: string;
  timestamp: Date;
  metrics: Record<string, number | string>;
  duration: number;
}

