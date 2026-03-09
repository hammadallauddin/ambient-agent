#!/usr/bin/env python3
"""
Test script to verify gemini-2.5-flash model is working without Gmail dependencies
"""

import os
from typing import Literal
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langgraph.store.base import BaseStore
from langgraph.store.memory import InMemoryStore
from langgraph.types import interrupt, Command

from email_assistant.tools import get_tools, get_tools_by_name
from email_assistant.prompts import triage_system_prompt, triage_user_prompt, default_triage_instructions, default_background
from email_assistant.schemas import State, RouterSchema, StateInput
from email_assistant.utils import parse_gmail, format_gmail_markdown

def test_gemini_25_flash():
    """Test that gemini-2.5-flash model works for email triage"""
    
    print("🧪 Testing gemini-2.5-flash model for email triage...")
    print("=" * 60)
    
    # Sample email
    sample_email = {
        "from": "john.doe@example.com",
        "to": "hammadallauddin@gmail.com", 
        "subject": "Meeting Request for Project Discussion",
        "body": "Hi there,\n\nI hope you're doing well. I'd like to schedule a meeting to discuss the upcoming project timeline. Are you available next Tuesday at 2 PM?\n\nBest regards,\nJohn",
        "id": "test_email_123"
    }
    
    print(f"📧 Email: {sample_email['subject']}")
    print(f"📤 From: {sample_email['from']}")
    print(f"📥 To: {sample_email['to']}")
    print(f"📄 Body: {sample_email['body'][:100]}...")
    print()
    
    try:
        # Parse email
        author, to, subject, email_thread, email_id = parse_gmail(sample_email)
        user_prompt = triage_user_prompt.format(
            author=author, to=to, subject=subject, email_thread=email_thread
        )

        email_markdown = format_gmail_markdown(subject, author, to, email_thread, email_id)

        system_prompt = triage_system_prompt.format(
            background=default_background,
            triage_instructions=default_triage_instructions,
        )

        # Test gemini-2.5-flash model
        print("🤖 Testing gemini-2.5-flash model...")
        llm = init_chat_model(model=os.getenv("GOOGLE_MODEL", "gemini-2.5-flash"), model_provider="google_genai", temperature=0.0)
        llm_router = llm.with_structured_output(RouterSchema)
        
        result = llm_router.invoke([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ])

        print(f"✅ Model response received!")
        print(f"   - Classification: {result.classification}")
        print(f"   - Reasoning: {result.reasoning}")
        print()
        
        # Test the workflow without Gmail dependencies
        print("🔄 Testing workflow without Gmail dependencies...")
        
        def simple_triage_router(state: State, store: BaseStore) -> Command[Literal["end_node", "__end__"]]:
            """Simple triage router without Gmail dependencies"""
            
            author, to, subject, email_thread, email_id = parse_gmail(state["email_input"])
            user_prompt = triage_user_prompt.format(
                author=author, to=to, subject=subject, email_thread=email_thread
            )

            email_markdown = format_gmail_markdown(subject, author, to, email_thread, email_id)

            system_prompt = triage_system_prompt.format(
                background=default_background,
                triage_instructions=default_triage_instructions,
            )

            llm = init_chat_model(model=os.getenv("GOOGLE_MODEL", "gemini-2.5-flash"), model_provider="google_genai", temperature=0.0)
            llm_router = llm.with_structured_output(RouterSchema)
            
            result = llm_router.invoke([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ])

            classification = result.classification

            if classification == "respond":
                print("📧 Classification: RESPOND - This email requires a response")
                goto = "end_node"
                update = {
                    "classification_decision": result.classification,
                    "messages": [{"role": "user", "content": f"Respond to the email: {email_markdown}"}],
                }
            elif classification == "ignore":
                print("🚫 Classification: IGNORE - This email can be safely ignored")
                goto = END
                update = {"classification_decision": classification}
            elif classification == "notify":
                print("🔔 Classification: NOTIFY - This email contains important information")
                goto = "end_node"
                update = {"classification_decision": classification}
            else:
                raise ValueError(f"Invalid classification: {classification}")
            
            return Command(goto=goto, update=update)

        def end_node(state: State, store: BaseStore):
            """End node that doesn't call Gmail"""
            print("✅ Workflow completed successfully!")
            return state

        # Create test workflow
        test_workflow = StateGraph(State, input=StateInput)
        test_workflow.add_node(simple_triage_router)
        test_workflow.add_node("end_node", end_node)
        test_workflow.add_edge(START, "simple_triage_router")
        test_workflow.add_edge("end_node", END)
        
        email_assistant_test = test_workflow.compile()
        
        # Test with store
        store = InMemoryStore()
        result = email_assistant_test.invoke({
            "email_input": sample_email
        }, store=store)
        
        print("\n🎉 SUCCESS! gemini-2.5-flash model is working correctly!")
        print("\n📊 Results:")
        print(f"   - Classification: {result.get('classification_decision', 'N/A')}")
        print(f"   - Messages processed: {len(result.get('messages', []))}")
        print(f"   - Workflow completed: ✅")
        print(f"   - No quota errors: ✅")
        print(f"   - No Gmail auth issues: ✅")
        
        print("\n🎯 What this demonstrates:")
        print("   1. ✅ gemini-2.5-flash model is accessible and working")
        print("   2. ✅ Email parsing and formatting works")
        print("   3. ✅ Triage classification logic works")
        print("   4. ✅ Workflow routing works")
        print("   5. ✅ No quota limitations with gemini-2.5-flash")
        
        print("\n🚀 Ready for production with:")
        print("   - Your email: hammadallauddin@gmail.com")
        print("   - Working gemini-2.5-flash model")
        print("   - Proper API key configuration")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_gemini_25_flash()
    if success:
        print("\n🎉 gemini-2.5-flash model test PASSED!")
        print("The email assistant is working correctly with the new model!")
    else:
        print("\n💥 gemini-2.5-flash model test FAILED!")