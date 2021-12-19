import os
import errno
import re
from model.Header import Header
from model.Path import Path
from model.ResponseAttribute import ResponseAttribute

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
    if not re.search("^[a-zA-Z]{1}.*", file_name):
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
        
    
    table = table_template.format(col1=header_header,col2=description_header,col3=type_header,col4=example_header)
    table += table_template.format(col1="-" * header_header_column_width,col2="-" * description_header_column_width,col3="-" * type_header_column_width,col4="-" * example_header_column_width)
    table += table_body
    return table

def __create_response_properties_table(properties: list[ResponseAttribute]) -> str:
    table_template = '| {col1} | {col2} | {col3} | {col4} | {col5} |\n'

    property_header = 'Property'
    property_header_column_width = len(property_header)
    
    description_header = 'Description'
    description_header_column_width = len(description_header)
    
    type_header = 'Type'
    type_header_column_width = len(type_header)

    required_header = 'Required'
    required_header_column_width = len(required_header)
    
    example_header = 'Example'
    example_header_column_width = len(example_header)

    table_body = ''
    for property in properties:
        header_name = property.name
        header_description = property.description
        header_required = 'Yes' if property.required else ''
        header_type = property.type
        header_example = property.example
        
        property_header_column_width = __create_table_separator(property_header_column_width, header_name)
        description_header_column_width = __create_table_separator(description_header_column_width, header_description)
        type_header_column_width = __create_table_separator(type_header_column_width, header_type)
        required_header_column_width = __create_table_separator(required_header_column_width, header_required)
        example_header_column_width = __create_table_separator(example_header_column_width, header_example)
        
        table_body += f'|{header_name}|{header_description}|{header_type}|{header_required}|{header_example}|\n'
    
    table = table_template.format(col1=property_header,col2=description_header,col3=type_header,col4=required_header,col5=example_header)
    table += table_template.format(col1="-" * property_header_column_width,col2="-" * description_header_column_width,col3="-" * type_header_column_width,col4="-" * required_header_column_width,col5="-" * example_header_column_width)
    table += table_body
    return table

def test(paths: list[Path]):
    __try_create_output_directory()


    for path in paths:
        file_name = __create_file_name(path.title)
        print(file_name)
        f = open(f'./output/{file_name}.md', "w")
        f.write(f'# {path.title}')

        for method in path.methods:
            f.write('\n```HTTP\n')
            f.write(method.method.upper() + ' ' + path.title + '\n')
            f.write('```\n')

            # TOC
            f.write('1. [Summary](#summary)')
            f.write('2. [Description](#summary)')
            f.write('3. [Request](#summary)')
            f.write('4. [Responses](#summary)')
            
            f.write(f'\n## Summary\n{method.summary}')
            f.write(f'\n## Description\n{method.description}')
            f.write('\n---')
            f.write('\n## Request')
            # if request_parameters:
            #     f.write('\n### Parameters\n')
            #     f.write(request_parameters_table)

            f.write('\n## Responses')
            for response_result in method.response.results:
                f.write(f'\n### {response_result.code}\n')
                f.write(response_result.description)
                f.write('\n#### Headers\n')
                f.write( __create_headers_table(response_result.headers))
                f.write('\n#### Content\n')
                for response_body in response_result.bodies:
                    f.write(f'\n##### {response_body.media_type}\n')
                    f.write( __create_response_properties_table(response_body.attributes))

        f.close()