# Conversation Prompt Builder for Spralingua
# Enhanced version with database-driven prompts and no conflicts

import yaml
import os
from typing import Dict, Optional, Tuple
from progress.progress_manager import ProgressManager
from topics.topic_manager import TopicManager
from level_rules.level_rules_manager import LevelRulesManager
from flask import current_app

class ConversationPromptBuilder:
    """Builds personalized conversation prompts based on user progress and character personality"""
    
    def __init__(self):
        """Initialize the ConversationPromptBuilder with managers"""
        self.progress_manager = ProgressManager()
        self.topic_manager = TopicManager()
        self.level_rules_manager = LevelRulesManager()
        self.personalities_path = os.path.join('prompts', 'personalities')
        
        # Cache for loaded files
        self._personality_cache = {}
        
        # Feature flag for enhanced system
        self.use_enhanced = os.environ.get('USE_ENHANCED_PROMPTS', 'true').lower() == 'true'
    
    def build_prompt(self, user_id: int, character: str = 'harry') -> Tuple[str, Dict]:
        """
        Build a complete conversation prompt for the given user and character
        
        Args:
            user_id: The user's ID
            character: The character name (default: 'harry')
            
        Returns:
            Tuple of (prompt_string, context_dict) where context contains user data
        """
        try:
            # Use enhanced system if enabled
            if self.use_enhanced:
                return self._build_enhanced_prompt(user_id, character)
            else:
                # Fall back to legacy system (will be removed later)
                return self._build_legacy_prompt(user_id, character)
            
        except Exception as e:
            print(f"[ERROR] ConversationPromptBuilder: {e}")
            # Return None to signal fallback to old system
            return None, None
    
    def _build_enhanced_prompt(self, user_id: int, character: str) -> Tuple[str, Dict]:
        """
        Build prompt using the enhanced database-driven system
        NO CONFLICTS, SINGLE SOURCE OF TRUTH
        """
        # 1. Load character personality (minimal, character traits only)
        personality = self._load_personality(character)
        
        # 2. Get user context
        user_context = self._get_user_context(user_id)
        
        # 3. Get level rules from database
        level_rules = self.level_rules_manager.get_level_rules(user_context['level'])
        
        # 4. Get topic-specific parameters from database
        topic_params = self._get_topic_parameters(
            user_context['level'],
            user_context['topic_number'],
            user_context['target_language']
        )
        
        # 5. Build the prompt without conflicts
        final_prompt = self._build_clean_prompt(
            personality,
            user_context,
            level_rules,
            topic_params
        )
        
        return final_prompt, user_context
    
    def _build_clean_prompt(self, personality: Dict, context: Dict, 
                           level_rules, topic_params: Dict) -> str:
        """
        Build a clean, non-redundant prompt with single source of truth
        """
        prompt_sections = []
        
        # 1. CHARACTER SECTION (from personality file only)
        character_section = f"""## Character Profile
{personality.get('background', '')}"""
        
        if personality.get('communication_style'):
            character_section += f"""

## Communication Style
{personality.get('communication_style', '')}"""
        
        prompt_sections.append(character_section)
        
        # 2. LANGUAGE CONFIGURATION (simple, no redundancy)
        prompt_sections.append(f"""## Language Configuration
- Conversation Language: {context['target_language'].capitalize()}
- Student's Native Language: {context['input_language'].capitalize()}
- IMPORTANT: Use ONLY {context['target_language'].capitalize()} in all responses""")
        
        # 3. LEVEL & TOPIC (from database)
        word_limit = topic_params.get('word_limit', 
                                     level_rules.base_word_limit if level_rules else 40)
        
        prompt_sections.append(f"""## Current Learning Context
- Level: {context['level']}
- Topic {context['topic_number']}: {context['topic_title']}
- Word Limit: {word_limit} words per response
- Number of Exchanges: {topic_params.get('number_of_exchanges', 5)}""")
        
        # 4. LEVEL GUIDELINES (from level_rules table)
        if level_rules:
            prompt_sections.append(f"""## Level {context['level']} Guidelines
{level_rules.general_guidelines}""")
        
        # 5. TOPIC FOCUS (from database)
        if context.get('subtopics'):
            subtopics_text = '\n'.join([f"  - {st}" for st in context['subtopics']])
            prompt_sections.append(f"""## Topic Focus Areas
{subtopics_text}""")
        
        # 6. OPENING PHRASE (if available for this topic)
        opening_phrase = topic_params.get('opening_phrase')
        if opening_phrase:
            prompt_sections.append(f"""## Your First Message
You MUST start with exactly: "{opening_phrase}" """)
        
        # 7. CONVERSATION FLOW (if defined)
        if topic_params.get('conversation_flow'):
            flow_text = '\n'.join([f"  {i+1}. {step}" 
                                  for i, step in enumerate(topic_params['conversation_flow'])])
            prompt_sections.append(f"""## Conversation Flow
Follow this structure:
{flow_text}""")
        
        # 8. VOCABULARY (if specified)
        if topic_params.get('required_vocabulary'):
            vocab_text = ', '.join(topic_params['required_vocabulary'][:10])  # Limit display
            prompt_sections.append(f"""## Key Vocabulary to Use
{vocab_text}""")
        
        # 9. TOPIC-SPECIFIC RULES (if any)
        if topic_params.get('topic_specific_rules'):
            prompt_sections.append(f"""## Topic-Specific Rules
{topic_params['topic_specific_rules']}""")
        
        # 10. CORE BEHAVIORAL RULES (non-negotiable)
        prompt_sections.append("""## Core Rules
1. NEVER correct student errors - continue naturally
2. Stay within the word limit per response
3. Focus on the current topic
4. After the specified number of exchanges, wrap up politely
5. Always stay in character""")
        
        # Join all sections
        return '\n\n'.join(prompt_sections)
    
    def _get_topic_parameters(self, level: str, topic_number: int, 
                             target_language: str) -> Dict:
        """
        Get all topic-specific parameters from the database
        """
        params = {}
        
        # Get word limit (topic override or level default)
        params['word_limit'] = self.topic_manager.get_topic_word_limit(level, topic_number)
        
        # Get opening phrase for the target language
        params['opening_phrase'] = self.topic_manager.get_opening_phrase(
            level, topic_number, target_language
        )
        
        # Get conversation flow
        params['conversation_flow'] = self.topic_manager.get_conversation_flow(
            level, topic_number
        )
        
        # Get required vocabulary
        params['required_vocabulary'] = self.topic_manager.get_required_vocabulary(
            level, topic_number
        )
        
        # Get topic-specific rules
        params['topic_specific_rules'] = self.topic_manager.get_topic_specific_rules(
            level, topic_number
        )
        
        # Get number of exchanges
        params['number_of_exchanges'] = self.topic_manager.get_number_of_exchanges(
            level, topic_number
        )
        
        return params
    
    def _load_personality(self, character: str) -> Dict:
        """Load personality YAML for the given character"""
        if character in self._personality_cache:
            return self._personality_cache[character]
        
        personality_file = os.path.join(self.personalities_path, f'{character}_personality.yaml')
        
        if not os.path.exists(personality_file):
            raise FileNotFoundError(f"Personality file not found: {personality_file}")
        
        with open(personality_file, 'r', encoding='utf-8') as file:
            personality_data = yaml.safe_load(file)
            self._personality_cache[character] = personality_data
            return personality_data
    
    def _get_user_context(self, user_id: int) -> Dict:
        """
        Get user's learning context from database
        
        Returns dict with:
            - input_language
            - target_language
            - level
            - current_topic
            - topic_details
        """
        context = {
            'input_language': 'english',  # Default
            'target_language': 'german',   # Default
            'level': 'A1',                 # Default
            'topic_number': 1,              # Default
            'topic_title': 'General Conversation',  # Default
            'subtopics': [],
            'conversation_contexts': []
        }
        
        try:
            # Get user's progress (most recent language pair)
            user_progress = self.progress_manager.get_user_progress(user_id)
            
            if user_progress:
                context['input_language'] = user_progress.input_language
                context['target_language'] = user_progress.target_language
                context['level'] = user_progress.current_level
                context['user_progress_id'] = user_progress.id
                
                # Determine current topic (next uncompleted topic)
                current_topic_number = self._determine_current_topic(user_progress.id, context['level'])
                context['topic_number'] = current_topic_number
                
                # Get topic details
                topic_def = self.topic_manager.get_topic_definition(context['level'], current_topic_number)
                if topic_def:
                    context['topic_title'] = self._translate_topic_title(topic_def.title_key)
                    context['topic_key'] = topic_def.title_key
                    context['subtopics'] = topic_def.subtopics
                    context['conversation_contexts'] = topic_def.conversation_contexts
            
        except Exception as e:
            print(f"[WARNING] Could not get user context: {e}")
            # Return default context
        
        return context
    
    def _determine_current_topic(self, user_progress_id: int, level: str) -> int:
        """
        Determine which topic the user should practice
        
        Returns the next uncompleted topic number (1-12)
        """
        try:
            # Get all topic progress for this user
            all_progress = self.topic_manager.get_user_topic_progress(user_progress_id)
            
            if not all_progress:
                # No progress yet, start with topic 1
                return 1
            
            # Find the first uncompleted topic
            for topic_num in range(1, 13):  # Topics 1-12
                topic_progress = next(
                    (tp for tp in all_progress if tp.topic_number == topic_num), 
                    None
                )
                
                if not topic_progress or not topic_progress.completed:
                    return topic_num
            
            # All topics completed, cycle back to 1
            return 1
            
        except Exception as e:
            print(f"[WARNING] Could not determine current topic: {e}")
            return 1  # Default to topic 1
    
    def _translate_topic_title(self, title_key: str) -> str:
        """Translate topic title key to readable title"""
        # Map of title keys to readable titles
        title_map = {
            'who_are_you': 'Who are you?',
            'what_do_you_do': 'What do you do?',
            'know_your_abc': 'Know your ABC',
            'can_you_spell_it': 'Can you spell it?',
            'whats_the_number': "What's the number?",
            'how_much_is_it': 'How much is it?',
            'whats_your_address': "What's your address?",
            'more_about_you': 'More about you',
            'what_are_they_like': 'What are they like?',
            'what_do_they_do': 'What do they do?',
            'what_time_is_it': 'What time is it?',
            'when_is_it': 'When is it?'
        }
        return title_map.get(title_key, title_key.replace('_', ' ').title())
    
    def get_feedback_context(self, user_id: int) -> Dict:
        """
        Get context for feedback generation (language hints and comprehensive feedback)
        
        Returns:
            Dict with input_language, target_language, and level
        """
        context = self._get_user_context(user_id)
        return {
            'input_language': context.get('input_language', 'english'),
            'target_language': context.get('target_language', 'german'),
            'level': context.get('level', 'A1')
        }
    
    # LEGACY METHOD - Will be removed after testing
    def _build_legacy_prompt(self, user_id: int, character: str) -> Tuple[str, Dict]:
        """Legacy prompt builder - kept for fallback during transition"""
        # This would contain the old implementation
        # For now, just return None to trigger fallback
        return None, None