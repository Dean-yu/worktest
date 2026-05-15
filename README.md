# worktest

用于构建一个 Web 入口的 AI 对话交互系统（Direct Chat + Agent Task）。

## 当前实现（v0.1 scaffold）
- FastAPI 后端骨架
- `/api/v1/chat` 统一入口
- 自动路由（direct / agent）
- Session 短期记忆（内存版）
- Agent 模式返回 planning 草案

## 快速启动
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## 示例请求
```bash
curl -X POST http://127.0.0.1:8000/api/v1/chat \
  -H 'content-type: application/json' \
  -d '{
    "user_id":"u1",
    "session_id":"s1",
    "message":"帮我规划一个自动化发布任务"
  }'
```

## 文档
- 架构说明：`docs/architecture.md`
