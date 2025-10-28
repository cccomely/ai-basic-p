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

# 创建工作目录
WORKDIR /workspace

# 预安装 Python 依赖（加速后续构建）
COPY ai-course-labs/requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt && rm /tmp/requirements.txt

# 设置 Python 环境变量
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1