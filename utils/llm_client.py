"""
统一的LLM客户端 - 支持OpenAI形式的多提供商调用
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

import time
import json
import logging
from typing import List, Dict, Any, Optional, Union
from openai import OpenAI
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMConfig:
    """LLM配置管理类"""
    
    # 默认参数
    DEFAULT_TEMPERATURE = 0.3
    DEFAULT_TOP_P = 0.95
    DEFAULT_MAX_TOKENS = 4096
    
    @staticmethod
    def get_provider_config(provider: str) -> Dict[str, Any]:
        """获取指定提供商的配置"""
        configs = {
            "gemini": {
                "api_key": Config.GEMINI_API_KEY,
                "model": Config.GEMINI_MODEL,
                "base_url": "https://generativelanguage.googleapis.com/v1beta",
                "temperature": Config.DEFAULT_TEMPERATURE,
                "top_p": Config.DEFAULT_TOP_P
            },
            "openai": {
                "api_key": Config.OPENAI_API_KEY,
                "model": "gpt-4",
                "base_url": "https://api.openai.com/v1",
                "temperature": Config.DEFAULT_TEMPERATURE,
                "top_p": Config.DEFAULT_TOP_P
            }
        }
        
        if provider not in configs:
            raise ValueError(f"Unsupported provider: {provider}")
        
        return configs[provider]


class ChatMessage:
    """聊天消息类"""
    
    def __init__(self, role: str, content: str, timestamp: Optional[float] = None):
        self.role = role  # "user", "assistant", "system"
        self.content = content
        self.timestamp = timestamp or time.time()
    
    def to_dict(self) -> Dict[str, str]:
        return {
            "role": self.role,
            "content": self.content
        }


class LLMClient:
    """统一的LLM客户端"""
    
    def __init__(self, default_provider: str = "gemini"):
        """
        初始化LLM客户端
        
        Args:
            default_provider: 默认的LLM提供商
        """
        self.default_provider = default_provider
        self.chat_history: List[ChatMessage] = []
        
        # 初始化Gemini客户端
        self._init_gemini()
    
    def _init_gemini(self):
        """初始化Gemini客户端"""
        try:
            config = LLMConfig.get_provider_config("gemini")
            if config.get("api_key"):
                genai.configure(api_key=config["api_key"])
                logger.info("✅ Gemini client initialized")
        except Exception as e:
            logger.warning(f"⚠️ Failed to initialize Gemini: {e}")
    
    def add_message(self, role: str, content: str):
        """添加消息到聊天历史"""
        message = ChatMessage(role, content)
        self.chat_history.append(message)
    
    def get_chat_history(self) -> List[Dict[str, str]]:
        """获取聊天历史（OpenAI格式）"""
        return [msg.to_dict() for msg in self.chat_history]
    
    def clear_history(self):
        """清空聊天历史"""
        self.chat_history = []
        logger.info("🗑️ Chat history cleared")
    
    def chat(self, user_message: str, provider: Optional[str] = None, 
             model: Optional[str] = None, temperature: Optional[float] = None, 
             top_p: Optional[float] = None, thinking_budget: Optional[int] = None,
             include_thoughts: Optional[bool] = None) -> str:
        """简单的聊天接口

        Args:
            user_message: 用户消息
            provider: 指定的LLM提供商（可选）
            model: 指定的模型名称（可选），会覆盖config中的默认模型
            temperature: 采样温度
            top_p: Top-p采样参数
            thinking_budget: 思考预算（仅gemini支持）
            include_thoughts: 是否包含思考过程（仅gemini支持）

        Returns:
            助手的响应
        """
        try:
            # 使用指定提供商或默认提供商
            provider = provider or self.default_provider
            
            # 获取提供商配置
            config = LLMConfig.get_provider_config(provider)
            
            # 使用指定模型或配置中的默认模型
            model_name = model or config.get('model')
            
            # 使用配置中的参数或传入的参数
            temperature = temperature or config.get('temperature', LLMConfig.DEFAULT_TEMPERATURE)
            top_p = top_p or config.get('top_p', LLMConfig.DEFAULT_TOP_P)

            # 添加用户消息到聊天历史
            self.add_message("user", user_message)

            # 调用LLM
            start_time = time.time()
            
            logger.info(f"开始调用 {provider} ({model_name})...")

            if provider == "gemini":
                result = self._call_gemini_direct(
                    user_message, model_name, temperature, top_p, 
                    thinking_budget, include_thoughts
                )
            else:
                # 使用OpenAI兼容接口
                client = OpenAI(
                    api_key=config["api_key"],
                    base_url=config["base_url"]
                )

                # 构造基础请求参数
                request_params = {
                    "model": model_name,
                    "messages": self.get_chat_history(),
                    "temperature": temperature,
                    "top_p": top_p
                }

                # 如果是gemini提供商且设置了thinking_budget，添加special格式
                if provider == "gemini" and thinking_budget is not None:
                    # 如果没有指定include_thoughts，默认为False
                    if include_thoughts is None:
                        include_thoughts = False
                    
                    request_params["extra_body"] = {
                        "generationConfig": {
                            "responseSchema": {
                                "type": "object",
                                "properties": {
                                    "thinking": {
                                        "type": "string"
                                    },
                                    "response": {
                                        "type": "string"
                                    }
                                }
                            }
                        }
                    }

                response = client.chat.completions.create(**request_params)
                result = response.choices[0].message.content

            elapsed = time.time() - start_time
            logger.info(f'{provider} ({model_name}) 响应时间: {elapsed:.2f}s')

            # 添加助手响应到聊天历史
            self.add_message("assistant", result)

            return result

        except Exception as e:
            logger.error(f"调用 {provider} ({model_name if 'model_name' in locals() else 'unknown'}) 失败: {str(e)}")
            raise
    
    def _call_gemini_direct(self, message: str, model_name: str, 
                           temperature: float, top_p: float,
                           thinking_budget: Optional[int] = None,
                           include_thoughts: Optional[bool] = None) -> str:
        """直接调用Gemini API"""
        try:
            # 创建模型实例
            model = genai.GenerativeModel(
                model_name=model_name,
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                }
            )
            
            # 准备生成配置
            generation_config = {
                "temperature": temperature,
                "top_p": top_p,
                "max_output_tokens": LLMConfig.DEFAULT_MAX_TOKENS,
            }
            
            # 如果设置了thinking_budget，添加相关配置
            if thinking_budget is not None:
                # Gemini 2.5的思考模式配置
                generation_config["response_format"] = {
                    "type": "json_object" if include_thoughts else "text"
                }
            
            # 生成响应
            response = model.generate_content(
                message,
                generation_config=generation_config
            )
            
            if response.candidates and len(response.candidates) > 0:
                result = response.candidates[0].content.parts[0].text
                
                # 如果启用了思考过程，解析JSON响应
                if thinking_budget is not None and include_thoughts:
                    try:
                        parsed_response = json.loads(result)
                        thinking = parsed_response.get("thinking", "")
                        actual_response = parsed_response.get("response", result)
                        
                        if thinking:
                            logger.info(f"🤔 Gemini thinking: {thinking[:100]}...")
                        
                        return actual_response
                    except json.JSONDecodeError:
                        logger.warning("⚠️ Failed to parse thinking response, using raw text")
                
                return result
            else:
                raise Exception("No valid response generated")
                
        except Exception as e:
            logger.error(f"Gemini API调用失败: {str(e)}")
            raise
    
    def simple_query(self, query: str, provider: Optional[str] = None, 
                    model: Optional[str] = None) -> str:
        """简单的单次查询，不保留历史记录"""
        original_history = self.chat_history.copy()
        self.clear_history()
        
        try:
            response = self.chat(query, provider=provider, model=model)
            return response
        finally:
            # 恢复原始历史记录
            self.chat_history = original_history
    
    def batch_query(self, queries: List[str], provider: Optional[str] = None,
                   model: Optional[str] = None) -> List[str]:
        """批量查询"""
        results = []
        
        for i, query in enumerate(queries):
            logger.info(f"Processing query {i+1}/{len(queries)}")
            result = self.simple_query(query, provider=provider, model=model)
            results.append(result)
            
            # 添加小延迟避免API限制
            time.sleep(0.5)
        
        return results
    
    def similarity_check(self, text1: str, text2: str, 
                        provider: Optional[str] = None) -> float:
        """使用LLM进行相似性检查"""
        prompt = f"""
请比较以下两个技术术语的相似性，并给出0-1之间的相似度分数。

术语1: {text1}
术语2: {text2}

请只返回一个0-1之间的数字，表示相似度（1表示完全相同，0表示完全不同）。
不要添加任何解释，只返回数字。
        """.strip()
        
        try:
            response = self.simple_query(prompt, provider=provider)
            # 尝试提取数字
            import re
            numbers = re.findall(r'0\.\d+|1\.0|0|1', response)
            if numbers:
                return min(float(numbers[0]), 1.0)
            else:
                logger.warning(f"⚠️ Could not parse similarity score from: {response}")
                return 0.0
        except Exception as e:
            logger.error(f"❌ Similarity check failed: {e}")
            return 0.0


if __name__ == "__main__":
    
    """测试LLM客户端功能"""
    client = LLMClient()
    
    print("🧪 Testing LLM Client")
    print("=" * 40)
    
    # 测试简单查询
    test_queries = [
        "什么是Large Language Model？",
        "GPT-4和Claude有什么区别？",
        "向量数据库的主要用途是什么？"
    ]
    
    for query in test_queries:
        try:
            print(f"\n❓ Query: {query}")
            response = client.simple_query(query)
            print(f"🤖 Response: {response[:200]}...")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # 测试相似性检查
    print(f"\n🔍 Testing similarity check:")
    similarity = client.similarity_check("LLM", "Large Language Model")
    print(f"'LLM' vs 'Large Language Model': {similarity}")