# LLM Learning Lab

从理解原理、独立实现到可复现实验与研究的大模型学习实验室。主方向：**LLM Systems + Reasoning / Coding Agents**。

> 当前处于规划初始化阶段，尚无学习成果验收记录。下一步是 [#22：能力诊断与实验环境](../../issues/22)，不是继续收集课程或直接启动大规模训练。

## 从这里开始

| 文档 | 解决的问题 |
|---|---|
| [ROADMAP.md](ROADMAP.md) | 八阶段目标、依赖、能力门槛与范围 |
| [CURRICULUM.md](CURRICULUM.md) | 主课程、选学章节、公开资源与版本限制 |
| [52 周执行基线](docs/weekly-plan.md) | 每周学习主题、实验、交付物和对应 Issue |
| [实验规范](docs/experiment-protocol.md) | 如何设计公平、可复核、不自欺的实验 |
| [研究计划](docs/research-plan.md) | 如何从复现进入可证伪的研究问题 |
| [Project 与权限](docs/project-management.md) | 字段、看板、授权与安全同步 |
| [PROGRESS.md](PROGRESS.md) | 已通过验收的成果；不是待办列表 |
| [AGENTS.md](AGENTS.md) | AI 助教与编码助手的职责边界 |

## 八阶段与现有任务

| 阶段跟踪 Issue | 学习目标 | 核心产物 |
|---|---|---|
| [M1 #2](../../issues/2) | 数学、概率与优化 | 推导、数值检验、能力诊断 |
| [M2 #3](../../issues/3) | 神经网络与训练循环 | NumPy MLP、PyTorch 对照、恢复测试 |
| [M3 #4](../../issues/4) | Transformer | BPE、因果注意力、Tiny GPT、评估器 |
| [M4 #5](../../issues/5) | 预训练与 CS336 A1–A4 | 数据到训练、评估、系统分析的完整流程 |
| [M5 #6](../../issues/6) | 后训练与 CS336 A5 | SFT/LoRA、偏好优化、可验证奖励实验 |
| [M6 #7](../../issues/7) | LLM Systems | GPU kernel、推理与通信成本实验 |
| [M7 #8](../../issues/8) | Reasoning / Agents | 有预算、验证器与隐藏测试的 Coding Agent |
| [M8 #9](../../issues/9) | 复现与研究 | 复现报告、可证伪假设、消融与研究报告 |

这些是 **Epic/阶段跟踪 Issues**，不等于已经创建了 GitHub 原生 Milestones 或 Sub-issues。当前共有 #1–#36：1 个管理任务、8 个阶段任务、27 个执行/实验任务。

## 执行原则

- 52 周、每周 10–15 小时只是待确认的规划假设；W01 从实际开始学习算起，没有自动设置日历截止日。
- 同时最多一个核心实现任务与一个配套阅读/实验任务。Systems 与 CS336 复用同一份成果，不额外叠加一份周工时。
- 看完视频、AI 写好代码、跑出一个好样例都不算掌握。完成必须有解释、代码/推导、可复核证据与局限说明。
- 实验首先验证正确性，再测效果与成本。负结果是合法成果；不要求每项实验都跑赢基线。
- 不在公开仓库上传密钥、私人/单位数据、大模型权重、原始受限数据或未经许可的课程作业答案。

## Project 同步

`planning/project.json` 保存初始化字段、父阶段与依赖；**不保存或覆盖实际学习进度**。GitHub Project 的实时 Status 由执行过程维护。

```bash
# 不访问网络，只校验本地计划
python3 scripts/sync_project.py --validate-only
python3 -m unittest discover -s tests -v

# 本机 gh 完成登录及 project 授权后：先只读预览，再确认写入
python3 scripts/sync_project.py
python3 scripts/sync_project.py --apply
```

脚本仅定位已有的 `LLM Learning & Research` Project，补充字段、加入本仓库 Issues、填充空字段；不新建 Project，不删除条目，不覆盖已有 Status/字段，不改可见性。Views、工作流及原生父子/阻塞关系不由该脚本配置。详细权限与限制见 [Project 指南](docs/project-management.md)。

## 内容组织

`notes/` 保存个人推导；`labs/` 保存独立实现；`papers/` 保存评审；`research/` 保存复现、实验和提案；`templates/` 保存记录模板。目录有真实内容才创建。大型数据与运行产物保存在仓库外，只提交可分享的摘要、配置和哈希。
