# probely_cli


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
