# Template Method Pattern in LLM Applications

The Template Method pattern is excellent for LLM applications where you have a common workflow structure but need to customize specific steps for different contexts, models, or domains.

## Why Template Method for LLM?

LLM applications often require:
- **Standardized workflows**: Common processing pipelines with customizable steps
- **Consistent structure**: Maintaining the same overall flow while allowing customization
- **Code reuse**: Shared infrastructure with domain-specific implementations
- **Quality control**: Enforced workflow patterns with flexibility in implementation details

## Key LLM Use Cases

### 1. AI Agent Workflow Template
A common structure for AI agent processing with customizable steps:

```python
from abc import ABC, abstractmethod

class AIAgentTemplate(ABC):
    """Template for AI agent processing workflow"""
    
    def process_request(self, user_input):
        """The template method defining the algorithm structure"""
        # Step 1: Preprocess input
        processed_input = self.preprocess_input(user_input)
        
        # Step 2: Analyze and understand the request
        analysis = self.analyze_request(processed_input)
        
        # Step 3: Generate response using LLM
        response = self.generate_response(analysis)
        
        # Step 4: Post-process and validate response
        final_response = self.postprocess_response(response)
        
        # Step 5: Log and monitor
        self.log_interaction(user_input, final_response)
        
        return final_response
    
    def preprocess_input(self, user_input):
        """Default preprocessing - can be overridden"""
        return user_input.strip().lower()
    
    @abstractmethod
    def analyze_request(self, input_text):
        """Must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def generate_response(self, analysis):
        """Must be implemented by subclasses"""
        pass
    
    def postprocess_response(self, response):
        """Default post-processing - can be overridden"""
        return response
    
    def log_interaction(self, input_text, response):
        """Default logging - can be overridden"""
        print(f"Input: {input_text[:50]}...")
        print(f"Output: {response[:50]}...")

class CodeAssistantAgent(AIAgentTemplate):
    def analyze_request(self, input_text):
        # Analyze if it's a coding question
        return {
            "type": "coding",
            "language": self.detect_language(input_text),
            "complexity": self.assess_complexity(input_text)
        }
    
    def generate_response(self, analysis):
        prompt = f"""
        You are a coding assistant. Help with this {analysis['language']} question.
        Complexity level: {analysis['complexity']}
        
        Question: {analysis['input']}
        
        Provide code examples and explanations.
        """
        return self.llm.generate(prompt)
    
    def detect_language(self, text):
        # Language detection logic
        return "python"  # simplified
    
    def assess_complexity(self, text):
        # Complexity assessment logic
        return "medium"  # simplified

class MathTutorAgent(AIAgentTemplate):
    def analyze_request(self, input_text):
        return {
            "type": "math",
            "topic": self.identify_math_topic(input_text),
            "level": self.assess_difficulty(input_text)
        }
    
    def generate_response(self, analysis):
        prompt = f"""
        You are a math tutor. Help with this {analysis['topic']} problem.
        Difficulty level: {analysis['level']}
        
        Problem: {analysis['input']}
        
        Provide step-by-step solution and explanation.
        """
        return self.llm.generate(prompt)
```

**Benefits:**
- Consistent workflow across different agent types
- Shared infrastructure and logging
- Easy to add new agent types
- Enforced quality control steps

### 2. RAG Pipeline Template
A standardized pipeline for Retrieval-Augmented Generation:

```python
class RAGPipelineTemplate(ABC):
    """Template for RAG processing pipeline"""
    
    def process_query(self, query, document_collection):
        """The template method for RAG processing"""
        # Step 1: Query preprocessing
        processed_query = self.preprocess_query(query)
        
        # Step 2: Document retrieval
        relevant_docs = self.retrieve_documents(processed_query, document_collection)
        
        # Step 3: Context preparation
        context = self.prepare_context(relevant_docs)
        
        # Step 4: Response generation
        response = self.generate_response(processed_query, context)
        
        # Step 5: Response validation and formatting
        final_response = self.format_response(response, relevant_docs)
        
        return final_response
    
    def preprocess_query(self, query):
        """Default query preprocessing"""
        return query.strip()
    
    @abstractmethod
    def retrieve_documents(self, query, documents):
        """Must implement retrieval strategy"""
        pass
    
    @abstractmethod
    def prepare_context(self, documents):
        """Must implement context preparation"""
        pass
    
    @abstractmethod
    def generate_response(self, query, context):
        """Must implement response generation"""
        pass
    
    def format_response(self, response, source_docs):
        """Default response formatting"""
        return {
            "answer": response,
            "sources": [doc.metadata for doc in source_docs]
        }

class ScientificRAG(RAGPipelineTemplate):
    def retrieve_documents(self, query, documents):
        # Scientific paper retrieval with citation importance
        embeddings = self.create_embeddings(query)
        scored_docs = self.semantic_search(embeddings, documents)
        return self.filter_by_citation_count(scored_docs)
    
    def prepare_context(self, documents):
        # Format with paper titles, authors, and abstracts
        context = []
        for doc in documents:
            context.append(f"""
            Paper: {doc.title} by {doc.authors}
            Abstract: {doc.abstract}
            Key findings: {doc.content[:500]}
            """)
        return "\n\n".join(context)
    
    def generate_response(self, query, context):
        prompt = f"""
        Based on these scientific papers:
        {context}
        
        Answer the research question: {query}
        
        Provide a scientifically accurate response with proper citations.
        """
        return self.llm.generate(prompt)

class LegalRAG(RAGPipelineTemplate):
    def retrieve_documents(self, query, documents):
        # Legal document retrieval with jurisdiction focus
        return self.search_with_legal_keywords(query, documents)
    
    def prepare_context(self, documents):
        # Format with case names, statutes, and legal precedents
        context = []
        for doc in documents:
            context.append(f"""
            Case: {doc.case_name}
            Jurisdiction: {doc.jurisdiction}
            Relevant statute: {doc.statute}
            Precedent: {doc.precedent}
            """)
        return "\n\n".join(context)
    
    def generate_response(self, query, context):
        prompt = f"""
        Based on these legal sources:
        {context}
        
        Legal question: {query}
        
        Provide a legal analysis with proper case citations.
        Disclaimer: This is for informational purposes only.
        """
        return self.llm.generate(prompt)
```

**Benefits:**
- Consistent RAG pipeline structure
- Domain-specific customization
- Reusable infrastructure components
- Quality assurance through standardized steps

### 3. Multi-Modal Processing Template
Template for handling different types of input (text, images, audio):

```python
class MultiModalTemplate(ABC):
    """Template for multi-modal AI processing"""
    
    def process_input(self, input_data):
        """Template method for multi-modal processing"""
        # Step 1: Input type detection
        input_type = self.detect_input_type(input_data)
        
        # Step 2: Input preprocessing
        processed_input = self.preprocess_input(input_data, input_type)
        
        # Step 3: Feature extraction
        features = self.extract_features(processed_input, input_type)
        
        # Step 4: AI processing
        ai_output = self.process_with_ai(features, input_type)
        
        # Step 5: Output formatting
        final_output = self.format_output(ai_output, input_type)
        
        return final_output
    
    @abstractmethod
    def detect_input_type(self, input_data):
        """Must detect input type (text, image, audio, etc.)"""
        pass
    
    @abstractmethod
    def preprocess_input(self, input_data, input_type):
        """Must preprocess based on input type"""
        pass
    
    @abstractmethod
    def extract_features(self, processed_input, input_type):
        """Must extract relevant features"""
        pass
    
    @abstractmethod
    def process_with_ai(self, features, input_type):
        """Must process with appropriate AI model"""
        pass
    
    def format_output(self, ai_output, input_type):
        """Default output formatting"""
        return {"result": ai_output, "type": input_type}

class DocumentAnalyzer(MultiModalTemplate):
    def detect_input_type(self, input_data):
        if isinstance(input_data, str):
            return "text"
        elif input_data.mime_type.startswith("image"):
            return "image"
        else:
            return "unknown"
    
    def preprocess_input(self, input_data, input_type):
        if input_type == "text":
            return input_data.strip()
        elif input_type == "image":
            return self.ocr_extraction(input_data)
    
    def extract_features(self, processed_input, input_type):
        if input_type == "text":
            return self.text_embeddings(processed_input)
        elif input_type == "image":
            return self.image_features(processed_input)
    
    def process_with_ai(self, features, input_type):
        if input_type == "text":
            return self.text_llm.analyze(features)
        elif input_type == "image":
            return self.vision_llm.analyze(features)
```

**Benefits:**
- Unified interface for different input types
- Consistent processing pipeline
- Easy extension to new input types
- Standardized feature extraction and processing

### 4. Evaluation and Testing Template
Template for evaluating LLM outputs with different metrics:

```python
class LLMEvaluationTemplate(ABC):
    """Template for LLM evaluation workflows"""
    
    def evaluate_model(self, test_cases, model):
        """Template method for model evaluation"""
        results = []
        
        for test_case in test_cases:
            # Step 1: Generate model output
            output = self.generate_output(test_case, model)
            
            # Step 2: Calculate metrics
            metrics = self.calculate_metrics(test_case, output)
            
            # Step 3: Perform qualitative analysis
            qualitative_score = self.qualitative_analysis(test_case, output)
            
            # Step 4: Aggregate results
            final_score = self.aggregate_scores(metrics, qualitative_score)
            
            results.append({
                "test_case": test_case,
                "output": output,
                "metrics": metrics,
                "score": final_score
            })
        
        # Step 5: Generate evaluation report
        return self.generate_report(results)
    
    def generate_output(self, test_case, model):
        """Default output generation"""
        return model.generate(test_case.input)
    
    @abstractmethod
    def calculate_metrics(self, test_case, output):
        """Must implement specific metrics calculation"""
        pass
    
    @abstractmethod
    def qualitative_analysis(self, test_case, output):
        """Must implement qualitative evaluation"""
        pass
    
    def aggregate_scores(self, metrics, qualitative_score):
        """Default score aggregation"""
        return (sum(metrics.values()) + qualitative_score) / (len(metrics) + 1)
    
    def generate_report(self, results):
        """Default report generation"""
        avg_score = sum(r["score"] for r in results) / len(results)
        return {"average_score": avg_score, "details": results}

class CodeGenerationEvaluator(LLMEvaluationTemplate):
    def calculate_metrics(self, test_case, output):
        return {
            "syntax_correctness": self.check_syntax(output),
            "functionality": self.test_functionality(output, test_case.expected),
            "code_quality": self.assess_code_quality(output)
        }
    
    def qualitative_analysis(self, test_case, output):
        # Human-like assessment of code readability and style
        return self.readability_score(output)
```

**Benefits:**
- Consistent evaluation framework
- Standardized metrics calculation
- Easy comparison across different models
- Comprehensive evaluation reports

## Implementation Advantages

### 1. **Code Reuse**
- Common workflow infrastructure shared across implementations
- Reduced duplication of boilerplate code
- Consistent error handling and logging
- Shared utility methods

### 2. **Maintainability**
- Clear separation between template structure and specific implementations
- Easy to modify common workflow without affecting implementations
- Centralized quality control and validation
- Consistent interface across different implementations

### 3. **Extensibility**
- Easy to add new implementations following the same template
- Hook methods allow fine-grained customization
- Template evolution doesn't break existing implementations
- Plugin-like architecture for new functionality

### 4. **Quality Assurance**
- Enforced workflow patterns ensure consistency
- Mandatory implementation of critical methods
- Built-in validation and error handling
- Standardized logging and monitoring

## Real-World Impact

The Template Method pattern in LLM applications provides:
- **Consistency**: Standardized workflows across different AI applications
- **Quality Control**: Enforced best practices and validation steps
- **Developer Productivity**: Reduced boilerplate code and faster development
- **System Reliability**: Proven workflow patterns and error handling

This pattern is essential for production LLM systems where you need consistent behavior across different implementations while allowing for domain-specific customization and optimization.