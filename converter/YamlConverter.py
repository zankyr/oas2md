from converter import HeaderConverter
from converter import ResponseBodyConverter

from model.Path import Path
from model.Method import Method
from model.Response import Response
from model.ResponseAttribute import ResponseAttribute
from model.ResponseBody import ResponseBody
from model.ResponseResult import ResponseResult


def __get_response_result(response: str, response_content: dict, components: dict) -> ResponseResult:
    result_code = int(response)
    result_description = response_content['description']
    result_headers = HeaderConverter.get_headers(response_content, components)
    result_bodies = ResponseBodyConverter.get_response_bodies(response_content, components)
    return ResponseResult(result_code, result_description, result_headers, result_bodies)


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

def convert_paths(file_data: dict) -> list[Path]:
    """
    """
    
    # the #/components section, required to solve the $ref declarations
    components = file_data['components']

    paths = []
    
    for path, path_content in file_data['paths'].items():
        converted_path = Path(path)
        converted_path.methods = __get_methods(path_content, components)
        paths.append(converted_path)
        # print(dataclasses.asdict(converted_path))

   
    return paths
