FROM cnbcool/default-dev-env:latest

# 安装系统依赖和Python环境
RUN apt update && apt install -y \
    python3 \
    python3-pip \
    python3-dev \
    nload \
    jq \
    && rm -rf /var/lib/apt/lists/*

# 确保python和pip命令可用
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1 && \
    update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

# 升级pip到最新版本
RUN pip install --upgrade pip setuptools wheel

# 安装 Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# 配置 Ollama 环境变量
ENV OLLAMA_MODELS=/workspace/models
ENV OLLAMA_HOST=0.0.0.0
ENV OLLAMA_ORIGINS=*

# 设置工作目录
WORKDIR /workspace/ai-course-labs

# 复制依赖文件
COPY ai-course-labs/requirements.txt /tmp/requirements.txt

# 安装 Python 依赖（预安装所有实验所需的包）
RUN pip install --no-cache-dir -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

# 验证Python环境和关键包已安装
RUN python --version && \
    pip --version && \
    python -c "import langchain; import pydantic; import pytest; print('✅ All dependencies installed successfully')"

# 重置工作目录
WORKDIR /workspace

# 刷新缓存
# Version: 2025-10-28