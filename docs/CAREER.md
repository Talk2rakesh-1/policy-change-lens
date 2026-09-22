# Career material

## LinkedIn post

I built ChangeLens, a local-first FastAPI service for comparing policy and technical-document versions. Instead of returning an opaque summary, it classifies section-level changes, attaches source evidence to every finding, and reports citation coverage. It also includes deterministic retrieval, input guardrails, request telemetry, tests, Docker, and CI—with no model download or paid API required. I learned that an inspectable baseline and measurable evidence coverage are valuable before adding generative behavior. Repository: https://github.com/Talk2rakesh-1/policy-change-lens

#GenerativeAI #ResponsibleAI #FastAPI #Python #RAG

## Interview preparation

1. **Why start with lexical retrieval instead of embeddings?** It provides a fast, reproducible, offline baseline with no model license or download. The protocol boundary and evaluation output make a later local-embedding adapter measurable.
2. **How do you defend against document prompt injection?** Documents never enter an instruction channel or execute code. Instruction-like phrases are flagged as untrusted data, input is validated, and the deterministic engine has no tools or secrets to expose.
3. **How do you evaluate trustworthiness?** Every finding must contain source evidence, and the API calculates citation coverage. Tests assert exact change classes, retrieval relevance, validation behavior, warnings, and endpoint contracts.
