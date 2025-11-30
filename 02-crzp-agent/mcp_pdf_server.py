# mcp_pdf_server.py
import subprocess
import atexit
import time

class MCPPdfServer:
    """
    Starts the document-loader MCP server as a subprocess
    and handles termination on exit.
    """
    def __init__(self):
        self.proc = None

    def start(self):
        """Start the MCP server subprocess"""
        self.proc = subprocess.Popen(
            ["uvx","pymupdf4llm-mcp@latest"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        # Give server some time to start
        time.sleep(5)
        print("MCP server started on stdio")

        # Ensure the process is terminated when Python exits
        atexit.register(self.stop)

    def stop(self):
        """Terminate the MCP server"""
        if self.proc:
            self.proc.terminate()
            self.proc.wait()
            print("MCP server stopped")
