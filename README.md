# cookies-backpack

This is a utility tool designed for desktop use. It uses a text editor for input and output.

## Installation & Uninstllation

If the latest features are not available, try uninstalling and then reinstalling the package.

```
pip install git+https://github.com/CookieBox26/cookies-backpack
pip uninstall cookies-backpack
```

## Prerequisites

- By default, this tool uses `~/.cb/` as its working directory. To change this, set the `COOKIES_BACKPACK_WORK_DIR` environment variable.
- This tool uses a text editor for input and output. By default, it launches `C:\\Windows\\System32\\notepad.exe`. If you want to change it, specify the path in `config.toml` under the working directory.

```
# text_editor = "C:\\Windows\\System32\\notepad.exe"  # default
text_editor = "C:\\Program Files (x86)\\sakura\\sakura.exe"
```

## Commands

**Note:** All commands open a text editor. After editing the settings, be sure to **close the editor**.

#### `cb --find`

Searches for files with specified extension(s) under a directory, and containing the specified string.

#### `cb --pdf`

Performs the following PDF operations. You can also specify a pre-downloaded PDF.

- Downloads the PDF from the specified URL into the specified directory.
- Converts the PDF to text using PyMuPDF (`xxx.raw.txt`).
- Formats the extracted text into a cleaned version (`xxx.formatted.txt`).
  - Assumes a specific structure (see below) and requires a title.
  - Currently extracts only the beginning of each section.


```
title (line breaks are allowed)
author
author
author
Abstract
xxx
xxx
1
section title
xxx
xxx
2
section title
xxx
xxx
```
