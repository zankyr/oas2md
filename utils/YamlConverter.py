import dataclasses
from model.Header import Header
from model.Path import Path
from model.Method import Method
from model.Response import Response
from model.ResponseResult import ResponseResult

def __get_header_from_components(header:str, header_content: dict, headers_components: dict) -> Header:
    h = Header(header)
    header_ref = header_content['$ref']
    header_ref_name = header_ref[header_ref.rfind('/') + 1:]
    if header_ref_name not in headers_components:
        raise Exception(f'{header_ref_name} not found in the \'components/headers\' section')
    header_component = headers_components[header_ref_name]
    h.type = header_component['schema']['type']
    h.example = header_component['schema']['example']
    h.description = header_component['description']
    return h

def __get_header(header:str, header_content: dict, headers_components: dict) -> Header:
    if '$ref' in header_content:
        return __get_header_from_components(header, header_content, headers_components)

    h = Header(header)
    h.type = header_content['schema']['type']
    h.example = header_content['schema']['example']
    h.description = header_content['description']
    return h


def __get_headers(response_content: dict, components: dict) -> list[Header]:
    headers_content = response_content['headers']
    headers_components = components['headers'] if 'headers' in components else None
    headers = []

    for header, header_content in headers_content.items():
        headers.append(__get_header(header, header_content, headers_components))

    return headers

def __get_response_result(response: str, response_content: dict, components: dict) -> ResponseResult:
    result_code = int(response)
    result_description = response_content['description']
    result_headers = __get_headers(response_content, components)
    return ResponseResult(result_code, result_description, result_headers)


def __get_response(method_content: dict, components: dict) -> Response:
    responses = method_content['responses']
    response_results = []
    for response, response_content in responses.items():
        response_results.append(__get_response_result(response, response_content, components))
    return Response(response_results)
        


def __get_methods(path_content: dict, components: dict) -> list[Method]:
    methods = []
    for method, method_content in path_content.items():
        m = Method(method, method_content['summary'], method_content['description'])
        m.response = __get_response(method_content, components)
        methods.append(m)
        
    return methods

def convert_paths(file_data: dict):
    """
    """
    # the paths (e.g. /login)
    paths = file_data['paths']
    
    # the #/components section, required to solve the $ref declarations
    components = file_data['components']

    for path, path_content in paths.items():
        p = Path(path)
        p.methods = __get_methods(path_content, components)
        print(dataclasses.asdict(p))