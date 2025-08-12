# Decorator Pattern in LLM Applications

The Decorator pattern wraps objects to add new functionality without changing their core implementation. In LLM applications, decorators excel at adding cross-cutting concerns like caching, retry logic, monitoring, and cost tracking.

## Why Decorator Pattern for LLM?

LLM applications often need:
- **Response caching**: Store expensive API calls to reduce costs and latency
- **Retry mechanisms**: Handle API failures gracefully with exponential backoff
- **Cost tracking**: Monitor spending across different providers and models
- **Performance monitoring**: Track response times and success rates
- **Rate limiting**: Control API call frequency to avoid quota issues

## Key LLM Use Cases

### 1. Response Caching Strategy
Cache LLM responses to improve performance and reduce costs:

```python
import functools
import hashlib
import json
from typing import Dict, Any, Optional

class LLMCache:
    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.max_size = max_size
        self.ttl = ttl  # Time to live in seconds
    
    def _generate_key(self, *args, **kwargs) -> str:
        """Generate cache key from function arguments"""
        key_data = {'args': str(args), 'kwargs': kwargs}
        return hashlib.md5(json.dumps(key_data, sort_keys=True).encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached value if exists and not expired"""
        if key in self.cache:
            entry = self.cache[key]
            if time.time() - entry['timestamp'] < self.ttl:
                return entry['value']
            else:
                del self.cache[key]  # Remove expired entry
        return None
    
    def set(self, key: str, value: Any):
        """Set cache value with timestamp"""
        if len(self.cache) >= self.max_size:
            # Remove oldest entry
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k]['timestamp'])
            del self.cache[oldest_key]
        
        self.cache[key] = {
            'value': value,
            'timestamp': time.time()
        }

def cache_llm_response(cache_instance: Optional[LLMCache] = None):
    """Decorator to cache LLM responses"""
    if cache_instance is None:
        cache_instance = LLMCache()
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = cache_instance._generate_key(*args, **kwargs)
            
            # Check cache first
            cached_result = cache_instance.get(cache_key)
            if cached_result is not None:
                print(f"🎯 Cache hit! Saved API call")
                return cached_result
            
            # Call original function
            print(f"🌐 Making API call...")
            result = func(*args, **kwargs)
            
            # Store in cache
            cache_instance.set(cache_key, result)
            print(f"💾 Response cached")
            
            return result
        
        wrapper.cache = cache_instance  # Expose cache for debugging
        return wrapper
    return decorator

# Usage example
@cache_llm_response()
def call_llm(prompt: str, model: str = "gpt-4") -> str:
    # Simulate expensive LLM API call
    time.sleep(2)  # Simulate network delay
    return f"Response to: {prompt[:50]}..."
```

**Benefits:**
- Significant cost reduction for repeated queries
- Improved response times for cached content
- Reduced API quota usage
- Better user experience with faster responses

### 2. Retry and Resilience Decorator
Handle API failures with intelligent retry logic:

```python
import time
import random
from functools import wraps

def retry_llm_call(max_attempts: int = 3, base_delay: float = 1.0, 
                   max_delay: float = 60.0, backoff_factor: float = 2.0):
    """Decorator to retry LLM calls with exponential backoff"""
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                
                except Exception as e:
                    last_exception = e
                    
                    if attempt == max_attempts - 1:
                        # Last attempt failed
                        print(f"❌ All {max_attempts} attempts failed")
                        raise last_exception
                    
                    # Calculate delay with exponential backoff
                    delay = min(max_delay, base_delay * (backoff_factor ** attempt))
                    jitter = random.uniform(0, 0.1) * delay  # Add jitter
                    total_delay = delay + jitter
                    
                    print(f"⚠️ Attempt {attempt + 1} failed: {str(e)[:50]}...")
                    print(f"🔄 Retrying in {total_delay:.2f} seconds...")
                    time.sleep(total_delay)
            
            raise last_exception
        
        return wrapper
    return decorator

# Usage example
@retry_llm_call(max_attempts=3, base_delay=1.0)
@cache_llm_response()
def reliable_llm_call(prompt: str) -> str:
    # Simulate potentially failing API call
    if random.random() < 0.3:  # 30% failure rate
        raise Exception("API temporarily unavailable")
    return f"Successful response to: {prompt}"
```

**Benefits:**
- Automatic recovery from transient failures
- Exponential backoff prevents API overwhelming
- Configurable retry policies per use case
- Maintains service reliability despite API issues

### 3. Cost Tracking Decorator
Monitor and control LLM spending:

```python
from datetime import datetime
from typing import Dict, List

class CostTracker:
    def __init__(self):
        self.costs: List[Dict[str, Any]] = []
        self.total_cost = 0.0
        
        # Pricing per 1K tokens (example prices)
        self.model_prices = {
            'gpt-4': {'input': 0.03, 'output': 0.06},
            'gpt-3.5-turbo': {'input': 0.001, 'output': 0.002},
            'claude-3-opus': {'input': 0.015, 'output': 0.075},
            'gemini-pro': {'input': 0.0005, 'output': 0.0015}
        }
    
    def estimate_tokens(self, text: str) -> int:
        """Rough token estimation (4 characters ≈ 1 token)"""
        return max(1, len(text) // 4)
    
    def calculate_cost(self, model: str, input_text: str, output_text: str) -> float:
        """Calculate cost for LLM call"""
        if model not in self.model_prices:
            return 0.0  # Unknown model
        
        prices = self.model_prices[model]
        input_tokens = self.estimate_tokens(input_text)
        output_tokens = self.estimate_tokens(output_text)
        
        cost = (input_tokens / 1000 * prices['input'] + 
                output_tokens / 1000 * prices['output'])
        return round(cost, 6)
    
    def add_cost(self, model: str, input_text: str, output_text: str):
        """Add cost entry"""
        cost = self.calculate_cost(model, input_text, output_text)
        self.total_cost += cost
        
        self.costs.append({
            'timestamp': datetime.now(),
            'model': model,
            'input_tokens': self.estimate_tokens(input_text),
            'output_tokens': self.estimate_tokens(output_text),
            'cost': cost
        })
    
    def get_summary(self) -> Dict[str, Any]:
        """Get cost summary"""
        if not self.costs:
            return {'total_cost': 0, 'total_calls': 0}
        
        return {
            'total_cost': round(self.total_cost, 4),
            'total_calls': len(self.costs),
            'average_cost': round(self.total_cost / len(self.costs), 4),
            'most_expensive_model': max(set(entry['model'] for entry in self.costs),
                                      key=lambda m: sum(e['cost'] for e in self.costs if e['model'] == m))
        }

def track_llm_cost(cost_tracker: CostTracker, model: str = "gpt-4"):
    """Decorator to track LLM costs"""
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract input from arguments
            input_text = str(args[0]) if args else str(kwargs.get('prompt', ''))
            
            # Call original function
            result = func(*args, **kwargs)
            
            # Track cost
            output_text = str(result)
            cost_tracker.add_cost(model, input_text, output_text)
            
            # Show cost info
            cost = cost_tracker.calculate_cost(model, input_text, output_text)
            print(f"💰 Cost: ${cost:.4f} | Total: ${cost_tracker.total_cost:.4f}")
            
            return result
        
        return wrapper
    return decorator

# Usage example
cost_tracker = CostTracker()

@track_llm_cost(cost_tracker, model="gpt-4")
@cache_llm_response()
def cost_aware_llm_call(prompt: str) -> str:
    return f"Processed: {prompt[:30]}... [Response length: 150 tokens]"
```

**Benefits:**
- Real-time cost monitoring
- Budget control and alerts
- Cost optimization insights
- Spending transparency across models

### 4. Performance Monitoring Decorator
Track response times and success rates:

```python
import time
from collections import defaultdict
from statistics import mean

class PerformanceMonitor:
    def __init__(self):
        self.metrics = defaultdict(list)
        self.success_count = 0
        self.failure_count = 0
    
    def record_call(self, duration: float, success: bool, model: str):
        """Record performance metrics"""
        self.metrics[model].append(duration)
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        total_calls = self.success_count + self.failure_count
        
        model_stats = {}
        for model, durations in self.metrics.items():
            if durations:
                model_stats[model] = {
                    'calls': len(durations),
                    'avg_duration': round(mean(durations), 3),
                    'min_duration': round(min(durations), 3),
                    'max_duration': round(max(durations), 3)
                }
        
        return {
            'total_calls': total_calls,
            'success_rate': round((self.success_count / total_calls) * 100, 2) if total_calls > 0 else 0,
            'model_performance': model_stats
        }

def monitor_performance(monitor: PerformanceMonitor, model: str = "default"):
    """Decorator to monitor LLM performance"""
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            success = False
            
            try:
                result = func(*args, **kwargs)
                success = True
                return result
            
            except Exception as e:
                success = False
                raise
            
            finally:
                duration = time.time() - start_time
                monitor.record_call(duration, success, model)
                
                if success:
                    print(f"⚡ Call completed in {duration:.3f}s")
                else:
                    print(f"💥 Call failed after {duration:.3f}s")
        
        return wrapper
    return decorator

# Usage example
performance_monitor = PerformanceMonitor()

@monitor_performance(performance_monitor, model="gpt-4")
@track_llm_cost(cost_tracker, model="gpt-4")
@retry_llm_call(max_attempts=2)
@cache_llm_response()
def full_featured_llm_call(prompt: str) -> str:
    """LLM call with all decorators applied"""
    time.sleep(random.uniform(0.5, 2.0))  # Simulate variable response time
    return f"Enhanced response to: {prompt}"
```

**Benefits:**
- Performance bottleneck identification
- SLA compliance monitoring
- Model comparison insights
- System health tracking

## Implementation Advantages

### 1. **Separation of Concerns**
- Core LLM logic remains clean and focused
- Cross-cutting concerns handled separately
- Easy to enable/disable features per environment
- Independent testing of each concern

### 2. **Composability**
- Stack multiple decorators for comprehensive functionality
- Order-dependent behavior (cache before retry, monitor everything)
- Mix and match based on requirements
- Reusable across different LLM functions

### 3. **Transparency**
- Original function interface unchanged
- Callers unaware of decorator enhancements
- Easy migration from basic to enhanced functions
- Backward compatibility maintained

### 4. **Configuration Flexibility**
- Runtime decorator configuration
- Environment-specific behavior
- A/B testing different decorator combinations
- Dynamic feature toggling

## Real-World Impact

The Decorator pattern in LLM applications provides:
- **Cost Savings**: Caching reduces API calls by 30-70% in typical applications
- **Reliability**: Retry mechanisms improve success rates from 95% to 99.9%
- **Performance**: Cached responses serve in milliseconds vs seconds
- **Observability**: Complete visibility into LLM usage patterns and costs

This pattern is essential for production LLM systems where reliability, performance, and cost control are critical requirements.