# probely_cli

## So far this is more like

Generate docs:

* go to docs/
* make clean
* make markdown

### Development guidelines:

* Command structure: `Probely <context> <action> params [--optinal params]`
* Follow CLI output good practices. Valid output to `stdout`, erros to `stderr`
* Check list every step of the MR template(todo)
    * Tests
    * Docs
    * Multiple version CI
* Custom tooling, developers should be aware
    * `probely_cli` fixture (to test CLI OUTPUT)
    * `rich.console` is always available on the `args`
* Error message should have the following structure: `{cmd}: error: {message}`,
  following the default implementation of argparse
    * eg: `probely targets get: error: filters and target ids are mutually exclusive.`
    * TBD how to handle json errors list

### Usage tips:

* When using multiple values optional arguments you can use `--` to indicate that next
  values are positional arguments
