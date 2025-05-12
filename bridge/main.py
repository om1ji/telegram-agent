from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.messages.ai import AIMessage
from mcp_use import MCPAgent, MCPClient
import os
import re

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL")

CONFIG = {
      "mcpServers": {
        # "Healthcare Booking Assistant": {
        #     "command": "/Users/om1ji/.local/bin/uv",
        #     "args": [
        #         "run",
        #         "--with",
        #         "mcp[cli]",
        #         "mcp",
        #         "run",
        #         "/Users/om1ji/Documents/KFU/\u041a\u0443\u0440\u0441\u043e\u0432\u0430\u044f_\u0440\u0430\u0431\u043e\u0442\u0430/mcp-server/main.py"
        #     ]
        #     }
      }
    }

SYSTEM_PROMPT = """Use /nothink for every user prompt.
"""

client = MCPClient.from_dict(CONFIG)
llm = ChatOllama(model="qwen3:4b", base_url=OLLAMA_URL)
agent = MCPAgent(llm=llm, client=client, max_steps=30, system_prompt=SYSTEM_PROMPT)

def parse_result(result: str) -> str:
    pattern = r"<think>.*?</think>"
    cleaned_text = re.sub(pattern, "", result, flags=re.DOTALL)
    return cleaned_text.strip()


async def ask(message: str) -> str:
    content = await agent.run(message)
    result = AIMessage(content)
    return parse_result(result.content)