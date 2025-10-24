"""
实验3：记忆系统的内容检索
学生需要使用 LangChain 的 ConversationBufferMemory 管理会话历史
"""
from typing import Dict
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


# 全局 Memory 映射：{session_id: ConversationBufferMemory 实例}
SESSION_MEMORIES: Dict[str, ConversationBufferMemory] = {}


def chat_with_langchain_memory(message: str, session_id: str) -> dict:
    """
    使用 LangChain 的 ConversationBufferMemory 进行对话
    
    参数:
        message: 用户消息
        session_id: 会话ID
    
    返回:
        字典，包含:
        - response (str): AI回复
        - memory_variables (dict): ConversationBufferMemory 的内部变量
    
    实现要求:
        1. 使用 ConversationBufferMemory 管理每个 session 的历史
        2. 将 Memory 对象与 Ollama LLM 集成
        3. memory_variables 应包含 'history' 键
        4. 不同 session 的 Memory 必须独立
    """
    global SESSION_MEMORIES
    
    # TODO: 学生需要实现此函数
    #
    # 实现步骤建议:
    # 1. 检查 session_id 是否存在对应的 Memory，不存在则创建
    # 2. 创建 Ollama LLM 实例
    # 3. 创建 PromptTemplate（包含历史上下文）
    # 4. 创建 LLMChain，连接 Prompt、LLM 和 Memory
    # 5. 运行链并获取响应
    # 6. 返回响应和 memory_variables
    
    # 初始化或获取 Memory
    if session_id not in SESSION_MEMORIES:
        SESSION_MEMORIES[session_id] = ConversationBufferMemory(
            memory_key="history",
            return_messages=False
        )
    
    memory = SESSION_MEMORIES[session_id]
    
    # 创建 Ollama LLM
    llm = Ollama(
        model="qwen3:8b",
        base_url="http://localhost:11434"
    )
    
    # 创建 Prompt 模板
    template = """以下是历史对话记录：
{history}

当前用户消息: {input}
助手回复:"""
    
    prompt = PromptTemplate(
        input_variables=["history", "input"],
        template=template
    )
    
    # 创建 LLMChain
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        verbose=False
    )
    
    # 运行链
    response = chain.predict(input=message)
    
    # 获取 memory variables
    memory_variables = memory.load_memory_variables({})
    
    return {
        "response": response.strip(),
        "memory_variables": memory_variables
    }


def get_memory_summary(session_id: str) -> str:
    """
    获取指定会话的完整历史记录摘要
    
    参数:
        session_id: 会话ID
    
    返回:
        格式化的历史记录字符串，如:
        "User: 你好\nAI: 你好！有什么可以帮助你的吗？\nUser: ..."
        
        如果会话不存在，返回空字符串或提示信息
    
    实现要求:
        1. 返回人类可读的格式
        2. 包含完整的用户输入和AI回复
        3. 对不存在的 session_id，返回空字符串或提示
    """
    global SESSION_MEMORIES
    
    # TODO: 学生需要实现此函数
    #
    # 实现步骤建议:
    # 1. 检查 session_id 是否存在
    # 2. 获取 Memory 的 buffer 或 chat_memory
    # 3. 格式化消息历史为可读字符串
    # 4. 返回格式化结果
    
    # 检查会话是否存在
    if session_id not in SESSION_MEMORIES:
        return ""
    
    memory = SESSION_MEMORIES[session_id]
    
    # 获取历史消息
    # ConversationBufferMemory 的历史存储在 chat_memory.messages 中
    messages = memory.chat_memory.messages
    
    if not messages:
        return ""
    
    # 格式化历史记录
    summary_lines = []
    for msg in messages:
        # LangChain 的消息对象有 type 属性
        if hasattr(msg, 'type'):
            role = "User" if msg.type == "human" else "AI"
        else:
            # 兼容处理
            role = "User" if "human" in str(type(msg)).lower() else "AI"
        
        summary_lines.append(f"{role}: {msg.content}")
    
    return "\n".join(summary_lines)


def clear_memory(session_id: str = None):
    """
    清除会话记忆（辅助函数，用于测试）
    
    参数:
        session_id: 要清除的会话ID，如果为 None 则清除所有会话
    """
    global SESSION_MEMORIES
    
    if session_id is None:
        SESSION_MEMORIES.clear()
    elif session_id in SESSION_MEMORIES:
        del SESSION_MEMORIES[session_id]


# 测试代码（可选，用于学生本地调试）
if __name__ == "__main__":
    # 清空记忆
    clear_memory()
    
    # 测试对话
    print("=== 测试 LangChain Memory ===")
    session_id = "test_session"
    
    result1 = chat_with_langchain_memory("我的电话是13800138000", session_id)
    print(f"第1次对话:")
    print(f"  Response: {result1['response'][:50]}")
    print(f"  Memory variables keys: {result1['memory_variables'].keys()}")
    
    result2 = chat_with_langchain_memory("我的邮箱是test@example.com", session_id)
    print(f"\n第2次对话:")
    print(f"  Response: {result2['response'][:50]}")
    
    # 获取历史摘要
    summary = get_memory_summary(session_id)
    print(f"\n历史摘要:\n{summary}")
    
    # 验证信息是否保存
    print(f"\n验证信息持久化:")
    print(f"  包含电话号码: {'13800138000' in summary}")
    print(f"  包含邮箱: {'test@example.com' in summary}")
