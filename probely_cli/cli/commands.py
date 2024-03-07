import json

import typer
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated

from probely_cli.exceptions import cli_exception_handler
from probely_cli.sdk.targets import list_targets

app = typer.Typer()
targets_app = typer.Typer(pretty_exceptions_enable=False)
app.add_typer(targets_app, name="targets", help="Manage users in the app.")

err_console = Console(stderr=True)
console = Console()


def get_tabled_target_list(targets_list):
    table = Table()
    table.add_column("ID")
    table.add_column("Asset name")
    table.add_column("Asset url")

    for target in targets_list:
        # print(json.dumps(target, indent=4))
        # console.print(target)
        asset = target.get("site")
        table.add_row(target.get("id"), asset.get("name"), asset.get("url"))

    return table


@targets_app.command("list", help="List all targets")
@cli_exception_handler
def get_targets(v: Annotated[bool, typer.Option("--verbose", "-v")] = False):
    targets_list = list_targets()

    if v:
        console.print(json.dumps(targets_list, indent=4))
        return

    table = get_tabled_target_list(targets_list)
    console.print(table)
