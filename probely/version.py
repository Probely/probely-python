from pathlib import Path

import toml

pyproject_content = toml.load(Path(__file__).parents[1] / "pyproject.toml")

__version__ = pyproject_content["project"]["version"]
