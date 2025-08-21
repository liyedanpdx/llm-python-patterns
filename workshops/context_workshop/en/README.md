# 🔧 Python Context Manager Workshop

## 📚 Introduction

This workshop teaches you to master Python Context Manager core concepts and practical techniques through 9 progressive modules, specifically designed for LLM application development.

1. [Basic Concepts](./context_workshop/en/01_basic_concepts.py)
2. [LLM Session Manager](./context_workshop/en/02_llm_session_manager.py)
3. [Async Manager](./context_workshop/en/03_async_manager.py)
4. [Smart Session](./context_workshop/en/04_smart_session.py)
5. [Nested Managers](./context_workshop/en/05_nested_managers.py)
6. [MCP Implementation](./context_workshop/en/06_mcp_implementation.md)
7. [AsyncExitStack vs @asynccontextmanager](./context_workshop/en/07_asyncexitstack_vs_asynccontextmanager.py)
8. [Local MCP Integration](./context_workshop/en/08_local_mcp_integration.py)
9. [Design Patterns Analysis](./context_workshop/en/09_design_patterns_analysis.md)

## 🎯 Learning Path

### 01. Basic Concepts (`01_basic_concepts.py`)
- Context Manager fundamentals and working principles
- `@contextmanager` decorator usage
- setup -> use -> cleanup pattern
- Basic timer and temporary configuration examples

**Run:** `python 01_basic_concepts.py`

### 02. LLM Session Manager (`02_llm_session_manager.py`)
- LLM session lifecycle management
- Token calculation and cost tracking
- Exception handling and state recovery
- Production-grade application examples

**Run:** `python 02_llm_session_manager.py`

### 03. Async Manager (`03_async_manager.py`)
- `@asynccontextmanager` usage
- GPU resource pool management
- Async LLM session processing
- Concurrent task coordination

**Run:** `python 03_async_manager.py`

### 04. Smart Session (`04_smart_session.py`)
- `contextvars` global state management
- Automatic session awareness mechanism
- No need to manually pass parameters
- Inspired by llamabot project

**Run:** `python 04_smart_session.py`

### 05. Nested Managers (`05_nested_managers.py`)
- Multi-layer Context Manager nesting
- Budget control + performance monitoring + session management
- Enterprise-grade system resource management
- Best practices for complex scenarios

**Run:** `python 05_nested_managers.py`

### 06. MCP Implementation (`06_mcp_implementation.md`)
- Model Context Protocol detailed analysis
- Enterprise-grade AI context management standards
- Multi-transport layer support (stdio/SSE/WebSocket)
- Advanced AsyncExitStack resource management patterns
- Comparison analysis with llamabot and OpenAI SDK

**Read:** View `06_mcp_implementation.md` document

### 07. AsyncExitStack vs @asynccontextmanager (`07_asyncexitstack_vs_asynccontextmanager.py`)
- Detailed comparison of two async context management approaches
- Single resource vs multiple resource management
- Dynamic resource management and error handling
- Best practices for combined usage

**Run:** `python 07_asyncexitstack_vs_asynccontextmanager.py`

### 08. Local MCP Integration (`08_local_mcp_integration.py`)
- Real scenarios for local integration of multiple MCP services
- Service orchestration for development and production environments
- Necessity of Context Manager in MCP integration
- Bad example vs good example comparison

**Run:** `python 08_local_mcp_integration.py`

### 09. Design Patterns Analysis (`09_design_patterns_analysis.md`)
- In-depth analysis of design patterns embodied in Context Manager
- Template Method, Builder, Composite and other pattern synergies
- Pattern application value in enterprise-grade architectures
- Design philosophy and practical guidance for multi-pattern collaboration

**Read:** View `09_design_patterns_analysis.md` document

## 🚀 Quick Start

```bash
# Clone project
cd workshops/context_workshop

# Run all modules in sequence
python 01_basic_concepts.py
python 02_llm_session_manager.py
python 03_async_manager.py
python 04_smart_session.py
python 05_nested_managers.py
```

## 💡 Real Application Scenarios

- **File Operations**: `with open() as f`
- **Database Connections**: Session management and transaction control
- **LLM API Calls**: Cost tracking and session management
- **GPU Resources**: Async resource pool management
- **Temporary Configurations**: Test environment configuration switching
- **Performance Monitoring**: Automatic timing and resource statistics

## 🔗 Related Projects

- **llamabot**: Uses PromptRecorder Context Manager to automatically record LLM conversations
- **OpenAI Agents SDK**: RunContextWrapper manages LLM runtime context
- **Model Context Protocol (MCP)**: Anthropic's open standard for enterprise AI context management
- **FastMCP**: Python framework for simplifying MCP server development

## ✅ Key Points

1. **Context Manager** ensures proper resource acquisition and release
2. **yield statement** separates setup and cleanup phases
3. **finally block** guarantees cleanup code execution
4. **Async support** suitable for high-concurrency and resource-intensive scenarios
5. **contextvars** enables global state awareness and automatic context passing
6. **Nested composition** provides powerful multi-layer resource management capabilities
7. **MCP protocol** standardized enterprise-grade AI context management solution
8. **Design pattern synergy** Context Manager is a typical example of elegant combination of multiple design patterns

These patterns are widely used in production by well-known projects like llamabot, OpenAI SDK, and Model Context Protocol!

## 🎯 Design Pattern Essence

Context Manager embodies the collaborative application of multiple classic design patterns:

- **Template Method** - Defines fixed resource management algorithm skeleton (Setup → Use → Cleanup)
- **Builder Pattern** - AsyncExitStack progressively builds complex resource structures
- **Composite Pattern** - Nested structures form hierarchical resource management trees
- **Facade Pattern** - Provides simplified unified interfaces for complex subsystems
- **Strategy Pattern** - Different resource management strategies for different scenarios
- **Observer Pattern** - Monitors and observes resource usage status
- **Factory Pattern** - Dynamically creates appropriate resource managers

This **multi-pattern synergy** design philosophy is the core concept of modern enterprise software architecture!