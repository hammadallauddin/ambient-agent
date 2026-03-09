#!/usr/bin/env python3
"""
Test script for basic email assistant functionality without memory store issues
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

from email_assistant.email_assistant_hitl_memory_gmail import email_assistant
from langgraph.store.memory import InMemoryStore

def test_basic_email_assistant():
    """Test the email assistant with a sample email"""
    
    # Sample email in Gmail format
    sample_email = {
        "from": "john.doe@example.com",
        "to": "you@example.com", 
        "subject": "Meeting Request for Project Discussion",
        "body": "Hi there,\n\nI hope you're doing well. I'd like to schedule a meeting to discuss the upcoming project timeline. Are you available next Tuesday at 2 PM?\n\nBest regards,\nJohn",
        "id": "test_email_123"
    }
    
    print("Testing email assistant with sample email...")
    print(f"Email: {sample_email['subject']}")
    print(f"From: {sample_email['from']}")
    print(f"Body: {sample_email['body'][:100]}...")
    print()
    
    try:
        # Create an in-memory store for testing
        store = InMemoryStore()
        
        # Test the assistant with the store and proper config
        result = email_assistant.invoke({
            "email_input": sample_email
        }, config={"configurable": {"thread_id": "test_thread_123"}}, store=store)
        
        print("✅ Email assistant ran successfully!")
        print("Result keys:", list(result.keys()))
        
        if "classification_decision" in result:
            print(f"Classification: {result['classification_decision']}")
        
        if "messages" in result:
            print(f"Number of messages: {len(result['messages'])}")
            for i, msg in enumerate(result['messages']):
                print(f"Message {i}: {type(msg).__name__}")
                if hasattr(msg, 'content'):
                    print(f"  Content: {str(msg.content)[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error running email assistant: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_basic_email_assistant()
    if success:
        print("\n🎉 Email assistant is working correctly!")
    else:
        print("\n💥 Email assistant has issues that need to be fixed.")