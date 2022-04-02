import argparse

import yaml

from converter import YamlConverter
from writer import MarkDownWriter

parser = argparse.ArgumentParser(description="Convert an OpenAPI YAML file to a Markdown file")
parser.add_argument("file", help="The file to parse")
args = parser.parse_args()

with open(args.file, "r") as stream:
    try:
        data = yaml.safe_load(stream)
        
        paths = YamlConverter.convert_paths(data)

        MarkDownWriter.write(paths)
       
    except yaml.YAMLError as exc:
        print(exc)
    except Exception as ex:
        print(ex)


