# Level Rules Manager for Spralingua
# Manages level-specific rules and guidelines

from database import db
from models.level_rule import LevelRule
from typing import Optional, Dict, Any

class LevelRulesManager:
    """Manages level rules and guidelines for language learning"""
    
    def __init__(self):
        """Initialize the LevelRulesManager"""
        self.db = db
        self._cache = {}  # Cache level rules to avoid repeated DB queries
    
    def get_level_rules(self, level: str) -> Optional[LevelRule]:
        """
        Get rules for a specific level
        
        Args:
            level: The level (A1, A2, B1, B2)
        
        Returns:
            LevelRule object or None
        """
        level_upper = level.upper()
        
        # Check cache first
        if level_upper in self._cache:
            return self._cache[level_upper]
        
        try:
            rules = LevelRule.query.filter_by(level=level_upper).first()
            if rules:
                self._cache[level_upper] = rules
            return rules
        except Exception as e:
            print(f"[ERROR] Failed to get level rules for {level}: {e}")
            return None
    
    def get_word_limit(self, level: str) -> int:
        """
        Get the default word limit for a level
        
        Args:
            level: The level (A1, A2, B1, B2)
        
        Returns:
            Word limit integer or 50 as default
        """
        rules = self.get_level_rules(level)
        if rules:
            return rules.base_word_limit
        
        # Fallback defaults if DB not available
        defaults = {
            'A1': 40,
            'A2': 50,
            'B1': 60,
            'B2': 70
        }
        return defaults.get(level.upper(), 50)
    
    def get_grammar_rules(self, level: str) -> Dict[str, Any]:
        """
        Get allowed grammar structures for a level
        
        Args:
            level: The level (A1, A2, B1, B2)
        
        Returns:
            Dictionary of grammar rules
        """
        rules = self.get_level_rules(level)
        if rules and rules.grammar_rules:
            return rules.grammar_rules
        
        # Fallback to basic rules
        return {
            'tenses': ['present_simple'],
            'structures': ['basic_questions', 'simple_statements'],
            'avoid': []
        }
    
    def get_vocabulary_complexity(self, level: str) -> str:
        """
        Get vocabulary complexity for a level
        
        Args:
            level: The level (A1, A2, B1, B2)
        
        Returns:
            Complexity string (basic, elementary, intermediate, upper_intermediate)
        """
        rules = self.get_level_rules(level)
        if rules:
            return rules.vocabulary_complexity
        
        # Fallback
        complexity_map = {
            'A1': 'basic',
            'A2': 'elementary',
            'B1': 'intermediate',
            'B2': 'upper_intermediate'
        }
        return complexity_map.get(level.upper(), 'basic')
    
    def get_general_guidelines(self, level: str) -> str:
        """
        Get general guidelines text for a level
        
        Args:
            level: The level (A1, A2, B1, B2)
        
        Returns:
            Guidelines text string
        """
        rules = self.get_level_rules(level)
        if rules:
            return rules.general_guidelines
        
        # Fallback
        return "Use appropriate vocabulary and grammar for the level."
    
    def get_all_level_rules(self) -> list:
        """
        Get all level rules from the database
        
        Returns:
            List of all LevelRule objects
        """
        try:
            return LevelRule.query.order_by(LevelRule.level).all()
        except Exception as e:
            print(f"[ERROR] Failed to get all level rules: {e}")
            return []
    
    def clear_cache(self):
        """Clear the internal cache"""
        self._cache = {}
    
    def format_level_description(self, level: str) -> str:
        """
        Get a formatted description for a level
        
        Args:
            level: The level (A1, A2, B1, B2)
        
        Returns:
            Formatted description string
        """
        descriptions = {
            'A1': 'Beginner - Basic phrases and simple sentences',
            'A2': 'Elementary - Simple conversations on familiar topics',
            'B1': 'Intermediate - Detailed conversations on various topics',
            'B2': 'Upper-Intermediate - Fluent conversations on abstract topics'
        }
        return descriptions.get(level.upper(), f'{level} Level')