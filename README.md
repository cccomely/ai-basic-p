# Run qwen3 on Ollama via CNB

![badge](https://cnb.cool/Anyexyz/Ollama/qwen3/-/badge/git/latest/code/vscode-started)

在 CNB 中直接 使用 Ollama 运行 qwen3，预置模型，无需等待，零帧起步。

## 快速体验

### 通过云原生开发体验

1. `Fork` 本仓库到自己的组织下
2. 选择喜欢的分支，点击 `云原生开发` 启动远程开发环境
3. 约 `5～9` 秒后，进入远程开发命令行，输入以下命令即可体验

> ${image} 为模型名称，如 `qwen3:8b`

```shell
ollama run ${image}
```

### 本仓库已内置模型列表

- `qwen3:0.6b`
- `qwen3:1.7b`
- `qwen3:1.7b-q8_0`
- `qwen3:4b`
- `qwen3:8b`
- `qwen3:14b`
- `qwen3:30b`
- `qwen3:32b`
- `qwen3-code:30b`

## 进阶

### 公网访问

在 `PORTS` 中将 Ollama 暴露到外网，添加 11434 端口即可。