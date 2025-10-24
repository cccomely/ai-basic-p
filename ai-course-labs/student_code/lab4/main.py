"""
实验4：LangChain 链的确定性输出
学生需要使用 LangChain 的 PromptTemplate 和 LLMChain 生成广告文案
"""
from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


def generate_ad(input_dict: dict) -> dict:
    """
    使用 LangChain 链生成广告文案
    
    参数:
        input_dict: 字典，包含:
            - product (str): 产品名称
            - feature (str): 核心特性
    
    返回:
        字典，包含:
        - ad_copy (str): 生成的广告文案
        - word_count (int): 文案字数（使用 len(ad_copy) 统计）
        - template_used (str): 使用的模板名称
    
    实现要求:
        1. 使用 PromptTemplate 定义广告文案生成模板
        2. 创建 LLMChain，连接 PromptTemplate 和 Ollama LLM
        3. 链的输出必须经过后处理，提取文案并计算字数
        4. 模板必须包含 {product} 和 {feature} 两个变量
        5. word_count 必须与 ad_copy 的实际长度一致
    """
    # TODO: 学生需要实现此函数
    #
    # 实现步骤建议:
    # 1. 创建 PromptTemplate，包含产品和特性变量
    # 2. 创建 Ollama LLM 实例
    # 3. 创建 LLMChain，连接 Prompt 和 LLM
    # 4. 运行链，传入产品和特性参数
    # 5. 提取文案，计算字数
    # 6. 返回结构化结果
    
    # 提取输入参数
    product = input_dict.get("product", "")
    feature = input_dict.get("feature", "")
    
    if not product or not feature:
        raise ValueError("input_dict 必须包含 'product' 和 'feature' 键")
    
    # 创建 Prompt 模板
    template = """你是一位专业的广告文案撰写专家。请为以下产品创作一条吸引人的广告文案。

产品名称: {product}
核心特性: {feature}

要求:
1. 文案长度控制在20-50字之间
2. 突出产品的核心特性
3. 语言简洁有力，富有吸引力
4. 直接输出文案内容，不要有其他说明

广告文案:"""
    
    prompt = PromptTemplate(
        input_variables=["product", "feature"],
        template=template
    )
    
    # 创建 Ollama LLM
    llm = Ollama(
        model="qwen3:8b",
        base_url="http://localhost:11434",
        temperature=0.7  # 适当的创造性
    )
    
    # 创建 LLMChain
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=False
    )
    
    # 运行链
    response = chain.run(product=product, feature=feature)
    
    # 后处理：清理文案
    ad_copy = response.strip()
    
    # 移除可能的多余标点或换行
    ad_copy = ad_copy.replace('\n', ' ').strip()
    
    # 如果文案过长，截取前100字
    if len(ad_copy) > 100:
        ad_copy = ad_copy[:100]
    
    # 计算字数
    word_count = len(ad_copy)
    
    # 返回结果
    return {
        "ad_copy": ad_copy,
        "word_count": word_count,
        "template_used": "standard_ad_template"
    }


def generate_ad_advanced(input_dict: dict, style: str = "passionate") -> dict:
    """
    高级版本：支持多种广告风格
    
    参数:
        input_dict: 包含 product 和 feature
        style: 广告风格，可选 'passionate'（激情型）、'rational'（理性型）、'humorous'（幽默型）
    
    返回:
        同 generate_ad
    
    扩展功能（可选实现）:
        - 根据风格选择不同的模板
        - 添加质量评分功能
        - 实现重试机制
    """
    # TODO: 可选扩展功能，学生可以实现高级特性
    
    product = input_dict.get("product", "")
    feature = input_dict.get("feature", "")
    
    # 根据风格选择模板
    templates = {
        "passionate": """激情型广告文案专家，请为产品创作充满激情和感染力的文案！

产品: {product}
特性: {feature}

要求: 20-50字，充满激情，使用感叹号和强烈的情感词汇！

文案:""",
        "rational": """理性型广告文案专家，请创作强调产品价值和实用性的文案。

产品: {product}
特性: {feature}

要求: 20-50字，理性客观，强调产品优势和价值。

文案:""",
        "humorous": """幽默型广告文案专家，请创作轻松幽默的文案。

产品: {product}
特性: {feature}

要求: 20-50字，轻松幽默，易于传播。

文案:"""
    }
    
    template_text = templates.get(style, templates["passionate"])
    
    prompt = PromptTemplate(
        input_variables=["product", "feature"],
        template=template_text
    )
    
    llm = Ollama(
        model="qwen3:8b",
        base_url="http://localhost:11434",
        temperature=0.8
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run(product=product, feature=feature)
    
    ad_copy = response.strip().replace('\n', ' ').strip()
    if len(ad_copy) > 100:
        ad_copy = ad_copy[:100]
    
    word_count = len(ad_copy)
    
    # 简单的质量评分
    quality_score = 0
    if product in ad_copy:
        quality_score += 40
    if feature in ad_copy or any(word in ad_copy for word in feature.split()):
        quality_score += 30
    if 10 <= word_count <= 100:
        quality_score += 30
    
    return {
        "ad_copy": ad_copy,
        "word_count": word_count,
        "template_used": f"{style}_template",
        "quality_score": quality_score  # 额外的质量评分
    }


# 测试代码（可选，用于学生本地调试）
if __name__ == "__main__":
    # 测试基础版本
    print("=== 测试基础广告生成 ===")
    test_inputs = [
        {"product": "智能手表", "feature": "心率监测"},
        {"product": "无线耳机", "feature": "降噪功能"},
        {"product": "扫地机器人", "feature": "自动避障"}
    ]
    
    for input_data in test_inputs:
        try:
            result = generate_ad(input_data)
            print(f"\n产品: {input_data['product']}")
            print(f"文案: {result['ad_copy']}")
            print(f"字数: {result['word_count']}")
            print(f"模板: {result['template_used']}")
        except Exception as e:
            print(f"错误: {e}")
    
    # 测试高级版本（可选）
    print("\n\n=== 测试高级广告生成（多风格） ===")
    test_input = {"product": "智能水杯", "feature": "记录饮水量"}
    
    for style in ["passionate", "rational", "humorous"]:
        try:
            result = generate_ad_advanced(test_input, style=style)
            print(f"\n风格: {style}")
            print(f"文案: {result['ad_copy']}")
            print(f"字数: {result['word_count']}")
            if 'quality_score' in result:
                print(f"质量评分: {result['quality_score']}")
        except Exception as e:
            print(f"错误: {e}")
