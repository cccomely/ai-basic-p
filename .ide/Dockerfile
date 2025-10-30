FROM python:3.10-slim

# 更新软件源并安装基础工具
RUN apt update && apt install -y \
    curl \
    nload \
    git \
    git-lfs \
    openssh-server \
    && rm -rf /var/lib/apt/lists/*

# 安装 code-server 与插件
RUN curl -fsSL https://code-server.dev/install.sh | sh &&\
    code-server --install-extension cnbcool.cnb-welcome &&\
    code-server --install-extension redhat.vscode-yaml &&\
    code-server --install-extension waderyan.gitblame &&\
    code-server --install-extension mhutchie.git-graph &&\
    code-server --install-extension donjayamanne.githistory &&\
    code-server --install-extension cloudstudio.live-server &&\
    code-server --install-extension tencent-cloud.coding-copilot

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