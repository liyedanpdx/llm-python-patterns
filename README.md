# LLM Python Patterns
Python is an easy-to-use language for hands-on development but may not be as strictly structured as Java or C++ in enforcing coding rules and design patterns.

However, Python has become a powerful partner for LLM development, helping to build modern applications through frameworks such as LangChain, LangGraph, and LangExtract, and playing a significant role in modern application development.

Inspired by the [python-patterns](https://github.com/faif/python-patterns) repo, this project demonstrates how classic design patterns solve real-world challenges in LLM applications. Through hands-on examples, enterprise case studies, and ready-to-use Claude Code templates, we explore practical implementations that enhance system robustness and maintainability.

We also aspire to enable Claude Code to systematically generate high-quality, pattern-based code by providing comprehensive templates and examples that can be intelligently combined for optimal AI system architecture.

## Design Patterns Overview

| Pattern Category | Pattern Name | Documentation | Project Link | LLM Application Focus |
|------------------|--------------|---------------|--------------|----------------------|
| **Behavioral** | Chain of Responsibility | [chain_of_responsibility_cases.md](./index/behavioral/chain_of_responsibility_cases.md) | - | Agent routing, request processing pipelines |
| | Command | - | - | Tool execution, operation history, undo/redo functionality |
| | Iterator | - | - | - |
| | Mediator | - | - | - |
| | Memento | - | - | - |
| | Observer | - | - | Real-time progress tracking, performance monitoring, cost tracking, system transparency |
| | Strategy | [strategy_cases.md](./index/behavioral/strategy_cases.md) | [strategy_pattern.ipynb](./index/behavioral/strategy_pattern.ipynb) | Multi-provider selection, cost optimization, routing algorithms, analysis algorithms |
| | Template Method | [template_method_cases.md](./index/behavioral/template_method_cases.md) | - | Standardized workflows, document processing pipelines, agent behavior templates |
| | Visitor | - | - | - |
| **Creational** | Abstract Factory | [abstract_factory_cases.md](./index/creational/abstract_factory_cases.md) | [factory_cases.ipynb](./index/creational/factory_cases.ipynb) | Multi-provider AI families, agent ecosystems, tool families |
| | Builder | [builder.md](./index/creational/builder.md) | - | Flexible recommendation systems, complex prompt construction, configurable pipelines |
| | Factory | [factory_cases.md](./index/creational/factory_cases.md) | - | Document parsers, AI provider selection, agent creation, tool instantiation |
| | Prototype | - | - | - |
| | Singleton | - | - | - |
| **Structural** | Adapter | - | - | API format standardization, AI provider integration, document format handling, legacy system integration |
| | Bridge | - | - | - |
| | Composite | - | - | Hierarchical agent systems |
| | Decorator | [decorator_cases.md](./index/structural/decorator_cases.md) | [decorator_pattern.ipynb](./index/structural/decorator_pattern.ipynb) | Response caching, LLM enhancement layers, middleware |
| | Facade | - | - | Unified API interfaces, CLI simplification, complex system abstraction |
| | Flyweight | - | - | - |
| | Proxy | - | - | Access control, rate limiting, caching, security |
| **Fundamental** | Delegation | - | - | Responsibility delegation, task forwarding |
| **Other** | Blackboard | - | - | Multi-agent knowledge sharing, collaborative reasoning |
| | Graph Search | - | - | AI pathfinding, decision trees, state space exploration |
| | Hierarchical State Machine (HSM) | - | - | Complex AI behavior modeling, state transitions |

## Workshop Projects

### 1. AI Agent Chain: Chain of Responsibility Pattern in Action - [ai_agent_chain_example.ipynb](./workshops/ai_agent_chain_example.ipynb)
   
   Notebook demonstrating how to build intelligent AI agent workflows using classic design patterns, similar to LangChain and LangGraph architectures.
   
   **Implemented Patterns:**
   - **Behavioral**: Chain of Responsibility, Strategy, Template Method
   - **Creational**: Abstract Factory (for different agent types)
   - **Structural**: Adapter (for API client abstraction)
   
   **Goal**: Build modular, scalable AI agent systems with proper separation of concerns
   
   **Similar Product Mindset**: LangChain agent workflows, LangGraph state machines, OpenAI Assistant API

### 2. JSON Schema Factory + Pydantic Validation: Structured LLM Output Control - [json_schema_factory_pydantic.ipynb](./workshops/json_schema_factory_pydantic.ipynb)
   
   Workshop showing how to get structured JSON from LLMs using Factory Pattern and Pydantic validation.
   
   **Patterns Used:**
   - Factory Pattern - Choose correct schema based on data type
   - Template Method - Standard prompt generation process
   
   **What it does:**
   - Takes any LLM output and validates it into clean JSON
   - Works with OpenAI, Gemini, Anthropic, or any LLM provider
   - Catches data errors before they enter your application
   - Alternative to OpenAI Function Calling with more control

## Workshop Project Pattern Mapping

| Workshop Project | Primary Patterns | Secondary Patterns | Focus Area | Link |
|------------------|------------------|-------------------|------------|------|
| AI Agent Chain | Chain of Responsibility, Strategy, Abstract Factory | Template Method, Adapter, Facade | Multi-agent workflows, request routing | [ai_agent_chain_example.ipynb](./workshops/ai_agent_chain_example.ipynb) |
| JSON Schema Factory + Pydantic | Factory, Template Method | - | Structured LLM output control, provider-independent validation | [json_schema_factory_pydantic.ipynb](./workshops/json_schema_factory_pydantic.ipynb) |
| *Future Project* | - | - | - | - |

## Enterprise Cases Analysis

Real-world production AI systems from leading companies, analyzing design patterns at enterprise scale.

| Company Project | Primary Patterns | Supporting Patterns | Architecture Focus | Analysis Link | Structure Link |
|-----------------|------------------|--------------------|--------------------|---------------|----------------|
| ByteDance Trae-Agent | Strategy, Command, Factory, Template Method | Observer, Facade, Registry, Configuration | Multi-LLM agent system, production-ready architecture | [bytedance_trae_agent_analysis.md](./cases_analysis/bytedance_trae_agent_analysis.md) | [tree_structure.md](./cases_analysis/tree_structures/bytedance_trae_agent_structure.md) |
| Resume-Matcher | Strategy, Template Method, Factory, Observer | Command, Facade, Builder, Adapter | AI-powered document analysis, privacy-first local processing | [resume_matcher_analysis.md](./cases_analysis/resume_matcher_analysis.md) | [tree_structure.md](./cases_analysis/tree_structures/resume_matcher_structure.md) |
| BerriAI LiteLLM | Adapter, Strategy, Factory, Proxy | Observer, Template Method, Decorator, Command | Enterprise LLM proxy, multi-provider abstraction, cost optimization | [litellm_analysis.md](./cases_analysis/litellm_analysis.md) | [tree_structure.md](./cases_analysis/tree_structures/litellm_structure.md) |
| *Future Analysis* | - | - | - | - | - |

## Claude Code Templates

Ready-to-use project templates for building AI applications with design patterns. Perfect for quickly starting new projects with proven architectural foundations.

| Template Name | Design Patterns Used | Use Case | Template Link |
|---------------|---------------------|----------|---------------|
| AI Agent System | Template Method, Factory, Chain of Responsibility, Strategy, Command | Multi-agent workflows, intelligent task routing, LangChain-style systems | [ai_agent_system_template.md](./claudecode_templates/ai_agent_system_template.md) |
| Multi-LLM Provider | Abstract Factory, Strategy, Facade, Observer, Command | Cost-optimized LLM integration, provider failover, vendor independence | [multi_llm_provider_template.md](./claudecode_templates/multi_llm_provider_template.md) |
| *Future Template* | - | - | - |

## Getting Started with Real LLM Testing

To test LLM in this project, you can  set up free API access:

### 🚀 **Quick Setup for Google AI Studio (Recommended)**
1. **Create Google Cloud Project**: Visit [Google Cloud Platform](https://console.cloud.google.com/) and create a new project
2. **Get Free Credits**: Google provides free credits for new users to test their AI services
3. **Generate API Key**: Go to [Google AI Studio](https://aistudio.google.com/), click "Get API Key" and create a new key
4. **Configure Environment**: 
   - Copy `example.env` to `.env`
   - Replace `YOUR_GEMINI_API_KEY` with your actual API key
   - Run the notebooks for real LLM testing!

### 📝 **Environment Setup**
```bash
# Copy the environment template
cp example.env .env

# Edit .env with your API keys
# The .env file is automatically ignored by git for security
```