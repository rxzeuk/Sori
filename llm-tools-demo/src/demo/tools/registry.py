from demo.tools.curl_tool import run_curl, curl_tool
from demo.tools.find_tools import find_files, find_tool
from demo.tools.system_command_tool import run_command, system_command_tool
from demo.tools.weather_tool import get_weather, weather_tool
from demo.tools.read_file_tools import read_file, read_file_tool


# all tools
# def build_tool_registry() -> dict:
#     return {
#         "tools": [weather_tool, system_command_tool, find_tool, curl_tool],
#         "handlers": {
#             "get_weather": get_weather,
#             "run_command": run_command,
#             "find_files": find_files,
#             "run_curl": run_curl,
#         },
#     }

# read file task in prompt
# def build_tool_registry() -> dict:
#     return {
#         "tools": [read_file_tool],
#         "handlers": {
#             "read_file": read_file,
#         },
#     }


# instructions injection
def build_tool_registry() -> dict:
    return {
        "tools": [system_command_tool, read_file_tool],
        "handlers": {
            "run_command": run_command,
            "read_file": read_file,
        },
    }

# no context demo
def build_tool_registry() -> dict:
    return {
        "tools": [system_command_tool],
        "handlers": {
            "run_command": run_command,
        },
    }