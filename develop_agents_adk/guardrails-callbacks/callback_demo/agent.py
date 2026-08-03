"""
Simple Callback Demo Agent
Demonstrates basic callback usage for logging and observability.

Reference: https://adk.dev/callbacks/
"""

from google.adk.agents import LlmAgent

# Callback 1: Log when agent starts
def log_agent_start(callback_context, **kwargs):
    """Logs when agent begin processing a request."""
    print(f"\n{'='*50}")
    print(f"[AGENT START]")
    print(f" Invocation ID: {callback_context.invocation_id}")
    print(f" Session ID: {callback_context.session.id}")
    print(f"\n{'='*50}")
    return None # Proceed with normal execution

# Callback 2: Log when agent finishes
def log_agent_end(callback_context, **kwargs):
    """Logs when agent completes processing."""
    print(f"\n{'='*50}")
    print(f"[AGENT END]")
    print(f" Response generated successfully")
    print(f"\n{'='*50}")
    return None # Use original response

# Callback 3: Log LLM calls
def log_model_call(callback_context, llm_request, **kwargs):
    """Logs LLM requests."""
    print(f"\n[MODEL CALL] Sending request to LLM")
    return None # Proceed to LLM

# Callback 4: Log LLM responses
def log_model_response(callback_context, llm_response, **kwargs):
    """Logs LLM responses."""
    print(f"\n[MODEL RESPONSE] Receiving response from LLM")
    return None # Use original response

# Create agent with logging callbacks
root_agent = LlmAgent(
    model = 'gemini-2.5-flash',
    name = 'callback_demo',
    description = 'Demonstrates callback usage for logging.',
    instruction = """
    You are a helpful assistant.
    Answer questions clearly and concisely.
    """,
    before_agent_callback = log_agent_start,
    after_agent_callback = log_agent_end,
    before_model_callback = log_model_call,
    after_model_callback = log_model_response
)

