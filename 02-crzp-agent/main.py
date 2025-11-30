"""Main entry point for the Thesis Search Assistant."""

from strands import Agent
from mcp import stdio_client, StdioServerParameters
from strands.tools.mcp import MCPClient
from mcp_pdf_server import MCPPdfServer
from czrp_scraper import thesis_fetch, thesis_abstract_fetch, thesis_retrieve_pdf_if_available


def display_welcome_message():
    """Display welcome message to the user."""
    print("=" * 60)
    print("Welcome to the Thesis Search Assistant!")
    print("=" * 60)
    print("\nI can help you search for diploma theses in Slovakia.")
    print("You can:")
    print("  - Search for theses by topic area")
    print("  - Request abstracts for specific theses")
    print("\nType 'exit', 'quit', or 'bye' to end the conversation.")
    print("=" * 60)
    print()


def is_exit_command(user_input: str) -> bool:
    """Check if user input is an exit command."""
    return user_input.lower().strip() in ['exit', 'quit', 'bye']


def run_conversation_loop(agent: Agent):
    """
    Run the conversational loop with the user.
    
    Handles user input, calls agent.run() for each message, and displays responses.
    Exits when user enters an exit command (exit, quit, bye).
    """
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            # Check for exit command
            if is_exit_command(user_input):
                print("\nGoodbye! Thank you for using the Thesis Search Assistant.")
                break
            
            # Skip empty input
            if not user_input:
                continue
            
            # Call agent with user input (Agent is callable)
            result = agent(user_input)
            
            # Display agent response (AgentResult converts to string)
            print(f"\nAssistant: {result}\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! Thank you for using the Thesis Search Assistant.")
            break
        except Exception as e:
            print(f"\nError: {e}\n")
            print("Please try again or type 'exit' to quit.\n")


def main():
    """Initialize the Agent and start the application."""
    # Display welcome message
    display_welcome_message()


    # System prompt with instructions for CRZP interaction
    system_prompt = """You are a helpful assistant that helps users search for diploma theses in the Slovak CRZP repository.

CRZP Repository Information:
- Website: https://opac.crzp.sk
- This is the Slovak national repository for diploma theses
- Content is primarily in Slovak language

Your Capabilities:
1. Search for theses by topic area
2. Retrieve thesis keywords

How to Search CRZP:
1. To search for theses, use the thesis_fetch tool to access the CRZP search interface

How to Parse Search Results:
1. Search results are in csv format
2. They they contain:
   - Thesis title
   - Whether PDF is available for download and further analysis
   - Keywords, that label the thesis

Important Guidelines:
- Never make direct HTTP requests
- Handle Slovak language content properly (UTF-8 encoding)
- If search returns no results, inform the user clearly
- Be helpful and conversational in your responses
- Format thesis information in a readable way for users
- Always show the thesis id, the sequential number in the search results, so it's easier for user to refer it as well

Error Handling:
- If you cannot find specific information, be honest with the user"""

    # start mcp pdf server
    server = MCPPdfServer()
    server.start()

    # initialize mcp client
    pdf_mcp_client = MCPClient(
        lambda: stdio_client(
            StdioServerParameters(
                command="uvx",
                args=["pymupdf4llm-mcp@latest", "stdio"]
            )
        )
    )

    # Manual lifecycle management
    with pdf_mcp_client:
        # Get the tools from the MCP server
        mcp_tools = pdf_mcp_client.list_tools_sync()

        # Initialize Agent with Amazon Nova Pro model and http_request tool
        # The strands.Agent handles AWS Bedrock authentication automatically
        # using credentials from ~/.aws/credentials or ~/.aws/config
        agent = Agent(
            model="amazon.nova-pro-v1:0",
            tools=[thesis_fetch, thesis_abstract_fetch, thesis_retrieve_pdf_if_available, mcp_tools],
            system_prompt=system_prompt
        )

        print("\nAssistant initialized successfully!")
        print("Ready to help you search for theses.\n")

        # Start conversation loop
        run_conversation_loop(agent)


if __name__ == "__main__":
    main()
