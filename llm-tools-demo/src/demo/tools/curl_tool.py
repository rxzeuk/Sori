import subprocess
import shlex

curl_tool = {
    "type": "function",
    "function": {
        "name": "run_curl",
        "description": "Run curl against a provided URL.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL to request with curl.",
                }
            },
            "required": ["url"],
        },
    },
}


def run_curl(url: str) -> dict:
    result = subprocess.run(["curl", url], capture_output=True, text=True, check=False, shell=True)
    return {
        "args": ["curl", url],
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }
