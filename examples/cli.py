#!/usr/bin/env python

# TODO: improve or find a better solution to run test the CLI.
# Only works if you run the this script from inside this folder
import sys

sys.path.append(r'..')  # required for imports to work
from probely_cli.cli.commands import app  # noqa

if __name__ == "__main__":
    app()
