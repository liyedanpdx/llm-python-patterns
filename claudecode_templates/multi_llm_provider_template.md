# Multi-LLM Provider Template

## Claude Code Template for Multi-Provider LLM Integration

This template provides a robust foundation for building applications that support multiple LLM providers with intelligent fallback, cost optimization, and seamless provider switching.

## 🏗️ Project Structure

```
your_multi_llm_project/
├── providers/
│   ├── __init__.py
│   ├── base_provider.py       # Provider interface (Strategy Pattern)
│   ├── factory.py            # Provider creation (Abstract Factory)
│   ├── manager.py            # Provider management and switching
│   └── implementations/
│       ├── openai_provider.py
│       ├── anthropic_provider.py
│       ├── google_provider.py
│       └── local_provider.py
├── core/
│   ├── __init__.py
│   ├── client.py             # Main client (Facade Pattern)
│   ├── router.py             # Request routing logic
│   └── fallback.py           # Fallback handling
├── config/
│   ├── __init__.py
│   ├── settings.py           # Configuration management
│   ├── provider_configs.py   # Provider-specific settings
│   └── environments/
│       ├── development.yaml
│       ├── production.yaml
│       └── testing.yaml
├── utils/
│   ├── __init__.py
│   ├── cost_tracker.py       # Cost monitoring
│   ├── performance_monitor.py # Performance tracking
│   └── retry_handler.py      # Retry logic with backoff
├── examples/
│   ├── basic_usage.py
│   ├── cost_optimization.py
│   └── failover_demo.py
└── main.py                   # Demo application
```

## 🎯 Design Patterns Applied

### 1. **Abstract Factory Pattern** - Provider Families
```python
# providers/factory.py
from abc import ABC, abstractmethod
from .implementations import (
    OpenAIProvider, AnthropicProvider, 
    GoogleProvider, LocalProvider
)

class LLMProviderFactory(ABC):
    @abstractmethod
    def create_llm_client(self):
        pass
    
    @abstractmethod
    def create_embedding_client(self):
        pass

class OpenAIFactory(LLMProviderFactory):
    def __init__(self, api_key, config=None):
        self.api_key = api_key
        self.config = config or {}
    
    def create_llm_client(self):
        return OpenAIProvider(
            api_key=self.api_key,
            model=self.config.get('model', 'gpt-4'),
            **self.config
        )
    
    def create_embedding_client(self):
        return OpenAIEmbeddingProvider(
            api_key=self.api_key,
            model=self.config.get('embedding_model', 'text-embedding-ada-002')
        )

class ProviderFactoryRegistry:
    _factories = {
        'openai': OpenAIFactory,
        'anthropic': AnthropicFactory,
        'google': GoogleFactory,
        'local': LocalFactory
    }
    
    @classmethod
    def create_factory(cls, provider_name, **kwargs):
        if provider_name not in cls._factories:
            raise ValueError(f"Unknown provider: {provider_name}")
        return cls._factories[provider_name](**kwargs)
    
    @classmethod
    def get_available_providers(cls):
        return list(cls._factories.keys())
```

### 2. **Strategy Pattern** - Provider Selection
```python
# providers/base_provider.py
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    def generate_text(self, prompt, **kwargs):
        pass
    
    @abstractmethod
    def get_model_info(self):
        pass
    
    @abstractmethod
    def estimate_cost(self, text):
        pass
    
    @abstractmethod
    def check_availability(self):
        pass

# core/router.py
class LLMRouter:
    def __init__(self, providers, selection_strategy='cost_optimal'):
        self.providers = providers
        self.selection_strategy = selection_strategy
        self.strategies = {
            'cost_optimal': self._select_cheapest,
            'performance': self._select_fastest,
            'quality': self._select_highest_quality,
            'availability': self._select_most_available
        }
    
    def select_provider(self, prompt, requirements=None):
        \"\"\"Select best provider based on strategy\"\"\"
        strategy_func = self.strategies[self.selection_strategy]
        return strategy_func(prompt, requirements or {})
    
    def _select_cheapest(self, prompt, requirements):
        available_providers = [p for p in self.providers if p.check_availability()]
        if not available_providers:
            raise Exception("No providers available")
        
        costs = [(p, p.estimate_cost(prompt)) for p in available_providers]
        return min(costs, key=lambda x: x[1])[0]
    
    def _select_fastest(self, prompt, requirements):
        # Implementation for fastest provider selection
        pass
```

### 3. **Facade Pattern** - Simplified Interface
```python
# core/client.py
class MultiLLMClient:
    \"\"\"Simplified interface for multi-provider LLM operations\"\"\"
    
    def __init__(self, config_path=None):
        self.config = self._load_config(config_path)
        self.providers = self._initialize_providers()
        self.router = LLMRouter(self.providers)
        self.fallback_handler = FallbackHandler(self.providers)
        self.cost_tracker = CostTracker()
    
    def generate(self, prompt, **kwargs):
        \"\"\"Simple interface for text generation\"\"\"
        try:
            # Select optimal provider
            provider = self.router.select_provider(prompt, kwargs)
            
            # Generate response
            response = provider.generate_text(prompt, **kwargs)
            
            # Track usage
            self.cost_tracker.track_usage(provider, prompt, response)
            
            return response
            
        except Exception as e:
            # Fallback handling
            return self.fallback_handler.handle_failure(prompt, e, **kwargs)
    
    def compare_providers(self, prompt, providers=None):
        \"\"\"Compare multiple providers for the same prompt\"\"\"
        providers = providers or self.providers
        results = {}
        
        for provider in providers:
            try:
                start_time = time.time()
                response = provider.generate_text(prompt)
                end_time = time.time()
                
                results[provider.get_model_info()['name']] = {
                    'response': response,
                    'cost': provider.estimate_cost(prompt),
                    'time': end_time - start_time,
                    'success': True
                }
            except Exception as e:
                results[provider.get_model_info()['name']] = {
                    'error': str(e),
                    'success': False
                }
        
        return results
```

### 4. **Observer Pattern** - Performance Monitoring
```python
# utils/performance_monitor.py
from abc import ABC, abstractmethod

class PerformanceObserver(ABC):
    @abstractmethod
    def on_request_start(self, provider, prompt):
        pass
    
    @abstractmethod
    def on_request_complete(self, provider, prompt, response, duration):
        pass
    
    @abstractmethod
    def on_request_failed(self, provider, prompt, error):
        pass

class CostObserver(PerformanceObserver):
    def __init__(self):
        self.total_costs = {}
    
    def on_request_complete(self, provider, prompt, response, duration):
        provider_name = provider.get_model_info()['name']
        cost = provider.estimate_cost(prompt)
        
        if provider_name not in self.total_costs:
            self.total_costs[provider_name] = 0
        self.total_costs[provider_name] += cost
    
    def get_cost_summary(self):
        return self.total_costs

class PerformanceTracker:
    def __init__(self):
        self.observers = []
    
    def add_observer(self, observer):
        self.observers.append(observer)
    
    def notify_request_start(self, provider, prompt):
        for observer in self.observers:
            observer.on_request_start(provider, prompt)
    
    def notify_request_complete(self, provider, prompt, response, duration):
        for observer in self.observers:
            observer.on_request_complete(provider, prompt, response, duration)
```

### 5. **Command Pattern** - Retry Logic
```python
# utils/retry_handler.py
from abc import ABC, abstractmethod
import time
import random

class RetryCommand(ABC):
    @abstractmethod
    def execute(self):
        pass

class LLMRequestCommand(RetryCommand):
    def __init__(self, provider, prompt, **kwargs):
        self.provider = provider
        self.prompt = prompt
        self.kwargs = kwargs
    
    def execute(self):
        return self.provider.generate_text(self.prompt, **self.kwargs)

class RetryHandler:
    def __init__(self, max_retries=3, base_delay=1.0, max_delay=60.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
    
    def execute_with_retry(self, command):
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                return command.execute()
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries:
                    delay = min(
                        self.base_delay * (2 ** attempt) + random.uniform(0, 1),
                        self.max_delay
                    )
                    time.sleep(delay)
                    continue
                break
        
        raise last_exception
```

## 🚀 Quick Start Guide

### 1. Basic Multi-Provider Setup
```python
# main.py
from core.client import MultiLLMClient

# Initialize client with configuration
client = MultiLLMClient('config/production.yaml')

# Simple usage
response = client.generate("Explain quantum computing in simple terms")
print(response)

# Provider comparison
comparison = client.compare_providers(
    "Write a Python function to sort a list",
    providers=['openai', 'anthropic', 'google']
)
print(comparison)
```

### 2. Cost Optimization Example
```python
# examples/cost_optimization.py
from core.client import MultiLLMClient
from utils.cost_tracker import CostTracker

client = MultiLLMClient()
client.router.selection_strategy = 'cost_optimal'

# Cost-sensitive requests
budget_queries = [
    "What's the weather like?",
    "Translate 'hello' to French",
    "Define machine learning"
]

total_cost = 0
for query in budget_queries:
    response = client.generate(query)
    cost = client.cost_tracker.get_last_request_cost()
    total_cost += cost
    print(f"Query: {query}")
    print(f"Cost: ${cost:.4f}")
    print(f"Response: {response[:100]}...")
    print("-" * 50)

print(f"Total cost: ${total_cost:.4f}")
```

### 3. Failover Configuration
```yaml
# config/production.yaml
providers:
  primary: "openai"
  fallback_chain: ["anthropic", "google", "local"]
  
routing:
  strategy: "cost_optimal"
  consider_availability: true
  consider_performance: true

retry:
  max_attempts: 3
  base_delay: 1.0
  max_delay: 60.0
  
monitoring:
  track_costs: true
  track_performance: true
  log_failures: true
```

## 🎯 Use Cases

This template is perfect for:

- **Cost-Sensitive Applications**: Automatically choose cheapest providers
- **High-Availability Systems**: Seamless failover between providers  
- **A/B Testing**: Compare provider performance and quality
- **Load Balancing**: Distribute requests across multiple providers
- **Vendor Risk Management**: Avoid single-provider dependency

## 🔧 Advanced Features

### Environment-Based Configuration
```python
# Different providers for different environments
environments = {
    'development': {'primary': 'local', 'fallback': ['openai']},
    'staging': {'primary': 'google', 'fallback': ['openai', 'anthropic']},
    'production': {'primary': 'openai', 'fallback': ['anthropic', 'google']}
}
```

### Custom Selection Strategies
```python
# Add your own selection logic
def custom_strategy(providers, prompt, requirements):
    # Your custom logic here
    if requirements.get('domain') == 'medical':
        return providers['anthropic']  # Preferred for safety-critical
    elif len(prompt) > 10000:
        return providers['google']     # Good for long context
    else:
        return providers['openai']     # Default choice
```

## 💡 Pro Tips

- **Monitor Costs**: Set up alerts for unexpected cost spikes
- **Cache Responses**: Implement caching for repeated queries
- **Rate Limiting**: Respect provider rate limits
- **Graceful Degradation**: Always have a fallback plan
- **Performance Testing**: Regularly test provider performance

Build robust, cost-effective multi-LLM applications with confidence! 🚀