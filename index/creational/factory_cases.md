# Factory Pattern in LLM Applications

The Factory pattern is essential for LLM applications that need to create different types of objects based on runtime conditions, such as selecting AI models, creating specialized tools, or instantiating different processing pipelines.

## Why Factory Pattern for LLM?

LLM applications often require:
- **Dynamic object creation**: Choose specific implementations based on runtime conditions
- **Decoupled instantiation**: Separate object creation from object usage
- **Configuration-driven creation**: Create objects based on user preferences or system settings
- **Easy extensibility**: Add new implementations without modifying existing code

## Key LLM Use Cases

### 1. AI Model Factory
Creating different AI models based on requirements:

```python
from abc import ABC, abstractmethod
from enum import Enum

class ModelType(Enum):
    FAST = "fast"
    BALANCED = "balanced" 
    ADVANCED = "advanced"
    SPECIALIZED = "specialized"

class AIModel(ABC):
    @abstractmethod
    def generate(self, prompt, **kwargs):
        pass
    
    @abstractmethod
    def get_model_info(self):
        pass

class FastModel(AIModel):
    def __init__(self):
        self.model_name = "gpt-3.5-turbo"
        self.max_tokens = 1000
        self.cost_per_token = 0.002
    
    def generate(self, prompt, **kwargs):
        # Fast, lightweight model for simple queries
        return f"Fast response to: {prompt}"
    
    def get_model_info(self):
        return {
            "name": self.model_name,
            "speed": "high",
            "cost": "low",
            "quality": "good"
        }

class BalancedModel(AIModel):
    def __init__(self):
        self.model_name = "gpt-4"
        self.max_tokens = 2000
        self.cost_per_token = 0.03
    
    def generate(self, prompt, **kwargs):
        # Balanced model for general use
        return f"Balanced response to: {prompt}"
    
    def get_model_info(self):
        return {
            "name": self.model_name,
            "speed": "medium",
            "cost": "medium", 
            "quality": "high"
        }

class AdvancedModel(AIModel):
    def __init__(self):
        self.model_name = "gpt-4-turbo"
        self.max_tokens = 4000
        self.cost_per_token = 0.06
    
    def generate(self, prompt, **kwargs):
        # Most capable model for complex tasks
        return f"Advanced response to: {prompt}"
    
    def get_model_info(self):
        return {
            "name": self.model_name,
            "speed": "low",
            "cost": "high",
            "quality": "excellent"
        }

class SpecializedModel(AIModel):
    def __init__(self, domain):
        self.domain = domain
        self.model_name = f"specialized-{domain}-model"
        self.max_tokens = 2000
    
    def generate(self, prompt, **kwargs):
        return f"Specialized {self.domain} response to: {prompt}"
    
    def get_model_info(self):
        return {
            "name": self.model_name,
            "domain": self.domain,
            "quality": "domain-optimized"
        }

class AIModelFactory:
    @staticmethod
    def create_model(model_type: ModelType, **kwargs):
        """Factory method to create AI models based on type"""
        if model_type == ModelType.FAST:
            return FastModel()
        elif model_type == ModelType.BALANCED:
            return BalancedModel()
        elif model_type == ModelType.ADVANCED:
            return AdvancedModel()
        elif model_type == ModelType.SPECIALIZED:
            domain = kwargs.get('domain', 'general')
            return SpecializedModel(domain)
        else:
            raise ValueError(f"Unknown model type: {model_type}")
    
    @staticmethod
    def create_model_by_requirements(requirements):
        """Create model based on specific requirements"""
        if requirements.get('speed_priority', False):
            return AIModelFactory.create_model(ModelType.FAST)
        elif requirements.get('cost_sensitive', False):
            return AIModelFactory.create_model(ModelType.FAST)
        elif requirements.get('quality_priority', False):
            return AIModelFactory.create_model(ModelType.ADVANCED)
        elif requirements.get('domain'):
            return AIModelFactory.create_model(
                ModelType.SPECIALIZED, 
                domain=requirements['domain']
            )
        else:
            return AIModelFactory.create_model(ModelType.BALANCED)

# Usage examples
def handle_user_query(query, user_preferences):
    # Create appropriate model based on user preferences
    model = AIModelFactory.create_model_by_requirements(user_preferences)
    response = model.generate(query)
    return response, model.get_model_info()

# Different usage scenarios
urgent_response = handle_user_query(
    "Quick math question", 
    {"speed_priority": True}
)

research_response = handle_user_query(
    "Complex analysis needed",
    {"quality_priority": True}
)

medical_response = handle_user_query(
    "Medical consultation",
    {"domain": "medical"}
)
```

**Benefits:**
- Dynamic model selection based on requirements
- Easy addition of new models
- Centralized model creation logic
- Requirement-based intelligent selection

### 2. Tool Factory for AI Agents
Creating different tools for AI agents based on needs:

```python
class AITool(ABC):
    @abstractmethod
    def execute(self, input_data):
        pass
    
    @abstractmethod
    def get_tool_info(self):
        pass

class CalculatorTool(AITool):
    def execute(self, expression):
        try:
            # Safe evaluation of mathematical expressions
            result = eval(expression)  # In production, use ast.literal_eval or safer methods
            return {"result": result, "success": True}
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def get_tool_info(self):
        return {
            "name": "calculator",
            "description": "Performs mathematical calculations",
            "input_type": "mathematical_expression"
        }

class WebSearchTool(AITool):
    def execute(self, query):
        # Simulate web search
        return {
            "results": [
                f"Web result 1 for: {query}",
                f"Web result 2 for: {query}",
                f"Web result 3 for: {query}"
            ],
            "success": True
        }
    
    def get_tool_info(self):
        return {
            "name": "web_search",
            "description": "Searches the internet for information",
            "input_type": "search_query"
        }

class CodeExecutorTool(AITool):
    def execute(self, code):
        # Simulate code execution (in production, use sandboxed environment)
        return {
            "output": f"Executed: {code[:50]}...",
            "success": True
        }
    
    def get_tool_info(self):
        return {
            "name": "code_executor",
            "description": "Executes code in a sandboxed environment",
            "input_type": "code"
        }

class FileReaderTool(AITool):
    def execute(self, file_path):
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            return {"content": content, "success": True}
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def get_tool_info(self):
        return {
            "name": "file_reader",
            "description": "Reads content from files",
            "input_type": "file_path"
        }

class ToolFactory:
    _tools = {
        "calculator": CalculatorTool,
        "web_search": WebSearchTool,
        "code_executor": CodeExecutorTool,
        "file_reader": FileReaderTool
    }
    
    @classmethod
    def create_tool(cls, tool_name):
        """Create a tool by name"""
        if tool_name in cls._tools:
            return cls._tools[tool_name]()
        else:
            raise ValueError(f"Unknown tool: {tool_name}")
    
    @classmethod
    def create_tools_for_agent_type(cls, agent_type):
        """Create appropriate tools based on agent type"""
        tool_mappings = {
            "math_tutor": ["calculator"],
            "research_assistant": ["web_search", "file_reader"],
            "coding_assistant": ["code_executor", "file_reader"],
            "general_assistant": ["calculator", "web_search", "file_reader"]
        }
        
        tool_names = tool_mappings.get(agent_type, ["calculator"])
        return [cls.create_tool(name) for name in tool_names]
    
    @classmethod
    def register_tool(cls, name, tool_class):
        """Register a new tool type"""
        cls._tools[name] = tool_class
    
    @classmethod
    def get_available_tools(cls):
        """Get list of available tool names"""
        return list(cls._tools.keys())

# Usage in AI Agent
class AIAgent:
    def __init__(self, agent_type):
        self.agent_type = agent_type
        self.tools = ToolFactory.create_tools_for_agent_type(agent_type)
        self.tool_map = {tool.get_tool_info()["name"]: tool for tool in self.tools}
    
    def use_tool(self, tool_name, input_data):
        if tool_name in self.tool_map:
            return self.tool_map[tool_name].execute(input_data)
        else:
            return {"error": f"Tool {tool_name} not available", "success": False}
    
    def get_available_tools(self):
        return [tool.get_tool_info() for tool in self.tools]

# Different agent types with appropriate tools
math_agent = AIAgent("math_tutor")
research_agent = AIAgent("research_assistant")
coding_agent = AIAgent("coding_assistant")
```

**Benefits:**
- Dynamic tool creation based on agent requirements
- Easy registration of new tools
- Type-specific tool sets
- Centralized tool management

### 3. Prompt Template Factory
Creating different prompt templates based on task types:

```python
class PromptTemplate(ABC):
    @abstractmethod
    def format(self, **kwargs):
        pass
    
    @abstractmethod
    def get_required_params(self):
        pass

class QuestionAnsweringTemplate(PromptTemplate):
    def format(self, context, question, **kwargs):
        return f"""
Based on the following context:
{context}

Please answer this question: {question}

Provide a clear and accurate answer based only on the given context.
"""
    
    def get_required_params(self):
        return ["context", "question"]

class CodeGenerationTemplate(PromptTemplate):
    def format(self, task_description, language="Python", **kwargs):
        return f"""
Write {language} code to accomplish the following task:
{task_description}

Requirements:
- Write clean, well-commented code
- Include error handling where appropriate
- Follow {language} best practices

Code:
"""
    
    def get_required_params(self):
        return ["task_description"]

class SummarizationTemplate(PromptTemplate):
    def format(self, text, max_length=200, **kwargs):
        return f"""
Please summarize the following text in approximately {max_length} words:

{text}

Summary:
"""
    
    def get_required_params(self):
        return ["text"]

class TranslationTemplate(PromptTemplate):
    def format(self, text, source_language, target_language, **kwargs):
        return f"""
Translate the following text from {source_language} to {target_language}:

{text}

Translation:
"""
    
    def get_required_params(self):
        return ["text", "source_language", "target_language"]

class ChainOfThoughtTemplate(PromptTemplate):
    def format(self, problem, **kwargs):
        return f"""
Let's solve this step by step:

Problem: {problem}

Step 1: Understand the problem
Step 2: Break it down into smaller parts
Step 3: Solve each part
Step 4: Combine the solutions

Let's begin:
"""
    
    def get_required_params(self):
        return ["problem"]

class PromptTemplateFactory:
    _templates = {
        "qa": QuestionAnsweringTemplate,
        "code_generation": CodeGenerationTemplate,
        "summarization": SummarizationTemplate,
        "translation": TranslationTemplate,
        "chain_of_thought": ChainOfThoughtTemplate
    }
    
    @classmethod
    def create_template(cls, template_type):
        """Create a template by type"""
        if template_type in cls._templates:
            return cls._templates[template_type]()
        else:
            raise ValueError(f"Unknown template type: {template_type}")
    
    @classmethod
    def create_template_by_task(cls, task_description):
        """Auto-select template based on task description"""
        task_lower = task_description.lower()
        
        if "translate" in task_lower:
            return cls.create_template("translation")
        elif "summarize" in task_lower or "summary" in task_lower:
            return cls.create_template("summarization")
        elif "code" in task_lower or "program" in task_lower:
            return cls.create_template("code_generation")
        elif "step" in task_lower or "explain" in task_lower:
            return cls.create_template("chain_of_thought")
        else:
            return cls.create_template("qa")
    
    @classmethod
    def register_template(cls, name, template_class):
        """Register a new template type"""
        cls._templates[name] = template_class

# Usage
class PromptProcessor:
    def process_request(self, task_description, **params):
        # Auto-select appropriate template
        template = PromptTemplateFactory.create_template_by_task(task_description)
        
        # Format the prompt
        formatted_prompt = template.format(**params)
        
        return formatted_prompt, template.get_required_params()

# Examples
processor = PromptProcessor()

# Auto-selects summarization template
summary_prompt, _ = processor.process_request(
    "Please summarize this document",
    text="Long document content here...",
    max_length=150
)

# Auto-selects code generation template  
code_prompt, _ = processor.process_request(
    "Write a Python function to sort a list",
    task_description="Create a function that sorts a list of numbers",
    language="Python"
)
```

**Benefits:**
- Automatic template selection based on task
- Consistent prompt formatting
- Easy template registration and extension
- Parameter validation and requirements

### 4. Evaluation Metric Factory
Creating different evaluation metrics based on task type:

```python
class EvaluationMetric(ABC):
    @abstractmethod
    def calculate(self, predictions, references, **kwargs):
        pass
    
    @abstractmethod
    def get_metric_info(self):
        pass

class AccuracyMetric(EvaluationMetric):
    def calculate(self, predictions, references, **kwargs):
        correct = sum(p == r for p, r in zip(predictions, references))
        total = len(predictions)
        return correct / total if total > 0 else 0
    
    def get_metric_info(self):
        return {
            "name": "accuracy",
            "range": [0, 1],
            "higher_is_better": True
        }

class BleuMetric(EvaluationMetric):
    def calculate(self, predictions, references, **kwargs):
        # Simplified BLEU calculation
        # In practice, use nltk.translate.bleu_score or similar
        scores = []
        for pred, ref in zip(predictions, references):
            # Simple word overlap calculation
            pred_words = set(pred.split())
            ref_words = set(ref.split())
            if len(pred_words) == 0:
                scores.append(0)
            else:
                overlap = len(pred_words.intersection(ref_words))
                scores.append(overlap / len(pred_words))
        
        return sum(scores) / len(scores) if scores else 0
    
    def get_metric_info(self):
        return {
            "name": "bleu",
            "range": [0, 1],
            "higher_is_better": True
        }

class RougeMetric(EvaluationMetric):
    def calculate(self, predictions, references, **kwargs):
        # Simplified ROUGE calculation
        scores = []
        for pred, ref in zip(predictions, references):
            pred_words = pred.split()
            ref_words = ref.split()
            
            if len(ref_words) == 0:
                scores.append(0)
            else:
                overlap = len(set(pred_words).intersection(set(ref_words)))
                scores.append(overlap / len(ref_words))
        
        return sum(scores) / len(scores) if scores else 0
    
    def get_metric_info(self):
        return {
            "name": "rouge",
            "range": [0, 1],
            "higher_is_better": True
        }

class SemanticSimilarityMetric(EvaluationMetric):
    def calculate(self, predictions, references, **kwargs):
        # Simplified semantic similarity using sentence transformers
        # In practice, use actual embedding models
        similarities = []
        for pred, ref in zip(predictions, references):
            # Placeholder for actual semantic similarity calculation
            # This would use embedding models in practice
            word_overlap = len(set(pred.split()).intersection(set(ref.split())))
            max_words = max(len(pred.split()), len(ref.split()))
            similarity = word_overlap / max_words if max_words > 0 else 0
            similarities.append(similarity)
        
        return sum(similarities) / len(similarities) if similarities else 0
    
    def get_metric_info(self):
        return {
            "name": "semantic_similarity",
            "range": [0, 1],
            "higher_is_better": True
        }

class MetricFactory:
    _metrics = {
        "accuracy": AccuracyMetric,
        "bleu": BleuMetric,
        "rouge": RougeMetric,
        "semantic_similarity": SemanticSimilarityMetric
    }
    
    @classmethod
    def create_metric(cls, metric_name):
        """Create a metric by name"""
        if metric_name in cls._metrics:
            return cls._metrics[metric_name]()
        else:
            raise ValueError(f"Unknown metric: {metric_name}")
    
    @classmethod
    def create_metrics_for_task(cls, task_type):
        """Create appropriate metrics based on task type"""
        task_metrics = {
            "classification": ["accuracy"],
            "translation": ["bleu", "semantic_similarity"],
            "summarization": ["rouge", "semantic_similarity"],
            "question_answering": ["accuracy", "semantic_similarity"],
            "text_generation": ["bleu", "rouge", "semantic_similarity"]
        }
        
        metric_names = task_metrics.get(task_type, ["accuracy"])
        return [cls.create_metric(name) for name in metric_names]

# Usage in evaluation system
class EvaluationSystem:
    def __init__(self, task_type):
        self.metrics = MetricFactory.create_metrics_for_task(task_type)
    
    def evaluate(self, predictions, references):
        results = {}
        for metric in self.metrics:
            metric_info = metric.get_metric_info()
            score = metric.calculate(predictions, references)
            results[metric_info["name"]] = {
                "score": score,
                "info": metric_info
            }
        return results

# Task-specific evaluation
translation_eval = EvaluationSystem("translation")
summarization_eval = EvaluationSystem("summarization")
qa_eval = EvaluationSystem("question_answering")
```

**Benefits:**
- Task-appropriate metric selection
- Consistent evaluation interfaces
- Easy metric registration and extension
- Comprehensive evaluation capabilities

## Implementation Advantages

### 1. **Flexibility**
- Runtime object creation based on conditions
- Easy switching between different implementations
- Configuration-driven object instantiation
- Dynamic behavior modification

### 2. **Extensibility**
- Easy addition of new types without modifying existing code
- Registration mechanism for new implementations
- Plugin-like architecture
- Modular component addition

### 3. **Maintainability**
- Centralized creation logic
- Clear separation of concerns
- Consistent object interfaces
- Simplified testing and debugging

### 4. **Scalability**
- Support for numerous object types
- Efficient object creation and management
- Resource optimization through appropriate selection
- Performance tuning through type-specific implementations

## Real-World Impact

The Factory pattern in LLM applications provides:
- **Dynamic Adaptation**: Create appropriate objects based on runtime requirements
- **System Flexibility**: Easy switching between different implementations and configurations
- **Development Efficiency**: Reduced boilerplate code and simplified object management
- **Quality Assurance**: Consistent object creation patterns and validation

This pattern is fundamental for production LLM systems where you need to create different types of objects dynamically based on user requirements, system conditions, or configuration settings while maintaining clean, maintainable code.