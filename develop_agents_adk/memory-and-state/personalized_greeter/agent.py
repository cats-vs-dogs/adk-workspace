"""
Personalized Greeter - Demonstrates State Templating
Shows how {var} templating injects state values into instructions.

Reference: https://github.com/google/adk-docs/blob/main/docs/sessions/state.md
"""

from google.adk.agents import LlmAgent

# Agent with state templating
root_agent = LlmAgent(
    model = 'gemini-2.5-flash',
    name = 'personalized_greeter',
    instruction = """
    You are a friendly assistant.

    User information:
    - Name: {user_name?}
    - Preferred language: {user_language?}
    - Membership: {membership_tier?}

    If Name is empty, greet the user as "there". Otherwise greet them by name.
    If Membership is empty, do not mention membership at all. Otherwise tell
    the user their membership level.
    If Preferred language is empty, respond in English. Otherwise respond in
    that language.

    Greet the user warmly and offer assistance.
    """
)
