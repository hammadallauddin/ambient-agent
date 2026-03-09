#!/usr/bin/env python3
"""
Simple test script for email assistant triage functionality
"""

from typing import Literal
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langgraph.store.base import BaseStore
from langgraph.store.memory import InMemoryStore
from langgraph.types import interrupt, Command

from email_assistant.tools import get_tools, get_tools_by_name
from email_assistant.tools.gmail.prompt_templates import GMAIL_TOOLS_PROMPT
from email_assistant.tools.gmail.gmail_tools import mark_as_read
from email_assistant.prompts import triage_system_prompt, triage_user_prompt, agent_system_prompt_hitl_memory, default_triage_instructions, default_background, default_response_preferences, default_cal_preferences, MEMORY_UPDATE_INSTRUCTIONS, MEMORY_UPDATE_INSTRUCTIONS_REINFORCEMENT
from email_assistant.schemas import State, RouterSchema, StateInput, UserPreferences
from email_assistant.utils import parse_gmail, format_for_display, format_gmail_markdown

def get_memory(store, namespace, default_content=None):
    """Get memory from the store or initialize with default if it doesn't exist."""
    if store is None:
        return default_content
    
    user_preferences = store.get(namespace, "user_preferences")
    if user_preferences:
        return user_preferences.value
    else:
        store.put(namespace, "user_preferences", default_content)
        return default_content 

def triage_router(state: State, store: BaseStore) -> Command[Literal["mark_as_read_node", "__end__"]]:
    """Analyze email content to decide if we should respond, notify, or ignore."""
    
    author, to, subject, email_thread, email_id = parse_gmail(state["email_input"])
    user_prompt = triage_user_prompt.format(
        author=author, to=to, subject=subject, email_thread=email_thread
    )

    email_markdown = format_gmail_markdown(subject, author, to, email_thread, email_id)
    triage_instructions = get_memory(store, ("email_assistant", "triage_preferences"), default_triage_instructions)

    system_prompt = triage_system_prompt.format(
        background=default_background,
        triage_instructions=triage_instructions,
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
        goto = "mark_as_read_node"
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
        goto = "mark_as_read_node"
        update = {"classification_decision": classification}
    else:
        raise ValueError(f"Invalid classification: {classification}")
    
    return Command(goto=goto, update=update)

def mark_as_read_node(state: State, store: BaseStore):
    """Mark email as read"""
    email_input = state["email_input"]
    author, to, subject, email_thread, email_id = parse_gmail(email_input)
    mark_as_read(email_id)

def test_simple_triage():
    """Test the email assistant triage with a sample email"""
    
    # Sample email in Gmail format
    sample_email = {
        "from": "john.doe@example.com",
        "to": "you@example.com", 
        "subject": "Meeting Request for Project Discussion",
        "body": "Hi there,\n\nI hope you're doing well. I'd like to schedule a meeting to discuss the upcoming project timeline. Are you available next Tuesday at 2 PM?\n\nBest regards,\nJohn",
        "id": "test_email_123"
    }
    
    print("Testing email assistant triage with sample email...")
    print(f"Email: {sample_email['subject']}")
    print(f"From: {sample_email['from']}")
    print(f"Body: {sample_email['body'][:100]}...")
    print()
    
    try:
        # Create an in-memory store for testing
        store = InMemoryStore()
        
        # Create a simple test workflow
        test_workflow = StateGraph(State, input=StateInput)
        test_workflow.add_node(triage_router)
        test_workflow.add_node("mark_as_read_node", mark_as_read_node)
        test_workflow.add_edge(START, "triage_router")
        test_workflow.add_edge("mark_as_read_node", END)
        
        email_assistant_test = test_workflow.compile()
        
        # Test the assistant with the store
        result = email_assistant_test.invoke({
            "email_input": sample_email
        }, store=store)
        
        print("✅ Email assistant triage ran successfully!")
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
    success = test_simple_triage()
    if success:
        print("\n🎉 Email assistant triage is working correctly!")
    else:
        print("\n💥 Email assistant triage has issues that need to be fixed.")