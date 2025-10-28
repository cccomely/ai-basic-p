FROM cnbcool/default-dev-env:latest

# 更新软件源并安装基础工具
RUN apt update && apt install -y \
    nload \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# 安装 Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# 配置 Ollama 环境变量
ENV OLLAMA_MODELS=/workspace/models
ENV OLLAMA_HOST=0.0.0.0
ENV OLLAMA_ORIGINS=*

# 设置 Python 环境变量
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 创建工作目录
WORKDIR /workspace