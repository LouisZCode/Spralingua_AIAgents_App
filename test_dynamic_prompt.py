"""
Test script for the dynamic prompt system
Tests that the ConversationPromptBuilder correctly fetches user data and builds prompts
"""

from prompts.conversation_prompt_builder import ConversationPromptBuilder

def test_dynamic_prompt():
    """Test the dynamic prompt system with the existing user"""
    
    print("[TEST] Testing Dynamic Prompt System")
    print("=" * 50)
    
    # Initialize the builder
    builder = ConversationPromptBuilder()
    
    # Test with the existing user (lgzg90@hotmail.com has user_id = 2)
    user_id = 2
    character = 'harry'
    
    print(f"[TEST] Building prompt for User ID: {user_id}, Character: {character}")
    
    try:
        # Build the prompt
        prompt, context = builder.build_prompt(user_id, character)
        
        if prompt:
            print("[SUCCESS] Dynamic prompt built successfully!")
            print("\n[CONTEXT]:")
            print(f"  Input Language: {context.get('input_language')}")
            print(f"  Target Language: {context.get('target_language')}")
            print(f"  Level: {context.get('level')}")
            print(f"  Topic Number: {context.get('topic_number')}")
            print(f"  Topic Title: {context.get('topic_title')}")
            print(f"  Subtopics: {context.get('subtopics')}")
            print(f"  Conversation Contexts: {context.get('conversation_contexts')}")
            
            print("\n[PROMPT PREVIEW] (first 500 chars):")
            print(prompt[:500])
            print("...")
            
            # Test feedback context
            feedback_context = builder.get_feedback_context(user_id)
            print("\n[FEEDBACK CONTEXT]:")
            print(f"  Input Language: {feedback_context.get('input_language')}")
            print(f"  Target Language: {feedback_context.get('target_language')}")
            print(f"  Level: {feedback_context.get('level')}")
            
        else:
            print("[ERROR] Failed to build dynamic prompt")
            
    except Exception as e:
        print(f"[ERROR] Exception occurred: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("[TEST] Test complete")

if __name__ == "__main__":
    test_dynamic_prompt()