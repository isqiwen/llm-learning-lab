# LLM Learning Lab

A structured, implementation-first path for learning, developing, and researching large language models.

The repository is organized around **measurable artifacts**, not course completion alone. The long-term goal is to progress from mathematical and deep-learning foundations to language-model pretraining, post-training, LLM systems, reasoning/agents, paper reproduction, and original research.

## Guiding principles

1. **Implement before abstracting.** Rebuild important components before relying on high-level frameworks.
2. **Measure systems work.** Performance claims require profiles, benchmarks, and memory/throughput numbers.
3. **Evaluate model work.** Training and post-training experiments require reproducible evaluation.
4. **Read papers as hypotheses.** Reproduce claims, run ablations, and document failure modes.
5. **Prefer durable concepts over transient frameworks.** Attention, optimization, verification, search, GPU kernels, distributed systems, and evaluation matter more than any particular agent library.

## Roadmap

| Phase | Focus | Primary outcome |
|---|---|---|
| 0 | Foundations | Math/ML essentials for LLM work |
| 1 | Deep Learning | Training loop and backprop from first principles |
| 2 | Transformers | Decoder-only Transformer and Tiny GPT |
| 3 | Pretraining | Complete Stanford CS336 and train from raw text |
| 4 | Post-training | SFT, LoRA, DPO, RL/reasoning experiments |
| 5 | LLM Systems | CUDA/Triton, FlashAttention, profiling, distributed training/inference |
| 6 | Reasoning & Agents | Verifiers, search, tools, memory, coding/research agents |
| 7 | Research | Paper reproduction, ablations, original research project |

See [ROADMAP.md](ROADMAP.md) for sequencing and [CURRICULUM.md](CURRICULUM.md) for courses/resources.

## Repository structure

```text
llm-learning-lab/
├── README.md
├── ROADMAP.md
├── CURRICULUM.md
├── PROGRESS.md
├── notes/
│   ├── foundations/
│   ├── deep-learning/
│   ├── transformers/
│   ├── pretraining/
│   ├── post-training/
│   ├── llm-systems/
│   ├── agents/
│   └── research/
├── labs/
│   ├── tiny-neural-network/
│   ├── tiny-transformer/
│   ├── tiny-lm/
│   ├── post-training-lab/
│   └── llm-systems/
├── papers/
│   ├── reading-list.md
│   └── reviews/
└── research/
    ├── reproductions/
    ├── experiments/
    └── proposals/
```

Directories are created when they acquire real content; empty scaffolding is intentionally avoided.

## Core courses

- MIT 18.06 — selected linear algebra
- Stanford CS229 — selected machine-learning foundations
- MIT 6.S191 — deep learning
- Stanford CS224N — NLP, Transformers, modern LLM topics
- Hugging Face LLM Course — practical companion
- **Stanford CS336 — Language Modeling from Scratch** — core implementation course
- GPU MODE lectures — GPU/LLM systems
- Berkeley CS285 — selected RL material
- **Stanford CS329A — Self-Improving AI Agents** — reasoning/agents
- Stanford CS25 — ongoing frontier seminar

## Project management

GitHub Issues are the executable units of work. The `LLM Learning & Research` GitHub Project is the planning surface.

Recommended project fields:

- **Status:** Backlog / Ready / In Progress / Review / Done
- **Phase:** Foundations / Deep Learning / Transformers / Pretraining / Post-training / LLM Systems / Reasoning & Agents / Research
- **Type:** Course / Reading / Implementation / Experiment / Paper / Milestone
- **Priority:** P0 / P1 / P2 / P3
- **Effort:** S / M / L / XL

Each substantial issue should define deliverables and objective exit criteria.

## Research direction

The preferred specialization is **LLM Systems + Reasoning/Coding Agents**: combine model behavior with objective software/system verifiers such as compilation, unit tests, correctness checks, latency, throughput, memory usage, and profiling data.

A representative long-term loop is:

```text
model/agent
  -> generate C++/CUDA implementation
  -> compile
  -> test correctness
  -> benchmark/profile
  -> verifier scores result
  -> search/refine
  -> repeat
```

This repository should eventually contain both model-level experiments and systems-level evidence.