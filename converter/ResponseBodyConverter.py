from model.Attribute import Attribute
from model.Content import Content


def __get_response_body(content_type: str, body_content: dict, body_components: dict) -> Content:
    response_properties = []

    for property_name, property_content in body_content['schema']['properties'].items():
        ra = Attribute(property_name)
        ra.description = (property_content['description']).replace('\n', '<br />')
        ra.type = property_content['type']
        ra.example = property_content['example'] if 'example' in property_content else ''
        response_properties.append(ra)

    return Content(content_type, response_properties)


def get_response_content(response_content: dict, components: dict) -> list[Content]:
    bodies = []
    for body, body_content in response_content['content'].items():
        bodies.append(__get_response_body(body, body_content, None))
    return bodies
