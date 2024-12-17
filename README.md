# ArgUI
Bind together or create a TUI for your Python CLI application

## Purpose

When Python scripts get sufficiently complex, you may start to see many entry point functions
or loads of parameters or sub subcommands. ArgUI will provide a means of creating a [TUI](https://en.wikipedia.org/wiki/Text-based_user_interface)
by switching out the Argparse implementation or by using a configuration to generate your entrypoint.

ArgUI application are both interactive *and* scriptable. You will enter the interactive mode based on CLI input. 
Interactive mode may be either opt-in or opt-out.

The drop-in replacement for `argparse.ArgumentParser` will be able to:

1. Identify duplicate parameters that conflict with the `interactive` flag
2. Build a dynamic TUI based around the inputs upon the call to `.parse_args`
3. Ensure that **required** parameters are only required in non-interactive contexts but require they be supplied within the TUI prior to operation

Calling ArgUI should be possible from outside your application to provide two needs:

1. Allow you to generate a new entry point that will create the CLI for both interactive and non-interactive modes based on a config
2. Launch a TUI based on the config without needing to generate anything based upon that config
