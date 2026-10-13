#!/usr/bin/env python3
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

HOST = "172.24.77.24"
USER = "anonymous"
PASSWORD = ""


def pause(msg="Press Enter to close this window..."):
    print("\n" + "=" * 41)
    try:
        input(msg)
    except (EOFError, KeyboardInterrupt):
        pass


def clean_path(raw):
    """Handle drag-and-drop quirks: wrapping quotes, backslash-escaped spaces, ~."""
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "'\"":
        raw = raw[1:-1]
    elif sys.platform != "win32":
        raw = re.sub(r"\\(.)", r"\1", raw)
    return Path(raw).expanduser()


def run_printer_upload():
    if shutil.which("curl") is None:
        print("System Error: 'curl' is not installed on this system.")
        print("Please install curl to run this script.")
        return 1

    print("=========================================")
    print("      Dont be stupid pls        ")
    print("=========================================\n")

    print("Step 1: Provide the file you want to print.")
    raw = input("   Drag & drop the file here or type the path: ")
    local_file = clean_path(raw)

    if not local_file.is_file():
        print(f"\nError: File '{local_file}' not found.")
        print("Please check the path and try again.")
        return 1

    remote_filename = local_file.name

    print("\nStep 2: Select transfer format.")
    print("   [1] Binary mode (PDFs, images, PostScript, PCL) - RECOMMENDED")
    print("   [2] ASCII mode  (plain text, logs, script files)")
    choice = input("   Enter choice (1 or 2, default is 1): ").strip()
    ascii_mode = choice == "2"
    mode_text = "ASCII" if ascii_mode else "Binary"

    print("\nStep 3: Number of copies.")
    copies_input = input("   Enter how many copies you want (default is 1): ").strip()
    try:
        copies = int(copies_input) if copies_input else 1
    except ValueError:
        print("   Invalid input. Defaulting to 1 copy.")
        copies = 1
    if copies < 1:
        copies = 1

    ftp_url = f"ftp://{HOST}/lp/{quote(remote_filename, safe='')}"

    cmd = [
        "curl",
        "--silent", "--show-error",
        "--globoff",
        "--connect-timeout", "10",
        "--user", f"{USER}:{PASSWORD}",
    ]
    if ascii_mode:
        cmd.append("--use-ascii")
    cmd += ["-T", str(local_file), ftp_url]

    print(f"\nSending '{remote_filename}' ({copies} copy/copies) via {mode_text} mode...")

    sent = 0
    for i in range(1, copies + 1):
        if copies > 1:
            print(f"   Sending copy {i} of {copies}...")
        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            detail = (e.stderr or "").strip() or "No details from curl."
            print(f"\nCurl error (exit {e.returncode}) on copy {i}: {detail}")
            print(f"{sent} of {copies} copies were sent before the failure.")
            return 1
        sent += 1

    print("\nSuccess! The file has been sent to the printer queue.")
    return 0


if __name__ == "__main__":
    try:
        code = run_printer_upload()
    except KeyboardInterrupt:
        print("\nCancelled.")
        code = 130
    pause("Process finished. Press Enter to close this window...")
    sys.exit(code)
