# Curriculum — 课程服务于能力，而不是刷课清单

资源核对日期：**2026-09-14**。以下“学习范围/输出”是本仓库的自学安排，不代表官方课程全部要求。开始正式作业时记录课程版本、材料日期与代码 commit；不要混用不同年份的 handout、测试和评分规则。

| 资源 | 学法与本仓库输出 | 官方入口 / 公开性说明 |
|---|---|---|
| MIT 18.06 | 选学矩阵、投影、最小二乘、SVD；#23 数值实验 | [Spring 2010 OCW](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/)；公开课程资源 |
| Stanford CS229 | 按缺口补似然、正则化、概率与优化；#24–25 | [课程主页](https://cs229.stanford.edu/)；优先可访问讲义，不把校内课程访问当作前提 |
| MIT 6.S191 | 神经网络、训练与序列建模核心内容；#26–28 | [官方主页](https://introtodeeplearning.com/)；按主页提供的公开材料学习 |
| PyTorch Learn the Basics | tensors/autograd/data/model/optimization/save-load；#27 | [官方教程](https://docs.pytorch.org/tutorials/beginner/basics/intro.html)；随实际环境固定版本 |
| Stanford CS224N | 主学 LM/attention/Transformer/evaluation；#10–12、#29 | [Winter 2026 主页](https://web.stanford.edu/class/cs224n/)；2026 校内视频要求登录，主页列出的完整公开视频为 2024 版，不能当成全部 2026 录播 |
| Hugging Face LLM Course | tokenizer/datasets/model APIs 与 fine-tuning；#14 的实践补充 | [官方课程](https://huggingface.co/learn/llm-course/en/chapter1/1)；与自己的底层实现对照，不替代推导 |
| Stanford CS336 | 核心实现课程，作业按下表映射 | [Spring 2026](https://cs336.stanford.edu/)；编程量大，先 CPU correctness，再选择算力规模 |
| GPU MODE | 按 MatMul/attention/profiling 任务选讲座，不全量刷 | [讲座仓库](https://github.com/gpu-mode/lectures)；#13、#16–18 |
| Triton tutorials | 从 vector add/MatMul 到 fused attention，重视测试与测量 | [官方教程](https://triton-lang.org/main/getting-started/tutorials/index.html)；#16–17 |
| Berkeley CS185/285 | 在后训练阶段选学 MDP、policy gradient、actor-critic | [官方主页](https://rail.eecs.berkeley.edu/deeprlcourse/)；不把完整 RL 课程设为所有 LLM/Agent 任务的前置 |
| Stanford CS329A | test-time compute、verification、tools、planning、evaluation；#19–20、#35 | [官方主页](https://cs329a.stanford.edu/)当前为 Autumn 2025；按公开阅读/作业资源自学，不承诺校内服务/API credits |
| Stanford CS25 | 基础成熟后的前沿补充；每月选一讲即可 | [Transformers United V6](https://web.stanford.edu/class/cs25/)；不替代基础课 |

## CS336 五个作业的覆盖

官方 Spring 2026 课程列出五个作业，不能只规划前四个。[来源](https://cs336.stanford.edu/)

| 作业 | 本仓库对应 | 完成口径 |
|---|---|---|
| A1 Basics | #30；复用 #10–12 | 核心模型/分词/优化/训练能力 |
| A2 Systems | #13、#16–17、#34 | profiling、attention、内存/并行；共享成果 |
| A3 Scaling | #31 | 可访问课程 API 或明确标注的小规模替代 |
| A4 Data | #32 | 数据管道、过滤/去重与质量评估 |
| A5 Alignment and Reasoning RL | #33；共享 #14–15 | SFT/RL，DPO 为可选 Part 2 |

M4 管 A1–A4 的预训练主线；A5 在 M5 完成后才有全课程覆盖记录。缩规模教学实验与官方原要求完成分别记录。

## 自学与公开仓库边界

课程官网可访问，不代表能使用 Gradescope、校内视频、算力额度或课程训练 API。遇到访问限制，先用公开材料和本地替代实验，并标注差异。

CS336 对 AI 代做作业和参考现成实现有明确限制；本仓库采用更审慎的学习方式：核心作业独立完成，AI 用于概念解释、提示和复查。官方作业答案默认在私有工作区；公开仓库主要存原创实验、推导、测量和合法引用。不要直接复制课程讲义、数据集或他人答案。

## 阅读方法

每次深读记录：问题、假设、关键公式、方法、强基线、评估协议、消融、局限、复现预算以及什么结果能推翻结论。每篇至少映射到一个可做的小实验，使用 [研究协议](docs/research-plan.md) 与 [实验模板](templates/experiment.md)。
