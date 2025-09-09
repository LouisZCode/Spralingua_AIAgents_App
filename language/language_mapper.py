# Language Mapper for Spralingua
# Maps database language strings to speech recognition codes and other formats

class LanguageMapper:
    """
    Maps between different language representations:
    - Database format (lowercase strings)
    - Speech recognition API codes
    - Display names
    """
    
    # Core mapping dictionary
    LANGUAGE_MAP = {
        'german': {
            'speech_code': 'de-DE',
            'display_name': 'German',
            'flag': '🇩🇪',
            'tts_code': 'German'  # For Minimax TTS
        },
        'spanish': {
            'speech_code': 'es-ES',
            'display_name': 'Spanish',
            'flag': '🇪🇸',
            'tts_code': 'Spanish'
        },
        'portuguese': {
            'speech_code': 'pt-PT',
            'display_name': 'Portuguese',
            'flag': '🇵🇹',
            'tts_code': 'Portuguese'
        },
        'english': {
            'speech_code': 'en-US',
            'display_name': 'English',
            'flag': '🇺🇸',
            'tts_code': 'English'
        }
    }
    
    @classmethod
    def get_speech_code(cls, db_language: str) -> str:
        """
        Get speech recognition API code for a database language string
        
        Args:
            db_language: Language string from database (e.g., 'german')
            
        Returns:
            Speech API code (e.g., 'de-DE') or None if not found
        """
        if not db_language:
            return None
            
        language_lower = db_language.lower()
        if language_lower in cls.LANGUAGE_MAP:
            return cls.LANGUAGE_MAP[language_lower]['speech_code']
        return None
    
    @classmethod
    def get_display_name(cls, db_language: str) -> str:
        """
        Get display name for a database language string
        
        Args:
            db_language: Language string from database (e.g., 'german')
            
        Returns:
            Display name (e.g., 'German') or the input if not found
        """
        if not db_language:
            return 'Unknown'
            
        language_lower = db_language.lower()
        if language_lower in cls.LANGUAGE_MAP:
            return cls.LANGUAGE_MAP[language_lower]['display_name']
        return db_language.capitalize()
    
    @classmethod
    def get_database_name(cls, speech_code: str) -> str:
        """
        Get database language string from speech API code (reverse mapping)
        
        Args:
            speech_code: Speech API code (e.g., 'de-DE')
            
        Returns:
            Database language string (e.g., 'german') or None if not found
        """
        for db_name, info in cls.LANGUAGE_MAP.items():
            if info['speech_code'] == speech_code:
                return db_name
        return None
    
    @classmethod
    def is_supported_language(cls, db_language: str) -> bool:
        """
        Check if a language is supported
        
        Args:
            db_language: Language string to check
            
        Returns:
            True if language is supported, False otherwise
        """
        if not db_language:
            return False
        return db_language.lower() in cls.LANGUAGE_MAP
    
    @classmethod
    def get_all_languages(cls) -> dict:
        """
        Get all supported languages with their mappings
        
        Returns:
            Dictionary of all language mappings
        """
        return cls.LANGUAGE_MAP.copy()
    
    @classmethod
    def get_supported_speech_codes(cls) -> list:
        """
        Get list of all supported speech recognition codes
        
        Returns:
            List of speech codes (e.g., ['de-DE', 'es-ES', ...])
        """
        return [info['speech_code'] for info in cls.LANGUAGE_MAP.values()]
    
    @classmethod
    def get_flag(cls, db_language: str) -> str:
        """
        Get flag emoji for a database language string
        
        Args:
            db_language: Language string from database (e.g., 'german')
            
        Returns:
            Flag emoji or empty string if not found
        """
        if not db_language:
            return ''
            
        language_lower = db_language.lower()
        if language_lower in cls.LANGUAGE_MAP:
            return cls.LANGUAGE_MAP[language_lower]['flag']
        return ''