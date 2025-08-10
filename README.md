# python-pattern-playbook
Python is a language very easy for hands-on but may not be structured like Java or C++ to give us strict rules for coding and design patterns. Inspired by the [python-patterns](https://github.com/faif/python-patterns) repo, we would like to implement some fun application achievements using design patterns directly in real-life projects to show their value in practical small projects.

Furthermore, Python is still a very strong language to cooperate with AI/LLM to help build modern applications by using frameworks like Langchain, Langgraph, Langextract, etc. So, how could we combine them together to give us a showcase of how a modern Python-based AI system should look like? I would also like to update once I meet in development.

## Update Index

1. **AI Agent Chain: Chain of Responsibility Pattern in Action** - [ai_agent_chain_example.ipynb](./ai_agent_chain_example.ipynb)
   
    Notebook demonstrating how to build intelligent AI agent workflows using classic design patterns, similar to LangChain and LangGraph architectures.
   
   **Implemented Patterns:**
   - **Behavioral**: Chain of Responsibility, Strategy, Template Method
   - **Creational**: Abstract Factory (for different agent types)
   - **Structural**: Adapter (for API client abstraction)
   
   **Goal**: Build modular, scalable AI agent systems with proper separation of concerns
   
   **Similar Product Mindset**: LangChain agent workflows, LangGraph state machines, OpenAI Assistant API



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