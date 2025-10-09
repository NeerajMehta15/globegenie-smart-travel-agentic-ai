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
        self.max_tokens = 4096
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
            
            # Extract from markdown
            if '```json' in cleaned:
                start = cleaned.find('```json') + 7
                end = cleaned.find('```', start)
                cleaned = cleaned[start:end].strip()
            
            # Remove comments
            cleaned = re.sub(r'//.*', '', cleaned)
            
            # Parse JSON
            return json.loads(cleaned)
            
        except json.JSONDecodeError as e:
            print(f"JSON parse failed, attempting repair...")
            
            # Try truncating to last valid closing brace
            try:
                last_brace = cleaned.rfind('}')
                if last_brace > 0:
                    # Keep everything up to and including last }
                    truncated = cleaned[:last_brace + 1]
                    result = json.loads(truncated)
                    print("Successfully repaired JSON by truncation")
                    return result
            except:
                pass
            
            print(f"Failed to parse JSON from content")
            print(f"Error at: {str(e)[:200]}")
            return {}