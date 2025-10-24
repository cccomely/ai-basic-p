"""
实验2测评脚本：有状态对话的快照验证
测试学生实现的 chat_with_memory 函数
"""
import pytest
from student_code.lab2.main import chat_with_memory, clear_session
from grader.fixtures import ollama_health_check, clean_session_state


@pytest.mark.lab2
class TestLab2StatefulChat:
    """实验2测评测试类"""
    
    def setup_method(self):
        """每个测试方法执行前清空所有会话"""
        clear_session()
    
    def test_first_message_history_length_zero(self, ollama_health_check):
        """
        测试1：验证首次对话 history_length 为 0
        权重：15%
        """
        session_id = "test_first_message"
        result = chat_with_memory("你好", session_id)
        
        assert result['history_length'] == 0, \
            f"首次对话的 history_length 应为 0，实际为 {result['history_length']}"
        assert result['session_id'] == session_id, \
            f"session_id 回显错误：期望 '{session_id}'，实际 '{result['session_id']}'"
        assert isinstance(result['response'], str), \
            f"response 必须是字符串类型，实际 {type(result['response'])}"
        assert len(result['response']) > 0, \
            "response 不能为空字符串"
    
    def test_history_accumulation(self, ollama_health_check):
        """
        测试2：验证历史消息累积
        权重：20%
        """
        session_id = "test_accumulation"
        
        # 第1次对话
        result1 = chat_with_memory("第一条消息", session_id)
        assert result1['history_length'] == 0, \
            f"第1次对话 history_length 应为 0，实际 {result1['history_length']}"
        
        # 第2次对话
        result2 = chat_with_memory("第二条消息", session_id)
        assert result2['history_length'] == 2, \
            f"第2次对话 history_length 应为 2（1对user+assistant），实际 {result2['history_length']}"
        
        # 第3次对话
        result3 = chat_with_memory("第三条消息", session_id)
        assert result3['history_length'] == 4, \
            f"第3次对话 history_length 应为 4（2对user+assistant），实际 {result3['history_length']}"
    
    def test_session_isolation(self, ollama_health_check):
        """
        测试3：验证会话隔离
        权重：25%
        """
        session_a = "session_A"
        session_b = "session_B"
        
        # Session A 第1次对话
        result_a1 = chat_with_memory("我是A用户", session_a)
        assert result_a1['history_length'] == 0, \
            f"Session A 第1次对话 history_length 应为 0，实际 {result_a1['history_length']}"
        
        # Session B 第1次对话
        result_b1 = chat_with_memory("我是B用户", session_b)
        assert result_b1['history_length'] == 0, \
            f"Session B 第1次对话 history_length 应为 0，实际 {result_b1['history_length']}"
        
        # Session A 第2次对话
        result_a2 = chat_with_memory("A的第二条消息", session_a)
        assert result_a2['history_length'] == 2, \
            f"Session A 第2次对话 history_length 应为 2，实际 {result_a2['history_length']}"
        
        # Session B 第2次对话
        result_b2 = chat_with_memory("B的第二条消息", session_b)
        assert result_b2['history_length'] == 2, \
            f"Session B 第2次对话 history_length 应为 2，实际 {result_b2['history_length']}"
    
    def test_cross_session_alternating(self, ollama_health_check):
        """
        测试4：交叉验证（交替向两个 session 发送消息）
        权重：25%
        """
        session_a = "alice"
        session_b = "bob"
        
        # 交替发送4次消息
        result_a1 = chat_with_memory("A消息1", session_a)  # A: history=0
        result_b1 = chat_with_memory("B消息1", session_b)  # B: history=0
        result_a2 = chat_with_memory("A消息2", session_a)  # A: history=2
        result_b2 = chat_with_memory("B消息2", session_b)  # B: history=2
        
        assert result_a1['history_length'] == 0, "Session A 第1次应为0"
        assert result_b1['history_length'] == 0, "Session B 第1次应为0"
        assert result_a2['history_length'] == 2, "Session A 第2次应为2"
        assert result_b2['history_length'] == 2, "Session B 第2次应为2"
    
    def test_output_structure(self, ollama_health_check):
        """
        测试5：验证输出字典结构
        权重：15%
        """
        session_id = "test_structure"
        result = chat_with_memory("测试消息", session_id)
        
        # 检查必需的键
        required_keys = ['response', 'history_length', 'session_id']
        for key in required_keys:
            assert key in result, \
                f"返回字典缺少必需的键: '{key}'，当前包含的键: {list(result.keys())}"
        
        # 检查数据类型
        assert isinstance(result['response'], str), \
            f"response 必须是字符串，实际 {type(result['response'])}"
        assert isinstance(result['history_length'], int), \
            f"history_length 必须是整数，实际 {type(result['history_length'])}"
        assert isinstance(result['session_id'], str), \
            f"session_id 必须是字符串，实际 {type(result['session_id'])}"
    
    def test_session_content_persistence(self, ollama_health_check):
        """
        测试6：验证历史内容确实被保存
        权重：加分项
        """
        session_id = "test_persistence"
        
        # 第1次：提供个人信息
        chat_with_memory("我叫李四", session_id)
        
        # 第2次：询问之前说了什么
        result = chat_with_memory("我刚才说我叫什么？", session_id)
        
        # 验证回复中包含之前的信息
        response_lower = result['response'].lower()
        assert '李四' in result['response'] or 'lisi' in response_lower, \
            f"AI 回复中应包含之前提供的信息（李四），实际回复: {result['response'][:100]}"
        
        print(f"✓ 内容持久化测试通过，AI正确回忆了历史信息")


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"])
