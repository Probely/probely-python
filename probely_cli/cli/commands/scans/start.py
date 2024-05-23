from probely_cli.sdk.scans import start_scan
from rich.console import Console

err_console = Console(stderr=True)
console = Console()


def start_scans_command_handler(args):
    target_id = args.target_id

    console.print("starting scan for target id: {}".format(target_id))

    scan = start_scan(target_id)

    if args.raw:
        console.print(scan)

    console.print(scan["id"])
