# Python Design Patterns for LLM
Python is an easy-to-use language for hands-on development but may not be as strictly structured as Java or C++ in enforcing coding rules and design patterns.

However, Python has become a powerful partner for LLM development, helping to build modern applications through frameworks such as LangChain, LangGraph, and LangExtract, and playing a significant role in modern application development.

Inspired by the [python-patterns](https://github.com/faif/python-patterns) repo, we aim to implement some fun application achievements using classic design patterns to demonstrate how Python patterns can be applied in LLM projects with simple steps, thereby enhancing the robustness of project building and the clarity of summaries.


## Design Patterns Overview

| Pattern Category | Pattern Name | Documentation | Project Link | LLM Application Focus |
|------------------|--------------|---------------|--------------|----------------------|
| **Behavioral** | Chain of Responsibility | [chain_of_responsibility_cases.md](./index/behavioral/chain_of_responsibility_cases.md) | - | Agent routing, request processing pipelines |
| | Command | - | - | - |
| | Iterator | - | - | - |
| | Mediator | - | - | - |
| | Memento | - | - | - |
| | Observer | - | - | Event-driven AI systems, model monitoring |
| | Strategy | [strategy_cases.md](./index/behavioral/strategy_cases.md) | - | Model selection, prompt strategies |
| | Template Method | [template_method_cases.md](./index/behavioral/template_method_cases.md) | - | AI workflow templates |
| | Visitor | - | - | - |
| **Creational** | Abstract Factory | [abstract_factory_cases.md](./index/creational/abstract_factory_cases.md) | [factory_cases.ipynb](./index/creational/factory_cases.ipynb) | Multi-provider AI clients, agent creation |
| | Builder | [builder.md](./index/creational/builder.md) | - | Prompt building, RAG pipelines, agent construction |
| | Factory | [factory_cases.md](./index/creational/factory_cases.md) | - | Model instantiation, tool creation |
| | Prototype | - | - | - |
| | Singleton | - | - | - |
| **Structural** | Adapter | - | - | API abstraction, model interface unification |
| | Bridge | - | - | - |
| | Composite | - | - | Hierarchical agent systems |
| | Decorator | - | - | LLM enhancement layers, middleware |
| | Facade | - | - | Simplified AI interfaces |
| | Flyweight | - | - | - |
| | Proxy | - | - | Rate limiting, caching, security |
| **Fundamental** | Delegation | - | - | Responsibility delegation, task forwarding |
| **Other** | Blackboard | - | - | Multi-agent knowledge sharing, collaborative reasoning |
| | Graph Search | - | - | AI pathfinding, decision trees, state space exploration |
| | Hierarchical State Machine (HSM) | - | - | Complex AI behavior modeling, state transitions |



## Workshop Projects

### 1. AI Agent Chain: Chain of Responsibility Pattern in Action - [ai_agent_chain_example.ipynb](./ai_agent_chain_example.ipynb)
   
    Notebook demonstrating how to build intelligent AI agent workflows using classic design patterns, similar to LangChain and LangGraph architectures.
   
   **Implemented Patterns:**
   - **Behavioral**: Chain of Responsibility, Strategy, Template Method
   - **Creational**: Abstract Factory (for different agent types)
   - **Structural**: Adapter (for API client abstraction)
   
   **Goal**: Build modular, scalable AI agent systems with proper separation of concerns
   
   **Similar Product Mindset**: LangChain agent workflows, LangGraph state machines, OpenAI Assistant API

## Workshop Project Pattern Mapping

| Workshop Project | Primary Patterns | Secondary Patterns | Focus Area | Link |
|------------------|------------------|-------------------|------------|------|
| AI Agent Chain | Chain of Responsibility, Strategy, Abstract Factory | Template Method, Adapter, Facade | Multi-agent workflows, request routing | [ai_agent_chain_example.ipynb](./workshops/ai_agent_chain_example.ipynb) |
| *Future Project* | - | - | - | - |
| *Future Project* | - | - | - | - |



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