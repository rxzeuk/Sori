import json

from openai import OpenAI


class Orchestrator:
    def __init__(
        self,
        model: str,
        tools: dict,
        max_steps: int = 6,
        stream: bool = True,
        verbose: bool = False,
    ) -> None:
        self.client = OpenAI()
        self.model = model
        self.tools = tools["tools"]
        self.handlers = tools["handlers"]
        self.max_steps = max_steps
        self.stream = stream
        self.verbose = verbose
        self.messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    def run_turn(self, user_text: str) -> str:
        self.messages.append({"role": "user", "content": user_text})

        for _ in range(self.max_steps):
            if self.stream:
                text, tool_calls = self._call_llm_stream()
            else:
                text, tool_calls = self._call_llm()

            if tool_calls:
                self.messages.append(
                    {
                        "role": "assistant",
                        "content": text,
                        "tool_calls": [
                            {
                                "id": call["id"],
                                "type": "function",
                                "function": {
                                    "name": call["name"],
                                    "arguments": call["arguments"],
                                },
                            }
                            for call in tool_calls
                        ],
                    }
                )

                for call in tool_calls:
                    name = call["name"]
                    try:
                        args = json.loads(call.get("arguments") or "{}")
                    except json.JSONDecodeError:
                        args = {}
                    if self.verbose:
                        print(f"\n[tool call] {name} {args}", flush=True)
                    result = self._run_tool(name, args)
                    if self.verbose:
                        print(f"[tool result] {result}", flush=True)
                    self.messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": call["id"],
                            "name": name,
                            "content": json.dumps(result),
                        }
                    )
                continue

            self.messages.append({"role": "assistant", "content": text})
            return text

        return "Reached max steps without a final response."

    def _call_llm(self) -> tuple[str, list[dict]]:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            tools=self.tools,
            tool_choice="auto",
        )
        message = response.choices[0].message
        tool_calls = []
        for call in (message.tool_calls or []):
            tool_calls.append(
                {
                    "id": call.id,
                    "name": call.function.name,
                    "arguments": call.function.arguments,
                }
            )
        return message.content or "", tool_calls

    def _call_llm_stream(self) -> tuple[str, list[dict]]:
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            tools=self.tools,
            tool_choice="auto",
            stream=True,
        )

        text_parts = []
        tool_calls: dict[int, dict] = {}

        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                text_parts.append(delta.content)
                print(delta.content, end="", flush=True)

            if delta.tool_calls:
                for call in delta.tool_calls:
                    entry = tool_calls.get(call.index) or {
                        "id": call.id,
                        "name": None,
                        "arguments": "",
                    }
                    if call.id:
                        entry["id"] = call.id
                    if call.function and call.function.name:
                        entry["name"] = call.function.name
                    if call.function and call.function.arguments:
                        entry["arguments"] += call.function.arguments
                    tool_calls[call.index] = entry

        ordered_calls = [tool_calls[i] for i in sorted(tool_calls.keys())]
        for index, call in enumerate(ordered_calls, start=1):
            if not call.get("id"):
                call["id"] = f"toolcall-{index}"
            if call.get("name") is None:
                call["name"] = ""
        return "".join(text_parts), ordered_calls

    def _run_tool(self, name: str, args: dict) -> dict:
        handler = self.handlers.get(name)
        if not handler:
            return {"error": f"unknown tool: {name}"}
        try:
            return handler(**args)
        except Exception as exc:
            return {"error": str(exc)}
