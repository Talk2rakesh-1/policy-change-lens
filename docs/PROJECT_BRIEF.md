# ChangeLens project brief

- **Repository:** `policy-change-lens`
- **Description:** Local-first API for evidence-linked document change analysis and retrieval.
- **Problem:** Raw diffs are noisy while AI summaries often lack traceable evidence.
- **Users:** Governance, security, platform, and technical-policy reviewers.
- **Recruiter value:** Demonstrates retrieval, evaluation, responsible AI boundaries, API engineering, observability, Docker, and CI.
- **MVP:** Section parsing, lexical matching, change classification, source evidence, citation coverage, search endpoint, guardrail warnings.
- **Stretch:** Local embeddings, richer document adapters, move detection, golden-set evaluation, and human-approved local-LLM summaries.
- **Architecture:** FastAPI validation → parser/retriever → classifier → evidence/evaluation → typed response.
- **Resources:** NIST guidance plus MIT/BSD dependencies; no corpus, model, or paid API.
- **License:** MIT-compatible across declared dependencies.
- **Risks:** Lexical similarity misses paraphrases; section boundaries and thresholds can influence results.

## Seven-day implementation plan

1. Validate the evidence and document-change use case.
2. Define typed contracts, input limits, and section normalization.
3. Implement deterministic matching, retrieval, and change classification.
4. Add evidence linking, citation evaluation, guardrail warnings, and telemetry.
5. Build unit/API tests and a non-root container.
6. Run lint, coverage, security, license, and smoke checks; polish documentation.
7. Publish, verify CI, and prepare portfolio/interview material.
