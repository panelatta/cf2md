# cf2md
A Python script written in order to easily obtain the Markdown version of a Codeforces problem description.

## Requirements

- `requests`
- `beautifulsoup4`
- `coloredlogs`

## Usage

```
usage: cf2md.py [-h] [-l LEVEL] [-d [DIR]] [-f [FILENAME]] problem_id

positional arguments:
  problem_id            ID of the problem. (e.g. 1462A)

optional arguments:
  -h, --help            show this help message and exit
  -l LEVEL, --level LEVEL
                        The highest title level of generated markdown
                        text. If this argument is not explicitly set, it
                        will be 2.
  -d [DIR], --dir [DIR]
                        Root directory of the generated markdown file. If
                        this argument is not explicitly set, it will be
                        current directory.
  -f [FILENAME], --filename [FILENAME]
                        Name of the generated markdown file. If this
                        argument is not explicitly set, it will be
                        "test.md".
```

## License

GNU GPL v2