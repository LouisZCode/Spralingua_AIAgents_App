# Feedback Generator for Casual Chat Module
# Enhanced with dynamic language support

import json
import re
from typing import List, Dict, Any, Optional
from prompts.feedback_prompts import FeedbackPromptBuilder

def clean_json_response(json_str):
    """
    Clean JSON string by removing control characters and fixing common issues.

    Args:
        json_str: Raw JSON string that may contain control characters

    Returns:
        Cleaned JSON string ready for parsing
    """
    # Remove control characters that break JSON parsing
    # This regex removes all control characters except tab (\t), newline (\n), and carriage return (\r)
    json_str = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', json_str)

    # Fix common JSON issues
    json_str = re.sub(r',\s*}', '}', json_str)  # Remove trailing commas in objects
    json_str = re.sub(r',\s*]', ']', json_str)  # Remove trailing commas in arrays

    return json_str

def get_message_requirement(user_level):
    """
    Determine the total number of messages required based on user proficiency level.

    Args:
        user_level: User's proficiency level (beginner, intermediate, advanced)

    Returns:
        int: Total number of messages required for the exercise
    """
    requirements = {
        'beginner': 3,      # Shorter practice for beginners
        'intermediate': 6,   # Standard practice length
        'advanced': 9        # Extended practice for advanced users
    }
    return requirements.get(user_level.lower() if user_level else 'intermediate', 6)

def generate_language_hint(message, claude_client, user_level='intermediate',
                         target_language='german', native_language='english'):
    """
    Generate a language hint based on the user's message.

    Args:
        message: The user's message to analyze
        claude_client: The Claude API client
        user_level: The user's proficiency level
        target_language: The language being learned
        native_language: The user's native language

    Returns:
        Dict with hint information
    """
    print(f"[TARGET] [HINT GENERATION] Starting hint generation for message: '{message[:50]}...'")
    print(f"[TARGET] [HINT GENERATION] User level: {user_level}")
    print(f"[TARGET] [HINT GENERATION] Target language: {target_language}, Native language: {native_language}")
    print(f"[TARGET] [HINT GENERATION] Claude client tools enabled: {getattr(claude_client, 'enable_tools', 'unknown')}")

    try:
        # Get the dynamic language analysis prompt
        feedback_builder = FeedbackPromptBuilder()
        analysis_prompt = feedback_builder.get_hint_prompt(target_language, native_language, user_level)
        print(f"[TARGET] [HINT GENERATION] Dynamic prompt loaded: {len(analysis_prompt)} characters")
        print(f"[DEBUG] Target: {target_language}, Native: {native_language}")

        # Replace placeholders
        analysis_prompt = analysis_prompt.replace('{message}', message)
        analysis_prompt = analysis_prompt.replace('{level}', user_level)

        # Debug: Show first 200 chars of the prompt to see language instruction
        print(f"[DEBUG] Prompt preview: {analysis_prompt[:200]}...")
        
        # Get hint from Claude - pass a clear analysis request as user_input
        print(f"[TARGET] [HINT GENERATION] Calling Claude with analysis request")
        
        # Temporarily disable tools for hint generation
        original_tools_state = claude_client.enable_tools
        claude_client.set_tools_enabled(False)
        print(f"[TARGET] [HINT GENERATION] Temporarily disabled tools (was: {original_tools_state})")

        hint_response = claude_client.send_message(
            f"Analyze this {target_language.capitalize()} message and provide a hint: '{message}'",
            analysis_prompt
        )
        
        # Restore original tools state
        claude_client.set_tools_enabled(original_tools_state)
        print(f"[TARGET] [HINT GENERATION] Restored tools state to: {original_tools_state}")
        
        print(f"[TARGET] [HINT GENERATION] Claude response received: {hint_response[:200]}...")
        
        # Try to parse JSON response
        import json
        try:
            # Clean up response if needed
            hint_response = hint_response.strip()
            
            # Try to extract JSON if wrapped in markdown or other text
            if '```json' in hint_response:
                json_start = hint_response.find('```json') + 7
                json_end = hint_response.find('```', json_start)
                hint_response = hint_response[json_start:json_end].strip()
            elif '```' in hint_response:
                json_start = hint_response.find('```') + 3
                json_end = hint_response.find('```', json_start)
                hint_response = hint_response[json_start:json_end].strip()
            elif '{' in hint_response:
                # Try to extract JSON object
                json_start = hint_response.find('{')
                json_end = hint_response.rfind('}') + 1
                hint_response = hint_response[json_start:json_end]
            
            # Parse the JSON
            hint_data = json.loads(hint_response)

            # Validate structure
            if 'phrase' in hint_data and 'hint' in hint_data:
                # Normalize hint types to recognized values
                hint_type = hint_data.get('type', 'warning')
                type_mapping = {
                    'correction': 'error',
                    'hint': 'warning',
                    'suggestion': 'warning',
                    'tip': 'warning'
                }
                hint_data['type'] = type_mapping.get(hint_type, hint_type)

                print(f"[SUCCESS] [HINT GENERATION] Successfully parsed hint: {hint_data}")
                return hint_data
            else:
                # Fallback if structure is wrong
                print(f"[WARNING] [HINT GENERATION] JSON structure invalid, using error indicator")
                return {
                    "type": "error",
                    "phrase": "System Notice",
                    "hint": "Hint generation unavailable. Please continue practicing.",
                    "system_error": True
                }

        except json.JSONDecodeError as e:
            print(f"[WARNING] JSON parsing error: {e}")
            print(f"[WARNING] Response was: {hint_response[:200] if len(hint_response) > 200 else hint_response}")
            # Return error indicator instead of fake hint
            return {
                "type": "error",
                "phrase": "System Error",
                "hint": "Hint generation failed. Please continue practicing.",
                "system_error": True
            }
        
    except Exception as e:
        print(f"[ERROR] Error generating hint: {e}")
        return {
            "type": "error",
            "phrase": "System Error",
            "hint": "Unable to generate hint. Please continue.",
            "system_error": True
        }

def generate_comprehensive_feedback(messages, claude_client, user_level='intermediate',
                                  target_language='german', native_language='english'):
    """
    Generate comprehensive feedback after practice session.

    Args:
        messages: List of user messages
        claude_client: The Claude API client
        user_level: The user's proficiency level
        target_language: The language being learned
        native_language: The user's native language

    Returns:
        Dict with comprehensive feedback
    """
    print(f"[COMPREHENSIVE] Starting comprehensive feedback generation")
    print(f"[COMPREHENSIVE] Messages count: {len(messages)}")
    print(f"[COMPREHENSIVE] Target: {target_language}, Native: {native_language}, Level: {user_level}")

    try:
        # Get the dynamic comprehensive feedback prompt
        feedback_builder = FeedbackPromptBuilder()
        feedback_prompt = feedback_builder.get_comprehensive_feedback_prompt(
            target_language, native_language, user_level
        )
        print(f"[COMPREHENSIVE] Prompt loaded: {len(feedback_prompt)} characters")
        
        # Format messages
        messages_text = "\n".join([f"Message {i+1}: {msg}" for i, msg in enumerate(messages)])
        feedback_prompt = feedback_prompt.replace('{messages}', messages_text)
        feedback_prompt = feedback_prompt.replace('{level}', user_level)
        
        # Get feedback from Claude - pass analysis request with correct parameter order
        print(f"[COMPREHENSIVE] Calling Claude for feedback analysis")
        feedback_response = claude_client.send_message(
            f"Provide comprehensive feedback on these {target_language.capitalize()} messages",
            feedback_prompt
        )
        print(f"[COMPREHENSIVE] Received response: {len(feedback_response)} characters")

        # Try to parse as JSON
        import json
        try:
            # Extract JSON from response if wrapped in markdown
            original_response = feedback_response  # Keep original for debugging
            if '```json' in feedback_response:
                json_start = feedback_response.find('```json') + 7
                json_end = feedback_response.find('```', json_start)
                feedback_response = feedback_response[json_start:json_end].strip()
            elif '```' in feedback_response:
                json_start = feedback_response.find('```') + 3
                json_end = feedback_response.find('```', json_start)
                feedback_response = feedback_response[json_start:json_end].strip()

            # Clean the JSON before parsing
            cleaned_response = clean_json_response(feedback_response)

            # Debug logging
            print(f"[DEBUG] First 200 chars of cleaned response: {cleaned_response[:200] if len(cleaned_response) > 200 else cleaned_response}")

            feedback_data = json.loads(cleaned_response)
            print(f"[COMPREHENSIVE] Successfully parsed feedback JSON")
            return feedback_data

        except json.JSONDecodeError as e:
            print(f"[ERROR] JSON parsing failed: {e}")
            print(f"[ERROR] Failed at position {e.pos if hasattr(e, 'pos') else 'unknown'}")
            print(f"[DEBUG] Raw response length: {len(feedback_response)}")
            # Return honest error message instead of fake feedback
            return {
                "error": True,
                "message": f"Sorry, the feedback system encountered an error and couldn't process your session properly. We're working on fixing this issue.",
                "top_mistakes": [],
                "strengths": [],
                "focus_areas": [],
                "overall_feedback": "The feedback system is temporarily unavailable. Please try again later or contact support if the problem persists."
            }
        except Exception as e:
            print(f"[ERROR] Unexpected error parsing feedback: {e}")
            return {
                "error": True,
                "message": "An unexpected error occurred while generating feedback.",
                "top_mistakes": [],
                "strengths": [],
                "focus_areas": [],
                "overall_feedback": "The feedback system encountered an unexpected error. Please try again later."
            }
            
    except Exception as e:
        print(f"[ERROR] Error generating comprehensive feedback: {e}")
        return {
            "error": True,
            "message": "Failed to generate feedback due to a system error.",
            "top_mistakes": [],
            "strengths": [],
            "focus_areas": [],
            "overall_feedback": f"System error: {str(e)}. Please try again later."
        }