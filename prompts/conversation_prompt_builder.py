# Conversation Prompt Builder for Spralingua
# Builds dynamic prompts by combining personality, template, and user data

import yaml
import os
from typing import Dict, Optional, Tuple
from progress.progress_manager import ProgressManager
from topics.topic_manager import TopicManager
from flask import current_app


class ConversationPromptBuilder:
    """Builds personalized conversation prompts based on user progress and character personality"""
    
    def __init__(self):
        """Initialize the ConversationPromptBuilder with managers"""
        self.progress_manager = ProgressManager()
        self.topic_manager = TopicManager()
        self.personalities_path = os.path.join('prompts', 'personalities')
        self.templates_path = os.path.join('prompts', 'templates')
        
        # Cache for loaded files
        self._personality_cache = {}
        self._template_cache = None
        self._topic_scripts_cache = None
        
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
            # 1. Load personality
            personality = self._load_personality(character)
            
            # 2. Load template
            template = self._load_template()
            
            # 3. Get user context (language pair, level, topic)
            user_context = self._get_user_context(user_id)
            
            # 4. Build the final prompt
            final_prompt = self._merge_personality_and_template(
                personality, 
                template, 
                user_context
            )
            
            return final_prompt, user_context
            
        except Exception as e:
            print(f"[ERROR] ConversationPromptBuilder: {e}")
            # Return None to signal fallback to old system
            return None, None
    
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
    
    def _load_template(self) -> Dict:
        """Load the conversation template"""
        if self._template_cache:
            return self._template_cache
        
        template_file = os.path.join(self.templates_path, 'conversation_template.yaml')
        
        if not os.path.exists(template_file):
            raise FileNotFoundError(f"Template file not found: {template_file}")
        
        with open(template_file, 'r', encoding='utf-8') as file:
            template_data = yaml.safe_load(file)
            self._template_cache = template_data
            return template_data
    
    def _load_topic_scripts(self, level: str) -> Dict:
        """Load topic-specific scripts for the given level"""
        if self._topic_scripts_cache:
            return self._topic_scripts_cache
        
        # For now, we only have A1 scripts
        if level.upper() == 'A1':
            scripts_file = os.path.join(self.templates_path, 'a1_topic_scripts.yaml')
            
            if os.path.exists(scripts_file):
                with open(scripts_file, 'r', encoding='utf-8') as file:
                    scripts_data = yaml.safe_load(file)
                    self._topic_scripts_cache = scripts_data
                    return scripts_data
        
        return {}  # Return empty dict if no scripts available
    
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
                    context['topic_key'] = topic_def.title_key  # Store the key for script lookup
                    context['subtopics'] = topic_def.subtopics
                    context['conversation_contexts'] = topic_def.conversation_contexts
                    context['topic_guidance'] = topic_def.llm_prompt_template
            
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
    
    def _merge_personality_and_template(self, personality: Dict, template: Dict, context: Dict) -> str:
        """
        Merge personality and template with user context to create final prompt
        
        Args:
            personality: Character personality data
            template: Conversation template data
            context: User learning context
            
        Returns:
            Complete prompt string ready for Claude
        """
        # Load topic-specific scripts if available (especially for A1)
        topic_scripts = self._load_topic_scripts(context.get('level', 'A1'))
        topic_script_text = ""
        
        # Get the specific script for this topic if available
        if context.get('level', '').upper() == 'A1' and context.get('topic_key'):
            script_key = f"topic_{context['topic_number']}_{context['topic_key']}"
            if script_key in topic_scripts:
                script_data = topic_scripts[script_key]
                topic_script_text = f"""

## ⚠️ CRITICAL: STRICT A1 TOPIC {context['topic_number']} INSTRUCTIONS ⚠️

{script_data.get('opening_script', '')}

THIS OVERRIDES ALL OTHER INSTRUCTIONS FOR A1 LEARNERS!
"""
        
        # Build personality section
        personality_text = f"""
## Character Profile
{personality.get('background', '')}

## Personality Traits
{personality.get('communication_style', '')}

## Interests and Topics
{', '.join(personality.get('interests_and_topics', []))}

{personality.get('behavioral_rules', '')}

{personality.get('conversation_approach', '')}
"""
        
        # Get level-specific configuration
        level_config = template.get('level_configs', {}).get(context['level'], {})
        
        # Get language-specific elements
        lang_elements = template.get('language_elements', {}).get(
            context['target_language'].lower(), 
            {}
        )
        
        # Format subtopics and contexts
        subtopics_text = '\n  '.join([f"- {st}" for st in context.get('subtopics', [])])
        contexts_text = '\n  '.join([f"- {ctx}" for ctx in context.get('conversation_contexts', [])])
        
        # Build template parameters
        template_params = {
            'target_language': context['target_language'].capitalize(),
            'input_language': context['input_language'].capitalize(),
            'level': context['level'],
            'level_description': level_config.get('level_description', ''),
            'word_limit': level_config.get('word_limit', 50),
            'topic_number': context['topic_number'],
            'topic_title': context['topic_title'],
            'subtopics': subtopics_text,
            'conversation_contexts': contexts_text,
            'complexity_guidelines': level_config.get('complexity_guidelines', ''),
            'topic_guidance': context.get('topic_guidance', '')
        }
        
        # Format the conversation template
        conversation_text = template.get('conversation_template', '').format(**template_params)
        
        # Combine personality and conversation template
        final_prompt = f"""
{personality_text}

---

{conversation_text}

## Language-Specific Elements for {context['target_language'].capitalize()}
Greetings: {', '.join(lang_elements.get('greetings', []))}
Reactions: {', '.join(lang_elements.get('reactions', []))}
Fillers: {', '.join(lang_elements.get('fillers', []))}

{topic_script_text}
"""
        
        return final_prompt
    
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