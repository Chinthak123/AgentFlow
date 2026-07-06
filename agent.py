import os
import json
from groq import Groq
from dotenv import load_dotenv
from tools import TOOL_SCHEMAS, run_tool

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set")

client = Groq(api_key=GROQ_API_KEY)

MODEL_NAME = "llama-3.3-70b-versatile"


def run_agent(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]

    max_loops = 6

    for _ in range(max_loops):

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=TOOL_SCHEMAS,
            tool_choice="auto"
        )

        response_message = response.choices[0].message
        messages.append(response_message)

        tool_calls = response_message.tool_calls

        if tool_calls:
            for call in tool_calls:
                tool_name = call.function.name
                tool_input = json.loads(call.function.arguments)

                result = run_tool(tool_name, tool_input)

                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "name": tool_name,
                    "content": str(result)
                })

            continue

        else:
            return response_message.content

    return "Agent stopped: too many steps taken (possible loop)."