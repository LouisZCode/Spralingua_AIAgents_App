"""
Test script for the progress tracking system
Tests the complete flow of a user progressing through topics and levels
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from database import db
from progress.exercise_progress_manager import ExerciseProgressManager
from topics.topic_manager import TopicManager
from tests.test_manager import TestManager

def test_exercise_completion():
    """Test completing exercises and topic advancement"""

    with app.app_context():
        print("[TEST] Starting Progress System Test")
        print("=" * 60)

        # Initialize managers
        exercise_mgr = ExerciseProgressManager()
        topic_mgr = TopicManager()
        test_mgr = TestManager()

        # Use Pepito's English->Spanish progress (user_progress_id = 12)
        user_progress_id = 12

        print("\n[TEST] Testing Topic 1 Exercise Completion")
        print("-" * 40)

        # Test 1: Complete Casual Chat with passing score
        print("\n1. Recording Casual Chat attempt with 60% score (PASS)")
        result = exercise_mgr.record_exercise_attempt(
            user_progress_id=user_progress_id,
            topic_number=1,
            exercise_type='casual_chat',
            score=60,
            messages_correct=3,
            messages_total=5
        )

        if result['success']:
            print(f"   [SUCCESS] Casual Chat recorded: Score={result['exercise_progress']['score']}%")
            print(f"   Completed: {result['exercise_progress']['completed']}")
            print(f"   Topic Advanced: {result['topic_advanced']}")
        else:
            print(f"   [ERROR] {result['error']}")

        # Test 2: Complete Email Writing with failing score
        print("\n2. Recording Email Writing attempt with 40% score (FAIL)")
        result = exercise_mgr.record_exercise_attempt(
            user_progress_id=user_progress_id,
            topic_number=1,
            exercise_type='email_writing',
            score=40
        )

        if result['success']:
            print(f"   [SUCCESS] Email Writing recorded: Score={result['exercise_progress']['score']}%")
            print(f"   Completed: {result['exercise_progress']['completed']}")
            print(f"   Topic Advanced: {result['topic_advanced']}")
        else:
            print(f"   [ERROR] {result['error']}")

        # Test 3: Retry Email Writing with passing score
        print("\n3. Retrying Email Writing with 55% score (PASS)")
        result = exercise_mgr.record_exercise_attempt(
            user_progress_id=user_progress_id,
            topic_number=1,
            exercise_type='email_writing',
            score=55
        )

        if result['success']:
            print(f"   [SUCCESS] Email Writing recorded: Score={result['exercise_progress']['score']}%")
            print(f"   Completed: {result['exercise_progress']['completed']}")
            print(f"   Topic Advanced: {result['topic_advanced']}")
        else:
            print(f"   [ERROR] {result['error']}")

        # Check topic status
        print("\n[TEST] Checking Topic Status")
        print("-" * 40)

        # Get topic status
        topic_status = exercise_mgr.get_topic_exercises_status(user_progress_id, 1)
        print(f"\nTopic 1 Status:")
        print(f"  Topic Complete: {topic_status['topic_complete']}")
        for ex_type, status in topic_status['exercises'].items():
            print(f"  {ex_type}: Completed={status['completed']}, Score={status['score']}%, Attempts={status['attempts']}")

        # Check current topic
        current = topic_mgr.get_current_topic(user_progress_id)
        if current:
            print(f"\nCurrent Item:")
            print(f"  Type: {current['type']}")
            if current['type'] == 'topic':
                print(f"  Topic Number: {current['topic_number']}")
            elif current['type'] == 'test':
                print(f"  Test: {current['test_type']}")
                print(f"  Message: {current['message']}")

        # Test 4: Complete topics 2-4 to unlock test
        print("\n[TEST] Fast-forwarding Topics 2-4")
        print("-" * 40)

        for topic_num in [2, 3, 4]:
            print(f"\nCompleting Topic {topic_num}:")

            # Complete both exercises for each topic
            for exercise_type in ['casual_chat', 'email_writing']:
                result = exercise_mgr.record_exercise_attempt(
                    user_progress_id=user_progress_id,
                    topic_number=topic_num,
                    exercise_type=exercise_type,
                    score=70  # Good passing score
                )

                if result['success']:
                    print(f"  {exercise_type}: Score=70% [PASS]")
                    if result['topic_advanced']:
                        print(f"  [INFO] Topic {topic_num} completed!")

        # Check if test is unlocked
        print("\n[TEST] Checking Test Unlock Status")
        print("-" * 40)

        current = topic_mgr.get_current_topic(user_progress_id)
        if current and current['type'] == 'test':
            print(f"\n[SUCCESS] Test unlocked!")
            print(f"  Test Type: {current['test_type']}")
            print(f"  Message: {current['message']}")

            # Check test unlock status
            unlocked, message = test_mgr.is_test_unlocked(user_progress_id, 'checkpoint_1')
            print(f"  Unlocked: {unlocked}")
            print(f"  Message: {message}")
        else:
            print(f"\n[WARNING] Expected test to be unlocked but got: {current}")

        # Test 5: Simulate test completion
        print("\n[TEST] Simulating Test 1 Completion")
        print("-" * 40)

        print("\n1. First attempt with failing score (40%)")
        success, result = test_mgr.record_test_attempt(
            user_progress_id=user_progress_id,
            test_type='checkpoint_1',
            score=40
        )

        if success:
            print(f"   Score: {result['score']}%")
            print(f"   Passed: {result['passed']}")
            print(f"   Attempts: {result['attempts']}")
        else:
            print(f"   [ERROR] {result['error']}")

        print("\n2. Second attempt with passing score (65%)")
        success, result = test_mgr.record_test_attempt(
            user_progress_id=user_progress_id,
            test_type='checkpoint_1',
            score=65
        )

        if success:
            print(f"   Score: {result['score']}%")
            print(f"   Passed: {result['passed']}")
            print(f"   Attempts: {result['attempts']}")
        else:
            print(f"   [ERROR] {result['error']}")

        # Check if topics 5-8 are now accessible
        print("\n[TEST] Checking Topic 5 Accessibility")
        print("-" * 40)

        can_access, reason = topic_mgr.can_access_topic(user_progress_id, 5)
        print(f"  Can access Topic 5: {can_access}")
        print(f"  Reason: {reason}")

        # Get current topic after test
        current = topic_mgr.get_current_topic(user_progress_id)
        if current and current['type'] == 'topic':
            print(f"\n[SUCCESS] Advanced to Topic {current['topic_number']}")

        # Final summary
        print("\n" + "=" * 60)
        print("[TEST] Test Summary")
        print("=" * 60)

        # Get all exercise progress
        all_exercises = exercise_mgr.get_all_exercises_for_user(user_progress_id)
        print(f"\nTotal Exercise Records: {len(all_exercises)}")

        completed_count = sum(1 for ex in all_exercises if ex.completed)
        print(f"Completed Exercises: {completed_count}/{len(all_exercises)}")

        # Get test summary
        test_summary = test_mgr.get_test_status_summary(user_progress_id)
        print(f"\nTest Status:")
        for test_type, status in test_summary.items():
            if status:
                print(f"  {test_type}: Passed={status['passed']}, Score={status['score']}%, Attempts={status['attempts']}")

        print("\n[TEST] Progress System Test Complete!")

if __name__ == "__main__":
    test_exercise_completion()