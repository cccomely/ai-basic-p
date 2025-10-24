"""
实验1测评脚本：结构化提示词与输出
测试学生实现的 classify_text 函数
"""
import pytest
from student_code.lab1.main import classify_text, TextClassification
from grader.fixtures import ollama_health_check, clean_session_state


@pytest.mark.lab1
class TestLab1Classification:
    """实验1测评测试类"""
    
    def test_return_type_is_pydantic_model(self, ollama_health_check):
        """
        测试1：验证返回值类型为 TextClassification
        权重：20%
        """
        text = "今天天气不错"
        result = classify_text(text)
        
        assert isinstance(result, TextClassification), \
            f"返回值类型错误：期望 TextClassification，实际 {type(result)}"
    
    def test_category_is_valid(self, ollama_health_check):
        """
        测试2：验证 category 字段在允许的枚举值内
        权重：20%
        """
        text = "阿里云发布新一代AI芯片"
        result = classify_text(text)
        
        valid_categories = ['新闻', '技术', '体育', '娱乐', '财经']
        assert result.category in valid_categories, \
            f"分类类别无效：{result.category}，必须是 {valid_categories} 之一"
    
    def test_confidence_score_range(self, ollama_health_check):
        """
        测试3：验证 confidence_score 在 0-1 范围内
        权重：15%
        """
        text = "测试文本内容"
        result = classify_text(text)
        
        assert 0 <= result.confidence_score <= 1, \
            f"置信度超出范围：{result.confidence_score}，必须在 0-1 之间"
    
    def test_keywords_not_empty(self, ollama_health_check):
        """
        测试4：验证 keywords 列表非空且元素有效
        权重：15%
        """
        text = "人工智能技术快速发展"
        result = classify_text(text)
        
        assert len(result.keywords) > 0, "关键词列表不能为空"
        assert len(result.keywords) <= 5, f"关键词数量超出限制：{len(result.keywords)}，最多5个"
        
        for keyword in result.keywords:
            assert isinstance(keyword, str), f"关键词必须是字符串类型：{type(keyword)}"
            assert len(keyword) > 0, "关键词不能是空字符串"
    
    def test_tech_classification(self, ollama_health_check):
        """
        测试5：验证技术类文本分类准确性
        权重：15%
        """
        text = "OpenAI发布GPT-5，性能提升10倍"
        result = classify_text(text)
        
        assert result.category == '技术', \
            f"技术类文本分类错误：期望 '技术'，实际 '{result.category}'"
        assert result.confidence_score > 0.5, \
            f"技术类文本置信度过低：{result.confidence_score}"
    
    def test_sports_classification(self, ollama_health_check):
        """
        测试6：验证体育类文本分类准确性
        权重：15%
        """
        text = "中国队在巴黎奥运会夺得金牌"
        result = classify_text(text)
        
        assert result.category == '体育', \
            f"体育类文本分类错误：期望 '体育'，实际 '{result.category}'"
        assert result.confidence_score > 0.5, \
            f"体育类文本置信度过低：{result.confidence_score}"
    
    def test_multiple_samples(self, ollama_health_check):
        """
        测试7：批量测试不同类别样本
        权重：加分项
        """
        test_cases = [
            ("央视新闻报道今日重要事件", ['新闻', '娱乐']),  # 新闻类
            ("Python 3.12发布新特性", ['技术']),  # 技术类
            ("NBA总决赛今晚开打", ['体育']),  # 体育类
            ("热门电影票房破10亿", ['娱乐', '新闻']),  # 娱乐类
            ("股市行情分析报告", ['财经']),  # 财经类
        ]
        
        correct_count = 0
        total_count = len(test_cases)
        
        for text, expected_categories in test_cases:
            try:
                result = classify_text(text)
                if result.category in expected_categories:
                    correct_count += 1
                print(f"✓ 文本: {text} | 分类: {result.category} | 关键词: {result.keywords}")
            except Exception as e:
                print(f"✗ 文本: {text} | 错误: {e}")
        
        accuracy = correct_count / total_count
        print(f"\n批量测试准确率: {accuracy * 100:.1f}% ({correct_count}/{total_count})")
        
        assert accuracy >= 0.6, \
            f"批量测试准确率过低：{accuracy * 100:.1f}%，要求至少60%"


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"])
