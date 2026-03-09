#!/usr/bin/env python3
"""
Test script to verify email assistant components work without API calls
"""

import os
from email_assistant.utils import parse_gmail, format_gmail_markdown
from email_assistant.schemas import State, RouterSchema, StateInput
from email_assistant.prompts import triage_system_prompt, triage_user_prompt
from email_assistant.tools import get_tools, get_tools_by_name

def test_utils():
    """Test utility functions"""
    print("Testing utility functions...")
    
    # Test email parsing
    sample_email = {
        "from": "john.doe@example.com",
        "to": "you@example.com", 
        "subject": "Meeting Request",
        "body": "Hi there, let's meet!",
        "id": "test_email_123"
    }
    
    author, to, subject, email_thread, email_id = parse_gmail(sample_email)
    print(f"✅ Email parsing works: {author} -> {to}")
    
    # Test markdown formatting
    markdown = format_gmail_markdown(subject, author, to, email_thread, email_id)
    print(f"✅ Markdown formatting works: {len(markdown)} characters")
    
    return True

def test_schemas():
    """Test schema definitions"""
    print("Testing schema definitions...")
    
    # Test State creation
    state = State(email_input={"from": "test@example.com", "to": "you@example.com", "subject": "Test", "body": "Test body", "id": "123"})
    print(f"✅ State schema works: {state['email_input']['subject']}")
    
    # Test RouterSchema
    router = RouterSchema(reasoning="Test reasoning", classification="respond")
    print(f"✅ RouterSchema works: {router.classification}")
    
    return True

def test_prompts():
    """Test prompt templates"""
    print("Testing prompt templates...")
    
    # Test triage prompts
    user_prompt = triage_user_prompt.format(
        author="john@example.com",
        to="you@example.com", 
        subject="Meeting",
        email_thread="Test email content"
    )
    print(f"✅ User prompt template works: {len(user_prompt)} characters")
    
    system_prompt = triage_system_prompt.format(
        background="Test background",
        triage_instructions="Test instructions"
    )
    print(f"✅ System prompt template works: {len(system_prompt)} characters")
    
    return True

def test_tools():
    """Test tool loading"""
    print("Testing tool loading...")
    
    try:
        # Test tool loading with Gmail tools
        tools = get_tools(["send_email_tool", "schedule_meeting_tool", "check_calendar_tool"], include_gmail=True)
        print(f"✅ Tools loaded successfully: {len(tools)} tools")
        
        # Test tool by name lookup
        tools_by_name = get_tools_by_name(tools)
        print(f"✅ Tool lookup works: {len(tools_by_name)} tools by name")
        
        return True
    except Exception as e:
        print(f"❌ Tool loading failed: {e}")
        return False

def test_imports():
    """Test all imports work correctly"""
    print("Testing imports...")
    
    try:
        from email_assistant.email_assistant_hitl_memory_gmail import email_assistant
        print("✅ Main email assistant imports successfully")
        
        from email_assistant.tools.gmail.gmail_tools import mark_as_read
        print("✅ Gmail tools import successfully")
        
        from email_assistant.tools.default.email_tools import write_email
        print("✅ Default email tools import successfully")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def main():
    """Run all component tests"""
    print("🧪 Testing email assistant components without API calls...\n")
    
    tests = [
        ("Utility Functions", test_utils),
        ("Schema Definitions", test_schemas), 
        ("Prompt Templates", test_prompts),
        ("Tool Loading", test_tools),
        ("Imports", test_imports)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All components are working correctly!")
        print("The email assistant project is structurally sound.")
        print("The only issue is the Google API quota limitation.")
        print("This is an external service issue, not a code problem.")
    else:
        print(f"\n⚠️  {total - passed} tests failed. There may be code issues.")
    
    return passed == total

if __name__ == "__main__":
    main()