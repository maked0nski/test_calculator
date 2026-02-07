import re
import sys


CYRILLIC_RE = re.compile(r"[\u0400-\u04FF\u0500-\u052F\u2DE0-\u2DFF\uA640-\uA69F]")


def main() -> int:
    errors = []
    for path in sys.argv[1:]:
        try:
            with open(path, encoding="utf-8", errors="ignore") as handle:
                for idx, line in enumerate(handle, start=1):
                    if CYRILLIC_RE.search(line):
                        errors.append(f"{path}:{idx}: Cyrillic symbols are introduced in this place")
        except OSError as exc:
            errors.append(f"{path}:1: {exc}")

    if errors:
        print("\n".join(errors))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
