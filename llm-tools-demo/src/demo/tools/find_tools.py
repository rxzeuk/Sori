import shlex
import subprocess


find_tool = {
    "type": "function",
    "function": {
        "name": "find_files",
        "description": "Run a file lookup tool against a provided path string.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path string to pass to find.",
                }
            },
            "required": ["file_path"],
        },
    },
}


def find_files(file_path: str) -> dict:
    result = subprocess.run(["find", file_path], capture_output=True, text=True, check=False, shell=True)
    return {
        "args": ["find", file_path],
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }
