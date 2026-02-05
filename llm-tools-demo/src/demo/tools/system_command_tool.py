import shlex
import subprocess

system_command_tool = {
    "type": "function",
    "function": {
        "name": "run_command",
        "description": "Run system command.",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "A full command, including any arguments.",
                },
            },
            "required": ["command"],
        },
    },
}


def run_command(command: str) -> dict:
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False, shell=True)
    except Exception as exc:
        return {"error": str(exc)}
    return {
        "args": command,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }
