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
    parts = shlex.split(command)
    if not parts:
        return {"error": "empty command"}
    try:
        result = subprocess.run(parts, capture_output=True, text=True, check=False)
    except Exception as exc:
        return {"error": str(exc)}
    return {
        "args": parts,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }
