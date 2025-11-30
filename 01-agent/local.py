from agent import run_agent

# Ask the agent a question that uses the available tools
message = """
    I have 3 requests:

    1. What is the time right now?
    2. Calculate 3111696 / 74088
    3. Tell me how many letter R's are in the word "strawberry"
    """

run_agent(message=message)