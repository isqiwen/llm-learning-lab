# Roadmap

This roadmap is designed for roughly **10–15 focused hours/week**. It is outcome-driven: each phase ends with an artifact that can be inspected, rerun, benchmarked, or reviewed.

## Phase 0 — Foundations (Weeks 1–4)

**Goal:** acquire only the math/ML background repeatedly used in LLM papers and implementations.

Focus:
- Linear algebra: matrix operations, orthogonality, eigendecomposition, SVD
- Probability and information theory: expectation, likelihood, entropy, cross-entropy, KL divergence
- Optimization: gradients, chain rule, SGD, Adam
- ML fundamentals: MLE/MAP, regularization, bias/variance

Primary resources: selected MIT 18.06 and Stanford CS229 material.

**Gate:** derive cross-entropy/KL, follow tensor-shape derivations, and implement a small gradient-based optimization example.

## Phase 1 — Deep Learning (Weeks 5–8)

**Goal:** understand the training loop before using high-level trainers.

Focus:
- Forward/backward propagation
- Autograd
- Initialization and normalization
- SGD/Adam
- PyTorch tensor/module/optimizer lifecycle

Primary resource: MIT 6.S191.

**Artifact:** NumPy MLP + equivalent PyTorch model with explicit training/evaluation loop.

## Phase 2 — Transformers (Weeks 9–14)

**Goal:** understand and implement a modern decoder-only Transformer.

Focus:
- BPE/tokenization
- Embeddings and positional information
- Self-attention and causal masking
- Multi-head attention
- MLP blocks, residuals, normalization
- Autoregressive sampling
- KV-cache fundamentals

Primary resource: Stanford CS224N; practical companion: Hugging Face LLM Course.

**Artifacts:** BPE tokenizer, causal attention, decoder-only Transformer, Tiny GPT training run.

## Phase 3 — Pretraining / Stanford CS336 (Weeks 15–26)

**Goal:** learn the complete language-model development pipeline from raw data to evaluation.

Workstreams:
- Model/tokenizer/optimizer/training implementation
- Profiling and GPU efficiency
- Data preparation and quality
- Scaling laws and compute allocation
- End-to-end pretraining

**Artifact:** a reproducible small LM trained from raw text, with training curves, evaluation, data documentation, and systems profile.

## Phase 4 — Post-training (Weeks 27–34)

**Goal:** understand how base models become instruction-following and reasoning models.

Focus:
- SFT and chat formatting
- Packing and masking
- LoRA / QLoRA
- Preference data and reward models
- DPO
- PPO/GRPO concepts
- Reasoning/verifier-oriented post-training

**Artifact:** a controlled comparison of base, SFT, parameter-efficient, and preference-optimized variants.

## Phase 5 — LLM Systems (Weeks 20–38, overlaps Phases 3–4)

This is a specialization track and should run in parallel once Transformer fundamentals are solid.

Focus:
- CUDA execution/memory hierarchy/Tensor Cores
- Triton
- Tiled/fused MatMul
- FlashAttention
- BF16/FP16/FP8 and memory accounting
- KV cache / PagedAttention / continuous batching
- Speculative decoding
- DDP/FSDP/ZeRO and TP/PP/CP/EP
- NCCL collectives and communication cost
- Profiling and bottleneck analysis

Primary resource: GPU MODE + CS336 systems material.

**Artifact:** benchmark suite showing at least one measured kernel/runtime optimization with correctness validation.

## Phase 6 — Reasoning & Agents (Weeks 39–46)

**Goal:** treat agents as generate–verify–search–act systems rather than prompt wrappers.

Focus:
- Test-time compute
- Best-of-N / majority voting
- Outcome and process verifiers
- Search and planning
- Tool use and execution feedback
- Memory
- Coding/research agents
- Long-horizon evaluation

Primary resource: Stanford CS329A.

**Artifact:** a coding agent whose loop uses objective feedback such as compile/test/benchmark results.

## Phase 7 — Research (Weeks 47–52 and ongoing)

**Goal:** transition from learning established material to generating evidence.

Workflow:
1. Select a recent paper.
2. Reproduce a baseline claim.
3. Run ablations.
4. Identify failure modes.
5. Form a falsifiable hypothesis.
6. Run controlled experiments.
7. Report positive and negative results.

Preferred specialization: **LLM Systems + Reasoning/Coding Agents**.

**Artifact:** first complete research report with reproducible code, baseline, ablations, results, and limitations.

## Milestones

- M1 — Math/ML foundations ready
- M2 — Deep-learning training loop understood and implemented
- M3 — Decoder-only Transformer + Tiny GPT complete
- M4 — Stanford CS336 / end-to-end pretraining complete
- M5 — Post-training pipeline complete
- M6 — LLM systems benchmark/optimization portfolio complete
- M7 — Stanford CS329A + verifier/search agent complete
- M8 — First paper reproduction and original research project complete

## Execution policy

Only keep a small number of tasks `In Progress` simultaneously. Prefer one conceptual task plus one implementation task. New topics remain in `Backlog` until prerequisites and an explicit deliverable are clear.