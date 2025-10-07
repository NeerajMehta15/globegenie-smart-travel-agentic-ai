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
                formatted_prompt = prompt_template.format_messages(**input_data)
            else:
                prompt = ChatPromptTemplate.from_messages([
                    ('system', prompt_template),
                    ('user', '{user_input}')
                ])
                formatted_prompt = prompt.format_messages(**input_data)
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
        try:
            cleaned = response_content.strip()
            if '```json' in cleaned:
                start = cleaned.find('```json') + 7
                end = cleaned.find('```', start)
                cleaned = cleaned[start:end].strip()
            

            return json.loads(cleaned)
            
        except Exception as e:
            print(f"Failed to parse JSON: {response_content}")
            print(f"Error: {e}")
            return {}