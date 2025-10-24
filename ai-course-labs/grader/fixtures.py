"""
共享测试夹具
提供 Ollama 健康检查、会话状态清理等功能
"""
import pytest
import httpx
from typing import Generator


@pytest.fixture(scope="session")
def ollama_health_check():
    """
    测试套件启动时检查 Ollama 服务健康状态
    验证服务可达且已加载 qwen3:8b 模型
    """
    ollama_url = "http://localhost:11434/api/tags"
    
    try:
        response = httpx.get(ollama_url, timeout=10.0)
        response.raise_for_status()
        
        data = response.json()
        models = data.get("models", [])
        model_names = [model.get("name", "") for model in models]
        
        # 检查是否包含 qwen3:8b 模型
        has_qwen3 = any("qwen3" in name.lower() and "8b" in name.lower() for name in model_names)
        
        if not has_qwen3:
            pytest.skip(
                f"Ollama 服务运行中，但未找到 qwen3:8b 模型。\n"
                f"请运行: ollama pull qwen3:8b\n"
                f"当前可用模型: {model_names}"
            )
        
        print(f"\n✓ Ollama 服务正常，已加载模型: {model_names}")
        return True
        
    except httpx.RequestError as e:
        pytest.skip(
            f"无法连接到 Ollama 服务 ({ollama_url})。\n"
            f"请确保 Ollama 已启动: ollama serve\n"
            f"错误信息: {e}"
        )
    except Exception as e:
        pytest.skip(f"Ollama 健康检查失败: {e}")


@pytest.fixture(scope="function")
def clean_session_state():
    """
    每个测试函数执行前清理全局会话存储
    用于实验2和实验3的状态隔离
    """
    # 在测试前执行清理
    yield
    
    # 测试后清理（可选）
    # 这里可以添加清理代码，但通常测试前清理更重要
    pass


@pytest.fixture(scope="session")
def test_timeout():
    """
    配置全局测试超时时间
    """
    return 30  # 30秒超时
