from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from utils.config import config
import json
from typing import Any, Dict, Union

class LLMClient:
    """Centralized LLM client for all agent communications."""
    
    def __init__(self, model: str = "llama-3.1-8b-instant", temperature: float = 0.1, 
                 max_tokens: int = None, max_retries: int = 2):
        """Initialize LLM client with configuration."""
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.max_retries = max_retries
        self.llm = ChatGroq(
            groq_api_key= config.GROQ_API_KEY,
            model=self.model, 
            temperature=self.temperature, 
            max_retries=self.max_retries,
            max_tokens=self.max_tokens
        )

    def _format_prompt(self, prompt_template: Union[ChatPromptTemplate, str], input_data: Dict[str, Any]):
        """Format prompt template with input data."""
        try:
            if isinstance(prompt_template, ChatPromptTemplate):
                # If already a LangChain prompt, just format it with inputs
                formatted_prompt = prompt_template.format_messages(**input_data)
            else:
                formatted_text = prompt_template.format(**input_data)
                
                from langchain.schema import HumanMessage
                formatted_prompt = [HumanMessage(content=formatted_text)]

            return formatted_prompt

        except Exception as e:
            print(f"Error formatting prompt: {e}")
            return None

    
    def invoke(self, formatted_prompt: Any) -> str:
        """Call LLM and return raw response string."""
        try:
            response = self.llm.invoke(formatted_prompt)
            return response.content.strip()
        except Exception as e:
            print(f"Error invoking LLM: {e}")
            return ""
    

    def _parse_json_response(self, response_content: str) -> dict:
        """Simple JSON parser for LLM responses."""
        import re
        import json
        
        try:
            cleaned = response_content.strip()
            
            # Method 1: Try to extract from ```json blocks
            if '```json' in cleaned:
                # Find everything between ```json and the next ```
                pattern = r'```json\s*(.*?)\s*```'
                match = re.search(pattern, cleaned, re.DOTALL)
                if match:
                    cleaned = match.group(1).strip()
            
            # Method 2: If no markdown, find the JSON object
            else:
                # Find first { and last }
                start = cleaned.find('{')
                end = cleaned.rfind('}')
                if start != -1 and end != -1:
                    cleaned = cleaned[start:end + 1]
            
            # Remove // comments
            cleaned = re.sub(r'//.*', '', cleaned)
            
            # Parse and return
            result = json.loads(cleaned)
            return result
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {response_content[:500]}...")
            print(f"JSON Error: {e}")
            return {}
        except Exception as e:
            print(f"Failed to parse JSON: {response_content[:500]}...")
            print(f"Error: {e}")
            return {}