#!/usr/bin/env python3

import argparse
import asyncio
import os

from telethon import TelegramClient


async def main():
    parser = argparse.ArgumentParser(
        description="Send lines from a text file to a Telegram bot."
    )

    parser.add_argument(
        "input",
        help="Input TXT file, one message per line",
    )

    parser.add_argument(
        "--bot",
        required=True,
        help="Telegram bot username, e.g. @my_test_bot",
    )

    parser.add_argument(
        "--output-dir",
        default="results",
        help="Directory for input/output files (default: results)",
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay between requests in seconds (default: 1.0)",
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=60.0,
        help="Maximum time to wait for bot response (default: 60s)",
    )

    args = parser.parse_args()

    api_id = os.environ.get("TELEGRAM_API_ID")
    api_hash = os.environ.get("TELEGRAM_API_HASH")

    if not api_id or not api_hash:
        raise RuntimeError(
            "Set TELEGRAM_API_ID and TELEGRAM_API_HASH environment variables."
        )

    api_id = int(api_id)

    os.makedirs(args.output_dir, exist_ok=True)

    with open(args.input, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\r\n") for line in f]

    # Skip empty lines
    lines = [line for line in lines if line]

    client = TelegramClient(
        "telegram_session",
        api_id,
        api_hash,
    )

    await client.start()

    async with client.conversation(
        args.bot,
        timeout=args.timeout,
    ) as conv:

        for i, text in enumerate(lines, start=1):
            seq = f"{i:05d}"

            input_path = os.path.join(
                args.output_dir,
                f"input_{seq}.txt",
            )

            output_path = os.path.join(
                args.output_dir,
                f"output_{seq}.txt",
            )

            # Save original input
            with open(input_path, "w", encoding="utf-8") as f:
                f.write(text)

            print(f"[{i}/{len(lines)}] SEND: {text}")

            try:
                sent = await conv.send_message(text)

                response = await conv.get_response(
                    sent,
                    timeout=args.timeout,
                )

                reply = response.raw_text or ""

                print(f"            REPLY: {reply}")

            except asyncio.TimeoutError:
                reply = "<TIMEOUT>"
                print("            REPLY: TIMEOUT")

            except Exception as e:
                reply = f"<ERROR: {e}>"
                print(f"            ERROR: {e}")

            # Save bot response
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(reply)

            if i < len(lines):
                await asyncio.sleep(args.delay)

    await client.disconnect()

    print()
    print(f"Done. Results saved to: {args.output_dir}")


if __name__ == "__main__":
    asyncio.run(main())
