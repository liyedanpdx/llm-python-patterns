from openai import OpenAI
from typing import Dict, Any, Optional, List
import logging
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import get_provider_config, API_PROVIDERS

class ChatMessage:
    """Chat message class"""
    
    def __init__(self, role: str, content: str, timestamp: Optional[float] = None):
        self.role = role  # "user", "assistant", "system"
        self.content = content
        self.timestamp = timestamp or time.time()
    
    def to_dict(self) -> Dict[str, str]:
        return {
            "role": self.role,
            "content": self.content
        }


class AIClient:
    def __init__(self, provider: str = "gemini", api_key: Optional[str] = None):
        """
        Initialize AI Client with specified provider
        
        Args:
            provider: API provider name (gemini, openai, anthropic, etc.)
            api_key: Optional API key override
        """
        self.provider = provider
        self.chat_history: List[ChatMessage] = []
        self._init_client(api_key)
        
    def _init_client(self, api_key_override: Optional[str] = None):
        """Initialize OpenAI-compatible client for specified provider"""
        try:
            # Get provider configuration
            self.config = get_provider_config(self.provider)
            
            # Override API key if provided
            if api_key_override:
                self.config["api_key"] = api_key_override
            
            # Initialize OpenAI client with provider's base URL
            self.client = OpenAI(
                api_key=self.config["api_key"],
                base_url=self.config["base_url"]
            )
            
            logger.info(f"✅ {self.provider} client initialized (model: {self.config['model']})")
            
        except Exception as e:
            logger.warning(f"⚠️ Failed to initialize {self.provider} client: {e}")
            raise
    
    @classmethod
    def get_available_providers(cls) -> List[str]:
        """Get list of available API providers"""
        return list(API_PROVIDERS.keys())
    
    def add_message(self, role: str, content: str):
        """Add message to chat history"""
        message = ChatMessage(role, content)
        self.chat_history.append(message)
    
    def get_chat_history(self) -> List[Dict[str, str]]:
        """Get chat history in OpenAI format"""
        return [msg.to_dict() for msg in self.chat_history]
    
    def clear_history(self):
        """Clear chat history"""
        self.chat_history = []
        logger.info("🗑️ Chat history cleared")
        
    def generate_text(self, prompt: str, model: Optional[str] = None, 
                     temperature: Optional[float] = None, top_p: Optional[float] = None) -> str:
        """Generate text using specified provider's API"""
        try:
            # Clear history and add current prompt
            self.clear_history()
            self.add_message("user", prompt)
            
            # Use provided parameters or config defaults
            model_name = model or self.config["model"]
            temp = temperature or self.config["temperature"]
            tp = top_p or self.config["top_p"]
            max_tokens = self.config["max_tokens"]
            
            # Make API call
            response = self.client.chat.completions.create(
                model=model_name,
                messages=self.get_chat_history(),
                temperature=temp,
                top_p=tp,
                max_tokens=max_tokens
            )
            
            result = response.choices[0].message.content
            
            # Add response to history
            self.add_message("assistant", result)
            
            return result
                
        except Exception as e:
            logger.error(f"{self.provider} API call failed: {str(e)}")
            raise Exception(f"API request failed: {str(e)}")
    
    def chat(self, user_message: str, model: Optional[str] = None, 
             temperature: Optional[float] = None, top_p: Optional[float] = None) -> str:
        """Chat with conversation history"""
        try:
            # Add user message to history
            self.add_message("user", user_message)
            
            # Use provided parameters or config defaults
            model_name = model or self.config["model"]
            temp = temperature or self.config["temperature"]
            tp = top_p or self.config["top_p"]
            max_tokens = self.config["max_tokens"]
            
            # Make API call with full history
            response = self.client.chat.completions.create(
                model=model_name,
                messages=self.get_chat_history(),
                temperature=temp,
                top_p=tp,
                max_tokens=max_tokens
            )
            
            result = response.choices[0].message.content
            
            # Add response to history
            self.add_message("assistant", result)
            
            return result
                
        except Exception as e:
            logger.error(f"{self.provider} chat API call failed: {str(e)}")
            raise Exception(f"API request failed: {str(e)}")
    
    def simple_query(self, query: str, model: Optional[str] = None) -> str:
        """Simple single query without preserving history"""
        original_history = self.chat_history.copy()
        self.clear_history()
        
        try:
            return self.generate_text(query, model)
        finally:
            # Restore original history
            self.chat_history = original_history
    
    def switch_provider(self, provider: str, api_key: Optional[str] = None):
        """Switch to a different API provider"""
        logger.info(f"🔄 Switching from {self.provider} to {provider}")
        self.provider = provider
        self._init_client(api_key)
        # Keep chat history when switching providers
    
    def get_provider_info(self) -> Dict[str, Any]:
        """Get current provider information"""
        return {
            "provider": self.provider,
            "model": self.config["model"],
            "base_url": self.config["base_url"],
            "temperature": self.config["temperature"],
            "top_p": self.config["top_p"]
        }


class MockAIClient:
    """Mock client for testing without API calls"""
    
    def __init__(self, provider: str = "mock", api_key: Optional[str] = None):
        self.provider = provider
        self.api_key = api_key  # Not used in mock
        self.chat_history: List[ChatMessage] = []
        logger.info(f"🧪 MockAIClient initialized for testing (provider: {provider})")
    
    def add_message(self, role: str, content: str):
        """Add message to chat history"""
        message = ChatMessage(role, content)
        self.chat_history.append(message)
    
    def get_chat_history(self) -> List[Dict[str, str]]:
        """Get chat history in OpenAI format"""
        return [msg.to_dict() for msg in self.chat_history]
    
    def clear_history(self):
        """Clear chat history"""
        self.chat_history = []
    
    @classmethod
    def get_available_providers(cls) -> List[str]:
        """Get list of available API providers"""
        return ["mock"] + list(API_PROVIDERS.keys())
    
    def generate_text(self, prompt: str, model: Optional[str] = None, 
                     temperature: Optional[float] = None, top_p: Optional[float] = None) -> str:
        """Generate mock response"""
        # Simulate different responses based on prompt keywords
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ['code', 'python', 'function', 'program']):
            return f"Mock coding response: Here's a simple Python function for your request about '{prompt[:30]}...'"
        elif any(word in prompt_lower for word in ['math', 'calculate', 'equation', 'solve']):
            return f"Mock math response: The solution to your mathematical query '{prompt[:30]}...' is calculated as follows."
        else:
            return f"Mock general response: This is a helpful response to your query about '{prompt[:30]}...'"
    
    def chat(self, user_message: str, model: Optional[str] = None, 
             temperature: Optional[float] = None, top_p: Optional[float] = None) -> str:
        """Mock chat with conversation history"""
        self.add_message("user", user_message)
        response = self.generate_text(user_message, model, temperature, top_p)
        self.add_message("assistant", response)
        return response
    
    def simple_query(self, query: str, model: Optional[str] = None) -> str:
        """Simple single query without preserving history"""
        return self.generate_text(query, model)
    
    def switch_provider(self, provider: str, api_key: Optional[str] = None):
        """Mock switch provider"""
        logger.info(f"🧪 Mock switching from {self.provider} to {provider}")
        self.provider = provider
    
    def get_provider_info(self) -> Dict[str, Any]:
        """Get mock provider information"""
        return {
            "provider": self.provider,
            "model": f"mock-{self.provider}-model",
            "base_url": "mock://api.example.com",
            "temperature": 0.7,
            "top_p": 0.95
        }


if __name__ == "__main__":
    """Test multi-provider AI client functionality"""
    
    print("🚀 Testing Multi-Provider AI Client")
    print("=" * 50)
    
    # Show available providers
    print(f"📋 Available providers: {AIClient.get_available_providers()}")
    
    # Test MockAIClient first
    print("\n🧪 Testing MockAIClient:")
    mock_client = MockAIClient("mock-gemini")
    
    test_queries = [
        "Write a Python function to sort a list",
        "Calculate the area of a circle with radius 10",
        "What is artificial intelligence?"
    ]
    
    for query in test_queries:
        print(f"\n❓ Query: {query}")
        try:
            response = mock_client.generate_text(query)
            print(f"🤖 Response: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Test provider switching with mock client
    print(f"\n🔄 Current provider info: {mock_client.get_provider_info()}")
    mock_client.switch_provider("mock-openai")
    print(f"🔄 After switching: {mock_client.get_provider_info()}")
    
    # Test real API client (will only work if API key is available)
    print("\n🌐 Testing Real API Client:")
    
    try:
        # Try Gemini first
        real_client = AIClient("gemini")
        
        test_prompt = "Hello, please introduce yourself briefly."
        print(f"\n❓ Query: {test_prompt}")
        response = real_client.generate_text(test_prompt)
        print(f"🤖 {real_client.provider} Response: {response[:100]}...")
        
        # Show provider info
        print(f"\n📊 Provider Info: {real_client.get_provider_info()}")
        
    except Exception as e:
        print(f"❌ Real API Error: {e}")
        print("💡 Note: This is expected if API keys are not properly configured")
    
    # Test conversation history
    print(f"\n💬 Testing Conversation History with Mock:")
    mock_chat = MockAIClient("mock-conversation")
    
    conversation = [
        "Hello, what's your name?",
        "Can you help me write Python code?",
        "What was my first question?"
    ]
    
    for msg in conversation:
        print(f"\n👤 User: {msg}")
        response = mock_chat.chat(msg)
        print(f"🤖 Assistant: {response}")
    
    print(f"\n📜 Full conversation history:")
    for i, msg in enumerate(mock_chat.get_chat_history(), 1):
        print(f"  {i}. {msg['role']}: {msg['content'][:60]}...")
    
    # Show provider switching capability
    print(f"\n🔀 Testing Provider Switching:")
    for provider in ["gemini", "gemini-pro", "openai", "openai-gpt3"]:
        try:
            test_client = AIClient(provider)
            info = test_client.get_provider_info()
            print(f"  ✅ {provider}: {info['model']} @ {info['base_url']}")
        except Exception as e:
            print(f"  ❌ {provider}: {str(e)[:60]}...")
    
    print(f"\n🎉 Multi-provider client testing completed!")
    
    # Demonstrate SubGraph concept (LangGraph-style)
    print(f"\n🔗 LangGraph SubGraph Concept Demo:")
    print(f"=" * 30)
    
    class SubGraphHandler:
        """
        SubGraph: Treat entire agent chain as a single processing unit
        This mimics LangGraph's subgraph concept where complex workflows
        can be encapsulated and reused as building blocks
        """
        
        def __init__(self, name: str, internal_agents: List):
            self.name = name
            self.internal_agents = internal_agents
            self.client = MockAIClient(f"subgraph-{name}")
        
        def process(self, request: str) -> Dict[str, Any]:
            """Process request through internal agent chain"""
            print(f"    🔸 SubGraph '{self.name}' processing...")
            
            # Simulate chain processing
            for agent in self.internal_agents:
                print(f"      → {agent} analyzing...")
            
            response = self.client.generate_text(request)
            return {
                "subgraph": self.name,
                "agents_used": self.internal_agents,
                "response": response
            }
    
    class MainGraphOrchestrator:
        """
        Main Graph that orchestrates multiple SubGraphs
        Similar to LangGraph's main workflow with embedded subgraphs
        """
        
        def __init__(self):
            # Create specialized subgraphs
            self.subgraphs = {
                "technical": SubGraphHandler("TechnicalSupport", 
                    ["CodeAgent", "DebugAgent", "ArchitectureAgent"]),
                "business": SubGraphHandler("BusinessLogic", 
                    ["MathAgent", "DataAgent", "ReportAgent"]),
                "general": SubGraphHandler("GeneralSupport", 
                    ["ChatAgent", "InfoAgent", "HelpAgent"])
            }
        
        def route_request(self, request: str) -> str:
            """Route request to appropriate subgraph (like LangGraph routing)"""
            request_lower = request.lower()
            
            if any(word in request_lower for word in ['code', 'bug', 'debug', 'technical']):
                chosen_subgraph = "technical"
            elif any(word in request_lower for word in ['calculate', 'data', 'business', 'report']):
                chosen_subgraph = "business"
            else:
                chosen_subgraph = "general"
            
            print(f"  🎯 Routing to '{chosen_subgraph}' subgraph")
            result = self.subgraphs[chosen_subgraph].process(request)
            
            return f"Processed by {result['subgraph']}: {result['response']}"
    
    # Demo SubGraph workflow
    print(f"\n🚀 Creating LangGraph-style Main Graph with SubGraphs:")
    main_graph = MainGraphOrchestrator()
    
    subgraph_test_cases = [
        "Fix this Python bug in my sorting algorithm",
        "Calculate quarterly revenue growth",
        "What's the weather like today?",
        "Debug my React component code",
        "Analyze sales data trends"
    ]
    
    for test_case in subgraph_test_cases:
        print(f"\n📝 Request: {test_case}")
        result = main_graph.route_request(test_case)
        print(f"✅ Result: {result[:80]}...")
    
    print(f"\n🎯 SubGraph Benefits (LangGraph Pattern):")
    print(f"  🔹 Modularity: Each subgraph is self-contained")
    print(f"  🔹 Reusability: Subgraphs can be used in multiple workflows") 
    print(f"  🔹 Scalability: Easy to add new subgraphs without changing main logic")
    print(f"  🔹 Testing: Each subgraph can be tested independently")
    print(f"  🔹 Composition: Complex workflows from simple building blocks")
    
    print(f"\n💡 Tips:")
    print(f"  - Use AIClient('gemini') for Gemini API")
    print(f"  - Use AIClient('openai') for OpenAI API") 
    print(f"  - Use MockAIClient() for testing without API calls")
    print(f"  - Add API keys to .env file for real API testing")
    print(f"  - SubGraphs enable LangGraph-style complex workflows! 🎉")