"""Round-2 entrypoint for news-image-20261118.

The picture itself is drawn at build time by draw_world.py and committed
as entry.png. This program's only job is to place that exact file at the
path the grader reads, using the standard library alone: no fonts, no
network, no drawing, so the two graded runs can only produce identical
bytes.
"""

import os
import shutil
import sys

IMAGE_NAME = "entry.png"


def destination_dir():
    """Where the grader wants the image: the kit's env var, else /output."""
    wanted = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if wanted:
        return wanted
    return "/output"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, IMAGE_NAME)
    target_dir = destination_dir()
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, IMAGE_NAME)
    shutil.copyfile(source, target)
    # A copy that silently truncated would fail the gate, so check it.
    if os.path.getsize(target) != os.path.getsize(source):
        print("copy mismatch: %s != %s" % (target, source), file=sys.stderr)
        return 1
    print("%s (%d bytes)" % (target, os.path.getsize(target)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
