# `argparse` Subcommands

Complex programs may need to perform multiple tasks. In the case of the colocated `argparse_example.py`,
we have a script that can create files or directories, delete files or directories, list files or
directories, and copy files or directories. Use of the script looks like:

```shell
# 1) Create a copy of `/path/to/target` at `/path/to/destination`
python3 argparse_example.py copy /path/to/target /path/to/destination

# 2) List everything at '.'
python3 argparse_example.py list

# 3) List everything at `/path/to/directory`
python3 argparse_example.py list --path /path/to/directory

# 4) List all files in '.'
python3 argparse_example.py list --type file

# 5) List all directories in `/path/to/directory`
python3 argparse_example.py list --type dir --path /path/to/directory

# 6) Delete the item at `/path/to/item`
python3 argparse_example.py delete /path/to/item

# 7) Create an empty file at `/path/to/file.txt`
python3 argparse_example.py create --type file /path/to/file.txt

# 8) Create a file at `/path/to/file.txt` with the text content of "Look at this content"
python3 argparse_example.py create --type file --content "Look at this content" /path/to/file.txt

# 9) Create a directory at `/path/to/directory`
python3 argparse_example.py create --type dir /path/to/directory
```

This essentially covers 4 programs:

* Create
* Delete
* List
* Copy

In terms of a TUI, this should form four independent workflows through one entrypoint.

By looking at the built `argparse.ArgumentParser`, ArgUI should be able to generate a TUI
if the `-i` flag is passed, that has 4 views that may be navigated to and fro - one for each "program".
Each "program" view should list the name of the view from the subparser ("Create", "Delete", "List", or "Copy")
with data from the `description`, `prog`, and/or `epilog` if available. It should have a field on screen with a label
and input widget for each parameter to be read - optional or not. Additionally, there should be a shared 'Submit' or 'Start'
and a 'Quit' or 'Exit' button. Clicking the 'Quit' or 'Exit' button should halt the application and exit with a
code of `0`. Clicking submit or start should start a new thread under the covers and open up a new view that just
shows streaming stdout and stderr.  Stdin handling may be considered out of scope for now. Submitting a new task
should be disabled until the previously started one returns.

Not passing `-i` should run the script as normal

## Fields

- [ ] Fields in the parser with a `choices` value should be represented by a `Select` populated by the `choices` values
- [ ] Fields in the parser with a 'store_true' or 'store_false' option should be represented by a 'Switch'
    - Extra handling will need to be added to handle `store_false` (since the logic is inverted), but it
        may be considered out of scope
- [ ] Fields with a type of `int` should be an `Input` with a `type` of `"integer"`
- [ ] Fields with a type of `float` should be an `Input` with a `type` of `"number"`
- [ ] Fields with a type that is an `Enum` should be represented by a `Select` populated by the enum names and values
- [ ] Fields with a type of `pathlib.Path` should be an `Input` with a button
    - [ ] The `Input` will be directly editable
    - [ ] Activating the button should pop up a new view with a `DirectoryTree` showing file paths and a `"Select"` and `"Cancel"` button
        - [ ] Clicking `"Select"` will either take the selected path and enter it into the initial `Input` or
        make an announcement that the selection was invalid
        - [ ] Clicking `"Cancel"` will close the new view and not update the `Input`
- [ ] Everything else should be an `Input` with a `type` of `text`

## Validation

`parse_args` should be called on the argument parser with the values from the given view with the correct command, wrapped in a `try...catch`
block. If the parsing fails, announce the issue. If it passes, call the intended function.

## Constraints that keep this from being a drop in replacement

There has to be something to route the selected parameters to the correct target function. This may be done as in the example via
a pattern like `parser_create.set_defaults(func=handler)`, then calling `parameters.func(parameters)` or by some other elegant solution.

The intended pattern needs to be established.

## Hints

It's probably safest to go into `interactive` mode by looking for the appropriate `-i` flag rather than by grabbing it from parsed
arguments.