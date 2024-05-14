import json

from rich.console import Console

from probely_cli import sdk, ProbelyException, ProbelyBadRequest

err_console = Console(stderr=True)
console = Console()


def add_targets(args):
    site_url = args.site_url
    site_name = args.site_name

    try:
        target: dict = sdk.add_target(site_url=site_url, site_name=site_name)
    except ProbelyException as probely_ex:
        err_console.print(str(probely_ex))
        if isinstance(probely_ex, ProbelyBadRequest):
            err_console.print(probely_ex.response_payload)
        return

    if args.raw:
        console.print(target)
        return

    console.print(target["id"])
