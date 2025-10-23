/**
 * Example: Retrieval-Augmented Generation (RAG)
 * 
 * This example demonstrates how to use RAG for knowledge injection.
 */

import {
  createModelConfig,
  createTrainingConfig,
  createRAGConfig,
  RAGStrategy,
} from '../index.js';

async function main() {
  console.log('🔍 RAG Example\n');

  // Create model configuration
  const modelConfig = createModelConfig('openai', 'gpt-3.5-turbo');

  // Create training configuration
  const trainingConfig = createTrainingConfig(modelConfig);

  // Create RAG configuration
  const ragConfig = createRAGConfig('local', {
    embeddingModel: 'all-MiniLM-L6-v2',
    retrievalTopK: 3,
    similarityThreshold: 0.3,
  });

  // Create RAG strategy
  const ragStrategy = new RAGStrategy(trainingConfig, ragConfig);

  // Add documents to the vector store
  const documents = [
    {
      id: 'doc1',
      content:
        'Machine learning is a subset of artificial intelligence that enables systems to learn from data.',
      metadata: { source: 'AI Basics', category: 'ML' },
    },
    {
      id: 'doc2',
      content:
        'Deep learning uses neural networks with multiple layers to learn hierarchical representations of data.',
      metadata: { source: 'AI Basics', category: 'DL' },
    },
    {
      id: 'doc3',
      content:
        'Natural language processing enables computers to understand and generate human language.',
      metadata: { source: 'AI Basics', category: 'NLP' },
    },
    {
      id: 'doc4',
      content:
        'Reinforcement learning trains agents to make decisions by rewarding desired behaviors.',
      metadata: { source: 'AI Basics', category: 'RL' },
    },
  ];

  ragStrategy.addDocuments(documents);

  console.log(`📚 RAG Configuration:`);
  console.log(`   Vector Store: ${ragConfig.vectorStoreType}`);
  console.log(`   Embedding Model: ${ragConfig.embeddingModel}`);
  console.log(`   Retrieval Top-K: ${ragConfig.retrievalTopK}`);
  console.log(`   Documents: ${documents.length}\n`);

  // Initialize RAG (index documents)
  console.log('⏳ Indexing documents...\n');
  const indexResult = await ragStrategy.train();

  console.log('✅ Indexing Complete!\n');
  console.log(`📈 Results:`);
  console.log(`   Success: ${indexResult.success}`);
  console.log(`   Documents Indexed: ${indexResult.metrics.documentsIndexed}`);
  console.log(`   Vector Store: ${indexResult.checkpointPath}\n`);

  // Perform retrieval queries
  console.log('🔎 Performing Retrieval Queries:\n');

  const queries = [
    'What is machine learning?',
    'How do neural networks work?',
    'Tell me about natural language processing',
  ];

  for (const query of queries) {
    console.log(`Query: "${query}"`);
    const results = await ragStrategy.retrieve({ query, topK: 2 });

    console.log(`Retrieved ${results.documents.length} documents:`);
    results.documents.forEach((doc, idx) => {
      const score = results.scores[idx];
      console.log(`  ${idx + 1}. [${score.toFixed(3)}] ${doc.content.substring(0, 60)}...`);
    });
    console.log();
  }

  // Display metrics
  const metrics = ragStrategy.getMetrics();
  console.log('📊 Detailed Metrics:');
  metrics.forEach((m) => {
    console.log(`   ${m.strategy}:`);
    Object.entries(m.metrics).forEach(([key, value]) => {
      console.log(`      ${key}: ${value}`);
    });
  });
}

main().catch(console.error);

