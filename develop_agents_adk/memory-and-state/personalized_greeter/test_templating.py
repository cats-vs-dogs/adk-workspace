"""
Test state templating with different state values.
Run with: python test_templating.py
"""

import asyncio

from dotenv import load_dotenv
load_dotenv(dotenv_path="../../../.env", override=True)

from agent import root_agent
from google.adk.events import Event
from google.adk.events.event_actions import EventActions
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part


async def main():
    # Setup
    session_service = InMemorySessionService()
    session = await session_service.create_session(
            app_name = "greeter_app",
            user_id = "user1",
            session_id = "session1"
        )
    runner = Runner(
        agent = root_agent,
        app_name = "greeter_app",
        session_service = session_service
    )
    # Test 1: No state set (all defaults)
    print("=== Test 1: No state (all defaults) ===")
    result1 =  runner.run(
        user_id = "user1",
        session_id = "session1",
        new_message = Content(parts = [Part(text = 'Hello')])
    )
    for event in result1:
        if event.is_final_response():
            print(f"Agent response: {event.content.parts[0].text}\n")


    # Test 2: Set user name only
    print("=== Test 2: With user name ===")
    await session_service.append_event(
        session,
        Event(author = "user", actions = EventActions(state_delta = {"user_name": "Alex"}))
    )
    result2 = runner.run(
        user_id = "user1",
        session_id = "session1",
        new_message = Content(parts = [Part(text = 'Hello again')])
    )
    for event in result2:
        if event.is_final_response():
            print(f"Agent response: {event.content.parts[0].text}\n")

    # Test 3: Set all state values
    print("=== Test 3: With all state values ===")
    await session_service.append_event(
        session,
        Event(author = "user", actions = EventActions(state_delta = {
            "user_name": "Alex",
            "user_language": "Spanish",
            "membership_tier": "premium",
        }))
    )
    result3 =  runner.run(
        user_id = "user1",
        session_id = "session1",
        new_message = Content(parts = [Part(text = 'Hola de nueva')])
    )
    for event in result3:
        if event.is_final_response():
            print(f"Agent response: {event.content.parts[0].text}\n")

    print("=== Current state ===")
    session = await session_service.get_session(
        app_name = "greeter_app",
        user_id = "user1",
        session_id = "session1"
    )
    print(session.state)


if __name__ == "__main__":
    asyncio.run(main())

