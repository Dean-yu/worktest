# AI 对话交互系统（重构 v0.1）

## 目标
- Web 入口
- 两条执行路径：Direct Chat / Agent Task
- 支持多模型（当前先保留路由位）
- 短期记忆（Session 级）
- 安全与 SLO 后续迭代

## 当前落地
- `POST /api/v1/chat`
- 自动路由：普通问答 -> direct；任务表达 -> agent
- agent 返回计划草案（planning 样式）

## 下一步
1. 接入真实模型适配层（OpenAI/Anthropic/Google）
2. 增加工具调用协议（参数校验、幂等）
3. 接入长期记忆（事实卡+置信度+过期）
4. 增加审核与审计日志
5. 完整可观测（trace/token/cost/latency）
