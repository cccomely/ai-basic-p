"""
实验2：有状态对话的快照验证
学生需要实现 chat_with_memory 函数，管理多个独立会话的历史记录
"""
from typing import Dict, List
import httpx
import json


# 全局会话存储：{session_id: [消息列表]}
# 每条消息格式: {"role": "user" | "assistant", "content": "消息内容"}
SESSION_HISTORY: Dict[str, List[Dict[str, str]]] = {}


def chat_with_memory(message: str, session_id: str) -> dict:
    """
    带记忆功能的对话函数，支持多会话隔离
    
    参数:
        message: 用户当前消息
        session_id: 会话唯一标识符
    
    返回:
        字典，包含以下键:
        - response (str): AI的回复内容
        - history_length (int): 当前会话在本次对话前的历史消息数量
        - session_id (str): 回显的会话ID
    
    实现要求:
        1. 不同 session_id 的对话历史必须完全独立
        2. 同一 session_id 的多次调用必须累积历史
        3. history_length 必须精确反映本次对话前的历史消息数（user+assistant成对计数）
        4. 调用模型前，将历史消息作为上下文拼接到 Prompt 中
    
    数据结构建议:
        SESSION_HISTORY = {
            "session_001": [
                {"role": "user", "content": "你好"},
                {"role": "assistant", "content": "你好！有什么可以帮助你的吗？"},
                {"role": "user", "content": "天气怎么样"},
                {"role": "assistant", "content": "抱歉..."}
            ]
        }
    """
    global SESSION_HISTORY
    
    # 1. 检查 session_id 是否存在，不存在则初始化空列表
    if session_id not in SESSION_HISTORY:
        SESSION_HISTORY[session_id] = []
    
    # 2. 计算 history_length（当前会话在本次对话前的消息数）
    history_length = len(SESSION_HISTORY[session_id])
    
    # 3. 构建 Prompt，包含历史上下文 + 当前消息
    # 构建历史对话上下文
    history_context = ""
    for i in range(0, len(SESSION_HISTORY[session_id]), 2):
        if i + 1 < len(SESSION_HISTORY[session_id]):
            user_msg = SESSION_HISTORY[session_id][i]
            assistant_msg = SESSION_HISTORY[session_id][i + 1]
            history_context += f"用户: {user_msg['content']}\n助手: {assistant_msg['content']}\n\n"
    
    prompt = f"""{history_context}用户: {message}
助手: """
    
    # 4. 调用 Ollama API 获取回复
    api_url = "http://localhost:11434/api/generate"
    payload = {
        "model": "qwen3:8b",
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = httpx.post(api_url, json=payload, timeout=30.0)
        response.raise_for_status()
        
        response_data = response.json()
        ai_response = response_data["response"].strip()
        
        # 5. 保存用户消息和助手回复到历史记录
        # 添加用户消息
        SESSION_HISTORY[session_id].append({"role": "user", "content": message})
        # 添加助手回复
        SESSION_HISTORY[session_id].append({"role": "assistant", "content": ai_response})
        
        # 6. 返回结构化结果
        return {
            "response": ai_response,
            "history_length": history_length,
            "session_id": session_id
        }
        
    except httpx.RequestError as e:
        # 如果API调用失败，返回错误信息
        error_response = f"API调用失败: {str(e)}"
        return {
            "response": error_response,
            "history_length": history_length,
            "session_id": session_id
        }
    except Exception as e:
        # 其他异常处理
        error_response = f"系统错误: {str(e)}"
        return {
            "response": error_response,
            "history_length": history_length,
            "session_id": session_id
        }


def clear_session(session_id: str = None):
    """
    清除会话历史（辅助函数，用于测试）
    
    参数:
        session_id: 要清除的会话ID，如果为 None 则清除所有会话
    """
    global SESSION_HISTORY
    
    if session_id is None:
        SESSION_HISTORY.clear()
    elif session_id in SESSION_HISTORY:
        del SESSION_HISTORY[session_id]


# 测试代码（可选，用于学生本地调试）
if __name__ == "__main__":
    # 清空历史
    clear_session()
    
    # 测试单会话
    print("=== 测试单会话 ===")
    session_id = "test_session"
    
    result1 = chat_with_memory("你好", session_id)
    print(f"第1次对话 - history_length: {result1['history_length']}, response: {result1['response'][:50]}")
    
    result2 = chat_with_memory("我叫来恩炜，你想怎样？", session_id)
    print(f"第2次对话 - history_length: {result2['history_length']}, response: {result2['response'][:50]}")
    
    result3 = chat_with_memory("我刚才说了什么？", session_id)
    print(f"第3次对话 - history_length: {result3['history_length']}, response: {result3['response'][:50]}")
    
    # 测试多会话隔离
    print("\n=== 测试会话隔离 ===")
    clear_session()
    
    result_a1 = chat_with_memory("香蕉", "session_A")
    print(f"Session A 第1次 - history_length: {result_a1['history_length']}")
    
    result_b1 = chat_with_memory("黄瓜", "session_B")
    print(f"Session B 第1次 - history_length: {result_b1['history_length']}")
    
    result_a2 = chat_with_memory("我之前说了什么？", "session_B")
    print(f"Session A 第2次 - history_length: {result_a2['history_length']}, response: {result_a2['response'][:50]}")
