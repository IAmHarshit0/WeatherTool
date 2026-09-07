import os
import sys

from ollama import chat
from pydantic import ValidationError

from .models import WeatherResponse
from .tool import get_weather

MODEL_NAME = os.getenv("OLLAMA_MODEL", "qwen3.5:4b")

TOOLS = {
    get_weather.__name__: get_weather,
}


def execute_tool_call(fn_name: str, fn_args: dict) -> str:
    if fn_name not in TOOLS:
        return f"Error: Tool '{fn_name}' does not exist."

    try:
        result = TOOLS[fn_name](**fn_args)

        if isinstance(result, WeatherResponse):
            return result.model_dump_json()
        return str(result)

    except ValidationError as err:
        return f"Invalid tool arguments: {err}"
    except (ValueError, RuntimeError) as err:
        return str(err)


def run_chat():
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant. Use the `get_weather` tool whenever "
                "a user asks about current weather conditions for any location."
            ),
        }
    ]

    print("=" * 50)
    print("  AdhokAI Assignment: Weather Tool-Calling Agent")
    print(f"  Model: {MODEL_NAME}")
    print("  Type 'exit' or 'quit' to end the session.")
    print("=" * 50 + "\n")

    while True:
        try:
            user_input = input("You > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit"):
                print("Goodbye!")
                break

            messages.append({"role": "user", "content": user_input})

            while True:
                response = chat(
                    model=MODEL_NAME,
                    messages=messages,
                    tools=[get_weather],
                )
                messages.append(response.message)

                if not response.message.tool_calls:
                    print(f"Assistant > {response.message.content}\n")
                    break

                for call in response.message.tool_calls:
                    fn_name = call.function.name
                    fn_args = call.function.arguments

                    # Clean, minimal log outputs
                    print(f"[Tool: {fn_name}] Args: {fn_args}")

                    result_str = execute_tool_call(fn_name, fn_args)

                    print(f"[Result]: {result_str}\n")

                    messages.append({
                        "role": "tool",
                        "tool_name": fn_name,
                        "content": result_str,
                    })

        except (KeyboardInterrupt, EOFError):
            print("\nSession terminated.")
            sys.exit(0)


if __name__ == "__main__":
    run_chat()