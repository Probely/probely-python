# probely

### Package level api key setup:

* Config File:
  Create `~/.probely/config` and add:

  ```
  [AUTH]
  api_key = <your_api_key>
  ```

* Environment Variables
  ```
  export PROBELY_API_BASE_URL=<your_api_key>
  ```
* Tool specific config (see below)

## CLI

### Usage

* Use `-h/--help` for available options
* General usage
  `Probely <context> <action> [positional_params ...] [--optinal params ...] -- [positional_params ...]`
    * `--` allows you to add positional args after optional
* add `--api-key` for command specific api key

## SDK

* Init `Probely` for specific config
  ```
  from probely_cli import Probely

  Probely.init(api_key=<your_api_key>)
  
  ...
  ```
* Import `probely_cli` for public interface

  ```
  import probely_cli

  target = probely_cli.add_target("http://target_url.com")
  ```

### Development guidelines:

* Command structure: `Probely <context> <action> params [--optinal params]`
* Follow CLI output good practices. Valid output to `stdout`, errors to `stderr`
* Custom tooling, developers should be aware
    * `rich.console` is always available on the `args`
    * `probely_cli` fixture (to test CLI OUTPUT)
* Error message should have the following structure: `{cmd}: error: {message}`,
  following the default implementation of argparse
    * eg: `probely targets get: error: filters and target ids are mutually exclusive.`

