"""
Minimax TTS Client - OOP implementation for Text-to-Speech functionality
Following Spralingua's OOP architecture pattern
"""

import os
import base64
import requests
from typing import Dict, Any, Optional, Tuple
from dotenv import load_dotenv

class MinimaxClient:
    """Client for Minimax Text-to-Speech API integration."""
    
    def __init__(self):
        """Initialize Minimax client and load environment variables."""
        load_dotenv()
        
        # API credentials
        self.api_key = os.getenv('MINIMAX_API_KEY')
        self.group_id = os.getenv('MINIMAX_GROUP_ID')
        self.default_voice_id = os.getenv('MINIMAX_VOICE_ID', 'female-shaonv')
        
        # API configuration - matching GTA-V2 exactly
        self.base_url = f"https://api.minimax.io/v1/t2a_v2?GroupId={self.group_id}"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Default TTS parameters - matching GTA-V2
        self.default_config = {
            "model": "speech-02-turbo",
            "speed": 1.2,
            "vol": 1.0,
            "pitch": 0,
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3"
        }
        
        # Character voice mappings (custom cloned voices from Minimax)
        self.character_voices = {
            'harry': 'AlpineSnowboardCoach_2024',  # Custom cloned voice for Harry
            'sally': 'SadSally_German_v2'          # Custom cloned voice for Sally
        }

        # Archive: Original Minimax default voices (before custom cloning)
        # These are built-in Minimax voices, kept for reference
        self.archived_voices = {
            'harry_original': 'male-qn-qingse',   # Cheerful male voice
            'sally_original': 'female-shaonv'     # Thoughtful female voice
        }
        
        print(f"[MINIMAX] Client initialized - API key configured: {bool(self.api_key)}")
    
    def validate_config(self) -> Tuple[bool, Optional[str]]:
        """
        Validate Minimax service configuration.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.api_key:
            return False, "Minimax API key not configured. Please set MINIMAX_API_KEY in .env"
        if not self.group_id:
            return False, "Minimax Group ID not configured. Please set MINIMAX_GROUP_ID in .env"
        return True, None
    
    def synthesize_speech(
        self, 
        text: str, 
        character: Optional[str] = None,
        voice_id: Optional[str] = None,
        speed: Optional[float] = None,
        volume: Optional[float] = None,
        pitch: Optional[int] = None
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Convert text to speech using Minimax API.
        
        Args:
            text: Text to convert to speech
            character: Character name (harry/sally) for voice selection
            voice_id: Specific voice ID (overrides character)
            speed: Speech speed (0.5 to 2.0)
            volume: Speech volume (0.0 to 10.0)
            pitch: Speech pitch (-12 to 12)
            
        Returns:
            Tuple of (success, result_dict)
            - If success: result_dict contains audio_data, format, voice_id
            - If failure: result_dict contains error message
        """
        # Validate configuration
        is_valid, error_msg = self.validate_config()
        if not is_valid:
            print(f"[MINIMAX ERROR] {error_msg}")
            return False, {"error": error_msg}
        
        # Clean and validate text
        text = text.strip()
        if not text:
            return False, {"error": "Text cannot be empty"}
        
        # Determine voice ID
        if not voice_id:
            if character and character in self.character_voices:
                voice_id = self.character_voices[character]
            else:
                voice_id = self.default_voice_id
        
        # Build request payload - matching GTA-V2's nested structure
        payload = {
            "model": self.default_config["model"],
            "text": text,
            "stream": False,
            "voice_setting": {
                "voice_id": voice_id,
                "speed": speed or self.default_config["speed"],
                "vol": volume or self.default_config["vol"],
                "pitch": pitch or self.default_config["pitch"]
            },
            "audio_setting": {
                "sample_rate": self.default_config["sample_rate"],
                "bitrate": self.default_config["bitrate"],
                "format": self.default_config["format"],
                "channel": 1
            }
        }
        
        print(f"[MINIMAX] Synthesizing speech - Voice: {voice_id}, Text length: {len(text)}")
        
        try:
            # Make API request
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            # Check response status
            if response.status_code != 200:
                error_msg = f"API error: {response.status_code}"
                try:
                    error_detail = response.json()
                    error_msg = error_detail.get('base_resp', {}).get('status_msg', error_msg)
                except:
                    pass
                print(f"[MINIMAX ERROR] {error_msg}")
                return False, {"error": error_msg}
            
            # Parse response
            result = response.json()
            print(f"[MINIMAX DEBUG] Response keys: {result.keys()}")
            print(f"[MINIMAX DEBUG] base_resp: {result.get('base_resp')}")
            
            # Check for API-level errors
            if result.get('base_resp', {}).get('status_code') != 0:
                error_msg = result.get('base_resp', {}).get('status_msg', 'Unknown API error')
                print(f"[MINIMAX ERROR] {error_msg}")
                return False, {"error": error_msg}
            
            # Get audio data from nested structure (matching GTA-V2)
            data_section = result.get('data', {})
            print(f"[MINIMAX DEBUG] data section keys: {list(data_section.keys())}")
            
            # Check TTS processing status
            tts_status = data_section.get('status')
            print(f"[MINIMAX DEBUG] TTS status: {tts_status}")
            
            # Check for audio data in either new or old field format
            audio_base64 = data_section.get('audio') or data_section.get('audio_file')
            
            if not audio_base64:
                print(f"[MINIMAX ERROR] No audio data in response. Full data section: {data_section}")
                return False, {"error": "No audio data received"}
            
            print(f"[MINIMAX SUCCESS] Audio generated - Size: {len(audio_base64)} chars")
            
            return True, {
                "audio_data": audio_base64,
                "format": self.default_config["format"],
                "voice_id": voice_id,
                "text_length": len(text)
            }
            
        except requests.exceptions.Timeout:
            print("[MINIMAX ERROR] Request timeout")
            return False, {"error": "Request timeout - Minimax API is slow"}
        except requests.exceptions.RequestException as e:
            print(f"[MINIMAX ERROR] Request failed: {e}")
            return False, {"error": f"Request failed: {str(e)}"}
        except Exception as e:
            print(f"[MINIMAX ERROR] Unexpected error: {e}")
            return False, {"error": f"Unexpected error: {str(e)}"}
    
    def get_character_voice(self, character: str) -> str:
        """
        Get the voice ID for a specific character.
        
        Args:
            character: Character name (harry/sally)
            
        Returns:
            Voice ID for the character
        """
        return self.character_voices.get(character, self.default_voice_id)
    
    def test_connection(self) -> bool:
        """
        Test the Minimax API connection with a simple request.
        
        Returns:
            True if connection successful, False otherwise
        """
        success, result = self.synthesize_speech(
            "Hello, this is a test.",
            voice_id=self.default_voice_id
        )
        return success


# Create a singleton instance
minimax_client = MinimaxClient()