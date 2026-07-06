notes_db = []


def calculator(expression: str):
    try:
        return eval(expression)
    except Exception as e:
        return f"error: {e}"


def get_weather(city: str):
    fake_weather_db = {
        "kochi": "31 C, humid",
        "kannur": "29 C, light rain",
        "delhi": "38 C, sunny"
    }
    return fake_weather_db.get(city.lower(), "weather data not available")


def save_note(note: str):
    notes_db.append(note)
    return f"saved note: '{note}' (total notes: {len(notes_db)})"


def list_notes():
    if not notes_db:
        return "no notes saved yet"
    return notes_db


TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluates a basic math expression like '5 + 3'",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Gets current weather for a given city name",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_note",
            "description": "Saves a short text note for the user to remember later",
            "parameters": {
                "type": "object",
                "properties": {"note": {"type": "string"}},
                "required": ["note"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_notes",
            "description": "Lists all notes saved so far",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]


def run_tool(tool_name: str, tool_input: dict):
    if tool_name == "calculator":
        return calculator(tool_input["expression"])
    elif tool_name == "get_weather":
        return get_weather(tool_input["city"])
    elif tool_name == "save_note":
        return save_note(tool_input["note"])
    elif tool_name == "list_notes":
        return list_notes()
    else:
        return "unknown tool requested"