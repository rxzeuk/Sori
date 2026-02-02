from demo.tools.system_command_tool import run_command, system_command_tool
from demo.tools.weather_tool import get_weather, weather_tool


def build_tool_registry() -> dict:
    return {
        "tools": [weather_tool, system_command_tool],
        "handlers": {
            "get_weather": get_weather,
            "run_command": run_command,
        },
    }
