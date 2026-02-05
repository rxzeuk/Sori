import shlex
import subprocess


read_file_tool = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "Read a file.",
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


def read_file(file_path: str) -> dict:
    split_file_path = shlex.split(file_path)
    result = subprocess.run(["cat", *split_file_path], capture_output=True, text=True, check=False)
    return {
        "args": ["cat", *split_file_path],
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }