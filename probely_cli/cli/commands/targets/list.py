from probely_cli import sdk
from rich.console import Console
from rich.table import Table


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


def list_targets(args):
    targets_list = sdk.list_targets()
    if args.count_only:
        console.print(len(targets_list))
        return

    if args.raw:
        console.print(targets_list)
        return

    table = get_tabled_target_list(targets_list)
    console.print(table)
