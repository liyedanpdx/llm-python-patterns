# AI Agent System Template

## Claude Code Template for Building Intelligent AI Agent Systems

This template provides a structured approach to building AI agent systems using proven design patterns. Perfect for creating LangChain-style workflows, multi-agent systems, or intelligent automation tools.

## 🏗️ Project Structure

```
your_ai_agent_project/
├── agents/
│   ├── __init__.py
│   ├── base_agent.py          # Abstract base class (Template Method)
│   ├── specialized_agents.py  # Concrete agent implementations
│   └── agent_factory.py       # Agent creation (Factory Pattern)
├── tools/
│   ├── __init__.py
│   ├── tool_registry.py       # Tool management (Registry Pattern)
│   ├── base_tool.py          # Tool interface (Command Pattern)
│   └── implementations/       # Specific tool implementations
├── providers/
│   ├── __init__.py
│   ├── llm_factory.py        # Provider creation (Abstract Factory)
│   ├── base_provider.py      # Provider interface (Strategy Pattern)
│   └── implementations/      # OpenAI, Anthropic, etc.
├── workflow/
│   ├── __init__.py
│   ├── chain_manager.py      # Request routing (Chain of Responsibility)
│   └── execution_engine.py  # Workflow orchestration
├── config/
│   ├── settings.py           # Configuration management
│   └── config.yaml          # Runtime configuration
├── utils/
│   ├── __init__.py
│   ├── logger.py            # Logging utilities
│   └── validators.py       # Input validation
└── main.py                  # Entry point (Facade Pattern)
```

## 🎯 Design Patterns Applied

### 1. **Template Method Pattern** - Agent Workflow
```python
# agents/base_agent.py
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def execute_task(self, task):
        \"\"\"Template method defining standard agent workflow\"\"\"
        # 1. Validate input
        validated_task = self.validate_input(task)
        
        # 2. Process task (subclass-specific)
        result = self.process_task(validated_task)
        
        # 3. Format response
        formatted_result = self.format_response(result)
        
        # 4. Log execution
        self.log_execution(task, formatted_result)
        
        return formatted_result
    
    def validate_input(self, task):
        \"\"\"Default validation - can be overridden\"\"\"
        if not task or not task.strip():
            raise ValueError("Task cannot be empty")
        return task.strip()
    
    @abstractmethod
    def process_task(self, task):
        \"\"\"Each agent implements its own processing logic\"\"\"
        pass
    
    def format_response(self, result):
        \"\"\"Default formatting - can be overridden\"\"\"
        return {"status": "completed", "result": result}
    
    def log_execution(self, task, result):
        \"\"\"Default logging\"\"\"
        print(f"Agent {self.__class__.__name__} executed: {task[:50]}...")
```

### 2. **Factory Pattern** - Agent Creation
```python
# agents/agent_factory.py
from .specialized_agents import CodeAgent, ResearchAgent, WritingAgent

class AgentFactory:
    _agents = {
        "code": CodeAgent,
        "research": ResearchAgent, 
        "writing": WritingAgent
    }
    
    @classmethod
    def create_agent(cls, agent_type, llm_provider=None):
        if agent_type not in cls._agents:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        agent_class = cls._agents[agent_type]
        return agent_class(llm_provider=llm_provider)
    
    @classmethod
    def create_agent_for_task(cls, task_description):
        \"\"\"Intelligent agent selection based on task\"\"\"
        task_lower = task_description.lower()
        
        if any(word in task_lower for word in ["code", "program", "debug"]):
            return cls.create_agent("code")
        elif any(word in task_lower for word in ["research", "analyze", "study"]):
            return cls.create_agent("research")
        else:
            return cls.create_agent("writing")
```

### 3. **Chain of Responsibility** - Request Routing
```python
# workflow/chain_manager.py
class AgentChain:
    def __init__(self):
        self.first_handler = None
    
    def add_agent(self, agent):
        if not self.first_handler:
            self.first_handler = agent
        else:
            current = self.first_handler
            while hasattr(current, 'next_agent') and current.next_agent:
                current = current.next_agent
            current.next_agent = agent
    
    def handle_request(self, task):
        if self.first_handler:
            return self.first_handler.handle(task)
        return {"error": "No agents available"}

class ChainAgent(BaseAgent):
    def __init__(self, can_handle_func, llm_provider=None):
        self.can_handle = can_handle_func
        self.llm_provider = llm_provider
        self.next_agent = None
    
    def handle(self, task):
        if self.can_handle(task):
            return self.execute_task(task)
        elif self.next_agent:
            return self.next_agent.handle(task)
        else:
            return {"error": f"No agent can handle: {task[:50]}..."}
```

### 4. **Strategy Pattern** - LLM Provider Selection
```python
# providers/base_provider.py
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    def generate_response(self, prompt, **kwargs):
        pass
    
    @abstractmethod
    def get_provider_info(self):
        pass

# providers/implementations/openai_provider.py
class OpenAIProvider(LLMProvider):
    def __init__(self, api_key, model="gpt-4"):
        self.api_key = api_key
        self.model = model
    
    def generate_response(self, prompt, **kwargs):
        # OpenAI API call implementation
        return f"OpenAI response to: {prompt[:50]}..."
    
    def get_provider_info(self):
        return {"provider": "OpenAI", "model": self.model}
```

### 5. **Command Pattern** - Tool System
```python
# tools/base_tool.py
from abc import ABC, abstractmethod

class Tool(ABC):
    @abstractmethod
    def execute(self, parameters):
        pass
    
    @abstractmethod
    def get_tool_info(self):
        pass

class CalculatorTool(Tool):
    def execute(self, parameters):
        expression = parameters.get('expression')
        try:
            result = eval(expression)  # Use safe evaluation in production
            return {"result": result, "success": True}
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def get_tool_info(self):
        return {
            "name": "calculator",
            "description": "Performs mathematical calculations",
            "parameters": ["expression"]
        }
```

## 🚀 Quick Start Guide

### 1. Create Your Agent System
```python
# main.py
from agents.agent_factory import AgentFactory
from providers.llm_factory import LLMProviderFactory
from workflow.chain_manager import AgentChain

# Create your AI agent system
def create_agent_system():
    # Setup LLM provider
    llm_provider = LLMProviderFactory.create_provider("openai")
    
    # Create specialized agents
    code_agent = AgentFactory.create_agent("code", llm_provider)
    research_agent = AgentFactory.create_agent("research", llm_provider)
    
    # Setup agent chain
    chain = AgentChain()
    chain.add_agent(code_agent)
    chain.add_agent(research_agent)
    
    return chain

# Usage
agent_system = create_agent_system()
result = agent_system.handle_request("Write a Python function to sort a list")
print(result)
```

### 2. Configure Your System
```yaml
# config/config.yaml
llm_providers:
  primary: "openai"
  fallback: "anthropic"
  
agents:
  enabled:
    - "code"
    - "research"
    - "writing"
  
tools:
  enabled:
    - "calculator"
    - "web_search"
    - "file_reader"

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

## 🎯 Use Cases

This template is perfect for:

- **Multi-Agent Systems**: Customer service, research assistants, coding helpers
- **Workflow Automation**: Document processing, data analysis pipelines
- **AI-Powered Tools**: Code generation, content creation, data extraction
- **Intelligent Routing**: Request classification and specialized handling

## 🔧 Customization Points

1. **Add New Agents**: Extend `BaseAgent` for domain-specific functionality
2. **New LLM Providers**: Implement `LLMProvider` interface
3. **Custom Tools**: Create new `Tool` implementations
4. **Routing Logic**: Modify `AgentChain` for complex routing rules

## 💡 Pro Tips

- Use the **Observer pattern** to add monitoring and analytics
- Implement **Retry logic** with exponential backoff for reliability
- Add **Caching** to improve performance and reduce costs
- Use **Configuration files** for easy environment switching

Start building your intelligent agent system with proven design patterns! 🚀