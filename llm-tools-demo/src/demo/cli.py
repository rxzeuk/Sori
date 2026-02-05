import argparse
from pprint import pformat
from pathlib import Path

from demo.orchestrator import Orchestrator
from demo.tools.registry import build_tool_registry


def main():
    ap = argparse.ArgumentParser(prog="llm-tools-demo")
    ap.add_argument("--model", default="gpt-5-nano", choices=["gpt-5-nano", "gpt-4.1-nano"])
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("--system-prompt", action="store_true")
    ap.add_argument("--show-messages", action="store_true")
    ap.add_argument("--max-steps", type=int, default=6)
    args = ap.parse_args()

    system_prompt = None
    if args.system_prompt:
        prompt_path = Path(__file__).with_name("system_prompt.txt")
        system_prompt = prompt_path.read_text(encoding="utf-8")

    tools = build_tool_registry()
    orch = Orchestrator(
        model=args.model,
        tools=tools,
        max_steps=args.max_steps,
        verbose=args.verbose,
        system_prompt=system_prompt,
    )

    # Simple REPL
    while True:
        try:
            user_text = input("user> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nbye.")
            break

        if not user_text:
            continue
        if user_text.lower() in {"quit", "exit"}:
            break

        if orch.stream:
            print("ai> ", end="", flush=True)
            answer = orch.run_turn(user_text)
            print()
        else:
            answer = orch.run_turn(user_text)
            print(f"ai> {answer}")

        if args.show_messages:
            for message in orch.messages:
                print(pformat(message))


if __name__ == "__main__":
    main()
