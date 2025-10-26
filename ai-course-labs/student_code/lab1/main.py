"""
实验1：结构化提示词与输出
学生需要实现 classify_text 函数，使用 Pydantic 模型返回结构化的文本分类结果
"""
from typing import List
from pydantic import BaseModel, Field
import httpx
import json


class TextClassification(BaseModel):
    """
    文本分类结果的数据模型
    """
    category: str = Field(
        ..., 
        description="文本分类类别，必须是以下之一：'新闻', '技术', '体育', '娱乐', '财经'"
    )
    confidence_score: float = Field(
        ..., 
        ge=0.0, 
        le=1.0,
        description="分类置信度，范围0.0-1.0"
    )
    keywords: List[str] = Field(
        ..., 
        min_length=1, 
        max_length=5,
        description="从文本中提取的1-5个关键词"
    )


def classify_text(text: str) -> TextClassification:
    """
    对输入文本进行分类，返回结构化的分类结果
    
    参数:
        text: 待分类的文本内容
    
    返回:
        TextClassification 实例，包含分类类别、置信度和关键词
    
    实现要求:
        1. 使用 Ollama API 调用 qwen3:8b 模型
        2. 设计结构化 Prompt，要求模型输出 JSON 格式
        3. 解析模型输出并验证为 TextClassification 模型
        4. category 必须是预定义的5个类别之一
        5. confidence_score 必须在 0-1 范围内
        6. keywords 列表长度为 1-5
    
    提示:
        - 在 Prompt 中明确指定输出格式和有效类别
        - 可以使用 Few-Shot 示例提高输出稳定性
        - 使用 Pydantic 的自动验证确保数据有效性
    """
    # TODO: 学生需要实现此函数
    # 
    # 实现步骤建议:
    # 1. 构建结构化 Prompt，要求模型输出 JSON 格式
    # 2. 调用 Ollama API (http://localhost:11434/api/generate)
    # 3. 解析响应中的 JSON 字符串
    # 4. 使用 TextClassification.model_validate() 创建实例
    # 5. 返回验证后的 Pydantic 模型实例
    
    # 示例 Prompt 结构（学生需要完善）:
    # prompt = f"""请对以下文本进行分类..."""
    
    # 提示：
    # 1. 构建结构化 Prompt，要求模型输出 JSON 格式
    # 2. 调用 Ollama API (http://localhost:11434/api/generate)
    # 3. 解析响应中的 JSON 字符串
    # 4. 使用 TextClassification.model_validate() 创建实例
    # 5. 返回验证后的 Pydantic 模型实例
    
    raise NotImplementedError("请实现 classify_text 函数")


# 测试代码（可选，用于学生本地调试）
if __name__ == "__main__":
    # 测试示例
    test_texts = [
        "OpenAI发布GPT-5，性能提升10倍",
        "中国队在巴黎奥运会夺得金牌",
        "A股市场今日大涨，沪指突破3000点"
    ]
    
    for text in test_texts:
        try:
            result = classify_text(text)
            print(f"\n文本: {text}")
            print(f"分类: {result.category}")
            print(f"置信度: {result.confidence_score}")
            print(f"关键词: {result.keywords}")
        except Exception as e:
            print(f"错误: {e}")
