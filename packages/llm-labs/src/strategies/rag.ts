/**
 * RAG strategy: Retrieval-Augmented Generation
 * 
 * Use case: Injecting external knowledge without retraining (perfect for legal, medical, financial)
 * Compute: Low (no model training, just retrieval)
 * Duration: Real-time
 */

import { BaseStrategy } from './base-strategy.js';
import {
  RAGConfig,
  RAGDocument,
  RAGQuery,
  RAGResult,
  TrainingResult,
  TrainingConfig,
} from '../types.js';

export class RAGStrategy extends BaseStrategy {
  private documents: RAGDocument[] = [];
  private ragConfig: RAGConfig;

  constructor(trainingConfig: TrainingConfig, ragConfig: RAGConfig) {
    super(trainingConfig);
    this.ragConfig = ragConfig;
  }

  /**
   * Add documents to the vector store
   */
  addDocuments(docs: RAGDocument[]): void {
    this.documents.push(...docs);
  }

  /**
   * Get all documents
   */
  getDocuments(): RAGDocument[] {
    return this.documents;
  }

  /**
   * Simple cosine similarity calculation
   */
  private cosineSimilarity(a: number[], b: number[]): number {
    const dotProduct = a.reduce((sum, val, i) => sum + val * b[i], 0);
    const magnitudeA = Math.sqrt(a.reduce((sum, val) => sum + val * val, 0));
    const magnitudeB = Math.sqrt(b.reduce((sum, val) => sum + val * val, 0));
    return dotProduct / (magnitudeA * magnitudeB);
  }

  /**
   * Generate simple embedding (mock)
   */
  private generateEmbedding(text: string): number[] {
    // Mock embedding: hash-based vector
    const hash = text.split('').reduce((h, c) => h + c.charCodeAt(0), 0);
    const embedding: number[] = [];
    for (let i = 0; i < 384; i++) {
      embedding.push(Math.sin((hash + i) * 0.1) * 0.5 + 0.5);
    }
    return embedding;
  }

  /**
   * Retrieve relevant documents
   */
  async retrieve(query: RAGQuery): Promise<RAGResult> {
    const queryEmbedding = this.generateEmbedding(query.query);
    const topK = query.topK || this.ragConfig.retrievalTopK || 5;
    const threshold = this.ragConfig.similarityThreshold || 0.3;

    const scored = this.documents.map((doc) => {
      const docEmbedding =
        doc.embedding || this.generateEmbedding(doc.content);
      const score = this.cosineSimilarity(queryEmbedding, docEmbedding);
      return { doc, score };
    });

    const results = scored
      .filter((item) => item.score >= threshold)
      .sort((a, b) => b.score - a.score)
      .slice(0, topK);

    return {
      query: query.query,
      documents: results.map((r) => r.doc),
      scores: results.map((r) => r.score),
    };
  }

  /**
   * RAG doesn't require training, but we implement train() for interface compatibility
   */
  async train(): Promise<TrainingResult> {
    const startTime = Date.now();

    try {
      if (this.documents.length === 0) {
        throw new Error('No documents provided for RAG');
      }

      // Index documents
      const indexedDocs = this.documents.map((doc) => ({
        ...doc,
        embedding: doc.embedding || this.generateEmbedding(doc.content),
      }));

      this.recordMetrics({
        documentsIndexed: indexedDocs.length,
        vectorStoreType: this.ragConfig.vectorStoreType,
        embeddingModel: this.ragConfig.embeddingModel,
        retrievalTopK: this.ragConfig.retrievalTopK || 5,
      });

      const duration = Date.now() - startTime;

      return {
        success: true,
        modelId: this.config.model.modelId,
        trainingTime: duration,
        metrics: {
          documentsIndexed: indexedDocs.length,
        },
        checkpointPath: `/vector-stores/${this.ragConfig.vectorStoreType}`,
      };
    } catch (error) {
      const duration = Date.now() - startTime;
      return {
        success: false,
        modelId: this.config.model.modelId,
        trainingTime: duration,
        metrics: {},
        error: error instanceof Error ? error.message : 'Unknown error',
      };
    }
  }

  /**
   * Get strategy description
   */
  getDescription(): string {
    return `RAG: Retrieval-Augmented Generation using ${this.ragConfig.vectorStoreType} vector store`;
  }
}

