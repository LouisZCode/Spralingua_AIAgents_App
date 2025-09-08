import yaml
from typing import Dict


class PromptManager:
    """Manages loading and accessing prompts from YAML configuration files."""
    
    def __init__(self, prompt_file: str = 'prompts.yaml'):
        """
        Initialize the PromptManager with a prompt file.
        
        Args:
            prompt_file: Path to the YAML file containing prompts
        """
        self.prompt_file = prompt_file
        self._prompts: Dict[str, str] = {}
        self.load_prompts()
    
    def load_prompts(self) -> None:
        """Load prompts from the YAML file."""
        try:
            with open(self.prompt_file, 'r', encoding='utf-8') as file:
                self._prompts = yaml.safe_load(file) or {}
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt file '{self.prompt_file}' not found")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file: {e}")
    
    def get_prompt(self, prompt_name: str, default: str = '') -> str:
        """
        Get a specific prompt by name.
        
        Args:
            prompt_name: Name of the prompt to retrieve
            default: Default value if prompt not found
            
        Returns:
            The prompt text or default value
        """
        return self._prompts.get(prompt_name, default)
    
    def get_all_prompts(self) -> Dict[str, str]:
        """
        Get all available prompts.
        
        Returns:
            Dictionary of all prompts
        """
        return self._prompts.copy()
    
    def has_prompt(self, prompt_name: str) -> bool:
        """
        Check if a prompt exists.
        
        Args:
            prompt_name: Name of the prompt to check
            
        Returns:
            True if prompt exists, False otherwise
        """
        return prompt_name in self._prompts
    
    def reload_prompts(self) -> None:
        """Reload prompts from the YAML file."""
        self.load_prompts()
        print(f"✅ [PROMPT MANAGER] Reloaded prompts from {self.prompt_file}")