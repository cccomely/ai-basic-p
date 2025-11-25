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


# def classify_text(text: str) -> TextClassification:
#     """
#     对输入文本进行分类，返回结构化的分类结果
    
#     参数:
#         text: 待分类的文本内容
    
#     返回:
#         TextClassification 实例，包含分类类别、置信度和关键词
    
#     实现要求:
#         1. 使用 Ollama API 调用 qwen3:8b 模型
#         2. 设计结构化 Prompt，要求模型输出 JSON 格式
#         3. 解析模型输出并验证为 TextClassification 模型
#         4. category 必须是预定义的5个类别之一
#         5. confidence_score 必须在 0-1 范围内
#         6. keywords 列表长度为 1-5
    
#     提示:
#         - 在 Prompt 中明确指定输出格式和有效类别
#         - 可以使用 Few-Shot 示例提高输出稳定性
#         - 使用 Pydantic 的自动验证确保数据有效性
#     """
#     # TODO: 学生需要实现此函数
#     # 
#     # 实现步骤建议:
#     # 1. 构建结构化 Prompt，要求模型输出 JSON 格式
#     # 2. 调用 Ollama API (http://localhost:11434/api/generate)
#     # 3. 解析响应中的 JSON 字符串
#     # 4. 使用 TextClassification.model_validate() 创建实例
#     # 5. 返回验证后的 Pydantic 模型实例
    
#     # 示例 Prompt 结构（学生需要完善）:
#     # prompt = f"""请对以下文本进行分类..."""
    
#     # 提示：
#     # 1. 构建结构化 Prompt，要求模型输出 JSON 格式
#     # 2. 调用 Ollama API (http://localhost:11434/api/generate)
#     # 3. 解析响应中的 JSON 字符串
#     # 4. 使用 TextClassification.model_validate() 创建实例
#     # 5. 返回验证后的 Pydantic 模型实例
    
#     raise NotImplementedError("请实现 classify_text 函数")
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
    prompt = f"""请对以下文本进行精确分类，并输出JSON格式的结果：
文本内容："{text}"

分类规则：
- "新闻"：一般时事报道、社会新闻、政治新闻等
- "技术"：科技产品发布、软件开发、AI技术、编程、硬件等
- "体育"：体育赛事、运动员、比赛结果等
- "娱乐"：电影、音乐、明星、综艺节目等
- "财经"：股票、经济、金融、投资等

要求：
1. 根据上述规则准确分类，特别是技术相关内容应归类为"技术"而非"新闻"
2. 置信度必须是0-1之间的小数
3. 提取1-5个关键词

请严格按照以下JSON格式输出，不要包含其他内容：
{{
    "category": "类别名称",
    "confidence_score": "置信度",
    "keywords": ["关键词1", "关键词2"]
}}"""

    # 2. 调用Ollama API
    api_url = "http://localhost:11434/api/generate"
    payload = {
        "model": "qwen3:8b",
        "prompt": prompt,
        "format": "json",
        "stream": False
    }
    
    response = httpx.post(api_url, json=payload, timeout=30.0)
    response.raise_for_status()
    
    # 3. 解析JSON响应
    response_data = response.json()
    json_str = response_data["response"]
    
    # 清理JSON字符串（移除可能的markdown格式）
    json_str = json_str.strip()
    if json_str.startswith("```json"):
        json_str = json_str[7:]
    if json_str.endswith("```"):
        json_str = json_str[:-3]
    
    # 解析JSON
    result_dict = json.loads(json_str)
    
    # 4. 创建Pydantic实例
    classification = TextClassification.model_validate(result_dict)
    
    # 5. 返回结果
    return classification


# 测试代码（可选，用于学生本地调试）
if __name__ == "__main__":
    # 测试示例
    test_texts = [
        "OpenAI发布GPT-5，性能提升10倍",
        "中国队在巴黎奥运会夺得金牌",
        "A股市场今日大涨，沪指突破4000点",
        "近日，一高校保洁阿姨手搓银杏叶周边，用秋叶打造校园童话世界：银杏叶伞、星星叶堆······浪漫，至死不渝。",
        "China's State Council Information Office on Saturday released a white paper titled \"Carbon Peaking and Carbon Neutrality China\'s Plans and Solutions.\"",
        "AI future depends as much on responsible governance as technology, experts say"
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
