import argparse
import sys

from guard import AdvancedPromptInput
from streamer import stream_local_ai


def main():
    parser = argparse.ArgumentParser(
        description="LocalOps Core Pipeline - CLI v1.0"
    )

    parser.add_argument(
        '--prompt',
        type=str,
        required=True,
        help='The prompt sent to the local LLM'
    )

    parser.add_argument(
        '--bypass_guard',
        action='store_true',
        help='Intentionally bypass the security guardrail'
    )

    args = parser.parse_args()

    if not args.bypass_guard:
        try:
            # Uses advanced validation including intent classification from Day 3
            AdvancedPromptInput(user_prompt=args.prompt)
        except ValueError as e:
            print(f"🛑 Pipeline Security Veto: {e}")
            sys.exit(1)

    stream_local_ai(args.prompt)


if __name__ == "__main__":
    main()

# For usage run in terminal:
# uv run python cli_app.py --prompt "How to kill process 1223?"