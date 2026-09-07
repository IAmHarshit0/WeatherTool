# Weather Tool-Calling Agent

A small CLI application that demonstrates LLM tool calling using a local model.

The user can ask for the current weather in natural language. The LLM decides when the weather tool is needed, calls it with the requested city, and uses the returned data to form the final response.

## How it works

```text
User
  ↓
Local LLM
  ↓
Tool call (if needed)
  ↓
Weather tool
  ↓
OpenWeather API
  ↓
Weather result
  ↓
Local LLM
  ↓
Response
```

For example:

```text
You > What's the weather in Hyderabad?
[Tool: get_weather] Args: {'city': 'Hyderabad'}
[Result]: {"condition":"Clear sky","temperature":27.61,"humidity":79}

Assistant > The current weather in Hyderabad is:

- **Condition**: Clear sky
- **Temperature**: 27.61°C
- **Humidity**: 79%

It looks like Hyderabad is experiencing pleasant weather with clear skies and comfortable temperature today.
```

For questions that don't require weather information, the tool is not called.

## Tech stack

- Python
- Ollama
- Qwen3.5 4B
- OpenWeather API
- Pydantic
- uv
- Pytest
- Ruff

## Project structure

```text
src/adhokai_weather_tool/
├── agent.py
├── main.py
├── models.py
└── tool.py

tests/
├── test_models.py
└── test_tool.py
```

- `agent.py` handles the LLM conversation and tool-calling loop.
- `tool.py` handles the weather API.
- `models.py` contains the request and response models.
- `main.py` starts the application.

## Setup

Make sure Ollama is installed and the `qwen3.5:4b` model is available.

Create a `.env` file:

```env
OPENWEATHER_API_KEY=your_api_key
```

Install the dependencies:

```bash
uv sync
```

Run the application:

```bash
uv run python -m adhokai_weather_tool.main
```

## Testing

Run the tests:

```bash
uv run pytest
```

Run the linter:

```bash
uv run ruff check .
```

## Design note

I kept the implementation intentionally small and used Ollama's native tool-calling interface instead of an agent framework.

The main goal was to keep the tool-calling flow explicit and easy to follow:

```text
LLM → tool call → validation → tool execution → result → LLM
```