# probely_cli

## So far this is more like 

Generate docs:
* go to docs/
* make clean
* make markdown


Development guidelines:
* Command structure: `Probely <context> <action> params [--optinal params]`
* Follow CLI output good practices. Valid output to `stdout`, erros to `stderr`
* Check list every step of the MR template(todo)
  * Tests
  * Docs
  * Multiple version CI
* Custom tooling, developers should be aware
  * `probely_cli` fixture (to test CLI OUTPUT)
  * `rich.console` is always available on the `args` 