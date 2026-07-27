"""
Namespace Demo - Shows all four state namespaces
Demonstrates temp:, session, user:, and app: persistence scopes.

Reference: https://github.com/google/adk-docs/blob/main/docs/sessions/state.md
"""

from google.adk.agents import LlmAgent
from google.adk.agents.readonly_context import ReadonlyContext


def build_instruction(context: ReadonlyContext) -> str:
    state = context.state

    def get(key: str) -> str:
        value = state.get(key)
        return str(value) if value not in (None, "") else "not set"

    return f"""
    You are a demo assistant showing state namespaces.

    === App State (global for all users) ===
    App name: {get('app:name')}
    App version: {get('app:version')}

    === User State (persists across sessions) ===
    User preference: {get('user:theme')}

    === Session State (persists this conversation) ===
    Conversation topic: {get('topic')}

    === Temp State (current turn only) ===
    Current step: {get('temp:step')}

    Respond with a friendly message showing these namespace values exactly as
    given above, including "not set" where shown.
"""


root_agent = LlmAgent(
    model = 'gemini-2.5-flash',
    name = 'namespace_demo',
    instruction = build_instruction,
    output_key = "response"
)
