# Curriculum

Courses are mapped to capabilities. Completion is secondary to producing the corresponding implementation or experiment.

## 1. Foundations

### MIT 18.06 — Linear Algebra
Use selectively for:
- matrix/vector spaces
- orthogonality and least squares
- eigenvalues/eigenvectors
- SVD

URL: https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/

### Stanford CS229 — Machine Learning
Use selectively for:
- MLE/MAP
- regularization
- optimization
- probabilistic modeling
- bias/variance

URL: https://cs229.stanford.edu/

## 2. Deep Learning

### MIT 6.S191 — Introduction to Deep Learning
Focus on:
- neural networks
- backpropagation
- optimization
- sequence/generative modeling

URL: https://introtodeeplearning.com/

Companion: Dive into Deep Learning — https://d2l.ai/

## 3. Transformers and Modern NLP

### Stanford CS224N
Focus on:
- language modeling
- attention and Transformers
- pretraining
- post-training/evaluation
- retrieval/agents where relevant

URL: https://web.stanford.edu/class/cs224n/

### Hugging Face LLM Course
Use as the practical companion for:
- tokenizer/model APIs
- datasets
- fine-tuning
- Accelerate
- causal LM workflows
- modern LLM topics

URL: https://huggingface.co/learn/llm-course/

## 4. Core Implementation Course

### Stanford CS336 — Language Modeling from Scratch
**Highest-priority implementation course in this roadmap.**

Focus on:
- tokenizer/model/optimizer/training from scratch
- systems profiling and efficiency
- scaling laws
- data processing
- end-to-end language-model training

URL: https://cs336.stanford.edu/

Expected outcome: a complete, reproducible small pretraining stack and technical report.

## 5. Post-training and Reinforcement Learning

### Berkeley CS285 — Deep Reinforcement Learning
Do not treat this as a prerequisite to all LLM work. Study selected material when entering RL-based post-training.

Focus on:
- MDP/policy/reward
- policy gradient
- actor-critic
- PPO-related foundations
- importance sampling and KL constraints

URL: https://rail.eecs.berkeley.edu/deeprlcourse/

Additional practical work:
- SFT
- LoRA/QLoRA
- reward modeling
- DPO
- PPO/GRPO-style reasoning experiments

## 6. LLM Systems

### GPU MODE Lectures
Primary systems companion.

Focus on:
- CUDA/GPU performance
- Triton
- GEMM optimization
- FlashAttention
- Tensor Cores
- profiling
- NCCL/multi-GPU
- inference optimization

URL: https://github.com/gpu-mode/lectures

Systems topics to study alongside:
- mixed precision
- activation/optimizer memory
- gradient checkpointing
- DDP/FSDP/ZeRO
- TP/PP/CP/EP
- KV cache
- PagedAttention
- continuous batching
- speculative decoding

## 7. Reasoning and Agents

### Stanford CS329A — Self-Improving AI Agents
Focus on:
- test-time compute
- verifier design
- search/planning
- RL and feedback
- tools/code execution
- memory
- coding/research agents
- long-horizon evaluation

URL: https://cs329a.stanford.edu/

Expected outcome: an agent with explicit objective verification and reproducible evaluation.

## 8. Frontier Tracking

### Stanford CS25 — Transformers United
Use after fundamentals are solid to track frontier ideas and researchers.

URL: https://web.stanford.edu/class/cs25/

## Reading discipline

For every paper selected for deep reading, record:
1. Problem
2. Motivation
3. Core hypothesis
4. Method
5. Baselines
6. Evaluation protocol
7. Ablations
8. Limitations/failure modes
9. What would falsify the paper's claim?
10. Reproduction difficulty and compute requirement

Store detailed reviews under `papers/reviews/` and maintain a prioritized queue in `papers/reading-list.md`.