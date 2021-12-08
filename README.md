# oas2md
Python-based converter which translates an OpenAPI YAML file to a MarkDown file

This script reads an OpenAPI descriptor and creates a markdown file for each path found in the `.yaml` file.

## File naming
The generated markdown file(s) will have the same name as the related path, sanitized as follow:
* all the `/` chars will be replaced by `-`;
* the file name has to start with a letter;

For example, a path defined as `/path1/path2` will be saved in a file named `path1-path2.md`

## Markdown template
The generated markdown file will have the following template (one file for each path):

```bash
file
│
├── title
├── endpoint(s)
├── summary
├── description
├── request
│   └── parameters
└── response
    └── http code
        ├── description
        └── headers
```


## Requirements
This script uses the [pyaml](https://pyyaml.org/) module to read and parse the `.yaml` file:
```bash
$ pip install pyyaml
```

## How to
Execute the script:
```bash
$ python /path/to/file/oas2md.py
```