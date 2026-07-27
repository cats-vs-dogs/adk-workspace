"""
Test state namespaces to see persistence differences.
Run with: python test_namespaces.py
"""

import asyncio

from dotenv import load_dotenv
load_dotenv(dotenv_path="../../../.env", override=True)

from agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part


async def main():
    # Setup
    session_service = InMemorySessionService()
    runner = Runner(
        agent = root_agent,
        app_name = "namespace_demo_app",
        session_service = session_service
    )

    # Set app/user/session state at creation time (temp: is turn-scoped and
    # can only be injected per-run via run_async's state_delta, not stored here).
    print("=== Setting state in all namespaces ===")
    session = await session_service.create_session(
        app_name = "namespace_demo_app",
        user_id = "user1",
        session_id = "session1",
        state = {
            "app:name": "Namespace Demo",
            "app:version": "2.0",
            "user:theme": "dark",
            "topic": "state management",
        }
    )
    temp_step_turn1 = "initialization"
    state_preview = {**session.state, "temp:step": temp_step_turn1}
    print(f"State before run: {state_preview}\n")

    # Run agent (Turn 1), injecting temp:step for this turn only
    print("=== Running agent (Turn 1) ===")
    async for event in runner.run_async(
        user_id = "user1",
        session_id = "session1",
        new_message = Content(parts = [Part(text = "Show me the namespace values")]),
        state_delta = {"temp:step": temp_step_turn1}
    ):
        if event.is_final_response():
            print(f"Agent response:\n{event.content.parts[0].text}\n")

    # Check state after turn
    session = await session_service.get_session(
        app_name = "namespace_demo_app", user_id = "user1", session_id = "session1"
    )
    print("=== State after Turn 1 ===")
    print(f"Full state: {session.state}")
    print(f"temp:step: {session.state.get('temp:step')}") # gone
    print(f"topic: {session.state.get('topic')}") # persist
    print(f"user:theme: {session.state.get('user:theme')}") # persist
    print(f"app:version: {session.state.get('app:version')}") # persist


    print("\n=== Simulating Turn 2 (same session) ===")
    async for event in runner.run_async(
        user_id = "user1",
        session_id = "session1",
        new_message = Content(parts = [Part(text = "Check state again")])
    ):
        if event.is_final_response():
            print(f"Agent response:\n{event.content.parts[0].text}\n")

    # Check state after turn
    session = await session_service.get_session(
        app_name = "namespace_demo_app", user_id = "user1", session_id = "session1"
    )
    print("=== State after Turn 2 ===")
    print(f"Full state: {session.state}")
    print(f"temp:step: {session.state.get('temp:step')}") # still gone
    print(f"topic: {session.state.get('topic')}") # persist
    print(f"user:theme: {session.state.get('user:theme')}") # persist
    print(f"app:version: {session.state.get('app:version')}") # persist


    # Simulate new session
    print("\n=== Simulating NEW Session (session2) ===")
    session2 = await session_service.create_session(
        app_name = "namespace_demo_app",
        user_id = "user1", # Same user
        session_id = "session2" # Different session
    )

    print(f"New session state: {session2.state}")
    print(f"topic: {session2.state.get('topic')}") # gone (was session-scoped)
    print(f"user:theme: {session2.state.get('user:theme')}") # persisted across sessions
    print(f"app:version: {session2.state.get('app:version')}") # persisted globally


if __name__ == "__main__":
    asyncio.run(main())
