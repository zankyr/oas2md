import errno
import os
import re
from io import StringIO

from model.Attribute import Attribute
from model.Header import Header
from model.Parameter import Parameter
from model.Path import Path
from model.Request import Request


def __try_create_output_directory():
    current_directory = os.getcwd()
    output_directory = os.path.join(current_directory, r'output')
    if not os.path.exists(output_directory):
        try:
            os.makedirs(output_directory)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise


def __create_file_name(title: str) -> str:
    file_name = title.replace("/", "-")
    if not re.search("^[a-zA-Z].*", file_name):
        file_name = file_name[1:]
        return __create_file_name(file_name)
    return file_name


def __create_table_separator(current_param_len: int, new_parameter: str):
    new_param_len = len(new_parameter) if new_parameter else 0
    if new_param_len > current_param_len:
        current_param_len = new_param_len if new_param_len <= 60 else 60
    return current_param_len


def __create_headers_table(headers: list[Header]) -> str:
    table_template = '| {col1} | {col2} | {col3} | {col4} |\n'

    header_header = 'Header'
    header_header_column_width = len(header_header)

    description_header = 'Description'
    description_header_column_width = len(description_header)

    type_header = 'Type'
    type_header_column_width = len(type_header)

    example_header = 'Example'
    example_header_column_width = len(example_header)

    table_body = ''
    for header in headers:
        header_name = header.name
        header_description = header.description
        header_type = header.type
        header_example = header.example

        header_header_column_width = __create_table_separator(header_header_column_width, header_name)
        description_header_column_width = __create_table_separator(description_header_column_width, header_description)
        type_header_column_width = __create_table_separator(type_header_column_width, header_type)
        example_header_column_width = __create_table_separator(example_header_column_width, header_example)

        table_body += f'|{header_name}|{header_description}|{header_type}|{header_example}|\n'

    table = table_template.format(col1=header_header, col2=description_header, col3=type_header, col4=example_header)
    table += table_template.format(col1="-" * header_header_column_width, col2="-" * description_header_column_width,
                                   col3="-" * type_header_column_width, col4="-" * example_header_column_width)
    table += table_body
    return table


def __create_response_properties_table(properties: list[Attribute]) -> str:
    table_template = '| {col1} | {col2} | {col3} | {col4} | {col5} | {col6} |\n'

    property_header = 'Property'
    property_header_column_width = len(property_header)

    parent_property_header = 'Parent property'
    parent_property_header_column_width = len(parent_property_header)

    description_header = 'Description'
    description_header_column_width = len(description_header)

    type_header = 'Type'
    type_header_column_width = len(type_header)

    required_header = 'Required'
    required_header_column_width = len(required_header)

    example_header = 'Example'
    example_header_column_width = len(example_header)

    table_body = ''
    for current_property in properties:
        header_name = current_property.name
        header_parent = current_property.parent_attribute if current_property.parent_attribute else ''
        header_description = current_property.description
        header_required = 'Yes' if current_property.required else ''
        header_type = current_property.type
        header_example = current_property.example

        property_header_column_width = __create_table_separator(property_header_column_width, header_name)
        parent_property_header_column_width = __create_table_separator(parent_property_header_column_width,
                                                                       header_parent)
        description_header_column_width = __create_table_separator(description_header_column_width, header_description)
        type_header_column_width = __create_table_separator(type_header_column_width, header_type)
        required_header_column_width = __create_table_separator(required_header_column_width, header_required)
        example_header_column_width = __create_table_separator(example_header_column_width, header_example)

        table_body += f'|{header_name}|{header_parent}|{header_description}|{header_type}|{header_required}|{header_example}|\n '

    table = table_template.format(col1=property_header, col2=parent_property_header, col3=description_header,
                                  col4=type_header, col5=required_header,
                                  col6=example_header)
    table += table_template.format(col1="-" * property_header_column_width,
                                   col2="-" * parent_property_header_column_width,
                                   col3="-" * description_header_column_width,
                                   col4="-" * type_header_column_width, col5="-" * required_header_column_width,
                                   col6="-" * example_header_column_width)
    table += table_body
    return table


def __create_request_parameters_table(parameters: list[Parameter]) -> str:
    table_template = '| {col1} | {col2} | {col3} | {col4} | {col5} | {col6} |\n'

    property_header = 'Parameter'
    property_header_column_width = len(property_header)

    location_header = 'Location'
    location_header_column_width = len(location_header)

    description_header = 'Description'
    description_header_column_width = len(description_header)

    type_header = 'Type'
    type_header_column_width = len(type_header)

    required_header = 'Required'
    required_header_column_width = len(required_header)

    example_header = 'Example'
    example_header_column_width = len(example_header)

    table_body = ''
    for current_parameter in parameters:
        header_name = current_parameter.name
        header_parent = current_parameter.location
        header_description = current_parameter.description
        header_required = 'Yes' if current_parameter.required else ''
        header_type = current_parameter.type
        header_example = current_parameter.example

        property_header_column_width = __create_table_separator(property_header_column_width, header_name)
        location_header_column_width = __create_table_separator(location_header_column_width,
                                                                header_parent)
        description_header_column_width = __create_table_separator(description_header_column_width, header_description)
        type_header_column_width = __create_table_separator(type_header_column_width, header_type)
        required_header_column_width = __create_table_separator(required_header_column_width, header_required)
        example_header_column_width = __create_table_separator(example_header_column_width, header_example)

        table_body += f'|{header_name}|{header_parent}|{header_description}|{header_type}|{header_required}|{header_example}|\n'

    table = table_template.format(col1=property_header, col2=location_header, col3=description_header,
                                  col4=type_header, col5=required_header,
                                  col6=example_header)
    table += table_template.format(col1="-" * property_header_column_width,
                                   col2="-" * location_header_column_width,
                                   col3="-" * description_header_column_width,
                                   col4="-" * type_header_column_width, col5="-" * required_header_column_width,
                                   col6="-" * example_header_column_width)
    table += table_body
    return table


def __write_request(request: Request) -> str:
    if not request:
        return ""

    output = StringIO()

    if request.parameters:
        output.write(f'\n### Parameters\n')
        output.write(__create_request_parameters_table(request.parameters))

    # for content in request.content:
    #     output.write(f'\n### {content.media_type}\n')
    #     output.write(__create_response_properties_table(content.attributes))

    return output.getvalue()


def write(paths: list[Path]):
    # Create output directory
    __try_create_output_directory()

    # Create one file for each path
    for path in paths:
        file_name = __create_file_name(path.name)
        print(f"Writing {file_name}...")

        f = open(f'./output/{file_name}.md', "w")
        f.write(f'# {path.name}')

        for operation in path.operations:
            f.write('\n```HTTP\n')
            f.write(operation.operation.upper() + ' ' + path.name + '\n')
            f.write('```\n')

            f.write('\n## Summary\n')
            f.write(operation.summary)

            f.write('\n## Description\n')
            f.write(operation.description)

            f.write('\n## Request')
            f.write(__write_request(operation.request))
            #
            # f.write('\n## Responses')
            # for response in method.responses:
            #     f.write(f'\n### {response.code}\n')
            #     f.write(response.description)
            #     f.write('\n#### Headers\n')
            #     f.write(__create_headers_table(response.headers))
            #     f.write('\n#### Content\n')
            #     for content in response.content:
            #         f.write(f'\n##### {content.media_type}\n')
            #         f.write(__create_response_properties_table(content.attributes))

        f.close()
