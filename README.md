# mdview

Simple markdown viewer inspired by
[restview](https://github.com/mgedmin/restview).

Features:

 - Support for different markdown flavors (such as markdown-extra).
 - Auto-reload in browser when previewed file is modified.
 - Syntax highlighting using [Pygments](https://pygments.org/).

## Installation

To install `mdview`, use pip:

    $ pip install mdview

Or install directly from Git:

    $ pip install git+https://github.com/guyru/mdview.git#egg=mdview


## Usage


```text
usage: mdview [-h] [-x EXTENSIONS] [--version] [--debug] filename

Simple markdown viewer.

positional arguments:
  filename

optional arguments:
  -h, --help            show this help message and exit
  -x EXTENSIONS, --extensions EXTENSIONS
                        markdown extensions separated by commas. Default:
                        extra,codehilite
  --version             show program's version number and exit
  --debug               run server in debug mode
```

### FAQ

#### Where can I find a list of supported markdown extensions?

List of supported flavors is available in
[python-markdown](https://python-markdown.github.io/extensions/#officially-supported-extensions)'s
documentation. By default the `extra` and `codehilite` extensions are turned on.

#### How can I run `mdview` without any extension?

    $ mdview --extensions "" path/to/file.md

#### What are those `error: [Errno 32] Broken pipe` errors I see on `stderr`?

It happens when you close the browser and `mdview` still tries to send to it
information. You can safely ignore this.

## Authors

  - Author: [Guy Rutenberg](https://www.guyrutenberg.com)

