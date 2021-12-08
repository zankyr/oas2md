#!/usr/bin/env/python

import yaml
import re


def __create_table_separator(current_param_len: int, new_parameter: str):
    new_param_len = len(new_parameter)
    if new_param_len > current_param_len:
        current_param_len = new_param_len if new_param_len <= 60 else 60
    return current_param_len

def __create_parameter_section(request_parameters: list) -> str:
    tableHeaderTemplate = '| {col1} | {col2} | {col3} | {col4} | {col5} |\n'
    
    parameterHeader = 'Parameter'
    parameterColumnWidth = len(parameterHeader)
    
    descriptionHeader = 'Description'
    descriptionColumnWidth = len(descriptionHeader)
    
    typeHeader = 'Type'
    typeColumnWidth = len(typeHeader)
    
    requiredHeader = 'Required'
    requiredColumnWidth = len(requiredHeader)
    
    exampleHeader = 'Example'
    exampleColumnWidth = len(exampleHeader)

    tableBody = ''
    for parameter in request_parameters:
        name = parameter['name']
        parameterColumnWidth = __create_table_separator(parameterColumnWidth, name)
        
        type = parameter['schema']['type']
        typeColumnWidth = __create_table_separator(typeColumnWidth, type)
       
        example = parameter['example']
        exampleColumnWidth = __create_table_separator(exampleColumnWidth, example)
       
        required = 'Yes' if parameter['required'] else 'No'
        requiredColumnWidth = __create_table_separator(requiredColumnWidth, required)
        
        description = parameter['description']
        descriptionColumnWidth = __create_table_separator(descriptionColumnWidth, description)

        tableBody += f'|{name}|{description}|{type}|{required}|{example}|\n'

    table = tableHeaderTemplate.format(col1=parameterHeader,col2=descriptionHeader,col3=typeHeader,col4=requiredHeader,col5=exampleHeader)
    table += tableHeaderTemplate.format(col1="-" * parameterColumnWidth,col2="-" * descriptionColumnWidth,col3="-" * typeColumnWidth,col4="-" * requiredColumnWidth,col5="-" * exampleColumnWidth)
    table += tableBody
    return table

def __create_headers_table(headers_section: dict, headers_components: dict) -> str:
    tableTemplate = '| {col1} | {col2} | {col3} | {col4} |\n'
    nameHeader = 'Header'
    nameHeaderColumnWidth = len(nameHeader)
    
    descriptionHeader = 'Description'
    descriptionHeaderColumnWidth = len(descriptionHeader)
    
    typeHeader = 'Type'
    typeHeaderColumnWidth = len(typeHeader)
    
    exampleHeader = 'Example'
    exampleHeaderColumnWidth = len(exampleHeader)

    tableBody = ''
    for header, header_content in headers_section.items():
        name = header
        nameHeaderColumnWidth = __create_table_separator(nameHeaderColumnWidth, name)

        if '$ref' in header_content:
            header_ref = header_content['$ref']
            header_ref_name = header_ref[header_ref.rfind('/') + 1:]
            if header_ref_name not in headers_components:
                raise Exception(f'{header_ref_name} not found in the \'components/headers\' section')
            header_component = headers_components[header_ref_name]
            type = header_component['schema']['type']
            example = header_component['schema']['example']
            description = header_component['description']
        else:
            type = header_content['schema']['type']
            example = header_content['schema']['example']
            description = header_content['description']

        typeHeaderColumnWidth = __create_table_separator(typeHeaderColumnWidth, type)
        exampleHeaderColumnWidth = __create_table_separator(exampleHeaderColumnWidth, example)
        descriptionHeaderColumnWidth = __create_table_separator(descriptionHeaderColumnWidth, description)

        tableBody += f'|{name}|{description}|{type}|{example}|\n'
    
    table = tableTemplate.format(col1=nameHeader,col2=descriptionHeader,col3=typeHeader,col4=exampleHeader)
    table += tableTemplate.format(col1="-" * nameHeaderColumnWidth,col2="-" * descriptionHeaderColumnWidth,col3="-" * typeHeaderColumnWidth,col4="-" * exampleHeaderColumnWidth)
    table += tableBody
    return table

def __create_file_name(title: str) -> str:
    file_name = title.replace("/", "-")
    if not re.search("^[a-zA-Z]{1}.*", file_name):
        file_name = file_name[1:]
        return __create_file_name(file_name)
    return file_name
    

with open("example.yaml", "r") as stream:
    try:
        data = yaml.safe_load(stream)
        
        paths = data['paths']
        headers_components = data['components']['headers'] if 'headers' in data['components'] else None

        for path, path_content in paths.items():
            # Title section
            title = path
            
            not_first = False
            method_section = ''
            summary = ''
            description = ''
            request_parameters = ''
            request_body = ''

            for method, method_content in path_content.items():
                # Methods section
                if not_first:
                    method_section += 'OR\n'    # The OR section is required due to bad design choices, where the same API could be exposed with GET and POST method at the same time, doing the same process
                method_section += '\n```HTTP\n'
                method_section += method.upper() + ' ' + title + '\n'
                method_section += '```\n'
                if not not_first:
                    not_first = True

                # Summary
                if not summary:
                    summary = method_content['summary']
                
                # Description
                if not description:
                    description = method_content['description']

                # Request parameters
                if not request_parameters and method_content['parameters']:
                    request_parameters = method_content['parameters']
                    request_parameters_table = __create_parameter_section(request_parameters)

                # Responses
                responses = method_content['responses']                    
                    


            file_name = __create_file_name(title)
            f = open(f'{file_name}.md', "w")
            f.write(f'# {title}')
            f.write(method_section)
            f.write(f'\n## Summary\n{summary}')
            f.write(f'\n## Description\n{description}')
            f.write('\n---')
            f.write('\n## Request')
            if request_parameters:
                f.write('\n### Parameters\n')
                f.write(request_parameters_table)

            f.write('\n## Responses')
            for response, response_content in responses.items():
                f.write(f'\n### {response}\n')
                f.write(response_content['description'])
                f.write('\n#### Headers\n')
                f.write( __create_headers_table(response_content['headers'], headers_components));
        
            f.close()

    except yaml.YAMLError as exc:
        print(exc)
    except Exception as ex:
        print(ex)


