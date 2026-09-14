# Paper Reading List

Prioritize papers that directly support the current phase. Do not accumulate an unbounded reading backlog.

## Transformer foundations

- [ ] Attention Is All You Need
- [ ] Language Models are Unsupervised Multitask Learners (GPT-2)
- [ ] Scaling Laws for Neural Language Models
- [ ] Training Compute-Optimal Large Language Models (Chinchilla)

## Architecture and efficiency

- [ ] FlashAttention
- [ ] FlashAttention-2
- [ ] RoPE / rotary positional embeddings
- [ ] RMSNorm
- [ ] Mixture-of-Experts reference work relevant to current experiments

## Post-training and reasoning

- [ ] InstructGPT / RLHF reference work
- [ ] Direct Preference Optimization (DPO)
- [ ] STaR
- [ ] Let's Verify Step by Step
- [ ] DeepSeekMath / GRPO-related work

## Agents and test-time compute

- [ ] ReAct
- [ ] Scaling LLM Test-Time Compute Optimally
- [ ] Large Language Monkeys / repeated sampling work
- [ ] LATS or a representative search/planning paper
- [ ] SWE-agent / coding-agent evaluation work relevant to experiments

## Systems

- [ ] PagedAttention / vLLM
- [ ] Megatron-LM / tensor-parallel reference work
- [ ] ZeRO / FSDP-related distributed-training work
- [ ] Recent inference-serving work selected when Phase 5 begins

## Review template

For each deep-read paper create `papers/reviews/<paper-slug>.md` containing:

```text
Problem
Motivation
Hypothesis
Method
Baselines
Evaluation
Ablations
Failure modes / limitations
Reproduction plan
Compute/data requirements
Open questions
```

The list should be revised as the field evolves; relevance to active experiments has priority over completeness.