import anthropic
import re
import time
from typing import List, Dict, Optional, Tuple


class ClaudeClient:
    """Handles all interactions with the Anthropic Claude API."""
    
    def __init__(self, model: str = "claude-3-haiku-20240307", max_tokens: int = 3000, temperature: float = 1.0):
        """
        Initialize the Claude client.
        
        Args:
            model: Claude model to use
            max_tokens: Maximum tokens for responses
            temperature: Temperature for response generation
        """
        self.client = anthropic.Anthropic()
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.conversation_history: List[Dict[str, str]] = []
        self.enable_tools = False  # Simplified version - no tools for now
        
    def send_message(self, user_input: str, system_prompt: str = '', context=None) -> str:
        """
        Send a message to Claude and get a response.
        
        Args:
            user_input: The user's message
            system_prompt: System prompt to use for the conversation
            context: Optional context (not used in simplified version)
            
        Returns:
            Claude's response text
            
        Raises:
            Exception: If there's an error communicating with the API
        """
        # Prepare messages
        messages_to_send = self.conversation_history.copy()
        
        # Add user message
        messages_to_send.append({
            "role": "user", 
            "content": user_input
        })
        
        try:
            # Send request to Claude
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=system_prompt,
                messages=messages_to_send
            )
            
            # Extract response text
            assistant_message = response.content[0].text
            
            # Update conversation history
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            # Keep conversation history manageable (last 20 messages)
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            return assistant_message
            
        except Exception as e:
            print(f"[ERROR] [CLAUDE CLIENT] Error sending message: {e}")
            raise e
    
    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
        print("[CLAUDE CLIENT] Conversation history cleared")
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the current conversation history."""
        return self.conversation_history.copy()
    
    def set_model(self, model: str):
        """Change the Claude model being used."""
        self.model = model
        print(f"[INFO] [CLAUDE CLIENT] Model changed to: {model}")
    
    def set_temperature(self, temperature: float):
        """Change the temperature setting."""
        self.temperature = temperature
        print(f"[TEMP] [CLAUDE CLIENT] Temperature changed to: {temperature}")
    
    def set_tools_enabled(self, enabled: bool):
        """
        Toggle tools on/off (compatibility method).
        In simplified version, this doesn't do anything.
        
        Args:
            enabled: Boolean to enable/disable tools
        """
        self.enable_tools = enabled