## AI Agent Demo

基于 AgentScope 框架的 AI Agent 工程

## 技术栈

- **后端**: Python + FastAPI + AgentScope
- **前端**: Vue 3 + Vite
- **依赖管理**: uv (Python), npm (Frontend)

## 功能

- 简单的 Chat Agent 对话功能

## 快速开始

### 1. 安装后端依赖

```bash
uv sync
```

### 2. 配置 API Key

编辑 `backend/main.py`，将 `your-api-key` 替换为你的实际 OpenAI API key。

### 3. 启动后端服务

```bash
uv run python backend/main.py
```

后端服务将在 `http://localhost:8000` 启动。

### 4. 安装前端依赖

```bash
cd frontend
npm install
```

### 5. 启动前端开发服务器

```bash
npm run dev
```

前端应用将在 `http://localhost:3000` 启动。

## API 接口

### POST /chat

发送聊天消息

**请求体**:
```json
{
  "message": "你好",
  "conversation_id": "default"
}
```

**响应**:
```json
{
  "response": "你好！有什么我可以帮助你的吗？",
  "conversation_id": "default"
}
```

### GET /health

健康检查

## 项目结构

```
ai-agent-demo/
├── backend/
│   └── main.py          # FastAPI 后端服务
├── frontend/
│   ├── App.vue          # Vue 主组件
│   ├── main.js          # Vue 入口文件
│   ├── index.html       # HTML 模板
│   ├── package.json     # 前端依赖配置
│   └── vite.config.js   # Vite 配置
├── pyproject.toml       # Python 项目配置
└── README.md            # 项目说明
```

## 注意事项

1. 需要有效的 OpenAI API key 才能使用对话功能
2. 后端服务默认运行在 8000 端口
3. 前端服务默认运行在 3000 端口