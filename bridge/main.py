import asyncio
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from mcp_use import MCPAgent, MCPClient

async def main():
    # Load environment variables
    load_dotenv()

    # Create configuration dictionary
    config = {
      "mcpServers": {
        "Healthcare Booking Assistant": {
            "command": "/Users/om1ji/.local/bin/uv",
            "args": [
                "run",
                "--with",
                "mcp[cli]",
                "mcp",
                "run",
                "/Users/om1ji/Documents/KFU/\u041a\u0443\u0440\u0441\u043e\u0432\u0430\u044f_\u0440\u0430\u0431\u043e\u0442\u0430/mcp-server/main.py"
            ]
            }
      }
    }

    client = MCPClient.from_dict(config)
    llm = ChatOllama(model="qwen3:14b")
    agent = MCPAgent(llm=llm, client=client, max_steps=30)

    result = await agent.run(
        "Какие специалисты есть у нас в Казани и как их зовут?",
    )
    print(f"\nResult: {result}")

if __name__ == "__main__":
    asyncio.run(main())