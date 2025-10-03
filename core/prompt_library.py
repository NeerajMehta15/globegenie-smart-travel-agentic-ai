
from langchain_core.prompts import ChatPromptTemplate


def load_prompt(prompt_name: str) -> str:
    """Load prompt text from file."""
    try:
        path = f"prompt/{prompt_name}"
        with open(path, 'r') as file:
            content = file.read()
        return content
    except Exception as e:
        raise