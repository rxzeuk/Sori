import argparse

from demo.orchestrator import Orchestrator
from demo.tools.registry import build_tool_registry


def main():
    ap = argparse.ArgumentParser(prog="llm-tools-demo")
    ap.add_argument("--model", default="gpt-5-nano")
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("--max-steps", type=int, default=6)
    args = ap.parse_args()

    tools = build_tool_registry()
    orch = Orchestrator(
        model=args.model,
        tools=tools,
        max_steps=args.max_steps,
        verbose=args.verbose,
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


if __name__ == "__main__":
    main()
