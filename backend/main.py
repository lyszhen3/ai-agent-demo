"""
AI Agent 后端服务 - 基于 AgentScope 框架
支持多模型配置
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from typing import Optional
import yaml
from pathlib import Path

app = FastAPI(title="AI Agent Demo API")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 加载配置文件
config_path = Path(__file__).parent / "config.yaml"
with open(config_path, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# 模型客户端缓存
model_clients: dict = {}


def get_model_client(provider: str) -> OpenAI:
    """获取或创建模型客户端"""
    if provider not in model_clients:
        provider_config = config["models"].get(provider)
        if not provider_config:
            raise ValueError(f"未知的模型提供商：{provider}")
        
        model_clients[provider] = OpenAI(
            api_key=provider_config["api_key"],
            base_url=provider_config.get("base_url")
        )
    
    return model_clients[provider]


class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None
    model_provider: Optional[str] = None  # 可选，不指定则使用默认模型
    model_name: Optional[str] = None  # 可选，不指定则使用提供商的默认模型


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    model_used: str  # 返回实际使用的模型


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """处理聊天请求"""
    try:
        # 确定使用的模型提供商和模型
        provider = request.model_provider or config["default_model"]["provider"]
        model_name = request.model_name or config["default_model"]["model_name"]
        
        # 获取系统提示词
        system_prompt = config.get("system_prompt", "你是一个友好的 AI 助手，帮助用户解决问题。")
        
        # 获取客户端并调用 API
        client = get_model_client(provider)
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.message}
            ],
            temperature=0.7
        )
        
        return ChatResponse(
            response=response.choices[0].message.content,
            conversation_id=request.conversation_id or "default",
            model_used=f"{provider}/{model_name}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


@app.get("/models")
async def list_models():
    """获取所有可用的模型列表"""
    models_info = []
    for provider, provider_config in config.get("models", {}).items():
        for model in provider_config.get("models", []):
            models_info.append({
                "provider": provider,
                "name": model["name"],
                "display_name": model["display_name"]
            })
    return {"models": models_info, "default": config.get("default_model")}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)