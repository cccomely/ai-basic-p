FROM cnbcool/default-dev-env:latest

RUN apt update && apt install -y nload

RUN curl -fsSL https://ollama.com/install.sh | sh

ENV OLLAMA_MODELS=/workspace/models

ENV OLLAMA_HOST=0.0.0.0

ENV OLLAMA_ORIGINS=*

# 刷新缓存