from converter import HeaderConverter
from converter import ResponseBodyConverter
from model.Operation import Operation
from model.Parameter import Parameter
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


def __parse_request_parameters(request_parameters: dict) -> list[Parameter]:
    parameters = []

    for parameter in request_parameters:
        p = Parameter()
        p.name = parameter['name']
        p.location = parameter['in']
        p.description = parameter['description'] if 'description' in parameter else ''
        p.required = parameter['required'] if 'required' in parameter else False
        p.type = parameter['schema']['type']
        parameters.append(p)

    return parameters


def __get_request(operation_content: dict, components: dict) -> Request:
    request = Request()

    if 'parameters' in operation_content:
        request.parameters = __parse_request_parameters(operation_content['parameters'])

    if 'requestBody' in operation_content:
        request.content = ResponseBodyConverter.get_response_content(operation_content['requestBody'], components)

    return request


def __get_operations(path_content: dict, components: dict) -> list[Operation]:
    operations = []
    for operation, operation_content in path_content.items():
        operation_object = Operation(operation)
        operation_object.summary = operation_content['summary'] if 'summary' in operation_content else ''
        operation_object.description = operation_content['description'] if 'description' in operation_content else ''
        operation_object.request = __get_request(operation_content, components)
        # m.responses = __get_responses(operation_content, components)
        operations.append(operation_object)

    return operations


def convert_paths(file_data: dict) -> list[Path]:
    """
    """

    # the #/components section, required to solve the $ref declarations
    components = file_data['components'] if 'components' in file_data else []

    paths = []
    try:
        for path, path_content in file_data['paths'].items():
            converted_path = Path(path)
            converted_path.operations = __get_operations(path_content, components)
            paths.append(converted_path)
        return paths
    except Exception as ex:
        print(f"Error parsing path [{path}]: {ex}")
