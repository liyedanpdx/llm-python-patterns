# Adapter Pattern in LLM Applications

The Adapter pattern bridges incompatible interfaces, making different systems work together seamlessly. In LLM applications, adapters excel at creating unified interfaces across multiple AI providers, handling different API formats, and integrating with legacy systems.

## Why Adapter Pattern for LLM?

LLM applications often need:
- **Multi-provider support**: Integrate OpenAI, Anthropic, Google, Azure, and local models
- **API standardization**: Create consistent interfaces despite different provider APIs
- **Legacy integration**: Connect modern LLM capabilities with existing systems
- **Data format adaptation**: Handle different input/output formats across providers
- **Protocol bridging**: Support REST, GraphQL, gRPC, and WebSocket protocols

## Key LLM Use Cases

### 1. Multi-Provider LLM Adapter
Create a unified interface for different LLM providers:

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import json

class LLMResponse:
    """Standardized response format"""
    def __init__(self, content: str, model: str, usage: Dict[str, int], metadata: Dict[str, Any] = None):
        self.content = content
        self.model = model
        self.usage = usage  # {'input_tokens': int, 'output_tokens': int, 'total_tokens': int}
        self.metadata = metadata or {}

class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> LLMResponse:
        pass
    
    @abstractmethod
    def get_models(self) -> List[str]:
        pass

class OpenAIAdapter(LLMProvider):
    """Adapter for OpenAI API"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.openai.com/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.models = ["gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"]
    
    def generate(self, prompt: str, model: str = "gpt-3.5-turbo", **kwargs) -> LLMResponse:
        """Generate response using OpenAI API format"""
        # Simulate OpenAI API call
        openai_request = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 1000)
        }
        
        # Mock OpenAI response format
        openai_response = {
            "choices": [{"message": {"content": f"OpenAI {model} response to: {prompt[:50]}..."}}],
            "usage": {"prompt_tokens": 20, "completion_tokens": 50, "total_tokens": 70},
            "model": model
        }
        
        # Adapt to standard format
        return LLMResponse(
            content=openai_response["choices"][0]["message"]["content"],
            model=openai_response["model"],
            usage={
                "input_tokens": openai_response["usage"]["prompt_tokens"],
                "output_tokens": openai_response["usage"]["completion_tokens"],
                "total_tokens": openai_response["usage"]["total_tokens"]
            },
            metadata={"provider": "openai", "request": openai_request}
        )
    
    def get_models(self) -> List[str]:
        return self.models

class AnthropicAdapter(LLMProvider):
    """Adapter for Anthropic Claude API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.models = ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"]
    
    def generate(self, prompt: str, model: str = "claude-3-sonnet", **kwargs) -> LLMResponse:
        """Generate response using Anthropic API format"""
        # Simulate Anthropic API call
        anthropic_request = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": kwargs.get("max_tokens", 1000),
            "temperature": kwargs.get("temperature", 0.7)
        }
        
        # Mock Anthropic response format
        anthropic_response = {
            "content": [{"text": f"Claude {model} response to: {prompt[:50]}..."}],
            "usage": {"input_tokens": 18, "output_tokens": 55},
            "model": model
        }
        
        # Adapt to standard format
        return LLMResponse(
            content=anthropic_response["content"][0]["text"],
            model=anthropic_response["model"],
            usage={
                "input_tokens": anthropic_response["usage"]["input_tokens"],
                "output_tokens": anthropic_response["usage"]["output_tokens"],
                "total_tokens": anthropic_response["usage"]["input_tokens"] + anthropic_response["usage"]["output_tokens"]
            },
            metadata={"provider": "anthropic", "request": anthropic_request}
        )
    
    def get_models(self) -> List[str]:
        return self.models

class GoogleGeminiAdapter(LLMProvider):
    """Adapter for Google Gemini API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.models = ["gemini-pro", "gemini-pro-vision", "gemini-ultra"]
    
    def generate(self, prompt: str, model: str = "gemini-pro", **kwargs) -> LLMResponse:
        """Generate response using Google Gemini API format"""
        # Simulate Gemini API call
        gemini_request = {
            "model": f"models/{model}",
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": kwargs.get("temperature", 0.7),
                "maxOutputTokens": kwargs.get("max_tokens", 1000)
            }
        }
        
        # Mock Gemini response format
        gemini_response = {
            "candidates": [{"content": {"parts": [{"text": f"Gemini {model} response to: {prompt[:50]}..."}]}}],
            "usageMetadata": {"promptTokenCount": 15, "candidatesTokenCount": 60, "totalTokenCount": 75},
            "modelVersion": model
        }
        
        # Adapt to standard format
        return LLMResponse(
            content=gemini_response["candidates"][0]["content"]["parts"][0]["text"],
            model=gemini_response["modelVersion"],
            usage={
                "input_tokens": gemini_response["usageMetadata"]["promptTokenCount"],
                "output_tokens": gemini_response["usageMetadata"]["candidatesTokenCount"],
                "total_tokens": gemini_response["usageMetadata"]["totalTokenCount"]
            },
            metadata={"provider": "google", "request": gemini_request}
        )
    
    def get_models(self) -> List[str]:
        return self.models

class UnifiedLLMClient:
    """Unified client that uses adapter pattern to support multiple providers"""
    
    def __init__(self):
        self.providers: Dict[str, LLMProvider] = {}
        self.default_provider = None
    
    def add_provider(self, name: str, provider: LLMProvider, set_as_default: bool = False):
        """Add a new provider adapter"""
        self.providers[name] = provider
        if set_as_default or self.default_provider is None:
            self.default_provider = name
    
    def generate(self, prompt: str, provider: str = None, **kwargs) -> LLMResponse:
        """Generate response using specified or default provider"""
        provider_name = provider or self.default_provider
        
        if provider_name not in self.providers:
            raise ValueError(f"Provider {provider_name} not found. Available: {list(self.providers.keys())}")
        
        return self.providers[provider_name].generate(prompt, **kwargs)
    
    def get_all_models(self) -> Dict[str, List[str]]:
        """Get all available models from all providers"""
        return {name: provider.get_models() for name, provider in self.providers.items()}

# Usage example
def demonstrate_multi_provider_adapter():
    """Demonstrate unified LLM client with multiple providers"""
    
    # Create unified client
    llm_client = UnifiedLLMClient()
    
    # Add different provider adapters
    llm_client.add_provider("openai", OpenAIAdapter("sk-dummy-key"))
    llm_client.add_provider("anthropic", AnthropicAdapter("sk-ant-dummy-key"))
    llm_client.add_provider("google", GoogleGeminiAdapter("google-dummy-key"))
    
    # Use same interface for different providers
    prompt = "Explain quantum computing in simple terms"
    
    for provider_name in llm_client.providers.keys():
        print(f"\n🔄 Using {provider_name.upper()} provider:")
        response = llm_client.generate(prompt, provider=provider_name)
        print(f"📝 Response: {response.content[:100]}...")
        print(f"🎯 Model: {response.model}")
        print(f"📊 Usage: {response.usage}")
        print(f"🏷️ Provider: {response.metadata['provider']}")
    
    # Show all available models
    print(f"\n📋 Available models: {llm_client.get_all_models()}")
```

**Benefits:**
- Seamless provider switching without code changes
- Consistent interface across all LLM providers
- Easy to add new providers
- Centralized configuration and management

### 2. Legacy System Integration Adapter
Connect modern LLM capabilities with existing enterprise systems:

```python
from datetime import datetime
from typing import Dict, Any, Union
import xml.etree.ElementTree as ET

class LegacySystemResponse:
    """Legacy system response format"""
    def __init__(self, status: str, data: Dict[str, Any], message: str = ""):
        self.status = status
        self.data = data
        self.message = message
        self.timestamp = datetime.now()

class XMLLegacySystemAdapter:
    """Adapter for XML-based legacy systems"""
    
    def __init__(self, system_name: str, llm_client: UnifiedLLMClient):
        self.system_name = system_name
        self.llm_client = llm_client
    
    def process_xml_request(self, xml_string: str) -> str:
        """Process XML request from legacy system and return XML response"""
        try:
            # Parse incoming XML
            root = ET.fromstring(xml_string)
            request_type = root.find('type').text
            content = root.find('content').text
            
            # Convert to modern LLM request
            if request_type == "SUMMARIZE":
                prompt = f"Provide a concise summary of the following text:\n\n{content}"
            elif request_type == "ANALYZE":
                prompt = f"Analyze the following content and provide key insights:\n\n{content}"
            elif request_type == "TRANSLATE":
                target_lang = root.find('target_language').text
                prompt = f"Translate the following text to {target_lang}:\n\n{content}"
            else:
                prompt = content
            
            # Get LLM response
            llm_response = self.llm_client.generate(prompt, provider="openai")
            
            # Convert back to XML format
            response_xml = self._create_xml_response(
                "SUCCESS", 
                llm_response.content, 
                {"model": llm_response.model, "tokens": llm_response.usage["total_tokens"]}
            )
            
            return response_xml
        
        except Exception as e:
            return self._create_xml_response("ERROR", str(e), {})
    
    def _create_xml_response(self, status: str, content: str, metadata: Dict[str, Any]) -> str:
        """Create XML response in legacy system format"""
        root = ET.Element("response")
        
        # Status
        status_elem = ET.SubElement(root, "status")
        status_elem.text = status
        
        # Timestamp
        timestamp_elem = ET.SubElement(root, "timestamp")
        timestamp_elem.text = datetime.now().isoformat()
        
        # Content
        content_elem = ET.SubElement(root, "content")
        content_elem.text = content
        
        # Metadata
        metadata_elem = ET.SubElement(root, "metadata")
        for key, value in metadata.items():
            meta_item = ET.SubElement(metadata_elem, key)
            meta_item.text = str(value)
        
        return ET.tostring(root, encoding='unicode')

class SOAPServiceAdapter:
    """Adapter for SOAP-based enterprise services"""
    
    def __init__(self, service_url: str, llm_client: UnifiedLLMClient):
        self.service_url = service_url
        self.llm_client = llm_client
    
    def process_soap_request(self, soap_envelope: str) -> str:
        """Process SOAP request and return SOAP response"""
        # Simplified SOAP processing - in reality would use proper SOAP library
        try:
            # Extract content from SOAP envelope (simplified)
            content_start = soap_envelope.find("<content>") + len("<content>")
            content_end = soap_envelope.find("</content>")
            content = soap_envelope[content_start:content_end]
            
            # Process with LLM
            prompt = f"Process this enterprise request: {content}"
            llm_response = self.llm_client.generate(prompt, provider="anthropic")
            
            # Return SOAP response
            return f"""<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <ProcessResponse>
            <Status>SUCCESS</Status>
            <Result>{llm_response.content}</Result>
            <Metadata>
                <Model>{llm_response.model}</Model>
                <Tokens>{llm_response.usage['total_tokens']}</Tokens>
                <Provider>anthropic</Provider>
            </Metadata>
        </ProcessResponse>
    </soap:Body>
</soap:Envelope>"""
        
        except Exception as e:
            return f"""<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <soap:Fault>
            <faultcode>PROCESSING_ERROR</faultcode>
            <faultstring>{str(e)}</faultstring>
        </soap:Fault>
    </soap:Body>
</soap:Envelope>"""

class DatabaseAdapterLLM:
    """Adapter to connect LLM with database query systems"""
    
    def __init__(self, llm_client: UnifiedLLMClient):
        self.llm_client = llm_client
        self.schema_info = {}
    
    def natural_language_to_sql(self, question: str, schema: str) -> Dict[str, Any]:
        """Convert natural language question to SQL query"""
        prompt = f"""
        Given the following database schema:
        {schema}
        
        Convert this natural language question to a SQL query:
        "{question}"
        
        Respond with only the SQL query, no explanation.
        """
        
        llm_response = self.llm_client.generate(prompt, provider="google")
        
        return {
            "sql_query": llm_response.content.strip(),
            "original_question": question,
            "model_used": llm_response.model,
            "confidence": "high" if "SELECT" in llm_response.content.upper() else "low"
        }
    
    def explain_query_results(self, sql_query: str, results: List[Dict[str, Any]]) -> str:
        """Explain database query results in natural language"""
        prompt = f"""
        SQL Query: {sql_query}
        
        Results: {json.dumps(results, indent=2)}
        
        Explain these query results in natural language, focusing on key insights and patterns.
        """
        
        llm_response = self.llm_client.generate(prompt, provider="openai")
        return llm_response.content

# Usage example
def demonstrate_legacy_integration():
    """Demonstrate legacy system integration with LLM"""
    
    # Setup
    llm_client = UnifiedLLMClient()
    llm_client.add_provider("openai", OpenAIAdapter("sk-dummy-key"))
    llm_client.add_provider("anthropic", AnthropicAdapter("sk-ant-dummy-key"))
    llm_client.add_provider("google", GoogleGeminiAdapter("google-dummy-key"))
    
    # XML Legacy System
    xml_adapter = XMLLegacySystemAdapter("MainframeSystem", llm_client)
    
    xml_request = """<?xml version="1.0"?>
    <request>
        <type>SUMMARIZE</type>
        <content>
            Our company's quarterly report shows significant growth in the AI sector.
            Revenue increased by 45% compared to last quarter, primarily driven by 
            our new machine learning products. Customer satisfaction improved by 23%,
            and we expanded our team by 150 new employees across engineering and sales.
        </content>
    </request>"""
    
    print("🏢 Legacy XML System Request:")
    xml_response = xml_adapter.process_xml_request(xml_request)
    print(f"📤 Response: {xml_response[:200]}...")
    
    # Database Integration
    db_adapter = DatabaseAdapterLLM(llm_client)
    
    schema = """
    CREATE TABLE employees (
        id INT PRIMARY KEY,
        name VARCHAR(100),
        department VARCHAR(50),
        salary DECIMAL(10,2),
        hire_date DATE
    );
    """
    
    question = "What is the average salary of employees in the engineering department?"
    sql_result = db_adapter.natural_language_to_sql(question, schema)
    print(f"\n💾 Database Query Generation:")
    print(f"❓ Question: {question}")
    print(f"🔍 Generated SQL: {sql_result['sql_query']}")
    print(f"🎯 Confidence: {sql_result['confidence']}")
```

**Benefits:**
- Modernizes legacy systems without replacing them
- Provides AI capabilities to existing enterprise infrastructure
- Maintains compatibility with established workflows
- Gradual migration path to modern architectures

### 3. Data Format Adaptation
Handle different data formats and protocols:

```python
from typing import Union, Dict, Any, List
import csv
import io
import json
import yaml

class DataFormatAdapter:
    """Adapter for different data formats in LLM processing"""
    
    def __init__(self, llm_client: UnifiedLLMClient):
        self.llm_client = llm_client
    
    def process_data(self, data: Union[str, Dict, List], 
                    input_format: str, output_format: str,
                    task: str = "analyze") -> Union[str, Dict, List]:
        """Process data with format adaptation"""
        
        # Convert input to standard format
        standardized_data = self._standardize_input(data, input_format)
        
        # Create appropriate prompt based on task
        prompt = self._create_task_prompt(standardized_data, task)
        
        # Get LLM response
        llm_response = self.llm_client.generate(prompt, provider="openai")
        
        # Convert output to requested format
        return self._format_output(llm_response.content, output_format)
    
    def _standardize_input(self, data: Union[str, Dict, List], input_format: str) -> str:
        """Convert input data to standardized string format"""
        if input_format.lower() == "json":
            if isinstance(data, str):
                return data
            return json.dumps(data, indent=2)
        
        elif input_format.lower() == "yaml":
            if isinstance(data, str):
                return data
            return yaml.dump(data, default_flow_style=False)
        
        elif input_format.lower() == "csv":
            if isinstance(data, str):
                return data
            # Convert list of dicts to CSV string
            if isinstance(data, list) and data and isinstance(data[0], dict):
                output = io.StringIO()
                fieldnames = data[0].keys()
                writer = csv.DictWriter(output, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
                return output.getvalue()
        
        elif input_format.lower() == "xml":
            return str(data)  # Assume already XML string
        
        else:
            return str(data)
    
    def _create_task_prompt(self, data: str, task: str) -> str:
        """Create appropriate prompt based on task"""
        task_prompts = {
            "analyze": f"Analyze the following data and provide key insights:\n\n{data}",
            "summarize": f"Provide a concise summary of this data:\n\n{data}",
            "transform": f"Transform this data into a more readable format:\n\n{data}",
            "extract": f"Extract the most important information from this data:\n\n{data}",
            "validate": f"Validate this data and identify any issues or inconsistencies:\n\n{data}"
        }
        return task_prompts.get(task.lower(), f"Process the following data: {data}")
    
    def _format_output(self, content: str, output_format: str) -> Union[str, Dict, List]:
        """Format LLM output to requested format"""
        if output_format.lower() == "json":
            try:
                # Try to extract JSON from response
                if "{" in content and "}" in content:
                    json_start = content.find("{")
                    json_end = content.rfind("}") + 1
                    return json.loads(content[json_start:json_end])
                else:
                    return {"analysis": content}
            except:
                return {"analysis": content, "format_note": "Could not parse as JSON"}
        
        elif output_format.lower() == "yaml":
            return yaml.dump({"analysis": content}, default_flow_style=False)
        
        elif output_format.lower() == "markdown":
            return f"# Analysis Report\n\n{content}\n\n---\n*Generated by LLM*"
        
        else:
            return content

class ProtocolAdapter:
    """Adapter for different communication protocols"""
    
    def __init__(self, llm_client: UnifiedLLMClient):
        self.llm_client = llm_client
    
    def handle_rest_request(self, method: str, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle REST API requests"""
        if method.upper() == "POST" and endpoint == "/analyze":
            prompt = data.get("text", "")
            response = self.llm_client.generate(f"Analyze: {prompt}")
            
            return {
                "status": "success",
                "data": {
                    "analysis": response.content,
                    "model": response.model,
                    "usage": response.usage
                },
                "timestamp": datetime.now().isoformat()
            }
    
    def handle_graphql_request(self, query: str, variables: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle GraphQL requests"""
        # Simplified GraphQL handling
        if "analyze" in query.lower():
            text = variables.get("text", "") if variables else ""
            response = self.llm_client.generate(f"Analyze: {text}")
            
            return {
                "data": {
                    "analyze": {
                        "result": response.content,
                        "metadata": {
                            "model": response.model,
                            "tokens": response.usage["total_tokens"]
                        }
                    }
                }
            }
    
    def handle_websocket_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle WebSocket messages"""
        message_type = message.get("type", "")
        
        if message_type == "generate":
            prompt = message.get("prompt", "")
            response = self.llm_client.generate(prompt)
            
            return {
                "type": "response",
                "id": message.get("id"),
                "data": {
                    "content": response.content,
                    "model": response.model,
                    "usage": response.usage
                }
            }

# Usage example
def demonstrate_data_format_adaptation():
    """Demonstrate data format adaptation"""
    
    # Setup
    llm_client = UnifiedLLMClient()
    llm_client.add_provider("openai", OpenAIAdapter("sk-dummy-key"))
    
    format_adapter = DataFormatAdapter(llm_client)
    
    # JSON input to Markdown output
    json_data = {
        "sales": [
            {"product": "AI Assistant", "revenue": 50000, "growth": 25},
            {"product": "ML Platform", "revenue": 75000, "growth": 40},
            {"product": "Data Analytics", "revenue": 30000, "growth": 15}
        ]
    }
    
    print("📊 JSON to Markdown Analysis:")
    result = format_adapter.process_data(
        json_data, 
        input_format="json", 
        output_format="markdown", 
        task="analyze"
    )
    print(result[:300] + "...")
    
    # CSV input to JSON output
    csv_data = """product,revenue,growth
AI Assistant,50000,25
ML Platform,75000,40
Data Analytics,30000,15"""
    
    print("\n📈 CSV to JSON Analysis:")
    result = format_adapter.process_data(
        csv_data,
        input_format="csv",
        output_format="json",
        task="summarize"
    )
    print(json.dumps(result, indent=2))
```

**Benefits:**
- Seamless data format conversion
- Protocol-agnostic LLM integration
- Flexible input/output handling
- Easy integration with existing systems

## Implementation Advantages

### 1. **Interface Unification**
- Single interface for multiple providers
- Consistent behavior across different systems
- Reduced coupling between client code and providers
- Easy provider switching and A/B testing

### 2. **Legacy System Modernization**
- Gradual modernization without complete replacement
- Maintains existing workflows while adding AI capabilities
- Minimal disruption to established processes
- Cost-effective AI integration

### 3. **Extensibility**
- Easy to add new providers without changing client code
- Support for future LLM providers and protocols
- Pluggable architecture for different data formats
- Backwards compatibility with existing integrations

### 4. **Error Handling and Resilience**
- Centralized error handling across providers
- Graceful degradation when providers fail
- Standardized error responses
- Failover mechanisms between providers

## Real-World Impact

The Adapter pattern in LLM applications provides:
- **Vendor Independence**: Avoid lock-in to specific LLM providers
- **Integration Flexibility**: Connect AI with any existing system
- **Development Efficiency**: Write once, work with any provider
- **Future-Proofing**: Easy adoption of new AI technologies

This pattern is essential for enterprise LLM systems where integration with existing infrastructure and flexibility across providers are critical requirements.