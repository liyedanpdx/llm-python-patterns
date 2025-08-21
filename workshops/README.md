# 🎓 Interactive Learning Workshops

This directory contains hands-on workshop series designed to provide practical, interactive learning experiences with Python design patterns in LLM applications.

## 📚 Available Workshops

### 🔧 [Python Context Manager Workshop](./context_workshop/)
**Status**: ✅ Completed (2025-08-21)  
**Modules**: 8 comprehensive modules  
**Focus**: Enterprise-grade resource management for LLM applications

A complete workshop series covering Context Manager mastery from basic concepts to enterprise-grade implementations:

1. **[Basic Concepts](./context_workshop/01_basic_concepts.py)** - Core `@contextmanager` usage
2. **[LLM Session Manager](./context_workshop/02_llm_session_manager.py)** - Production session management
3. **[Async Manager](./context_workshop/03_async_manager.py)** - `@asynccontextmanager` concurrency
4. **[Smart Session](./context_workshop/04_smart_session.py)** - `contextvars` global state
5. **[Nested Managers](./context_workshop/05_nested_managers.py)** - Multi-layer orchestration
6. **[MCP Implementation](./context_workshop/06_mcp_implementation.md)** - Model Context Protocol analysis
7. **[AsyncExitStack vs @asynccontextmanager](./context_workshop/07_asyncexitstack_vs_asynccontextmanager.py)** - Advanced comparison
8. **[Local MCP Integration](./context_workshop/08_local_mcp_integration.py)** - Real-world scenarios

**Key Learnings:**
- Context Manager is essential for enterprise LLM applications
- `AsyncExitStack` enables complex multi-resource management
- MCP protocol requires sophisticated resource orchestration
- Production-ready error handling and cleanup strategies

### 🤖 [AI Agent Chain Workshop](./ai_agent_chain_workshop.md)
Multi-agent systems using Chain of Responsibility pattern, featuring LangGraph-style SubGraph architecture.

### 🔄 [JSON Schema Factory Workshop](./json_schema_factory_workshop.md)  
Structured LLM output control using Factory pattern with Pydantic validation across multiple providers.