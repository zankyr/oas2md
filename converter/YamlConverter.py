from converter import HeaderConverter
from converter import ResponseBodyConverter
from model.Method import Method
from model.Path import Path
from model.Request import Request
from model.Response import Response


def __get_response(response: str, response_content: dict, components: dict) -> Response:
    result_code = int(response)
    description = response_content['description']
    headers = HeaderConverter.get_headers(response_content, components)
    content = ResponseBodyConverter.get_response_content(response_content, components)
    return Response(result_code, description, headers, content)


def __get_responses(method_content: dict, components: dict) -> list[Response]:
    responses = []
    for response, response_content in method_content['responses'].items():
        responses.append(__get_response(response, response_content, components))
    return responses


def __get_request(method_content: dict, components: dict) -> Request:
    if 'requestBody' not in method_content:
        return Request([])

    bodies = ResponseBodyConverter.get_response_content(method_content['requestBody'], components)
    return Request(bodies)


def __get_methods(path_content: dict, components: dict) -> list[Method]:
    methods = []
    for method, method_content in path_content.items():
        m = Method(method, method_content['summary'], method_content['description'])
        m.request = __get_request(method_content, components)
        m.responses = __get_responses(method_content, components)
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
