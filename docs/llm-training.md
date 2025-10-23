# LLM Training
For **agentic resume tailoring** the most efficient—and highest-quality—setup is a **RAG + LoRA fine-tune** with light preference optimization. Here’s the playbook.

The LLM training lab is located here:
".\packages\llm-labs\"

# 1) Target outcome

Given a job post, produce a **tailored resume JSON** (and PDF) that:

* Mirrors the posting’s **must-haves** and **language**
* Selects and rewrites bullets from your **experience corpus** (e.g., `experiences.json`)
* Preserves truthfulness + verifiable evidence
* Outputs **ATS-friendly** structure (sections, skills, keywords)

# 2) System architecture (agentic)

1. **Ingestion/RAG**

   * Parse job post → extract role, stack, must-haves, nice-to-haves.
   * Embed & index your **experience snippets** (bullets, tags, metrics) + portfolio links.
   * Retrieve top-K experiences per requirement.

2. **Planner agent**

   * Builds a tailoring plan: which projects map to which job requirements; gap notes.

3. **Writer agent**

   * Generates tailored **Summary**, **Core Skills**, and **Experience bullets** using the plan + retrieved evidence.
   * Emits strict **JSON schema** your pipeline expects.

4. **Critique/Verifier agent**

   * Runs checks: truthfulness, metric presence, keyword coverage, duplication, tone, length, ATS formatting.
   * Can re-prompt the Writer with targeted edits (self-critique loop).

5. **Exporter**

   * Converts JSON → PDF/Docx and persists the tailored JSON for reuse.

# 3) Training strategy (efficient)

**A. Start with zero training (prompt + RAG)**

* Solid system prompts + structured JSON schemas + retrieval gets you far.
* Add a few **seed exemplars** of “job post → tailored JSON” to stabilize outputs.

**B. Add LoRA/QLoRA fine-tuning (cheap & high ROI)**

* Fine-tune on **instruction pairs**:
  `(job_post, user_corpus) -> (tailored_resume_json + rationale)`.
* Focus on **style & structure** (active verbs, quantified impact, tense, ATS do’s/don’ts), not on “knowledge.”

**C. Light preference optimization (DPO or RLAIF)**

* Generate 2–3 variants per job; have a small rubric rank them (coverage, truthfulness, clarity, metrics).
* Use **DPO** (simpler than RLHF) to nudge toward preferred variants.

# 4) Data you need (small but high quality)

* 50–200 curated examples:

  * Input: Job description + retrieved snippets (K=8–12) + user metadata (industry, seniority).
  * Output: **Tailored resume JSON** (summary, skills, selected bullets rewritten, tags) + a short **self-rationale** (“why these bullets map to JD”).
* Add **counterexamples** (bad outputs) with reasons to improve preference signals.

# 5) Guardrails (critical)

* **Truth filter**: Every bullet must map to a retrieved snippet or numeric evidence.
* **No hallucinations**: If a requirement is a gap, the plan flags it (optionally suggests adjacent proof).
* **JSON schema validation**: Fail closed → repair loop.
* **Length & ATS**: Max tokens per section; enforce standard section order and keyword coverage.

# 6) Metrics

* **Coverage@Req**: % JD must-haves addressed by at least one bullet.
* **TruthScore**: % bullets with verifiable source snippet.
* **ImpactScore**: % bullets with numbers/metrics.
* **Readability**: grade level / sentence length.
* **ATS Keyword HitRate**: % of extracted keywords present.
* **Human Preference** (DPO pairs): variant A wins vs B.

# 7) Using your `@bpm/llm-labs` (example)

```ts
import {
  createModelConfig, createTrainingConfig,
  createFineTuningConfig, FineTuningStrategy,
  RAGStrategy, LabOrchestrator
} from '@bpm/llm-labs';

// Base model
const model = createModelConfig('openai', 'gpt-4o-mini', { apiKey: process.env.OPENAI_API_KEY });

// RAG for experience selection
const rag = new RAGStrategy(
  createTrainingConfig(model, { temperature: 0.2 }),
  { embeddingModel: 'all-MiniLM-L6-v2', retrievalTopK: 10, similarityThreshold: 0.35 }
);
// (index your experiences.json here)
await rag.indexDocuments(loadExperiencesAsChunks());

// LoRA/QLoRA FT to lock style/structure
const ft = new FineTuningStrategy(
  createFineTuningConfig(model, {
    loraRank: 8, loraAlpha: 16, useQLoRA: true, targetModules: ['q_proj','v_proj'],
    epochs: 3, batchSize: 32, lr: 2e-4, evalEverySteps: 200
  })
);
// Add training pairs: {prompt: job+retrieved, response: tailored_resume_json}
ft.addTrainingPairs(await loadCuratedPairs());

// Orchestrate experiment
const lab = new LabOrchestrator();
lab.createExperiment({
  name: 'Agentic-Resume-Tailor-v1',
  strategies: [rag, ft]
});
const results = await lab.runExperiment();
lab.compareStrategies('Agentic-Resume-Tailor-v1');
```

# 8) Prompting patterns (core)

**System**:
“You are a resume-tailoring agent. Produce strictly valid JSON matching the schema. Use only retrieved evidence. If evidence is missing, flag gaps in `notes`.”

**Schema (excerpt)**
`{ summary: string, skills: string[], experiences: [{ employer, role, bullets: string[] }], keywords: string[], notes: string[] }`

**Critique checklist**

* Each bullet: `{verb}{what}{how}{impact% or $}{tech}`
* No first-person, no fluff, no unverifiable claims.
* Replace passive verbs; ensure tense consistency; dedupe skills.

# 9) Great use cases (concrete)

* **Westlaw AI role** (your current target):

  * JD → extract: Python, FastAPI, AWS, CI/CD, RAG, observability, security.
  * Retrieve from your corpus (Cox, Edward Jones, BPM).
  * Generate bullets that **prove**: LLM orchestration, Terraform-driven CI/CD, AES/KeeperSecurity practices, RAG pipelines, metrics (latency ↓, release cadence ↑, defect rate ↓).
  * Output a crisp **summary** emphasizing legal-adjacent strengths: accuracy, explainability, data lineage, secure handling.

* **High-volume auto-apply workflow**:

  * Batch runs where the agent tailors JSON per posting, enforces guardrails, and exports PDFs.
  * Keep an **application ledger** (company, role, date, version hash) for A/B of summaries and skill stacks.

# 10) Minimal training recipe to ship this week

1. Implement RAG over `experiences.json` and your master resume bullets.
2. Write 25 gold-standard pairs (JD → tailored JSON) for LoRA; train for 2–3 epochs.
3. Add a tiny DPO set (10–20 pairs) using your critique rubric to prefer higher Coverage@Req + TruthScore.
4. Wire the **repair loop** (JSON validation + critique prompts).
5. Track the 5 metrics above and keep the top-performing template.

