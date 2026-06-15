# 🌲 dir_tree – Directory Structure Viewer

The `dir_tree` command prints a directory structure in a visual tree-like format.

It can show only folders or folders with files, limit recursion depth, exclude selected patterns, include hidden entries, use ASCII output, and save the result to a text file.

---

## 🔧 Options

| Option                            | Description                                                                       |
| --------------------------------- | --------------------------------------------------------------------------------- |
| `--files`, `-f`                   | Include files, not just folders                                                   |
| `--depth N`, `-d N`               | Limit recursion depth, where `0` means root only                                  |
| `--output FILE`, `-o FILE`        | Save the tree output to a text file                                               |
| `--hidden`, `-hd`                 | Include hidden files and folders                                                  |
| `--exclude PATTERN`, `-x PATTERN` | Exclude files or folders matching a pattern, e.g. `__pycache__`, `*.pyc`, `*.log` |
| `--ascii`, `-a`                   | Use ASCII characters instead of Unicode box-drawing lines                         |
| `--lang-help pl/eng`              | Show localized extended help                                                      |

---

## 📦 Examples

Show only directories:
shellman dir_tree .

Show directories and files:
shellman dir_tree . --files

Show files and limit depth to 2:
shellman dir_tree . --files --depth 2

Use ASCII output:
shellman dir_tree . --files --ascii

Exclude cache and log files:
shellman dir_tree . --files --exclude __pycache__ --exclude "*.log"

Save the result to a file:
shellman dir_tree . --files --output tree.txt

Show Polish help:
shellman dir_tree --lang-help pl
