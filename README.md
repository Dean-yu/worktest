# worktest

用于构建一个 Web 入口的 AI 对话交互系统（Direct Chat + Agent Task）。

## 当前实现（v0.2 scaffold）
- FastAPI 后端骨架
- `/api/v1/chat` 统一入口
- 前置意图识别与分发（支持 `auto`）
- 歧义请求补充信息引导（推荐选项 + 自定义）
- Session 短期记忆（默认记忆）
- 记忆 CRUD API（支持用户增删改）
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
    "message":"帮我看一下这个方案"
  }'
```

## 记忆管理 API
- `GET /api/v1/memory/{session_id}`：查看当前 session 记忆
- `PUT /api/v1/memory/{session_id}/{message_id}`：更新指定记忆
- `DELETE /api/v1/memory/{session_id}/{message_id}`：删除指定记忆

## 文档
- 架构说明：`docs/architecture.md`
