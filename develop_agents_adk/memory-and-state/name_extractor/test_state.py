"""
Test script to see state access directly.
Run with: python test_state.py
"""

import asyncio

from dotenv import load_dotenv
load_dotenv(dotenv_path="../../../.env", override=True)

from agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part


async def main():
    # Setup session and runner
    session_service = InMemorySessionService()

    session = await session_service.create_session(
        app_name = "name_extractor_app",
        user_id = "test_user",
        session_id = "test_session"
    )

    runner = Runner(
        agent = root_agent,
        app_name = "name_extractor_app",
        session_service = session_service
    )

    # Test: Extract name
    user_message = Content(parts=[Part(text = "Hi, my name is Dart Vader and I was a jedi knight that converted to the Dark Side.")])

    print("===== Running name extracting agent =====")
    async for event in runner.run_async(
        user_id = "test_user",
        session_id = "test_session",
        new_message = user_message
    ):
        if event.is_final_response():
            print(f"\nAgent response: {event.content.parts[0].text}")

    # Access state programmatically
    # Note: `session` is only a snapshot from creation time. The Runner updates its
    # own copy inside session_service, so we must re-fetch to see current state.
    session = await session_service.get_session(
        app_name = "name_extractor_app",
        user_id = "test_user",
        session_id = "test_session"
    )

    print(f"\n===== State after execution =====")
    print(f"Full state: {session.state}")
    print(f"Extracted name: {session.state.get('user_name')}")

    # Your code can now make decisions based on state
    if session.state.get('user_name'):
        print("Name was successfully extracted and stored!")
    else:
        print("Name extraction failed.")

    # Test accessing in subsequent turns
    user_message_2 = Content(parts=[Part(text = "What is my name?")])
    async for event in runner.run_async(
        user_id = "test_user",
        session_id = "test_session",
        new_message = user_message_2
    ):
        if event.is_final_response():
            print(f"\nAgent response: {event.content.parts[0].text}")

    session = await session_service.get_session(
        app_name = "name_extractor_app",
        user_id = "test_user",
        session_id = "test_session"
    )
    print(f"\nState still contains: {session.state.get('user_name')}")
    print("State persists across turns!")


if __name__ == "__main__":
    asyncio.run(main())
