"""One Line, One Laugh entry.

Writes a single funny line to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR).
The line is a fixed literal: no input, no network, no randomness, so the
output is byte-identical on every run.
"""

import os

LINE = "My therapist fired me for making too much progress in the waiting room."


def main() -> None:
    text = LINE
    assert 1 <= len(text) <= 200, f"line is {len(text)} chars, gate needs 1-200"
    assert text.strip(), "line must not be only whitespace"
    assert "\n" not in text, "entry must be a single line"

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Atomic write: a crash mid-write can never leave a torn entry.txt.
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    os.replace(tmp_path, path)

    with open(path, "rb") as f:
        written = f.read()
    assert written == text.encode("utf-8"), "read-back mismatch"
    assert written == LINE.encode("utf-8")
    assert len(written) == 71, f"entry must be 71 bytes, got {len(written)}"


if __name__ == "__main__":
    main()
